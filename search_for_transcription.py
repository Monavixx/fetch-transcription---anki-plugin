from .internet_dictionary import search_in_cambridge_dictionary, search_in_oxford_dictionary
from .local_dictionary import search_in_local_dictionary
from .config import get_config_origin
from .utils import SpecialWord


def search_in_dictionary(word, tag):
    if get_config_origin() == 'oxford':
        return search_in_oxford_dictionary(word, tag)
    else:
        return search_in_cambridge_dictionary(word)



# Returns None if the word is "the"
# Returns array if number of variants is more than 1 else returns string
def search_for_transcription(word, tag, useLocalIfAny=True, manually=False):

    word = word.lower()

    # process some words
    if word in ('the', 'to'):
        return SpecialWord(word)
    
    if not manually:
        if word == 'a':
            return 'ə'
    else:
        if word == 'a':
            return ['ə', 'eɪ']

    if not useLocalIfAny:
        return search_in_dictionary(word, tag)
    else:
        localTrans = search_in_local_dictionary(word)
        if localTrans is None:
            return search_in_dictionary(word, tag)
        return localTrans



