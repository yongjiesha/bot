import os
from flask import Flask, request, jsonify, render_template
import openai
import logging
from openai import OpenAI
from openai import AsyncOpenAI
import mysql.connector

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Database configuration
db_config = {
    'user': 'root',  # Replace with your database username
    'password': '',  # Replace with your database password
    'host': '127.0.0.1',
    'database': 'safetynetbot'
}

def insert_conversation(user_id, UserInput, GPTResponse):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "INSERT INTO conversation (UserID, UserInput, GPTResponse) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, UserInput, GPTResponse))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except mysql.connector.Error as err:
        logging.error(f"Error: {err}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    logging.debug(f"Received request data: {data}")
    prompt = data.get('prompt', '')
    if not prompt:
        logging.error("No prompt found in the request")
        return jsonify({"error": "No prompt provided"}), 400

    try:
        response = client.chat.completions.create(
             model="gpt-4o",  # Use the specified model
             messages=[{"role": "user", "content": prompt}],
             max_tokens=300,
             n=1,
             stop=None,
             temperature=0.7
         )
        answer = response.choices[0].message.content
        logging.debug(f"OpenAI response: {response}")

        # Insert conversation into the database
        user_id = "user123"  # Replace with actual user ID if available
        if not insert_conversation(user_id, prompt, answer):
            return jsonify({"error": "Failed to save conversation to database"}), 500

        return jsonify({"response": answer})
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    
# def ask():
#     data = request.json
#     logging.debug(f"Received request data: {data}")
#     prompt = data.get('prompt', '')
#     if not prompt:
#         logging.error("No prompt found in the request")
#         return jsonify({"error": "No prompt provided"}), 400

#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o",  # Use the specified model
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=300,
#             n=1,
#             stop=None,
#             temperature=0.7
#         )
#         answer = response.choices[0].message.content
#         print("Assistant: " + response.choices[0].message.content)
#         # for chunk in response:
#         #     choices = chunk['choices']
#         #     for choice in choices:
#         #         if 'delta' in choice and 'content' in choice['delta']:
#         #             answer += choice['delta']['content']
        
#         logging.debug(f"OpenAI response: {response}")
#         return jsonify({"response": answer})
#     except Exception as e:
#         logging.error(f"Unexpected error: {e}")
#         return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)
