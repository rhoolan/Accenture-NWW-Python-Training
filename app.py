from flask import Flask, jsonify, request, send_from_directory
import os
from dotenv import load_dotenv
from openai import OpenAI
from variance import _find_variance

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='')


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/variance', methods=['POST'])
def compute_variance():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    if 'scores' not in data:
        return jsonify({'error': 'Missing "scores" key'}), 400

    scores = data['scores']
    if not isinstance(scores, list):
        return jsonify({'error': 'scores must be a list of integers'}), 400

    try:
        variance = _find_variance(scores)
    except (TypeError, ValueError) as exc:
        return jsonify({'error': str(exc)}), 400
    except Exception as exc:
        return jsonify({'error': 'Internal server error', 'detail': str(exc)}), 500

    return jsonify({'variance': variance, 'input': scores}), 200


@app.route('/api/variance-explanation', methods=['POST'])
def get_variance_explanation():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    if 'variance' not in data or 'scores' not in data:
        return jsonify({'error': 'Missing "variance" or "scores" key'}), 400

    variance = data['variance']
    scores = data['scores']
    
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return jsonify({'error': 'OpenAI API key not configured'}), 500
        
        client = OpenAI(api_key=api_key)
        
        prompt = f"""Given the variance value of {variance:.4f} calculated from scores {scores}, 
provide a brief, one-paragraph explanation (2-3 sentences max) of what this variance means in 
practical terms. Explain whether this indicates high or low spread in the data and what that suggests."""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful statistics expert. Provide clear, concise explanations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        explanation = response.choices[0].message.content.strip()
        return jsonify({'explanation': explanation}), 200
        
    except Exception as exc:
        return jsonify({'error': 'Failed to generate explanation', 'detail': str(exc)}), 500


@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
