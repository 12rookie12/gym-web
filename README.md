# Gym Web Project

This is a Flask-based web application for a gym website. It includes various pages such as home, contact, progress, programs, and a chatbot feature.

## Prerequisites

- Python 3.8 or higher installed on your machine.
- Recommended to use a virtual environment to manage dependencies.

## Setup and Running Locally

Follow these steps to set up and run the project locally on your machine:

1. **Clone or download the project files** to your local machine.

2. **Create a virtual environment** (optional but recommended):

   On Windows (Command Prompt):
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

   On macOS/Linux (bash):
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required dependencies**:

   ```
   pip install -r requirements.txt
   ```

4. **Set environment variables** (optional):

   The app uses a secret key for session management. By default, it uses a hardcoded key, but you can set your own:

   On Windows (Command Prompt):
   ```
   set SECRET_KEY=your_secret_key_here
   ```

   On macOS/Linux (bash):
   ```
   export SECRET_KEY=your_secret_key_here
   ```

5. **Run the Flask application**:

   ```
   python app.py
   ```

6. **Access the application**:

   Open your web browser and go to [http://localhost:5000](http://localhost:5000)

## Notes

- The project uses Flask-Session for session management.
- The app includes blueprints for chatbot and visualization features.
- Static files and templates are included in the `static/` and `templates/` directories respectively.

## Sharing

To share this project on your resume or portfolio, you can include this README along with the project files. Anyone with Python installed can follow these instructions to run the app locally.

---
