from flask import Flask, render_template
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

# Initialize main Flask app
app = Flask(__name__, static_folder='static')


# =================================================================
# 1. ROUTES FOR STATIC HTML PAGES
# =================================================================
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/bot")
def bot():
    return render_template("bot.html")

@app.route("/contact")
def contact():
    return render_template("contact_us.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/get-started")
def get_started():
    return render_template("get_started.html")

@app.route("/programs")
def programs():
    return render_template("our_programs.html")

@app.route("/track")
def progress():
    return render_template("progress.html")

# =================================================================
# 2. INTEGRATE SUB-APPS (NO CHANGES TO chat.py OR visual.py)
# =================================================================
# Import and mount existing apps
from chat import app as chat_app  # Your original chat.py (Flask app)
#from visual import server as visual_server  # Your original visual.py (Dash app)

# Mount them under specific URLs
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/chat': chat_app,      # Access at http://localhost:5000/chat
    #'/track': visual_server # Access at http://localhost:5000/track
})

# =================================================================
# 3. RUN THE APP
# =================================================================
if __name__ == "__main__":
    app.run('localhost', 5000, app.wsgi_app, use_reloader=True, use_debugger=True)