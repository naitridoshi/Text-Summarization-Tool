from django.contrib import messages
from django.shortcuts import render, redirect
import fitz
import spacy
from heapq import nlargest
from django.core.files.storage import FileSystemStorage
from PIL import Image
import pytesseract

# Create your views here.


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def summarize(request):
    if request.method != "POST":
        return redirect("home")

    # Debug logs — remove later
    print("content-type:", request.META.get("CONTENT_TYPE"))
    print("files keys:", list(request.FILES.keys()))

    f = request.FILES.get("file")
    if not f:
        messages.error(request, "No file uploaded. Please choose a PDF.")
        return redirect("home")

    fs = FileSystemStorage()
    try:
        file = fs.save(content=f, name=f.name)
        path = fs.path(file)
    except Exception as e:
        return render(request, "result.html", {"result_sentences": [f"Upload error: {e}"]})

    text = ""
    try:
        with fitz.open(path) as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                page_text = page.get_text("text")
                if len(page_text) > 30:
                    text += page_text
                else:
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text += pytesseract.image_to_string(img)
    except Exception as e:
        return render(request, "result.html", {"result_sentences": [f"Error processing file: {e}"]})

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    word_frequencies = {}
    for word in doc:
        if not word.is_stop and not word.is_punct:
            word_frequencies[word.text.lower()] = word_frequencies.get(word.text.lower(), 0) + 1

    if not word_frequencies:
        return render(request, "result.html", {"result_sentences": [
            "Could not generate summary. The document might be empty or image-only without OCRable text."
        ]})

    max_frequency = max(word_frequencies.values())
    for w in word_frequencies:
        word_frequencies[w] /= max_frequency

    sentence_scores = {}
    for sent in doc.sents:
        for word in sent:
            score = word_frequencies.get(word.text.lower())
            if score:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + score

    summary_length = max(1, int(len(list(doc.sents)) * 0.4))
    summary_sentences = nlargest(summary_length, sentence_scores, key=sentence_scores.get)
    final_summary = [sent.text for sent in summary_sentences]

    return render(request, "result.html", {"result_sentences": final_summary})