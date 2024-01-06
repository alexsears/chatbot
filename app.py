from flask import Flask, request, jsonify, render_template, session
from flask_session import Session
from langchain.chains.llm import LLMChain  # Correct import for LLMChain
from langchain.llms import OpenAI  # Assuming you are using OpenAI's models
from langchain.prompts import PromptTemplate

import openai
import os

app = Flask(__name__)

# Rest of your Flask app setup...


# Configuration
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_secret_key_here')  # It's good to have a fallback secret key

# Ensure sessions are set up correctly
Session(app)
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    print("Received data:", data)  # Debugging: check received data

    user_message = data['message']
    custom_instruction = data.get('custom_instruction', '')
    print("User message:", user_message)  # Debugging: user message
    print("Custom instruction:", custom_instruction)  # Debugging: custom instruction

    # Retrieve and update the current session's history
    history = session.get('history', [])
    history.append(f"User: {user_message}")
    print("Updated history:", history)  # Debugging: check history

    # Construct the prompt with custom instruction
    full_prompt = f"{custom_instruction}\n" + "\n".join(history) if custom_instruction else "\n".join(history)
    print("Constructed prompt:", full_prompt)  # Debugging: check the full prompt

    try:
        # Initialize LangChain and process the prompt
        prompt = PromptTemplate(input_variables=[], template=full_prompt)
        llm_chain = LLMChain(llm=OpenAI(), prompt=prompt)
        response = llm_chain.run({"prompt": full_prompt})
        print("Response from LLMChain:", response)  # Debugging: check response

        # Directly use the response string
        bot_response = response  
        history.append(f"Chatbot: {bot_response}")
        session['history'] = history

        return jsonify({'message': bot_response})
    except Exception as e:
        print(f"An error occurred: {e.__class__.__name__}: {e}")  # Improved error message
        return jsonify({'error': 'An error occurred while processing your message.'})

@app.route('/set_custom_instruction', methods=['POST'])
def set_custom_instruction():
    data = request.json
    session['custom_instruction'] = data['instruction']
    return jsonify({'message': 'Custom instruction set successfully'})

@app.route('/')
def index():
    # Using 'index.html' is more conventional than 'chatbot.html'
    return render_template('index.html')  

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.logger.setLevel('DEBUG')
    app.run(host='0.0.0.0', port=port, debug=True)
