import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types

app = Flask(__name__)
CORS(app)

# Initialize Client
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

    # THE FIX: A list of backup brains
    # 1. gemini-1.5-flash-001 (The specific stable version ID)
    # 2. gemini-1.5-flash (The alias)
    # 3. gemini-1.5-pro (The heavy lifter)
    models_to_try = ["gemini-1.5-flash-001", "gemini-1.5-flash", "gemini-1.5-pro"]
    
    last_error = ""

    for model_name in models_to_try:
        try:
            print(f"Attempting connection to: {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=user_message
            )
            # If we get here, it worked! Return the answer.
            return jsonify({'reply': response.text})
            
        except Exception as e:
            print(f"Failed on {model_name}: {str(e)}")
            last_error = str(e)
            # If it fails, the loop continues to the next model automatically
            continue

    # If ALL models fail, show the error
    return jsonify({'error': f"All Neural Links Failed. Last error: {last_error}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
