# Import necessary libraries
import os
import pandas as pd
from transformers import pipeline
from flask import Flask, request, jsonify
from pyngrok import ngrok
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from config import API_KEY
from sklearn.model_selection import train_test_split

# Set your OpenAI GPT-3 API key as an environment variable
os.environ['API_KEY'] = API_KEY

# Load and preprocess the provided dataset for intent recognition
file_path = r'C:\Users\vshwe\Documents\AI project/dialogs.txt'
data = pd.read_csv(file_path, sep='\t', names=['Question', 'Answer'])
X = data['Question']
y = data['Answer']

# Initialize intent recognition model
tfidf_vectorizer = TfidfVectorizer()
X_tfidf = tfidf_vectorizer.fit_transform(X)
intent_model = MultinomialNB()
intent_model.fit(X_tfidf, y)

# Initialize GPT-3 pipeline for response generation
generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')

# Create a Flask web app
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    if 'user_message' in request.form:
        user_message = request.form['user_message']

        # Recognize the intent of the user message
        user_message_tfidf = tfidf_vectorizer.transform([user_message])
        recognized_intent = intent_model.predict(user_message_tfidf)[0]

        # Generate a response based on the recognized intent using GPT-3
        bot_response = generator(user_message, max_length=50, do_sample=True)[0]['generated_text']

        return jsonify({'intent': recognized_intent, 'bot_response': bot_response})
    else:
        return jsonify({'error': 'Invalid request'})

if __name__ == '__main__':
    # Set up Ngrok to create a public URL for the Flask app
    public_url = ngrok.connect(addr='5000')
    print(' * ngrok tunnel "' + public_url.public_url + '" -> "http://127.0.0.1:5000"')

    # Start the Flask app
    app.run(host='0.0.0.0', port=5000)

