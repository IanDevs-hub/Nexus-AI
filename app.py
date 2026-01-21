import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# This allows your GitHub Pages site to talk to this Render server
CORS(app)

# 1. STABILITY UPGRADE: Use "rest" transport for reliable free-tier connections
# This prevents the "Interface Timeout" errors
genai.configure(
    api_key=os.environ.get("GEMINI_API_KEY"),
    transport="rest"
)

@app.route('/')
def home():
    # 2. HEALTH CHECK: This is what UptimeRobot looks for to keep Nexus awake
    return "Nexus Core Online", 200

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    # 3. BRAIN UPGRADE: Support for Gemini 3 and Gemini 2.5
    # Defaulting to 'gemini-3-flash-preview' for 2026 speed
    chosen_model = data.get('model', 'gemini-3-flash-preview')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Initialize the chosen Brain
        model = genai.GenerativeModel(chosen_model)
        
        # Generate the response
        response = model.generate_content(user_message)
        
        return jsonify({'reply': response.text})
    
    except Exception as e:
        # EMERGENCY RECOVERY: If a specific model is down, use base Flash
        try:
            fallback_model = genai.GenerativeModel('gemini-3-flash-preview')
            fallback_res = fallback_model.generate_content(user_message)
            return jsonify({'reply': fallback_res.text})
        except:
            # If everything fails, tell the user to wait for the wake-up
            return jsonify({'error': "Nexus Core Re-syncing. Please retry in 10s."}), 500

if __name__ == '__main__':
    # 4. PORT BINDING: Essential for Render to find your app
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
