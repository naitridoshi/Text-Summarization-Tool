from django.shortcuts import render
import fitz
import spacy
from heapq import nlargest
from django.core.files.storage import FileSystemStorage

# Create your views here.


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def summarize(request):
    if request.method == "POST":
        f = request.FILES['file']
        fs = FileSystemStorage()
        file = fs.save(content=f, name=f.name)
        path = fs.path(file)

        # 1. Text Extraction
        with fitz.open(path) as doc:
            text = "".join(page.get_text() for page in doc)

        # 2. NLP Processing with spaCy
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)

        # 3. Word Frequency Calculation
        word_frequencies = {}
        for word in doc:
            if not word.is_stop and not word.is_punct:
                if word.text.lower() not in word_frequencies:
                    word_frequencies[word.text.lower()] = 1
                else:
                    word_frequencies[word.text.lower()] += 1
        
        if not word_frequencies:
             return render(request, 'result.html', {'result': "Could not generate summary from the document."})

        max_frequency = max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word] = word_frequencies[word] / max_frequency

        # 4. Sentence Scoring
        sentence_scores = {}
        for sent in doc.sents:
            for word in sent:
                if word.text.lower() in word_frequencies:
                    if sent not in sentence_scores:
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

        # 5. Summarization
        summary_length = int(len(list(doc.sents)) * 0.4)
        summary_sentences = nlargest(summary_length, sentence_scores, key=sentence_scores.get)
        
        final_summary = [sent.text for sent in summary_sentences]

        return render(request, 'result.html', {'result_sentences': final_summary})