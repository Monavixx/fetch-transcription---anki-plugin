import requests
from bs4 import BeautifulSoup
from .local_dictionary import cache_transcription
from .utils import make_a_word_without_transcription
from .debug import debug
from urllib.parse import unquote

headers = {
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'http://www.wikipedia.org/',
    'Connection': 'keep-alive',
}

def search_in_cambridge_dictionary(word):    
    html = requests.get('https://dictionary.cambridge.org/dictionary/english/' + word.lower(), headers=headers, timeout=5).text
    soup = BeautifulSoup(html, 'html.parser')

    us_els = soup.find_all(class_='us')
    variantsOfTranscription = []
    trans = ''

    for us in us_els:
        if 'pos-header' in us.parent['class']:
            pron_element = us.find(class_="pron")
            if pron_element:
                ipa_els = pron_element.find_all(class_="ipa")
                for ipa_element in ipa_els:
                    transcriptionText = ipa_element.text.strip().replace('·', '.')
                    if transcriptionText not in variantsOfTranscription:
                        variantsOfTranscription.append(transcriptionText)

    if len(variantsOfTranscription) == 0:
        trans = make_a_word_without_transcription(word)
    elif len(variantsOfTranscription) == 1:
        trans = variantsOfTranscription[0]

        #cache transcription without other variants
        cache_transcription (word, trans)
    else:
        #it will be cached when the user selects some variant
        trans = variantsOfTranscription

    return trans



def select_appropriate_transcriptions(variants: list, tag: str):
    res = []
    return variants




def search_in_oxford_dictionary(word, tag: str):
    debug(tag)
    variantsOfTranscription = [] # [[trans, tag], [trans2, tag2]]
    number = 1
    url_without_number = None

    while True:
        response = requests.get(('https://www.oxfordlearnersdictionaries.com/search/english/?q=' + word.lower()) if url_without_number is None else (url_without_number + "_" + str(number)), headers=headers, timeout=5)
        #debug(('https://www.oxfordlearnersdictionaries.com/search/english/?q=' + word.lower()) if url_without_number is None else (url_without_number + "_" + str(number)))
        if url_without_number is None:
            url_without_number = unquote(response.url)[:-(len(word)+3)].rsplit('_', 1)[0]
        #debug(response.url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        webtop_el = soup.find('div', class_='webtop')
        if webtop_el is None:
            break

        pos_el = webtop_el.find('span', class_='pos')
        if pos_el is None:
            break

        n_am_el = webtop_el.find(class_='phons_n_am')
        if n_am_el is None:
            break
        phon_el = n_am_el.find(class_='phon')
        if phon_el is None:
            break

        

        transcription = phon_el.text.strip()
        transcription = transcription[1:] if transcription[0] == '/' else transcription
        transcription = transcription[:-1] if transcription[-1] == '/' else transcription
        if transcription not in map(lambda x: x[0], variantsOfTranscription):
                variantsOfTranscription.append([transcription, pos_el.text.strip()])
        number += 1

    variantsOfTranscription = select_appropriate_transcriptions(variantsOfTranscription, tag)

    trans = None
    if len(variantsOfTranscription) == 0:
        trans = word
    elif len(variantsOfTranscription) == 1:
        trans = variantsOfTranscription[0][0]

        #cache transcription without other variants
        cache_transcription (word, trans)
    else:
        #it will be cached when the user selects some variant
        trans = list(map(lambda x: x[0], variantsOfTranscription))

    return trans


