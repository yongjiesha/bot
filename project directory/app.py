import os
from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = data['prompt']
    try:
        response = openai.Completion.create(
            engine="gpt-4",  # Corrected engine name
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7
        )
        answer = response.choices[0].text.strip()  # Extracting the response text
        return jsonify({"response": answer})
    except openai.error.OpenAIError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
