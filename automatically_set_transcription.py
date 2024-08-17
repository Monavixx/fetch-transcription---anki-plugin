from aqt import mw
import re

from bs4 import BeautifulSoup
import requests

from .utils import get_transcription_of_the, get_transcription_of_to
from .search_for_transcription import SpecialWord, search_for_transcription
from .ChooseTranscriptionDialog import ChooseTranscriptionDialog
from aqt.browser import Browser
from .local_dictionary import cache_transcription
from .internet_dictionary import headers
from .debug import debug
import nltk


def preprocess_english(note: str):
    res = note.strip()
    while True:
        res = res.strip()
        strt = False
        if res[0] == '-':
            res = res[1:]
        else:
            strt = True
        if res[-1] == '-':
            res = res[:-1]
        elif not strt:
            break



# useLocalIfAny means that the local dict will be used
# manually means that dialog will be showed if there are more than one variants of transcription
def automatically_set_transcription(browser: Browser, useLocalIfAny=True, manually=False):
    selected_notes = browser.selectedNotes()
    
    for n_id in selected_notes:
        note = mw.col.getNote(n_id)

        words = list(filter(lambda e: len(e) != 0, re.split(r'\s|,|\.|\?|!|:|;|/|\(|\)|\s\-\s', note['English'].strip())))
        #words = nltk.word_tokenize(note['English'])
        tokens = nltk.pos_tag(words, tagset='universal')
        #debug(str(words))

        transcriptions = []
        isThereSeveralVariants = False

        for token in tokens:
            transcription = search_for_transcription(token[0], token[1], useLocalIfAny=useLocalIfAny, manually=manually) # None means 'the'
            if isinstance(transcription, list):
                isThereSeveralVariants = True
            transcriptions.append(transcription)

        # We have to replace all None into the correct transcription of 'the'
        if not manually or not isThereSeveralVariants:
            for i in range(len(transcriptions)):
                if isinstance(transcriptions[i], SpecialWord):
                    if transcriptions[i].word == 'the':
                        if i == len(transcriptions) - 1:
                            transcriptions[i] = get_transcription_of_the(None)
                        if isinstance(transcriptions[i+1], list):
                            # Automatically choose the first one
                            transcriptions[i] = get_transcription_of_the(transcriptions[i+1][0])
                        else:
                            transcriptions[i] = get_transcription_of_the(transcriptions[i+1])
                    elif transcriptions[i].word == 'to':
                        if i == len(transcriptions) - 1:
                            transcriptions[i] = get_transcription_of_to(None)
                        if isinstance(transcriptions[i+1], list):
                            # Automatically choose the first one
                            transcriptions[i] = get_transcription_of_to(transcriptions[i+1][0])
                        else:
                            transcriptions[i] = get_transcription_of_to(transcriptions[i+1])


        if isThereSeveralVariants:
            if manually:
                ctd = ChooseTranscriptionDialog(words, transcriptions, max_width=browser.width())
                ctd.exec()
                transcriptions = ctd.getDoneTranscriptions()
            else:
                #cache the first variant
                for i in range(len(transcriptions)):
                    if isinstance(transcriptions[i], list):
                        cache_transcription(words[i], transcriptions[i][0])

                # Automatically choose the first variant
                transcriptions = list(map(lambda t: t[0] if isinstance(t, list) else t, transcriptions))

        note['Transcription'] = ' '.join(transcriptions)
        note.flush()
        mw.reset()



headers = {
    'Origin': 'https://tophonetics.com',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*',
    'Referer': 'https://tophonetics.com/',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

def fetch_from_tophonetics(browser: Browser):
    selected_notes = browser.selectedNotes()
    
    for n_id in selected_notes:
        note = mw.col.getNote(n_id)

        query = note['English']
        data = {
            "text_to_transcribe": query,
            "output_dialect": "am",
            "output_style": "only_tr",
            "submit": "Show transcription",
            "weak_forms": "on",
            "speech_support": '0',
            "preBracket": '',
            "postBracket": ''
        }
        html = requests.post('https://tophonetics.com/', data=data, headers=headers, timeout=5).text
        debug(html)
        soup = BeautifulSoup(html, 'html.parser')

        transcr_output = soup.find(id='transcr_output')
        trans = transcr_output.text.replace('ɛ', 'e')


        note['Transcription'] = trans
        note.flush()
        mw.reset()

        