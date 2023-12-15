from flask import Flask, render_template, request,Blueprint
import pdfplumber
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
import nltk

nltk.download('punkt')
nltk.download('stopwords')

pdfsummarizer_app = Blueprint('pdfsummarizer',__name__)

@pdfsummarizer_app.route('/', methods=['GET', 'POST'])
def index():
    summary = ""

    if request.method == 'POST':
        uploaded_file = request.files['file']

        if uploaded_file:
            with pdfplumber.open(uploaded_file) as pdf:
                first_page = pdf.pages[0]
                text = first_page.extract_text()

            # Tokenize sentences
            sentences = sent_tokenize(text)
            # Count word frequencies
            word_freq = Counter(word.lower() for sentence in sentences for word in sentence.split() if word.lower() not in stopwords.words('english'))
            # Sort and get top sentences for summary
            summary_sentences = sorted(sentences, key=lambda sentence: sum(word_freq[word.lower()] for word in sentence.split()), reverse=True)
            summary = ' '.join(summary_sentences[:3])  # Top 3 sentences as summary

    return render_template('pdfsummarizer.html', summary=summary)


