from flask import Flask, render_template
from flask_session import Session
from bot import app as bot_app
from visual import app as visual_app
import os

app = Flask(__name__)

# Enhanced session configuration
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "supersecretkey123"),
    SESSION_TYPE="filesystem",
    SESSION_COOKIE_NAME="your_session_cookie",  # Explicitly set cookie name
    SESSION_FILE_DIR="/tmp/flask_session",  # Required for filesystem sessions
    SESSION_PERMANENT=False,
    PERMANENT_SESSION_LIFETIME=3600  # 1 hour
)

# Initialize session before registering blueprints
Session(app)

# Register blueprints
app.register_blueprint(bot_app, url_prefix='/bot')
app.register_blueprint(visual_app, url_prefix='/visual')

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contactus.html')

@app.route('/progress')
def progress():
    return render_template('progress.html')

@app.route('/getstarted')
def getstarted():
    return render_template('getstarted.html')

@app.route('/spinning')
def spinning():
    return render_template('spinning.html')

@app.route('/freeweight')
def freeweight():
    return render_template('freeweight.html')

@app.route('/cardio')
def cardio():
    return render_template('cardio.html')

@app.route('/equipments')
def equipments():
    return render_template('equipments.html')

@app.route('/programs')
def programs():
    return render_template('programs.html')

@app.route('/getfreetrial')
def getfreetrial():
    return render_template('getfreetrial.html')

@app.route('/bot')
def urassistant():
    return render_template('bot.html')

if __name__ == '__main__':
    # Create session directory if it doesn't exist
    if app.config['SESSION_TYPE'] == 'filesystem':
        os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)