import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)

# This line is CRITICAL - it allows your GitHub website to talk to this server
CORS(app)

# SECURITY: We tell the code to look for a secret variable called 'GEMINI_API_KEY'
# You will set this in the Render Dashboard under 'Environment Variables'
API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
else:
    print("WARNING: No API Key found. Check your Render Environment Variables.")

@app.route('/')
def home():
    return "Nexus Backend is Online"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"error": "No message received"}), 400

        # Ask Gemini for the response
        response = model.generate_content(user_message)
        
        return jsonify({"reply": response.text})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Nexus Brain is processing... please try again."}), 500

if __name__ == '__main__':
    # Use the port Render provides, or default to 5000 for local testing
    port = int(os.environ.get("PORT", 5000))

    app.run(host='0.0.0.0', port=port)
