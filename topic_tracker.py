import openai
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TopicTracker:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            logger.error("OPENAI_API_KEY is not set in the environment variables")
            raise ValueError("OPENAI_API_KEY is not set")
        openai.api_key = self.api_key

    def track_topics(self, text):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert topic analyzer. Identify the main topics discussed in the given text, provide a brief summary of each topic, and rate their relevance to the overall conversation."},
                    {"role": "user", "content": f"Analyze the main topics in the following text:\n\n{text}"}
                ]
            )
            topic_analysis = response.choices[0].message['content'].strip()
            logger.info("Topic analysis completed successfully")
            return self.parse_topic_analysis(topic_analysis)
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API error in topic analysis: {str(e)}")
            return [{"topic": "Error", "summary": "OpenAI API error occurred.", "relevance": "N/A"}]
        except Exception as e:
            logger.error(f"Unexpected error in topic analysis: {str(e)}")
            return [{"topic": "Error", "summary": "An unexpected error occurred.", "relevance": "N/A"}]

    def parse_topic_analysis(self, analysis):
        # This is a simple parser and might need to be adjusted based on the actual output format
        topics = []
        current_topic = {}
        for line in analysis.split('\n'):
            if line.startswith("Topic:"):
                if current_topic:
                    topics.append(current_topic)
                current_topic = {"topic": line[6:].strip()}
            elif line.startswith("Summary:"):
                current_topic["summary"] = line[8:].strip()
            elif line.startswith("Relevance:"):
                current_topic["relevance"] = line[10:].strip()
        if current_topic:
            topics.append(current_topic)
        return topics
