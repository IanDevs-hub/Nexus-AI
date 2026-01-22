import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

# Initialize the Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def home():
    return "Nexus Core Online", 200

@app.route('/health')
def health():
    return "Healthy", 200

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    try:
        # FIX: Switched from 'gemini-2.0-flash' to 'gemini-1.5-flash'
        # '1.5-flash' is the stable version with the open Free Tier quota.
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=user_message
        )
        return jsonify({'reply': response.text})
    except Exception as e:
        error_msg = str(e)
        # If we still hit a rate limit, tell the user clearly
        if "429" in error_msg:
            return jsonify({'error': "Nexus Cooling Down. Please wait 30s."}), 429
        return jsonify({'error': f"Neural Link Error: {error_msg}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
