import os
import logging
from flask import Flask, render_template, request, jsonify
from audio_processor import AudioProcessor
from fact_checker import FactChecker
from topic_tracker import TopicTracker
from suggestion_generator import SuggestionGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Check if the OpenAI API key is set
if not os.environ.get("OPENAI_API_KEY"):
    logger.error("OPENAI_API_KEY environment variable is not set")
    raise ValueError("OPENAI_API_KEY environment variable is not set")

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
    try:
        text = audio_processor.transcribe(audio_data)
        conversation_analysis = audio_processor.analyze_conversation(text)
        facts = fact_checker.check_facts(text)
        topics = topic_tracker.track_topics(text)
        suggestions = suggestion_generator.generate_suggestions(topics, conversation_analysis['sentiment_analysis'], conversation_analysis['dynamics_analysis'])
        
        return jsonify({
            'transcription': text,
            'conversation_analysis': conversation_analysis,
            'facts': facts,
            'topics': topics,
            'suggestions': suggestions
        })
    except Exception as e:
        logger.error(f"Error in process_audio: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
