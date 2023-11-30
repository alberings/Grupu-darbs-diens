from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Dummy user data - replace with a real database in production
# users = {'user1@example.com': {'password': 'password123', 'name': 'User One'}}

@app.route('/')
def home():
    # Render the home page
    return render_template('index.html')

@app.route('/get-menu-plan', methods=['GET', 'POST'])
def get_menu_plan():
    if request.method == 'POST':
        # Handle form submission for the menu plan
        # Redirect to home for now
        return redirect(url_for('home'))

    # Render the 'Get Menu Plan' page
    return render_template('get_menu_plan.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return 'User already exists'

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new user instance and add it to the database
        new_user = User(email=email, password=hashed_password, name=name)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Query the user from the database
        user = User.query.filter_by(email=email).first()

        # Check if user exists and the password is correct
        if user and check_password_hash(user.password, password):
            session['user'] = {'email': user.email, 'name': user.name}
            return redirect(url_for('profile'))

        return redirect(url_for('login', error=True))

    return render_template('login.html', error=request.args.get('error'))

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('profile.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'  # Use the database of your choice
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Define your user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(100))

# Other route definitions...

if __name__ == '__main__':
    app.run(debug=True)
