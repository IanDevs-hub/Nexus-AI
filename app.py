from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)  # This allows your website to talk to your server

# SETUP: Using your API Key
# For now, we put it here. On Render, we will hide it.
API_KEY = "AIzaSyBDEsJJBlTLyz5dVlrqPNvaJVOJueLfE_g"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message")
        
        # Talk to Gemini
        response = model.generate_content(user_message)
        
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # We run on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)