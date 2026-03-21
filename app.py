from flask import Flask, jsonify, request, send_from_directory
import os
import logging
from dotenv import load_dotenv
from openai import OpenAI
from variance import _find_variance

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    logger.info(f"Received explanation request: {data}")
    
    if data is None:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    if 'variance' not in data or 'scores' not in data:
        return jsonify({'error': 'Missing "variance" or "scores" key'}), 400

    variance = data['variance']
    scores = data['scores']
    
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error('OpenAI API key not configured')
            return jsonify({'error': 'OpenAI API key not configured'}), 500
        
        logger.info(f'Using OpenAI API key (first 10 chars): {api_key[:10]}...')
        client = OpenAI(api_key=api_key)
        
        prompt = f"""Given the variance value {variance:.4f} calculated from the scores {scores}, 
write a brief explanation (2–3 sentences, one paragraph max) of what this variance means in practical terms.

Your response must:
- Explicitly reference and restate the scores ({scores}) in the explanation
- State whether the variance indicates high or low spread
- Briefly explain what that implies about the consistency of the data"""
        
        logger.info(f'Sending prompt to OpenAI: {prompt}')
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
        logger.info(f'Received explanation: {explanation}')
        return jsonify({'explanation': explanation}), 200
        
    except Exception as exc:
        logger.error(f'Failed to generate explanation: {str(exc)}', exc_info=True)
        return jsonify({'error': 'Failed to generate explanation', 'detail': str(exc)}), 500


@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
