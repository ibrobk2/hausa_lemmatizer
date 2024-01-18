# lemmatizer.py
import nltk
from flask import Flask, render_template, request
from docx import Document

app = Flask(__name__)

nltk.download('punkt')

def custom_tokenize(text):
    # Split words based on spaces
    return text.split()

def apply_stripping_rules(word, stripping_rules):
    for rule in stripping_rules:
        if word.endswith(rule):
            return word[:-len(rule)]
    return word

def lemmatize_text(text, stripping_rules):
    words = custom_tokenize(text)
    lemmatized_words = [apply_stripping_rules(word, stripping_rules) for word in words]
    return lemmatized_words

def read_text_file(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Try with a different encoding if utf-8 fails
        with open(file, 'r', encoding='latin-1') as f:
            return f.read()

def read_docx_file(file):
    doc = Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

def process_file(file, stripping_rules):
    if file.filename.endswith('.docx'):
        return read_docx_file(file)
    elif file.filename.endswith('.txt'):
        return read_text_file(file)
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    stripping_rules = ["aa", "n", "r", ".", ",", ":"]  # Define your stripping rules here

    if request.method == 'POST':
        file = request.files['file']
        if file:
            text = process_file(file, stripping_rules)
            if text:
                lemmatized_words = lemmatize_text(text, stripping_rules)
                result = list(zip(custom_tokenize(text), lemmatized_words))
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
