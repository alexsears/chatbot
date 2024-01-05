from flask import Flask, request, jsonify, render_template, session
from flask_session import Session
import openai
import os

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_secret_key_here')  # Set a secret key for session
Session(app)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    custom_instruction = data.get('custom_instruction', '')
    user_message = data['message']



    
    # Retrieve the current session's history
    if 'history' not in session:
        session['history'] = []

    history = session['history']

    try:
        # Include the custom instruction and user message in the prompt
        # Construct the prompt with custom instruction and user message
        # Construct the prompt with custom instruction and user message
        prompt = f"{custom_instruction}\nUser: {user_message}"
        print(f"Sending prompt to OpenAI: {prompt}")

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        # Update history in the session
        history.append(f"User: {user_message}")
        history.append(f"Chatbot: {response.choices[0].message['content']}")
        session['history'] = history

        return jsonify({'message': response.choices[0].message['content']})
    except Exception as e:
        # Log the exception and return an error message
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred while processing your message.'})

@app.route('/set_custom_instruction', methods=['POST'])
def set_custom_instruction():
    data = request.json
    session['custom_instruction'] = data['instruction']
    return jsonify({'message': 'Custom instruction set successfully'})

@app.route('/')
def index():
    return render_template('chatbot.html')

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.logger.setLevel('DEBUG')
    app.run(host='0.0.0.0', port=port, debug=True)
