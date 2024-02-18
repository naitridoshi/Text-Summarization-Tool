from django.shortcuts import render, HttpResponse
import pandas as pd
import numpy as np
import fitz
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from nltk import word_tokenize
from heapq import nlargest
from django.core.files.storage import FileSystemStorage
import io

# Create your views here.


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def summarize(request):
    if request.method == "POST":
        # f = request.FILES['file']
        f = request.FILES['file']
        fs = FileSystemStorage()
        filename, ext = str(f).split('.')
        file = fs.save(content=f, name=f.name)
        fileurl = fs.url(file)
        size = fs.size(file)
        path = f"media\\{f.name}"
        stopwords = list(STOP_WORDS)
        nlp = spacy.load('en_core_web_sm')
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc = nlp(text)
        from string import punctuation
        punctuation = punctuation + '’\n“”'
        updated_list = []
        for word in doc:
            if word.text.lower() not in stopwords:
                if word.text.lower() not in punctuation:
                    updated_list.append(word)

        updated_text = ' '.join(str(l) for l in updated_list)
        tokens = word_tokenize(updated_text)
        word_frequency = {}
        for word in tokens:
            if word.lower() not in word_frequency.keys():
                word_frequency[word.lower()] = 1
            else:
                word_frequency[word.lower()] += 1
        max_frequency = max(word_frequency.values())
        for word in word_frequency.keys():
            word_frequency[word] = word_frequency[word]/max_frequency
        sents = []
        for sent in doc.sents:
            #     sent=remove_newline(sent.text)
            sents.append(sent)
        sent_frequency = {}
        for sent in sents:
            #     word=word_tokenize(sent)
            for w in sent:
                if w.text.lower() in word_frequency.keys():
                    if sent not in sent_frequency.keys():
                        sent_frequency[sent] = word_frequency[w.text.lower()]
                    else:
                        sent_frequency[sent] += word_frequency[w.text.lower()]
        # sum = 0
        # maxi = 0
        # mini = 0
        # i = 0
        # j = 0
        # for sent in sents:
        #     #     word= word_tokenize(sent)
        #     #     i=len(word)
        #     i = len(sent)
        #     sum += len(sent)
        #     maxi = max(i, j)
        #     mini = min(i, j)
        #     j = i
        # mean = sum//len(sents)
        # summary_length = (500//((maxi+mini)//2))
        # summary_length = int(summary_length)
        summary_length = int(len(sents)*0.4)
        summary = nlargest(summary_length, sent_frequency,
                           key=sent_frequency.get)
        final_summary = []
        for word in summary:
            final_summary.append(word)
        summary = ' '.join(str(l) for l in final_summary)
        return render(request, 'result.html', {'result': summary})
