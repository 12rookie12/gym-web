from flask import request, jsonify, render_template, session
from datetime import datetime, timedelta
import json
import os
from flask import Blueprint

app = Blueprint('visual', __name__, static_folder='static', template_folder='templates')

# File to store data
DATA_FILE = 'calorie_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        'consumed': 0,
        'burned': 0,
        'foodEntries': [],
        'exerciseEntries': [],
        'dailyHistory': {},
        'currentWeight': None
    }

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_today():
    return datetime.now().strftime('%Y-%m-%d')

def update_daily_history(data, date, consumed_change=0, burned_change=0):
    if date not in data['dailyHistory']:
        data['dailyHistory'][date] = {'consumed': 0, 'burned': 0}
    
    data['dailyHistory'][date]['consumed'] += consumed_change
    data['dailyHistory'][date]['burned'] += burned_change

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-data')
def get_data():
    data = load_data()
    return jsonify(data)

@app.route('/add-food', methods=['POST'])
def add_food():
    data = load_data()
    entry = request.get_json()
    
    # Add to entries
    data['foodEntries'].append(entry)
    
    # Update totals
    calories = int(entry['calories'])
    data['consumed'] += calories
    
    # Update daily history
    today = get_today()
    update_daily_history(data, today, consumed_change=calories)
    
    save_data(data)
    return jsonify({
        'consumed': data['consumed'],
        'foodEntries': data['foodEntries'],
        'dailyHistory': data['dailyHistory']
    })

@app.route('/add-exercise', methods=['POST'])
def add_exercise():
    data = load_data()
    entry = request.get_json()
    
    # Add to entries
    data['exerciseEntries'].append(entry)
    
    # Update totals
    calories = int(entry['calories'])
    data['burned'] += calories
    
    # Update daily history
    today = get_today()
    update_daily_history(data, today, burned_change=calories)
    
    save_data(data)
    return jsonify({
        'burned': data['burned'],
        'exerciseEntries': data['exerciseEntries'],
        'dailyHistory': data['dailyHistory']
    })

@app.route('/update-weight', methods=['POST'])
def update_weight():
    data = load_data()
    weight_data = request.get_json()
    
    # Update current weight
    data['currentWeight'] = float(weight_data['weight'])
    
    save_data(data)
    return jsonify({
        'currentWeight': data['currentWeight']
    })

if __name__ == '__main__':
    app.run(debug=True)