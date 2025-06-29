import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import string

# Optional: Uncomment if you want Hugging Face models later
# from transformers import pipeline

nltk.download('punkt')
nltk.download('stopwords')

def clean_text(text):
    # Remove punctuation and lowercase
    return text.translate(str.maketrans('', '', string.punctuation)).lower()

def extractive_summary(text, num_sentences=5):
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return sentences  # Just return all

    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(clean_text(text))
    word_freq = Counter([word for word in word_tokens if word not in stop_words])

    sentence_scores = []
    for sent in sentences:
        words = word_tokenize(clean_text(sent))
        score = sum(word_freq.get(word, 0) for word in words)
        sentence_scores.append((score, sent))

    top_sentences = sorted(sentence_scores, reverse=True)[:num_sentences]
    return [s for _, s in top_sentences]


# Placeholder for future abstractive summarization (HuggingFace)
def abstractive_summary(text):
    # summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    # summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    # return [summary[0]['summary_text']]
    return ["(Abstractive mode is under construction. Defaulting to extractive.)"]

def summarize_text(text, method='extractive', num_sentences=5):
    if method == 'extractive':
        return extractive_summary(text, num_sentences)
    elif method == 'abstractive':
        return abstractive_summary(text)
    else:
        raise ValueError("Unknown summarization method. Choose 'extractive' or 'abstractive'.")
