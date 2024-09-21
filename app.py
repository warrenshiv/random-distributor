from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Enable CORS

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///number_picker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance

db = SQLAlchemy(app)  # Initialize the database

# Model for the User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    number = db.Column(db.Integer, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# List of provided email addresses
member_emails = [
    "adegoshadracktrap@gmail.com",
    "felixshigx7@gmail.com",
    "esthercherotich199@gmail.com",
    "lucymillie580@gmail.com",
    "warrenshiv@gmail.com",
    "Shigolidarius062@gmail.com",
    "raelouma@gmail.com",
    "delfredricluyenji@gmail.com",
    "marthaalimlim1@gmail.com",
    "jecintahnjoki94@gmail.com",
    "ayesajenty@gmail.com",
    "sarahchelagat87@gmail.com",
    "Mosesokiri29@gmail.com",
    "naomgesare81@gmail.com",
    "alicelooremetto@gmail.com",
    "Lynelinsley@gmail.com",
    "linettewanjiru17@gmail.com",
    "evelynatemba19@gmail.com",
    "isaackiprono27@gmail.com"
]

# In-memory data
members = {email: f"Member {i+1}" for i, email in enumerate(member_emails)}
available_numbers = list(range(1, len(member_emails) + 1))
selected_numbers = {}

# Function to verify if the email exists in the system
def verify_email(email):
    return email in members

# API to select a random number and save it to the database
@app.route('/select_number', methods=['POST'])
def select_number():
    data = request.json
    email = data.get('email')

    if email and verify_email(email):
        # Check if the user has already selected a number
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": f"{members[email]} has already selected number {existing_user.number}!", "status": "error"}), 400
        
        # Select a random number
        if available_numbers:
            chosen_number = random.choice(available_numbers)
            available_numbers.remove(chosen_number)
            selected_numbers[email] = chosen_number
            
            # Save the selected number in the database
            new_user = User(email=email, number=chosen_number)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({"message": f"{members[email]} has selected number {chosen_number}.", "status": "success", "number": chosen_number}), 200
        else:
            return jsonify({"message": "No more numbers available.", "status": "error"}), 400
    else:
        return jsonify({"message": "Invalid email. Please try again.", "status": "error"}), 400

# API to show the final selected numbers from the database
@app.route('/show_results', methods=['GET'])
def show_results():
    users = User.query.all()
    results = {user.email: user.number for user in users}
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
