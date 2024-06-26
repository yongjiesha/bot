import os
from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)  # Make sure this is a valid Flask app instance.
openai.api_key = os.getenv("OPENAI_API_KEY")  # Replace with your environment variable name.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = data['prompt']
    try:
        response = openai.Completion.create(
            engine="gpt-4o",  # Check the engine - 'gpt-4o' seems incorrect.
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7
        )
        return jsonify(response)
    except openai.error.OpenAIError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
