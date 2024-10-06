from flask import Flask, render_template, request, jsonify

from opneAI import ask_openai

app = Flask(__name__)

# Initialize a conversation history
conversation_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    conversation_history.append(f"You: {user_input}")

    response = ask_openai(user_input)
    conversation_history.append(f"Bot: {response}")

    return jsonify(conversation=conversation_history)

if __name__ == '__main__':
    app.run(debug=True)
