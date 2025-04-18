from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allows Flutter frontend to access API

# Secure API Key (Store in environment variables in production)
GEMINI_API_KEY = "AIzaSyCbtnrQQ5xWNSMfMxiY_9iDABEZn-y6HTc"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

@app.route('/get_suggestion', methods=['POST'])
def get_suggestion():
    try:
        data = request.json
        energy_level = data.get("energyLevel")
        preferences = data.get("preferences", [])

        if not energy_level:
            return jsonify({"error": "Energy level is required"}), 400

        prompt = f"""You are a mental wellness assistant. 
        My energy level is {energy_level}. 
        I prefer {', '.join(preferences) if preferences else 'any'} activities. 
        Suggest 3 activities with brief descriptions."""

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        response = requests.post(GEMINI_API_URL, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            suggestion = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
            return jsonify({"suggestion": suggestion})
        else:
            return jsonify({"error": f"API Error: {response.status_code} - {response.text}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
