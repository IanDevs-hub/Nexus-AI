import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# 1. 2026 CONNECTIVITY: Using the stable 'rest' transport
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"), transport="rest")

@app.route('/', methods=['GET'])
def home():
    return "Nexus Core Online", 200

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    # 2. 2026 MODEL MAPPING: Fixing the 404 Error
    # We map your UI buttons to the new 2026 production names
    model_map = {
        "gemini-3-flash-preview": "gemini-3-flash",
        "gemini-3-pro-preview": "gemini-3-pro",
        "gemini-2.5-pro": "gemini-2.5-pro"
    }
    
    # Get the model name, or use the 'latest' alias which never 404s
    requested_name = data.get('model')
    model_name = model_map.get(requested_name, "gemini-flash-latest")

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(user_message)
        return jsonify({'reply': response.text})
    
    except Exception as e:
        # 3. SMART FALLBACK: If 'Gemini 3' is busy, use the universal anchor
        try:
            fallback = genai.GenerativeModel("gemini-flash-latest")
            res = fallback.generate_content(user_message)
            return jsonify({'reply': res.text})
        except Exception as e2:
            return jsonify({'error': f"Neural Link Failure: {str(e2)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
