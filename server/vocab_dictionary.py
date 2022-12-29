import nltk
from nltk.corpus import wordnet


class Vocab_Dictionary:

    ALBUM_RELATED_WORDS = { "urban": ["city", "town", "downtown", "streets"],
                            "nature": ["wild", "landscape"],
                            "sunset": ["sunrise", "golden hour", "sun"],
                            "day": ["sky"],
                            "night": ["dark", "evening", "nighttime"],
                            "portraits": ["portrait"],
                            "pets": ["pet"],
                            "cars": ["car", "vehicle", "vehicles", "auto"]}

    KEYWORD_RELATED_WORDS = { "forest": ["tree", "trees", "wood", "woods"] }

    def get_synonyms(self, word):
        synonyms = wordnet.synsets(word)
        syn_list = []
        for syns in synonyms:
            syn_list += syns.lemma_names()
        syn_set = set(syn_list)
        return list(syn_set)

    def is_related(self, word1: str, word2: str):
        """
        true if word1 and word2 are similar / is synonyms
        """
        word1_syn = set(self.get_synonyms(word1))
        word2_syn = set(self.get_synonyms(word2))
        if len(list(word1_syn & word2_syn)) > 0:
            return True
        return False

    def word_in_album_related_words(self, word):
        for album, syn_list in self.ALBUM_RELATED_WORDS.items():
            if word in syn_list:
                return album
        return None

    def word_in_keywords_related_words(self, word):
        for keyword, syn_keywords in self.KEYWORD_RELATED_WORDS.items():
            if word in syn_keywords:
                return keyword
        return None



if __name__ == "__main__":
    vocab_dict = Vocab_Dictionary(["portraits", "pets", "cars", "interior", "food", "nature", "urban", "sunset", "night"])
    print(vocab_dict.get_closest_keywords("home"))
