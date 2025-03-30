from flask import Flask, request, jsonify, render_template, send_from_directory, url_for
import os
import uuid 
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, TRANSCRIPT_FOLDER, logger
from src.document_processor import process_input_document  
from src.audio_utils import convert_audio, transcribe_audio_with_whisper
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)

def is_allowed_extension(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_text: str = request.form.get('user_text', '')
    logger.info("Received message: %s", user_text)
    response_message = f"Text received: {user_text}. "

    document_file = request.files.get('document')
    document_filepath = None
    if document_file and document_file.filename:
        try:
            document_filename = f"{uuid.uuid4().hex}_{secure_filename(document_file.filename)}"
            document_filepath = os.path.join(app.config['UPLOAD_FOLDER'], document_filename)
            document_file.save(document_filepath)
            response_message += f"Document {document_filename} uploaded. "
            logger.info("Document saved: %s", document_filepath)
        except Exception as e:
            logger.exception("Error saving document file: %s", e)
            return jsonify({'error': 'Failed to save document file'}), 500
    else:
        response_message += "No document uploaded. "

    signature_file = request.files.get('signature')
    signature_filepath = None
    if signature_file and signature_file.filename:
        try:
            signature_filename = f"{uuid.uuid4().hex}_{secure_filename(signature_file.filename)}"
            signature_filepath = os.path.join(app.config['UPLOAD_FOLDER'], signature_filename)
            signature_file.save(signature_filepath)
            response_message += f"Signature {signature_filename} uploaded. "
            logger.info("Signature saved: %s", signature_filepath)
        except Exception as e:
            logger.exception("Error saving signature file: %s", e)
            return jsonify({'error': 'Failed to save signature file'}), 500
    else:
        response_message += "No signature uploaded. "


    output_pdf_filename = f"report_{uuid.uuid4().hex}.pdf"
    output_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], output_pdf_filename)

    if signature_filepath:
        success = process_input_document(
            text_input=user_text,
            output_pdf_path=output_pdf_path,
            signature_path=signature_filepath
        )
        if not success:
            return jsonify({'error': 'Failed to process input document'}), 500

    download_url = url_for('download_file', filename=output_pdf_filename, _external=True)
    return jsonify({'message': response_message, 'download_url': download_url}), 200

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        logger.error("No audio file part in the request")
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    audio_filename = f"{uuid.uuid4().hex}_{secure_filename(audio_file.filename)}"
    if not audio_filename:
        logger.error("No audio file selected")
        return jsonify({'error': 'No selected file'}), 400

    try:
        model_option = int(request.form.get('option', 1))
    except ValueError:
        logger.error("Invalid model option provided")
        return jsonify({'error': 'Invalid model option'}), 400

    if audio_file and is_allowed_extension(audio_filename):
        audio_filepath = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
        try:
            audio_file.save(audio_filepath)
            logger.info("Audio file saved to %s", audio_filepath)
            converted_audio_filename = f"converted_{uuid.uuid4().hex}.wav"
            converted_audio_filepath = os.path.join(app.config['UPLOAD_FOLDER'], converted_audio_filename)
            convert_audio(audio_filepath=audio_filepath, converted_audio_filepath=converted_audio_filepath)
            logger.info("Audio file converted to 16-bit PCM WAV: %s", converted_audio_filepath) 
            audio_filepath = converted_audio_filepath
        except Exception as e:
            logger.exception("Failed to process audio file: %s", e)
            return jsonify({'error': str(e)}), 500

        transcript = transcribe_audio_with_whisper(
            audio_path=audio_filepath,
            model=model_option
        )
        return jsonify({'transcript': transcript}), 200
    else:
        logger.error("Audio file type not allowed")
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    import webbrowser
    from threading import Timer

    def open_browser():
        webbrowser.open("http://127.0.0.1:5000")

    # Start a timer to open the browser after a short delay
    Timer(1, open_browser).start()
    app.run(debug=False)