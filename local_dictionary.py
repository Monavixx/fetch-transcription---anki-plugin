
import os


#C:\Users\Данил\AppData\Local\Programs\Anki\
folder_of_local_dictionary = 'fetchTranscription'
filename_of_local_dictionary = folder_of_local_dictionary + '/localDict.txt'



def cache_transcription(word, transcription):
    found = False
    lines = []

    try:
        with open(filename_of_local_dictionary, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) >= 2:
                    current_word = parts[0]
                    if current_word.lower() == word.lower():
                        lines.append(f"{word.lower()} {transcription}\n")
                        found = True
                    else:
                        lines.append(line)
                else:
                    lines.append(line)
    except FileNotFoundError:
        if not os.path.exists(folder_of_local_dictionary):
            os.makedirs(folder_of_local_dictionary)

    if not found:
        lines.append(f"{word.lower()} {transcription}\n")

    with open(filename_of_local_dictionary, 'w') as file:
        file.writelines(lines)





def search_in_local_dictionary(word):
    try:
        with open(filename_of_local_dictionary, 'r', encoding='utf-8') as dict_file:
            for line in dict_file:
                parts = line.strip().split(maxsplit=1)
                if len(parts) >= 2:
                    dict_word = parts[0]
                    definition = parts[1]
                    if dict_word.lower() == word.lower():
                        return definition
        return None
    except FileNotFoundError:
        return None
    except Exception:
        return None