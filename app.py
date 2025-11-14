import os
import json
import datetime
from functools import wraps

from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
import jwt

from database import init_db, create_user, get_user_by_email, get_user_by_id, create_chat, update_chat, list_chats_for_user, get_chat_messages
import config

# Initialize DB
init_db()

# App config
app = Flask(__name__)
# Enable CORS for development: allow requests from frontend (or all origins).
# In production, restrict `origins` to your frontend domain.
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, expose_headers=["Content-Type", "Authorization"], allow_headers=["Content-Type", "Authorization"]) 


# Ensure OPTIONS (preflight) requests get a 200 response with appropriate CORS headers.
@app.before_request
def handle_options_preflight():
    if request.method == 'OPTIONS':
        # Build an empty 200 response; `after_request` will add CORS headers as well.
        from flask import make_response
        resp = make_response(('', 200))
        resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        resp.headers['Access-Control-Allow-Credentials'] = 'true'
        return resp


# Add CORS headers to all responses as a fallback
@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin:
        response.headers['Access-Control-Allow-Origin'] = origin
    else:
        response.headers.setdefault('Access-Control-Allow-Origin', '*')
    response.headers.setdefault('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.setdefault('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.setdefault('Access-Control-Allow-Credentials', 'true')
    return response

SECRET_KEY = os.environ.get("JWT_SECRET", getattr(config, 'SECRET_KEY', 'change-me-in-prod'))
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 60 * 60 * 24  # 24 hours


def generate_token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    # PyJWT returns str in v2
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return jsonify({"error": "Token de autorização ausente"}), 401
        parts = auth.split()
        if parts[0].lower() != 'bearer' or len(parts) != 2:
            return jsonify({"error": "Header Authorization inválido"}), 401
        token = parts[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except Exception:
            return jsonify({"error": "Token inválido"}), 401
        user = get_user_by_id(payload.get('user_id'))
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 401
        request.user = user
        return f(*args, **kwargs)

    return decorated


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    if not email or not password:
        return jsonify({"error": "email e password são obrigatórios"}), 400
    existing = get_user_by_email(email)
    if existing:
        return jsonify({"error": "Email já cadastrado"}), 400
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_id = create_user(email, password_hash.decode('utf-8'), username)
    if not user_id:
        return jsonify({"error": "Email já cadastrado"}), 400
    return jsonify({"message": "Usuário criado com sucesso"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "email e password são obrigatórios"}), 400
    user = get_user_by_email(email)
    if not user:
        return jsonify({"error": "Credenciais inválidas"}), 401
    stored_hash = user.get('password_hash')
    if not stored_hash:
        return jsonify({"error": "Credenciais inválidas"}), 401
    if not bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return jsonify({"error": "Credenciais inválidas"}), 401
    token = generate_token(user['id'])
    return jsonify({"access_token": token}), 200


@app.route('/history', methods=['GET'])
@token_required
def history():
    user_id = request.user['id']
    chats = list_chats_for_user(user_id)
    return jsonify(chats), 200


@app.route('/history/<int:chat_id>', methods=['GET'])
@token_required
def get_history(chat_id):
    user_id = request.user['id']
    chat = get_chat_messages(chat_id, user_id)
    if not chat:
        return jsonify({"error": "Chat não encontrado"}), 404
    return jsonify(chat), 200


@app.route('/chat', methods=['POST'])
@token_required
def chat():
    user_id = request.user['id']
    data = request.get_json() or {}
    bot_name = data.get('bot_name')
    history = data.get('history', [])
    new_message = data.get('new_message')
    chat_id = data.get('chat_id')  # optional
    title = data.get('title')

    if not bot_name or new_message is None:
        return jsonify({"error": "`bot_name` e `new_message` são obrigatórios"}), 400

    # Simple placeholder bot logic - echo with bot name
    bot_response = f"{bot_name} resposta automática: {new_message}"

    # Build new history
    new_history = list(history) if isinstance(history, list) else []
    new_history.append({"role": "user", "content": new_message})
    new_history.append({"role": "assistant", "content": bot_response})

    # Title fallback
    if not title:
        # try to create from first user message if available
        title = (new_history[0]['content'][:60] + '...') if new_history else f"Chat with {bot_name}"

    # Save or update
    if chat_id:
        ok = update_chat(chat_id, user_id, new_history)
        if not ok:
            # If update failed (not found), create new
            chat_id = create_chat(user_id, bot_name, title, new_history)
    else:
        chat_id = create_chat(user_id, bot_name, title, new_history)

    return jsonify({"response": bot_response, "chat_id": chat_id}), 200


if __name__ == '__main__':
    port = getattr(config, 'BACKEND_PORT', 5000)
    debug = getattr(config, 'DEBUG_MODE', True)
    app.run(host='0.0.0.0', port=port, debug=debug)
