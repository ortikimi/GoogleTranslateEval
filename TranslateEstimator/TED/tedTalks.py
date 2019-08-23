from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import csv
import os

TED_FILE = 'ted_talks.csv'

def get_parallel_corpus():
    if os.path.isfile(TED_FILE) == False:
        init_ted_talks()
    with open(TED_FILE, 'rt', encoding='utf-16') as fh:
        text_dict = csv.DictReader(fh, delimiter='\t')
    return text_dict

def init_ted_talks():
    talks_list = []
    enlist_talk_names(talks_list)
    hebrew_sentences = []
    english_sentences = []
    for link in talks_list:
        extract_talk(link,'he', hebrew_sentences)
        extract_talk(link, 'en', english_sentences)
    with open(TED_FILE, encoding='utf-16', mode='w') as ted_talks_file:
        tedtalks_writer = csv.writer(ted_talks_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        tedtalks_writer.writerow(['en', 'he'])
        total_sentences = min(len(hebrew_sentences), len(english_sentences))
        for i in range(total_sentences):
            tedtalks_writer.writerow([english_sentences[i], hebrew_sentences[i]])

def enlist_talk_names(talks_list):
    contents = urllib.request.urlopen("https://www.ted.com/talks?language=he&sort=popular").read()
    soup = BeautifulSoup(contents)
    talks = soup.find_all("a", class_='ga-link')
    for i in talks:
        if i.attrs['href'].find('/talks/') == 0:
            link = i.attrs['href']
            index_q = link.rfind('?')
            transcript_link = 'https://www.ted.com' + link[:index_q] + '/transcript'
            if transcript_link not in talks_list:
                talks_list.append(transcript_link)

def extract_talk(path, lang, lang_sentences):
    lang_path = path + '?language=' + lang
    hdr = {'User-Agent': 'parallel corpus'}
    req = urllib.request.Request(lang_path, headers=hdr)
    contents = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(contents)
    paragraphes = soup.find_all('p')
    page_text = []
    for p in paragraphes:
        text = p.text.replace('\t', '')
        text = text.replace('\n', ' ')
        page_text.append(text)
    lang_sentences.append(page_text)

