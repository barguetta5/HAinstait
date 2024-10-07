from sqlalchemy import create_engine, Column, String, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, request, jsonify
from datetime import datetime

from opneAI import ask_openai

app = Flask(__name__)

# Change to your local or global database server
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:king1471@localhost/UsersFeedback'

# Initialize SQLAlchemy
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# Define the ChatHistory model
class ChatHistory(Base):
    __tablename__ = 'chat_history'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# Create the database tables if they don't exist
Base.metadata.create_all(engine)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_id = request.form['user_id']  # Assuming user_id is sent from the frontend
    username = request.form['username']  # Assuming username is sent from the frontend
    user_input = request.form['user_input']

    # Generate response from OpenAI
    response = ask_openai(user_input)

    # Save to database
    chat_entry = ChatHistory(user_id=user_id, username=username, question=user_input, answer=response)
    session.add(chat_entry)
    session.commit()

    # Print all the DB
    results = session.query(ChatHistory).all()
    print(results)

    # results = session.query(Users).filter(Users.ID == 123)
    # for r in results:
    #     print(r)

    return jsonify(question=user_input, answer=response)


if __name__ == '__main__':
    app.run(debug=True)
