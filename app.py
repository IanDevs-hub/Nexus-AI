import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

# Initialize Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# --- DIAGNOSTIC TOOL ---
# This runs once when the server starts to find valid model names
print("--- SYSTEM SCAN: SEARCHING FOR BRAINS ---", file=sys.stdout)
try:
    # We ask Google: "What models can I use?"
    for m in client.models.list():
        # We only care about models that generate content
        if "generateContent" in m.supported_actions:
            print(f"✅ FOUND: {m.name}", file=sys.stdout)
except Exception as e:
    print(f"❌ SCAN ERROR: {str(e)}", file=sys.stdout)
print("-----------------------------------------", file=sys.stdout)
# -----------------------

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

    # STRATEGY: Try the Experimental 2.0 model first (usually open access)
    # If that fails, try the generic 'gemini-2.0-flash' again
    models_to_try = ["gemini-2.0-flash-exp", "gemini-2.0-flash"]
    
    last_error = ""

    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=user_message
            )
            return jsonify({'reply': response.text})
            
        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ Failed on {model_name}: {error_msg}", file=sys.stdout)
            last_error = error_msg
            
            # If it's a Rate Limit (429), tell the user to wait
            if "429" in error_msg:
                return jsonify({'error': "Nexus Overloaded. Please wait 60 seconds."}), 429
            
            continue

    return jsonify({'error': f"All frequencies jammed. Last error: {last_error}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
