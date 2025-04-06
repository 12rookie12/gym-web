from flask import Flask, request, jsonify, render_template, session
from textblob import TextBlob
import difflib
import re
import os
from flask_session import Session

app = Flask(__name__)


app.config["SESSION_TYPE"] = "filesystem" 
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey123")  
Session(app)


responses = {
    "hi": "Hello!",
    "hello": "Hey there! How can I help you with your fitness goals?",
    "hey": "Hi there! Ready to crush your fitness goals today? 🚀",
    "gym timings": "We are open from 6 AM to 10 PM daily.",
    "membership fees": "Our monthly membership starts at $30. We also offer yearly discounts!",
    "personal trainer": "Yes! We have certified trainers available. Would you like a session?",
    "facilities": "We have a full range of cardio machines, free weights, resistance training, and group classes!",
    "group classes": "We offer yoga, HIIT, Zumba, and strength training classes. Interested in joining?",
    "location": "Oxy-Genz Gym is located at Malad(East). Visit us anytime!",
    "workout plan": "It depends on your goal! Do you want a plan for weight loss, muscle gain, or general fitness?",
    "best exercise": "Squats, deadlifts, and bench press are great for strength. Want a detailed workout?",
    "cardio or weights": "Both are important! Cardio for endurance and fat loss, weights for muscle growth.",
    "how often should i train": "For best results, aim for at least 3-5 workout sessions per week!",
    "warm-up exercises": "Jogging, jumping jacks, and dynamic stretches help prevent injuries!",
    "cool-down exercises": "Stretching and deep breathing after workouts help in muscle recovery.",
    "protein intake": "For muscle growth, aim for 1.6-2.2g of protein per kg of body weight.",
    "best sources of protein": "Chicken, fish, eggs, lentils, tofu, and protein shakes are great choices!",
    "pre-workout meal": "Eat carbs and protein 30-60 mins before training for energy!",
    "post-workout meal": "Protein + carbs help in muscle recovery. Try a protein shake or chicken with rice!",
    "how to lose weight": "A mix of cardio, strength training, and a calorie deficit diet works best!",
    "how to gain muscle": "Lift heavy, eat protein-rich meals, and get enough rest for recovery!",
    "cheat meal": "One cheat meal is fine! Just don’t turn it into a cheat week. 😆",
    "recovery tips": "Stretch, hydrate, and sleep 7-9 hours for better muscle recovery!",
    "muscle soreness": "Try foam rolling, stretching, and staying hydrated to reduce soreness.",
    "best supplements": "Whey protein, creatine, BCAAs, and multivitamins can help, but food comes first!",
    "hydration": "Drink at least 3 liters of water daily to stay hydrated and perform well!",
    "motivation": "Results take time! Stay consistent and trust the process. 💯🔥",
    "gym quotes": "No pain, no gain! 💪 What’s your excuse today? 😏",
    "fitness goal": "Whether it's weight loss, muscle gain, or endurance, I'm here to guide you!",
    "changing room facilities": "Yes, we have clean changing rooms with lockers!",
    "parking": "Yes, we have a dedicated parking area for gym members.",
    "membership cancellation": "You can cancel your membership anytime, but we’d love to have you stay!",
    "bye": "Goodbye! Stay fit and healthy! 💪🔥",
    "see you": "Take care and keep training hard! See you soon! 🚀",
    "thanks": "You're welcome! Keep pushing towards your goals! 🔥",
    "assalamualaikum": "walaikumassalam",  
    "no": "ok!fine",
    "yes": "please have the conversation on counter",
    "located": "Oxy-Genz Gym is located at Malad(East). Visit us anytime!",
    
}

def contains_vowel(name):
    vowels = "aeiouAEIOU"
    for char in name:
        if char in vowels:
            return True
    return False

def is_consonant(char):
    return char.isalpha() and char.lower() not in "aeiou"

def is_valid_name(name):
    vowels = "aeiouAEIOU"
    
    
    if len(name) < 4 or len(name) > 10:
        return False
    
    
    if name[0] not in vowels and not contains_vowel(name[1:]):
        return False
    
    
    if len(name) >= 4:
        if is_consonant(name[2]) and is_consonant(name[3]):
            return False
    
    return True

def extract_name(user_input):
    """Extracts the name from phrases like 'my name is Anas' or 'Anas is my name'."""
    
    user_input = re.sub(r"[^\w\s]", "", user_input)
    
    
    patterns = [
        r"my name is (\w+)",
        r"(\w+) is my name"
    ]
    for pattern in patterns:
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            return match.group(1).capitalize()
    return None

@app.route("/")
def home():
    return render_template("bot.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handles chatbot responses, including name extraction."""
    user_input = request.json.get("message", "").strip().lower()
    if not user_input:
        return jsonify({"response": "Please enter a valid question."})

    response = ""
    
    
    if "bmi" in user_input or re.search(r"\d+\s*(cm|m)?[^\d]*\d+\s*kg", user_input):
        response = calculate_bmi(user_input)
    
    
    elif difflib.get_close_matches(user_input, ["assalamualaikum"], n=1, cutoff=0.6):
        name = session.get("username", "there")
        response = f"Walaikumassalam {name}, how are you doing?"
    
 
    elif any(greet in user_input for greet in ["hello", "hi", "hey"]):
        name = session.get("username", "there")
        response = f"Hi {name}, how are you doing?"
    
    
    elif user_input in responses:
        response = responses[user_input]

    
    
    elif "quote" in user_input:
        if "gym" in user_input:
            response = responses.get("gym quotes", "I'm not sure I understand. Could you rephrase?")
        else:
            response = responses.get("gym quotes", "I'm not sure I understand. Could you rephrase?")
    
    
    else:
        name = extract_name(user_input)
        if name:
            if is_valid_name(name):
                session["username"] = name
                response = f"Got it, {name}! How can I assist you?"
            else:
                response = "Please enter a valid name. It must be 4-10 characters long, contain vowels, and the third and fourth characters cannot both be consonants."
        else:
            
            if re.fullmatch(r"^[a-z]+$", user_input) and user_input not in responses:
                if is_valid_name(user_input):
                    session["username"] = user_input.capitalize()
                    response = f"Got it, {session['username']}! How can I assist you?"
                else:
                    response = "Please enter a valid name. It must be 4-10 characters long, contain vowels, and the third and fourth characters cannot both be consonants."
            else:
                corrected_input = correct_spelling(user_input)
                response = find_best_match(corrected_input)
    
    session["last_question"] = user_input
    return jsonify({"response": response})

@app.route("/contextual_yes", methods=["POST"])
def get_contextual_yes():
    """Handles 'yes' responses based on previous context."""
    last_question = session.get("last_question", "")
    context_responses = {
        "personal trainer": "Great! You can book a trainer session at the front desk.",
        "group classes": "Awesome! Our classes run daily. Just drop by and join in!",
    }
    response = context_responses.get(last_question, "I appreciate your response! How else can I help?")
    return jsonify({"response": response})

def correct_spelling(text):
    """Corrects misspelled words in user input using TextBlob."""
    return str(TextBlob(text).correct()).lower()

def find_best_match(user_input):
    """Finds the best match from the responses dictionary using fuzzy matching."""
    possible_keys = list(responses.keys())
    closest_match = difflib.get_close_matches(user_input, possible_keys, n=1, cutoff=0.6)
    if closest_match:
        return responses.get(closest_match[0], "I'm not sure I understand. Could you rephrase?")
    
    
    for key in possible_keys:
        if key in user_input:
            return responses.get(key, "I'm not sure I understand. Could you rephrase?")
    
    return "I couldn't find an answer. Please ask something else!"

def calculate_bmi(user_message):
    """Extracts height and weight from user message and calculates BMI."""
    try:
        
        if "." in user_message:
            return "Please enter approximate values without decimal points for height and weight."
        
        match = re.search(r"(\d+)\s*(cm|m)?[^\d]*(\d+)\s*kg", user_message, re.IGNORECASE)
        if match:
            height = float(match.group(1))
            if match.group(2) and match.group(2).lower() == "cm":
                height /= 100  
            weight = float(match.group(3))
            bmi = weight / (height**2)
            category = (
                "Underweight" if bmi < 18.5 else
                "Normal weight" if bmi < 25 else
                "Overweight" if bmi < 30 else
                "Obese"
            )
            return f"Your BMI is {bmi:.2f}. Category: {category}."
        return "Please enter height and weight properly, e.g., '170 cm 70 kg'."
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)