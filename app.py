from flask import Flask, request, jsonify, send_file, render_template
from TTS.api import TTS
import os
import uuid
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize TTS model
tts_model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DCA", progress_bar=True, gpu=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_tts', methods=['POST'])
def generate_tts():
    data = request.get_json()

    if 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']
    
    # Generate speech
    filename = f"{uuid.uuid4()}.wav"
    try:
        tts_model.tts_to_file(text=text, file_path=filename)
        logging.debug(f"File saved as {filename}")
    except Exception as e:
        logging.error(f"Error saving file: {e}")
        return jsonify({'error': 'Error generating speech file'}), 500
    
    try:
        response = send_file(filename, as_attachment=True, mimetype='audio/wav')
    except Exception as e:
        logging.error(f"Error sending file: {e}")
        return jsonify({'error': 'Error sending file'}), 500

    @response.call_on_close
    def cleanup():
        try:
            os.remove(filename)
            logging.debug(f"File {filename} deleted")
        except Exception as e:
            logging.error(f"Error deleting file: {e}")

    return response

if __name__ == '__main__':
    app.run(debug=False)