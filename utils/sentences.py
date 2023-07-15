from nltk.tokenize import word_tokenize
import numpy as np


def get_sentences_similarity(sentence_1, sentence_2):
    tk_list_sent_1 = [*sentence_1.lower()]
    tk_list_sent_2 = [*sentence_2.lower()]

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


if __name__ == '__main__':
    get_sentences_similarity("Tiene experiencia en y Python cuantos años son ", 'Cuántos años de experiencia tienes con Python')


