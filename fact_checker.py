import random

class FactChecker:
    def __init__(self):
        self.facts_database = [
            "The Earth is round.",
            "Water boils at 100 degrees Celsius at sea level.",
            "There are 24 hours in a day.",
            "The capital of France is Paris.",
            "The human body has 206 bones."
        ]

    def check_facts(self, text):
        # In a real implementation, we would use an actual fact-checking API or database
        # For this example, we'll return random facts from our mock database
        return random.sample(self.facts_database, 2)
