from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # This will allow all origins by default

# Generate 30 random email addresses for testing
def generate_random_emails(num):
    emails = []
    for i in range(1, num + 1):
        emails.append(f"member{i}@example.com")
    return emails

# List of randomly generated members (emails)
members = {email: f"Member {i+1}" for i, email in enumerate(generate_random_emails(30))}

# List of available numbers from 1 to 30
available_numbers = list(range(1, 31))

# Dictionary to store selected numbers for each member
selected_numbers = {}

# Function to verify the identity using email
def verify_email(email):
    return email in members

# API to select a random number
@app.route('/select_number', methods=['POST'])
def select_number():
    global available_numbers, selected_numbers

    data = request.json
    email = data.get('email')

    if email and verify_email(email):
        if email not in selected_numbers:
            chosen_number = random.choice(available_numbers)
            available_numbers.remove(chosen_number)
            selected_numbers[email] = chosen_number
            return jsonify({"message": f"{members[email]} has selected number {chosen_number}.", "status": "success", "number": chosen_number}), 200
        else:
            return jsonify({"message": f"{members[email]} has already selected a number!", "status": "error"}), 400
    else:
        return jsonify({"message": "Invalid email. Please try again.", "status": "error"}), 400

# API to show the final selected numbers
@app.route('/show_results', methods=['GET'])
def show_results():
    results = {members[email]: number for email, number in selected_numbers.items()}
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
