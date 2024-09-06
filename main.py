from flask import Flask, render_template, request, jsonify
from audio_processor import AudioProcessor
from fact_checker import FactChecker
from topic_tracker import TopicTracker
from suggestion_generator import SuggestionGenerator

app = Flask(__name__)

audio_processor = AudioProcessor()
fact_checker = FactChecker()
topic_tracker = TopicTracker()
suggestion_generator = SuggestionGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    audio_data = request.json['audio']
    text = audio_processor.transcribe(audio_data)
    facts = fact_checker.check_facts(text)
    topics = topic_tracker.track_topics(text)
    suggestions = suggestion_generator.generate_suggestions(topics)
    
    return jsonify({
        'transcription': text,
        'facts': facts,
        'topics': topics,
        'suggestions': suggestions
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
