from .internet_dictionary import search_in_cambridge_dictionary
from .local_dictionary import search_in_local_dictionary



# Returns None if the word is "the"
# Returns array if number of variants is more than 1 else returns string
def search_for_transcription(word, useLocalIfAny=True, manually=False):
    word = word.lower()

    # process some words
    if word == 'the':
        return None
    
    if not manually:
        if word == 'a':
            return 'ə'
    else:
        if word == 'a':
            return ['ə', 'eɪ']

    if not useLocalIfAny:
        return search_in_cambridge_dictionary(word)
    else:
        localTrans = search_in_local_dictionary(word)
        if localTrans is None:
            return search_in_cambridge_dictionary(word)
        return localTrans

