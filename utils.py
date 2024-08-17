from aqt.qt import QInputDialog



def prompt_user_to_select_variant(word, variants):
    item, ok = QInputDialog.getItem(None, "Select Transcription", f"Select the transcription for '{word}':", [*variants, 'NONE'], 0, False)
    if ok and item:
        return item
    else:
        return None
    
def make_a_word_without_transcription(word):
    return '<span class=\'error\'>' + word.lower() + '</span>'


def is_first_sound_vowel(transcription):
    vowels = ['a', 'e', 'i', 'o', 'u', 'ɪ', 'ɔ', 'ɑ', 'ʌ', 'æ', 'ə', 'e', 'ɛ', "I", 'ɚ', 'ɜ']
    symbols = ["ˈ", "'", ",", "."]
    
    for i in range(len(transcription)):
        if transcription[i] in symbols:
            continue
        else:
            if transcription[i] in vowels:
                return True
            else:
                return False
    return False
    

def get_transcription_of_the(next_transcription):
    if next_transcription == None or not is_first_sound_vowel(next_transcription) or (isinstance(next_transcription, SpecialWord) and next_transcription.word=='the'):
        return "ðə"
    else:
        return "ðiː"

def get_transcription_of_to(next_transcription):
    if next_transcription == None or not is_first_sound_vowel(next_transcription) or (isinstance(next_transcription, SpecialWord) and next_transcription.word=='to'):
        return "tə"
    else:
        return "tʊ"
    

class SpecialWord:
    def __init__(self, word):
        self.word = word
