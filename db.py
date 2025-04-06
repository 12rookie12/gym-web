from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = 'gym_progress.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS progress
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  date TEXT,
                  exercise TEXT,
                  weight REAL,
                  reps INTEGER)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_progress', methods=['POST'])
def add_progress():
    data = request.json
    user_id = data['user_id']
    date = datetime.now().strftime('%Y-%m-%d')
    exercise = data['exercise']
    weight = data['weight']
    reps = data['reps']

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT INTO progress (user_id, date, exercise, weight, reps) VALUES (?, ?, ?, ?, ?)',
              (user_id, date, exercise, weight, reps))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

@app.route('/get_progress/<int:user_id>')
def get_progress(user_id):
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql_query(f'SELECT * FROM progress WHERE user_id = {user_id}', conn)
    conn.close()

    if df.empty:
        return jsonify({'error': 'No data found'})

    
    fig = px.line(df, x='date', y='weight', color='exercise', title='Gym Progress Over Time')
    graph_json = fig.to_json()

    return jsonify({'graph_json': graph_json})

if __name__ == '__main__':
    app.run(debug=True)