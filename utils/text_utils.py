
import numpy as np
from langdetect import detect
from nltk import word_tokenize
from translate import Translator


def get_sentences_similarity(sentence_1, sentence_2):
    tk_list_sent_1 = word_tokenize(sentence_1.lower())
    tk_list_sent_2 = word_tokenize(sentence_2.lower())

    print(tk_list_sent_1)

    words_set = set(tk_list_sent_1) | set(tk_list_sent_2)

    sent1_array = []
    sent2_array = []
    for word in words_set:
        sent1_array.append(1 if word in tk_list_sent_1 else 0)
        sent2_array.append(1 if word in tk_list_sent_2 else 0)

    sent1_np_array = np.array(sent1_array)
    sent2_np_array = np.array(sent2_array)

    similarity = (sent1_np_array @ sent2_np_array) / (np.linalg.norm(sent1_np_array) * np.linalg.norm(sent2_np_array))

    print(similarity)


def translate_sentence(sentence, to_lang='en'):
    text_lang = detect(sentence)
    if text_lang == to_lang:  # In case sentence is already in desired lang
        return sentence

    translator = Translator(from_lang=text_lang, to_lang=to_lang)
    translation = translator.translate(sentence)
    return translation


if __name__ == '__main__':
    sent1 = "¿Cuántos años de experiencia laboral tiene con"
    sent2 = 'How many years of hands-on experience do you have with Docker?'

    sent1 = translate_sentence(sent1)
    print(sent1)
    get_sentences_similarity(sent1,
                             sent2)


