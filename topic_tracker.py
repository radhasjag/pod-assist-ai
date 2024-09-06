import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')

class TopicTracker:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def track_topics(self, text):
        # Tokenize the text and remove stop words
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalnum() and word not in self.stop_words]

        # Count word frequencies
        word_freq = Counter(words)

        # Return the top 3 most frequent words as topics
        return [word for word, _ in word_freq.most_common(3)]
