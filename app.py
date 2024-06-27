import os
from flask import Flask, request, jsonify, render_template
import openai
import logging

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure logging
logging.basicConfig(level=logging.DEBUG)

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
        response = openai.Completion.create(
            engine="gpt-4",  # Ensure this is the correct engine
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7
        )
        logging.debug(f"OpenAI response: {response}")
        answer = response.choices[0].text.strip()
        return jsonify({"response": answer})
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)
