from aqt import mw
import re

from .utils import get_transcription_of_the
from .search_for_transcription import search_for_transcription
from .ChooseTranscriptionDialog import ChooseTranscriptionDialog
from aqt.browser import Browser
from .local_dictionary import cache_transcription


# useLocalIfAny means that the local dict will be used
# manually means that dialog will be showed if there are more than one variants of transcription
def automatically_set_transcription(browser: Browser, useLocalIfAny=True, manually=False):
    selected_notes = browser.selectedNotes()
    
    for n_id in selected_notes:
        note = mw.col.getNote(n_id)

        words = list(filter(lambda e: len(e) != 0, re.split(r'\s|,|\.|\?|!|:|;|/|\(|\)', note['English'])))
        transcriptions = []
        isThereSeveralVariants = False

        for word in words:
            transcription = search_for_transcription(word, useLocalIfAny=useLocalIfAny, manually=manually) # None means 'the'
            if isinstance(transcription, list):
                isThereSeveralVariants = True
            transcriptions.append(transcription)

        # We have to replace all None into the correct transcription of 'the'
        if not manually:
            for i in range(len(transcriptions)):
                if transcriptions[i] is None:
                    if i == len(transcriptions) - 1:
                        break
                    if isinstance(transcriptions[i+1], list):
                        # Automatically choose the first one
                        transcriptions[i] = get_transcription_of_the(transcriptions[i+1][0])
                    else:
                        transcriptions[i] = get_transcription_of_the(transcriptions[i+1])

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

