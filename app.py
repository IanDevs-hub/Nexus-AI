import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure API Key from Render Environment Variables
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def home():
    return "Nexus Core Online"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    # NEW: Listen for the model choice from the UI
    # Options: gemini-3-flash-preview, gemini-3-pro-preview, gemini-2.5-pro
    chosen_model = data.get('model', 'gemini-3-flash-preview')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Initialize the specific model requested
        model = genai.GenerativeModel(chosen_model)
        
        # If it's a thinking model, we use the standard generate_content
        response = model.generate_content(user_message)
        
        return jsonify({'reply': response.text})
    except Exception as e:
        # If there's an error (like model not found), fall back to basic Flash
        try:
            fallback = genai.GenerativeModel('gemini-3-flash-preview')
            response = fallback.generate_content(user_message)
            return jsonify({'reply': response.text})
        except:
            return jsonify({'error': f"Nexus Brain Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
