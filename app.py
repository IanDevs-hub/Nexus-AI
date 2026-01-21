import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Stability: Force REST transport
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"), transport="rest")

@app.route('/', methods=['GET'])
def home():
    # This specifically fixes the UptimeRobot 405 error
    return "Nexus Core Online", 200

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    # Using the most stable 2026 model names
    model_map = {
        "gemini-3-flash-preview": "gemini-1.5-flash", # Use 1.5-flash as the stable anchor
        "gemini-3-pro-preview": "gemini-1.5-pro",
        "gemini-2.5-pro": "gemini-1.5-pro"
    }
    
    # Get the real model name or default to flash
    model_name = model_map.get(data.get('model'), "gemini-1.5-flash")

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(user_message)
        return jsonify({'reply': response.text})
    except Exception as e:
        # If the preview models are "shaking", this fallback will save it
        try:
            fallback = genai.GenerativeModel("gemini-1.5-flash")
            res = fallback.generate_content(user_message)
            return jsonify({'reply': res.text})
        except Exception as e2:
            return jsonify({'error': f"Core Error: {str(e2)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
