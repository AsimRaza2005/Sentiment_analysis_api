from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Define Groq API Key and Endpoint (Replace with actual values)
GROQ_API_KEY = "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"
GROQ_LLM_URL = "https://api.groq.com/openai/v1/chat/completions"

# In-memory storage for analyzed data
sentiment_data = []

# Function to call Groq LLM for sentiment analysis
def analyze_sentiment(text):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "Analyze the sentiment of the following text and classify it as Positive, Negative, or Neutral."},
            {"role": "user", "content": text}
        ]
    }

    response = requests.post(GROQ_LLM_URL, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Route for POST method (Sentiment Analysis)
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "Text is required"}), 400

        sentiment = analyze_sentiment(text)
        
        # Store the result in sentiment_data list
        sentiment_data.append({"text": text, "sentiment": sentiment})

        return jsonify({"text": text, "sentiment": sentiment})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for GET method (Retrieve stored sentiment data)
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify({"stored_data": sentiment_data})

# Route for GET method (Health Check)
@app.route('/status', methods=['GET'])
def status():
    return jsonify({"message": "Sentiment Analysis API is running"}), 200

if __name__ == '__main__':
    app.run(debug=True)
