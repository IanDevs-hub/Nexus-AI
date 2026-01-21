import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configuration for 2026 Stable Models
# Make sure GEMINI_API_KEY is in your Render Environment Variables!
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def home():
    return "Nexus Core Online"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    # 2026 Stable Model Names
    # Fast: gemini-3-flash-preview | Pro: gemini-3-pro-preview | Logic: gemini-2.5-pro
    chosen_model = data.get('model', 'gemini-3-flash-preview')

    try:
        model = genai.GenerativeModel(chosen_model)
        response = model.generate_content(user_message)
        return jsonify({'reply': response.text})
    except Exception as e:
        # EMERGENCY FALLBACK: If the chosen model is busy or name is wrong
        try:
            fallback = genai.GenerativeModel('gemini-3-flash-preview')
            res = fallback.generate_content(user_message)
            return jsonify({'reply': res.text})
        except:
            return jsonify({'error': "Neural Link Failure. Please check Render Logs."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
