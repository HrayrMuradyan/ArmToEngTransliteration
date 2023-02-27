import numpy as np
import re
import io


def generate_mappings(arm_characters_path = 'hy_characters.npy', eng_characters_path = 'en_characters.npy', mapping_characters_path = 'mapping_characters.npy'):
	characters = list(np.load(arm_characters_path))
	english_characters = list(np.load(eng_characters_path))
	mapping_characters = list(np.load(mapping_characters_path, allow_pickle=True))
	mapping = dict(zip(characters[:len(mapping_characters)], mapping_characters))
	return characters, english_characters, mapping

def valid_word(word):
    response = True
    if ' ' in word:
        if not word.isspace():
            response=False
    return response

def transliteration(word):
    if not valid_word(word):
        return 'Invalid'
    initial_replace = {'ու':'u', 'Ու':'U', 'ՈՒ':'U', 'եւ':'ev', 'Եւ':'Ev'}
    for i, j in initial_replace.items():
        word = word.replace(i, j)
    old_word = word
    splitted = [*word] 
    if not any(letter in characters for letter in splitted):
        return old_word
    new_word = []
    first_char = True
    for char in splitted:
        if char in characters:
            if char == 'ո' and (first_char):
                new_word.append('vo')
            elif char == 'Ո' and (first_char):
                new_word.append('Vo')
            elif char == 'ե' and (first_char):
                new_word.append(np.random.choice(['e', 'ye'], p = [0.9, 0.1]))
            elif char == 'Ե' and (first_char):
                new_word.append(np.random.choice(['E', 'Ye'], p = [0.9, 0.1]))
            else:
                new_char = mapping[char]
                if isinstance(new_char, str):
                    new_word.append(new_char)               
                elif isinstance(new_char, dict):
                    new_word.append(np.random.choice(list(new_char.keys()), p = list(new_char.values())))
            first_char = False
        elif char in english_characters:
            new_word.append(char)
    new_word = ''.join(new_word)
    return new_word


def transliterate_text(text):
    text = re.findall('[' + ''.join(characters)+']+'+'|[\w.,՝։:;%?*+]|[" "]+', text)
    translited_words = list(map(transliteration, text))
    return ''.join(translited_words)

characters, english_characters, mapping = generate_mappings()


if __name__ == "__main__":

	transliterate_text('Բարև, ոնց ես?')