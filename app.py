from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# Replace with your Render PostgreSQL database URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://my_db_haa1_user:s3wHj1tHFRwq0F8YuhjBzLa6O280wxAO@dpg-d09navruibrs73fghjt0-a.oregon-postgres.render.com/my_db_haa1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return '''
    <h2>Flask Login & Register</h2>
    <h3>Register</h3>
    <input id="reg_user" placeholder="Username">
    <input id="reg_pass" type="password" placeholder="Password">
    <button onclick="register()">Register</button>

    <h3>Login</h3>
    <input id="log_user" placeholder="Username">
    <input id="log_pass" type="password" placeholder="Password">
    <button onclick="login()">Login</button>

    <pre id="output"></pre>

    <script>
    async function register() {
        const username = document.getElementById('reg_user').value;
        const password = document.getElementById('reg_pass').value;
        const res = await fetch('/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        document.getElementById('output').innerText = await res.text();
    }

    async function login() {
        const username = document.getElementById('log_user').value;
        const password = document.getElementById('log_pass').value;
        const res = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        document.getElementById('output').innerText = await res.text();
    }
    </script>
    '''

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return 'Username already exists', 400
    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return 'User registered successfully', 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return 'Invalid username or password', 401
    return 'Login successful', 200

if __name__ == '__main__':
    app.run(debug=True)
