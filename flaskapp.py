#flaskapp.py
from flask import Flask, render_template
import csv, re, collections
from collections import Counter

app = Flask(__name__)

@app.route('/')
def main():
    text = ""
    with open('askacademia.csv', 'rt') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for idx, row in enumerate(reader):
            if idx > 0 and idx % 1000 == 0:
                break
            if  'text' in row:
                nolinkstext = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', row['text'], flags=re.MULTILINE)
                text += nolinkstext

            if 'title' in row:
                nolinkstext = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', row['title'], flags=re.MULTILINE)
                text += nolinkstext

    stripped_text = []
    stripped_text = [word for word in text.split() if word.isalpha() and word.lower() not in open("stopwords", "r").read() and len(word) >= 2]

    word_freqs = Counter(stripped_text)
    word_freqs = dict(word_freqs)

    word_freqs_js = []


    for key,value in word_freqs.items():
        temp = {"text": key, "size": value}
        word_freqs_js.append(temp)

    max_freq = max(word_freqs.values())

    return render_template('index.html', word_freqs=word_freqs_js, max_freq=max_freq)

if __name__ == '__main__':
  app.run(debug= True,host="127.0.0.1",port=5000, threaded=True)
