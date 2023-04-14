from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from agent.agent import ChatBot
import time
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

agent = ChatBot()

messages = [
    {'text': "hiiiiii", 'sender': 'bot', 'timestamp': "time"},
    {'text': "hiiiiii", 'sender': 'user', 'timestamp': "time"},
    {'text': "hiiiiii", 'sender': 'bot', 'timestamp': "time"},
    {'text': "hiiiiii", 'sender': 'user', 'timestamp': "time"},
    {'text': "hiiiiii", 'sender': 'bot', 'timestamp': "time"}
]

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    # Retrieve the video ID from the request
    video_id = request.form['video_id']
    
    # Use the video ID to retrieve the video captions and summarize them
    # captions = get_captions(video_id)
    # summary = summarize_captions(captions)
    
    # Return the summary as a JSON response
    response = {'summary': summary}
    return jsonify(response)


def generate_response(message):
    # Placeholder function that returns a random message as a response
    bot_response = agent.chat(input_message=message)
    print(bot_response)
    return bot_response

@socketio.on('message')
def handle_message(message_text):
    user_message = {'text': message_text, 'sender': 'user', 'timestamp': str(datetime.now())}
    messages.append(user_message)
    emit('update_messages', {'messages': messages}, broadcast=True)
    bot_message = {'text': generate_response(message_text), 'sender': 'bot', 'timestamp': str(datetime.now())}
    time.sleep(1)
    messages.append(bot_message)
    emit('update_messages', {'messages': messages}, broadcast=True)

@socketio.on('connect')
def on_connect():
    # Send message history to the user
    emit('update_messages', {'messages': messages})


if __name__ == '__main__':
    socketio.run(app, debug=True)
