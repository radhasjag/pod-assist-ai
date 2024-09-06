import openai
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SuggestionGenerator:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            logger.error("OPENAI_API_KEY is not set in the environment variables")
            raise ValueError("OPENAI_API_KEY is not set")
        openai.api_key = self.api_key

    def generate_suggestions(self, topics, sentiment, conversation_dynamics):
        try:
            topics_str = ", ".join([f"{t['topic']} (Relevance: {t['relevance']})" for t in topics])
            prompt = f"""
            Based on the following information about a podcast conversation:

            Topics: {topics_str}
            Overall Sentiment: {sentiment}
            Conversation Dynamics: {conversation_dynamics}

            Generate 3-5 suggestions for the podcast hosts to improve the conversation, dive deeper into interesting topics, or address any issues in the discussion dynamics. Provide context for each suggestion.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert podcast coach. Provide insightful suggestions to improve the podcast conversation based on the given information."},
                    {"role": "user", "content": prompt}
                ]
            )
            suggestions = response.choices[0].message['content'].strip()
            logger.info("Suggestions generated successfully")
            return self.parse_suggestions(suggestions)
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API error in generating suggestions: {str(e)}")
            return [{"suggestion": "Error: OpenAI API error occurred.", "context": "N/A"}]
        except Exception as e:
            logger.error(f"Unexpected error in generating suggestions: {str(e)}")
            return [{"suggestion": "Error: An unexpected error occurred.", "context": "N/A"}]

    def parse_suggestions(self, suggestions):
        # This is a simple parser and might need to be adjusted based on the actual output format
        parsed_suggestions = []
        current_suggestion = {}
        for line in suggestions.split('\n'):
            if line.startswith("Suggestion:"):
                if current_suggestion:
                    parsed_suggestions.append(current_suggestion)
                current_suggestion = {"suggestion": line[11:].strip()}
            elif line.startswith("Context:"):
                current_suggestion["context"] = line[8:].strip()
        if current_suggestion:
            parsed_suggestions.append(current_suggestion)
        return parsed_suggestions
