import openai
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FactChecker:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            logger.error("OPENAI_API_KEY is not set in the environment variables")
            raise ValueError("OPENAI_API_KEY is not set")
        openai.api_key = self.api_key

    def check_facts(self, text):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert fact-checker. Analyze the given text and provide a detailed fact-check report. For each claim, determine its accuracy, provide evidence or counterevidence, and rate the claim's importance in the context of the conversation."},
                    {"role": "user", "content": f"Fact-check the following text and provide a detailed report:\n\n{text}"}
                ]
            )
            fact_check_report = response.choices[0].message['content'].strip()
            logger.info("Fact-checking completed successfully")
            return self.parse_fact_check_report(fact_check_report)
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API error in fact-checking: {str(e)}")
            return [{"claim": "Error", "accuracy": "N/A", "evidence": "OpenAI API error occurred.", "importance": "N/A"}]
        except Exception as e:
            logger.error(f"Unexpected error in fact-checking: {str(e)}")
            return [{"claim": "Error", "accuracy": "N/A", "evidence": "An unexpected error occurred.", "importance": "N/A"}]

    def parse_fact_check_report(self, report):
        # This is a simple parser and might need to be adjusted based on the actual output format
        facts = []
        for line in report.split('\n'):
            if line.startswith("Claim:"):
                facts.append({"claim": line[6:].strip()})
            elif line.startswith("Accuracy:"):
                facts[-1]["accuracy"] = line[9:].strip()
            elif line.startswith("Evidence:"):
                facts[-1]["evidence"] = line[9:].strip()
            elif line.startswith("Importance:"):
                facts[-1]["importance"] = line[11:].strip()
        return facts
