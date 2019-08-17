import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import codecs
import os, glob

def init_ted_talks():
    all_talk_names = {}
    #for i in range(1, 61):
        #path = "https://www.ted.com/talks/rachel_botsman_the_currency_of_the_new_economy_is_trust/transcript"
        #all_talk_names = enlist_talk_names(path, all_talk_names)
    #all_talk_names =
    #for i in all_talk_names:
    extract_talk('https://www.ted.com/talks/anthony_mccarten_a_not_so_scientific_experiment_on_laughter/transcript', 'anthony_mccarten_a_not_so_scientific_experiment_on_laughter')

    path = 'D:\temp'
    os.chdir(path)
    pieces = []
    for file in glob.glob('*.csv'):
        print(file)
        frame = pd.read_csv(path + file, sep='\t', encoding='utf-8')
        pieces.append(frame)
    df = pd.concat(pieces, ignore_index=True)
    df.to_csv('TED_TALKS', sep='\t', encoding='utf-8')
    df[['he, en']]


def enlist_talk_names(path, dict_):
    with urlopen(path) as conn:
        soup = BeautifulSoup(conn)
        talks = soup.find_all("a", class_='')
        for i in talks:
            if i.attrs['href'].find('/talks/')==0 and dict_.get(i.attrs['href'])!=1:
                dict_[i.attrs]['href'] = 1
        return dict_

def extract_talk(path, talk_name):
    df = pd.DataFrame()
    print(path)
    path_english = path+'?language=en'
    path_hebrew = path +'?language=he'
    contents = urllib.request.urlopen(path_english).read()
    soup1 = BeautifulSoup(contents)
    time_frame = []
    text_talk = []
    paragraph = soup1.find('p')
    text_talk.append(paragraph.text.replace('\t', ''))
    df1 = pd.DataFrame()
    df1['en'] = paragraph
    df = pd.concat([df, df1], axis=1)
    contents = urllib.request.urlopen(path_hebrew).read()
    soup1 = BeautifulSoup(contents)
    text_talk = []
    paragraph = soup1.find('p')
    text_talk.append(paragraph.text.replace('\t', ''))
    df1 = pd.DataFrame()
    df1['he'] = paragraph
    df = pd.concat([df, df1], axis=1)
    df.to_csv(talk_name+'.csv', sep='\t', encoding='utf-8')

