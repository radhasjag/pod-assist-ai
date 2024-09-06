import openai
import os
import logging
from textblob import TextBlob
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
import json
from transformers import pipeline
from gensim import corpora
from gensim.models import LdaMulticore
from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import simple_preprocess

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            logger.error("OPENAI_API_KEY is not set in the environment variables")
            raise ValueError("OPENAI_API_KEY is not set")
        openai.api_key = self.api_key
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.zero_shot_classifier = pipeline("zero-shot-classification")

    def transcribe(self, audio_data):
        try:
            # In a real implementation, we would send the actual audio data
            # For this example, we'll use a mock audio file
            with open("mock_audio.mp3", "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)
            logger.info("Transcription completed successfully")
            return transcript["text"]
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return "Error in transcription. OpenAI API error occurred."
        except Exception as e:
            logger.error(f"Unexpected error in transcription: {str(e)}")
            return "Error in transcription. Please try again."

    def analyze_sentiment(self, text):
        try:
            # Use TextBlob for initial sentiment analysis
            blob = TextBlob(text)
            textblob_sentiment = blob.sentiment.polarity

            # Use Hugging Face Transformers for more advanced sentiment analysis
            hf_sentiment = self.sentiment_analyzer(text[:512])[0]  # Limit to 512 tokens

            # Use GPT-3.5 for more nuanced analysis
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a sentiment and emotion analyzer. Provide a detailed analysis of the given text, including the overall sentiment, specific emotions detected, and their intensities. Return the analysis as a JSON object with keys: overall_sentiment, emotions, and explanation."},
                    {"role": "user", "content": f"Analyze the sentiment and emotions in this text: {text}"}
                ]
            )
            gpt_analysis = json.loads(response.choices[0].message['content'].strip())

            # Combine all analyses
            combined_analysis = {
                "textblob_sentiment": textblob_sentiment,
                "huggingface_sentiment": {
                    "label": hf_sentiment["label"],
                    "score": hf_sentiment["score"]
                },
                "gpt_analysis": gpt_analysis
            }

            logger.info("Sentiment and emotion analysis completed successfully")
            return combined_analysis
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API error in sentiment analysis: {str(e)}")
            return {"error": "Error in sentiment analysis. OpenAI API error occurred."}
        except Exception as e:
            logger.error(f"Unexpected error in sentiment analysis: {str(e)}")
            return {"error": "Error in sentiment analysis. Please try again."}

    def detect_conversation_dynamics(self, text):
        try:
            # Tokenize the text into sentences and words
            sentences = sent_tokenize(text)
            words = word_tokenize(text)
            
            # Remove stopwords
            stop_words = set(stopwords.words('english'))
            filtered_words = [word for word in words if word.lower() not in stop_words]
            
            # Analyze turn-taking and sentence complexity
            turn_taking = len(sentences)
            avg_sentence_length = sum(len(s.split()) for s in sentences) / turn_taking
            avg_word_length = sum(len(word) for word in filtered_words) / len(filtered_words)
            
            # Use GPT-3.5 for more advanced dynamics analysis
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in conversation analysis. Analyze the given text for conversation dynamics, including turn-taking patterns, interruptions, topic coherence, overall flow, and speaker engagement. Return the analysis as a JSON object with keys: turn_taking, interruptions, topic_coherence, flow, speaker_engagement, and explanation."},
                    {"role": "user", "content": f"Analyze the conversation dynamics in this text: {text}"}
                ]
            )
            gpt_analysis = json.loads(response.choices[0].message['content'].strip())
            
            # Combine basic metrics with GPT-3.5 analysis
            combined_analysis = {
                "basic_metrics": {
                    "turn_taking": turn_taking,
                    "avg_sentence_length": avg_sentence_length,
                    "avg_word_length": avg_word_length
                },
                "gpt_analysis": gpt_analysis
            }
            
            logger.info("Conversation dynamics analysis completed successfully")
            return combined_analysis
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API error in conversation dynamics analysis: {str(e)}")
            return {"error": "Error in conversation dynamics analysis. OpenAI API error occurred."}
        except Exception as e:
            logger.error(f"Unexpected error in conversation dynamics analysis: {str(e)}")
            return {"error": "Error in conversation dynamics analysis. Please try again."}

    def analyze_topics(self, text):
        try:
            # Preprocess the text
            def preprocess(text):
                result = []
                for token in simple_preprocess(text):
                    if token not in STOPWORDS and len(token) > 3:
                        result.append(token)
                return result

            processed_text = preprocess(text)

            # Create a dictionary representation of the documents
            dictionary = corpora.Dictionary([processed_text])

            # Create a corpus
            corpus = [dictionary.doc2bow(text) for text in [processed_text]]

            # Train the LDA model
            lda_model = LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=5)

            # Get the topics
            topics = lda_model.print_topics()

            # Use zero-shot classification for topic labeling
            topic_labels = ["politics", "technology", "sports", "entertainment", "science"]
            zero_shot_result = self.zero_shot_classifier(text, topic_labels)

            topic_analysis = {
                "lda_topics": [{"topic_id": topic_id, "keywords": keywords} for topic_id, keywords in topics],
                "zero_shot_classification": {
                    "labels": zero_shot_result["labels"],
                    "scores": zero_shot_result["scores"]
                }
            }

            logger.info("Topic analysis completed successfully")
            return topic_analysis
        except Exception as e:
            logger.error(f"Unexpected error in topic analysis: {str(e)}")
            return {"error": "Error in topic analysis. Please try again."}

    def analyze_conversation(self, text):
        sentiment_analysis = self.analyze_sentiment(text)
        dynamics_analysis = self.detect_conversation_dynamics(text)
        topic_analysis = self.analyze_topics(text)
        
        return {
            "sentiment_analysis": sentiment_analysis,
            "dynamics_analysis": dynamics_analysis,
            "topic_analysis": topic_analysis
        }
