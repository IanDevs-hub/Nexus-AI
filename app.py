import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai # This is the NEW 2026 library

app = Flask(__name__)
CORS(app)

# Initialize the NEW Client
# Make sure GEMINI_API_KEY is in your Render Env Variables!
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def home():
    # This keeps UptimeRobot happy (returning 200)
    return "Nexus Core Online", 200

@app.route('/health')
def health():
    # This fixes the 404 error UptimeRobot was getting at /health
    return "Healthy", 200

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    # 2026 Model Names
    # We use 'gemini-2.0-flash' or 'gemini-3.0-flash'
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=user_message
        )
        return jsonify({'reply': response.text})
    except Exception as e:
        # If the key is leaked or model is busy, show clear error
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg:
            return jsonify({'error': "SECURITY ALERT: New API Key needed in Render Settings."}), 403
        return jsonify({'error': f"Neural Link Error: {error_msg}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
