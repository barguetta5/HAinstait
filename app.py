import json

import pytest
import psycopg2
from psycopg2 import sql
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, Text, DateTime, inspect
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, request, jsonify, session as flask_session
from opneAI import ask_openai

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Not necessary for now

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:king1471@localhost/InasitAsigment'

# Initialize SQLAlchemy
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base = declarative_base()
Session = sessionmaker(bind=engine)
db_session = Session()
user_history = []


# ChatHistory DB set another why by terminal running alembic.
class ChatHistory(Base):
    __tablename__ = 'chat_history'
    user_id = Column(String(200), primary_key=True)
    username = Column(String(100), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# Create the database table if not exist
# above the class ChatHistory make some bugs with creating the DB
Base.metadata.create_all(engine)

# The implement with the front side
@app.route('/')
def index():
    return render_template('index.html')

# Login pop up massage for user
@app.route('/set_user', methods=['POST'])
def set_user():
    user_id = request.form['user_id']
    username = request.form['username']

    # Check if the user already exists
    user_exists = user_check(user_id)

    # Set a pop up massage for exist users or not exist users.
    if user_exists:
        flask_session['user_id'] = user_id
        flask_session['username'] = username
        return jsonify({"message": "User exists, proceed to chat."}), 200
    else:
        flask_session['user_id'] = user_id
        flask_session['username'] = username
        return jsonify({"message": "New user created, proceed to chat."}), 200


@pytest.fixture
@app.route('/chat', methods=['POST'])
def chat():
    user_id = flask_session.get('user_id')  # Get user_id from session
    username = flask_session.get('username')  # Get username from session
    user_input = request.form['user_input']

    # If user have no internet or open AI key so he can't get chat response
    try:
        response = ask_openai(user_input,user_id)
        # user_history.append([user_input, response])
        # user_inputs = [user_in[0] for user_in in user_history]
        # responses = [res[1] for res in user_history]
        #
        # user_update(user_id, username, user_inputs, responses)
        # return jsonify(question=user_input, answer=response)

        user_history.append([user_input, response])

        # Use json.dumps to create JSON from user history
        user_inputs_json = json.dumps([user_in[0] for user_in in user_history])
        responses_json = json.dumps([res[1] for res in user_history])

        # Update user data with the serialized JSON
        user_update(user_id, username, user_inputs_json, responses_json)

        # Return the response
        return jsonify(question=user_input, answer=response)

    except:
        flask_session['user_id'] = user_id
        flask_session['username'] = username
        return jsonify({"message": "openAI key wrong"}), 200



@pytest.fixture
@app.route('/get_chat_history', methods=['POST'])
def get_chat_history():
    user_id = flask_session.get('user_id')

    # Fetch all chat history for the user
    chat_history = get_last_chat(user_id)

    # Insert all the chat history to array before printing
    history = []
    for entry in chat_history:
        history.append({
            "question": entry.question,
            "answer": entry.answer,
        })

    return jsonify(history)


def db_creating():
    # Establishing the connection
    conn = psycopg2.connect(
        database="postgres", user='postgres', password='king1471', host='127.0.0.1', port='5432'
    )
    conn.autocommit = True

    # Creating a cursor object
    cursor = conn.cursor()

    # Database name
    db_name = 'InasitAsigment'

    # Check if the database exists
    cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [db_name])
    exists = cursor.fetchone()

    if not exists:
        # Prepare to create the database
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        print(f"Database '{db_name}' created successfully.")
    else:
        print(f"Database '{db_name}' already exists.")

    # Closing the connection
    cursor.close()
    conn.close()


def user_check(user_id):
    return db_session.query(ChatHistory).filter_by(user_id=user_id).first() is not None

def user_update(user_id, username, user_inputs, responses):
    # Check if user_id exist
    existing_chat = db_session.query(ChatHistory).filter_by(user_id=user_id).first()

    if existing_chat:
        # Update the existing record
        existing_chat.question = user_inputs
        existing_chat.answer = responses
    else:
        # Create a new chat entry
        chat_entry = ChatHistory(user_id=user_id, username=username, question=user_inputs, answer=responses)
        db_session.add(chat_entry)

    db_session.commit()

def get_last_chat(user_id):
    return db_session.query(ChatHistory).filter_by(user_id=user_id).all()
