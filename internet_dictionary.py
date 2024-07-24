import requests
from bs4 import BeautifulSoup
from .local_dictionary import cache_transcription
from .utils import make_a_word_without_transcription

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
