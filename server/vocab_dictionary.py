import nltk
from nltk.corpus import wordnet


class Vocab_Dictionary:

    def __init__(self, all_keywords: list):
        self.all_keywords = all_keywords
        self.keywords_syn_dict = {}
        if len(self.all_keywords) != 0:
            for word in self.all_keywords:
                self.keywords_syn_dict[word] = Vocab_Dictionary.get_synonyms(word)
        # print(f"keywords dictionary: {self.keywords_syn_dict}")

    def get_closest_keywords(self, input_word: str):
        input_syn_list = Vocab_Dictionary.get_synonyms(input_word)
        input_syn_set = set(input_syn_list)
        # print(f"input synonyms list: {input_syn_list}\n\n")
        closest_keywords = []
        for keyword, syn_words in self.keywords_syn_dict.items():
            keyword_syn_set = set(syn_words)
            if len(list(input_syn_set & keyword_syn_set)) != 0:
                closest_keywords.append(keyword)
        return closest_keywords

    @staticmethod
    def get_synonyms(word):
        synonyms = wordnet.synsets(word)
        syn_list = []
        for syns in synonyms:
            syn_list += syns.lemma_names()
        syn_set = set(syn_list)
        return list(syn_set)


if __name__ == "__main__":
    vocab_dict = Vocab_Dictionary(["portraits", "pets", "cars", "interior", "food", "nature", "urban", "sunset", "night"])
    print(vocab_dict.get_closest_keywords("home"))
