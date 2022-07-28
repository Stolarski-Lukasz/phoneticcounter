from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import os
import re
import string
import csv
import os.path
from django.views.decorators.csrf import csrf_exempt


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# diplaying interface
def home(request):
    return render(request, 'index.html')


# calculation functions
consonant_count_a = 0
consonant_count_b = 0
vowel_count_a = 0
vowel_count_b = 0
syllable_count = 0

consonants = ["b", "c", "d", "f", "g", "h", "g", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "z"]
vowels = ["a", "o", "e", "i", "u", "y"]

# data sets dealing with noun inflexion - plural
final_o_no_es = ["dynamo", "kimono", "piano", "kilo", "photo", "soprano"] # these end in "o" and stil take regulral "s" in plural
f_exceptions = ["calf", "half", "knife", "leaf", "life", "loaf", "self", "sheaf", "shelf", "thief", "wife", "wolf"] # these words take "ves" in plural
f_double_exceptions = ["hoof", "scarf", "wharf"] # these forms take in plural either "s" of "ves"
vowel_change_plural_dict = {"foot": "feet", "goose": "geese", "louse": "lice", "man": "men", "mouse": "mice",
                            "tooth": "teeth", "woman": "women", "child": "children", "ox": "oxen", "crisis": "crises",
                            "erratum": "errata", "memorandum": "memoranda", "oasis": "oases", "phenomenon": "phenomena",
                            "radius": "radii", "terminus": "termini"
                            }
two_plurals_dict = {"formula": ["formulas", "formulae"], "appendix": ["appendixes", "appendices"],
                    "index": ["indexes", "indices"], "libretto": ["libretti", "librettos"], "tempo": ["tempi", "tempos"]
                    }
no_plural_dict = ["sheep", "deer", "aircraft", "counsel"]

# irregular verbs

irregular_verbs_dict2 = {'flee': ['fled', 'fled'], 'stink': ['stank', 'stunk'], 'fall': ['fell', 'fallen'], 'bleed': ['bled', 'bled'], 'fight': ['fought', 'fought'], 'lend': ['lent', 'lent'], 'slit': ['slit', 'slit'], 'bid': ['bid', 'bid'], 'hear': ['heard', 'heard'], 'bind': ['bound', 'bound'], 'sweep': ['swept', 'swept'], 'choose': ['chose', 'chosen'], 'beat': ['beat', 'beaten'], 'hold': ['held', 'held'], 'sink': ['sank', 'sunk'], 'feed': ['fed', 'fed'], 'teach': ['taught', 'taught'], 'cast': ['cast', 'cast'], 'forgive': ['forgave', 'forgiven'], 'sling': ['slung', 'slung'], 'read': ['read', 'read'], 'grind': ['ground', 'ground'], 'spin': ['spun', 'spun'], 'eat': ['ate', 'eaten'], 'wring': ['wrung', 'wrung'], 'let': ['let', 'let'], 'sing': ['sang', 'sung'], 'cling': ['clung', 'clung'], 'shed': ['shed', 'shed'], 'show': ['showed', 'shown'], 'get': ['got', 'gotten'], 'make': ['made', 'made'], 'spread': ['spread', 'spread'], 'catch': ['caught', 'caught'], 'send': ['sent', 'sent'], 'set': ['set', 'set'], 'weave': ['wove', 'woven'], 'ring': ['rang', 'rung'], 'mean': ['meant', 'meant'], 'sew': ['sewed', 'sewn'], 'tread': ['trod', 'trodden'], 'burst': ['burst', 'burst'], 'meet': ['met', 'met'], 'shake': ['shook', 'shaken'], 'steal': ['stole', 'stolen'], 'wear': ['wore', 'worn'], 'tell': ['told', 'told'], 'thrust': ['thrust', 'thrust'], 'drive': ['drove', 'driven'], 'see': ['saw', 'seen'], 'stand': ['stood', 'stood'], 'lead': ['led', 'led'], 'come': ['came', 'come'], 'fling': ['flung', 'flung'], 'feel': ['felt', 'felt'], 'find': ['found', 'found'], 'run': ['ran', 'run'], 'give': ['gave', 'given'], 'stick': ['stuck', 'stuck'], 'keep': ['kept', 'kept'], 'tear': ['tore', 'torn'], 'hit': ['hit', 'hit'], 'go': ['went', 'gone'], 'drink': ['drank', 'drunk'], 'sleep': ['slept', 'slept'], 'hide': ['hid', 'hidden'], 'write': ['wrote', 'written'], 'say': ['said', 'said'], 'rid': ['rid', 'rid'], 'sow': ['sowed', 'sown'], 'creep': ['crept', 'crept'], 'fly': ['flew', 'flown'], 'bite': ['bit', 'bitten'], 'swim': ['swam', 'swum'], 'lay': ['laid', 'laid'], 'breed': ['bred', 'bred'], 'shoot': ['shot', 'shot'], 'slink': ['slunk', 'slunk'], 'leave': ['left', 'left'], 'quit': ['quit', 'quit'], 'strive': ['strove', 'striven'], 'think': ['thought', 'thought'], 'ride': ['rode', 'ridden'], 'string': ['strung', 'strung'], 'seek': ['sought', 'sought'], 'dwell': ['dwelt', 'dwelt'], 'build': ['built', 'built'], 'rend': ['rent', 'rent'], 'slide': ['slid', 'slid'], 'shrink': ['shrank', 'shrunk'], 'wed': ['wed', 'wed'], 'deal': ['dealt', 'dealt'], 'draw': ['drew', 'drawn'], 'weep': ['wept', 'wept'], 'know': ['knew', 'known'], 'awake': ['awoke', 'awaken'], 'sting': ['stung', 'stung'], 'blow': ['blew', 'blown'], 'put': ['put', 'put'], 'wind': ['wound', 'wound'], 'forget': ['forgot', 'forgotten'], 'freeze': ['froze', 'frozen'], 'sell': ['sold', 'sold'], 'split': ['split', 'split'], 'buy': ['bought', 'bought'], 'begin': ['began', 'begun'], 'lose': ['lost', 'lost'], 'bet': ['bet', 'bet'], 'swing': ['swung', 'swung'], 'have': ['had', 'had'], 'swell': ['swelled', 'swollen'], 'cost': ['cost', 'cost'], 'take': ['took', 'taken'], 'swear': ['swore', 'sworn'], 'bring': ['brought', 'brought'], 'sit': ['sat', 'sat'], 'win': ['won', 'won'], 'lie': ['lay', 'lain'], 'hurt': ['hurt', 'hurt'], 'spend': ['spent', 'spent'], 'stride': ['strode', 'stridden'], 'rise': ['rose', 'risen'], 'pay': ['paid', 'paid'], 'cut': ['cut', 'cut'], 'break': ['broke', 'broken'], 'bend': ['bent', 'bent'], 'speak': ['spoke', 'spoken'], 'do': ['did', 'done'], 'wet': ['wet', 'wet'], 'dig': ['dug', 'dug'], 'grow': ['grew', 'grown']}


# irregular adjectives

irregular_adjectives_dict = {"good": ["better", "best"], }

################## CLASSES START ####################
class Noun(object):
    # some more consideration may be given to the gerund...
    def __init__(self, name):
        self.name = name

    def forms(self):
        standard_plural = ""
        es_plural = ""
        consonant_y_plural = ""
        ves_plural = ""
        irregular_plural = ""
        vowel_change_plural = ""
        first_plural = ""
        second_plural = ""
        genitive = ""
        plural_genitive = ""
        length = len(self.name)

        if self.name in no_plural_dict:
            pass
        elif self.name in two_plurals_dict:
            first_plural = two_plurals_dict[self.name][0]
            second_plural = two_plurals_dict[self.name][1]
        elif self.name not in final_o_no_es and self.name[length-1] == "o" or self.name[length-1] == "x" or self.name[length-2:] == "ch" or self.name[length-2:] == "sh" or self.name[length-2:] == "ss":
            es_plural = self.name + "es"
        elif self.name[length-1] == "y" and self.name[length-2] in consonants:
            consonant_y_plural = self.name[:length-1] + "ies"
            genitive = self.name + "'s"
            plural_genitive = consonant_y_plural + "'"
        elif self.name in f_exceptions:
            if self.name[length-2:] == "fe":
                ves_plural = self.name[:length-2] + "ves"
                genitive = self.name + "'s"
                plural_genitive = ves_plural + "'"
            else:
                ves_plural = self.name[:length-1] + "ves"
                genitive = self.name + "'s"
                plural_genitive = ves_plural + "'"
        elif self.name in f_double_exceptions:
            ves_plural = self.name[:length - 1] + "ves"
            standard_plural = self.name + "s"
        elif self.name in vowel_change_plural_dict:
            vowel_change_plural = vowel_change_plural_dict[self.name]

        else:
            standard_plural = self.name + "s"
            genitive = self.name + "'s"
            plural_genitive = standard_plural + "'"

        return self.name, standard_plural, es_plural, consonant_y_plural, ves_plural, irregular_plural, vowel_change_plural, first_plural, second_plural, genitive, plural_genitive

class Verb(object):

    def __init__(self, name):
        self.name = name

    def forms(self):

        def past_and_perfect(self):
            standard_ps_or_pp = ""
            final_e_ps_or_pp = ""
            irregular_ps = ""
            irregular_pp = ""
            ied_ps_or_pp = ""
            length = len(self.name)
            if self.name in irregular_verbs_dict2:
                irregular_ps = irregular_verbs_dict2[self.name][0]
                irregular_pp = irregular_verbs_dict2[self.name][1]
            elif self.name[length-1] == "e":
                final_e_ps_or_pp = self.name + "d"
            elif self.name[length - 1] == "y" and self.name[length - 2] in consonants:
                ied_ps_or_pp = self.name[:length - 1] + "ied"
            else:
                standard_ps_or_pp = self.name + "ed"

            return self.name, standard_ps_or_pp, final_e_ps_or_pp, ied_ps_or_pp, irregular_ps, irregular_pp

        def present_simple(self):
            third_person_sg = ""
            length = len(self.name)
            if self.name[length - 1] == "y" and self.name[length - 2] in consonants:
                third_person_sg = self.name[:length - 1] + "ies"
            elif self.name[length-1] == "o" or self.name[length-1] == "x" or self.name[length-2:] == "ch" or self.name[length-2:] == "sh" or self.name[length-2:] == "ss":
                third_person_sg = self.name + "es"
            else:
                third_person_sg = self.name + "s"

            return third_person_sg

        def present_participle(self):
            # more work could be devoted to verbs with two or more syllables in which the stress is not on the final syllable - e.g. enter; the gerund should be "entering" and not "enterring"
            gerund = ""
            length = len(self.name)
            if self.name[length-1] == "e" and self.name[length-2] != "e" and self.name != "age" and self.name != "dye" and self.name != "singe":
                gerund = self.name[:length-1] + "ing"
            elif self.name[length-1] in consonants and self.name[length-2] in vowels:
                gerund = self.name + self.name[length-1] + "ing"
            else:
                gerund = self.name + "ing"

            return gerund
        return past_and_perfect(self), present_simple(self), present_participle(self)

class Adjective(object):

    def __init__(self, name):
        self.name = name

    def forms(self):
        comparative = ""
        superlative = ""
        comparative = self.name + "er"
        superlative = self.name + "est"
        return self.name, comparative, superlative


class Noun_and_Verb(object):

    def __init__(self, name):
        self.name = name

    def forms(self):
        standard_plural = ""
        es_plural = ""
        consonant_y_plural = ""
        ves_plural = ""
        irregular_plural = ""
        vowel_change_plural = ""
        first_plural = ""
        second_plural = ""
        genitive = ""
        plural_genitive = ""
        standard_ps_or_pp = ""
        final_e_ps_or_pp = ""
        ied_ps_or_pp = ""
        irregular_ps = ""
        irregular_pp = ""
        length = len(self.name)

        if self.name in no_plural_dict:
            pass
        elif self.name in two_plurals_dict:
            first_plural = two_plurals_dict[self.name][0]
            second_plural = two_plurals_dict[self.name][1]
        elif self.name not in final_o_no_es and self.name[length - 1] == "o" or self.name[
                    length - 1] == "x" or self.name[length - 2:] == "ch" or self.name[length - 2:] == "sh" or self.name[
                                                                                                              length - 2:] == "ss":
            es_plural = self.name + "es"
            standard_ps_or_pp = self.name + "ed"
        elif self.name[length - 1] == "y" and self.name[length - 2] in consonants:
            consonant_y_plural = self.name[:length - 1] + "ies"
            genitive = self.name + "'s"
            plural_genitive = consonant_y_plural + "'"
            ied_ps_or_pp = self.name[:length - 1] + "ied"
        elif self.name in f_exceptions:
            if self.name[length - 2:] == "fe":
                ves_plural = self.name[:length - 2] + "ves"
                genitive = self.name + "'s"
                plural_genitive = ves_plural + "'"
            else:
                ves_plural = self.name[:length - 1] + "ves"
                genitive = self.name + "'s"
                plural_genitive = ves_plural + "'"
        elif self.name in f_double_exceptions:
            ves_plural = self.name[:length - 1] + "ves"
            standard_plural = self.name + "s"
        elif self.name in vowel_change_plural_dict:
            vowel_change_plural = vowel_change_plural_dict[self.name]

        else:
            standard_plural = self.name + "s"
            genitive = self.name + "'s"
            plural_genitive = standard_plural + "'"
            if self.name in irregular_verbs_dict2:
                irregular_ps = irregular_verbs_dict2[self.name][0]
                irregular_pp = irregular_verbs_dict2[self.name][1]
            elif self.name[length - 1] == "e":
                final_e_ps_or_pp = self.name + "d"
            else:
                standard_ps_or_pp = self.name + "ed"


        def present_participle(self):
            # more work could be devoted to verbs with two or more syllables in which the stress is not on the final syllable - e.g. enter; the gerund should be "entering" and not "enterring"
            gerund = ""
            length = len(self.name)
            if self.name[length-1] == "e" and self.name[length-2] != "e" and self.name != "age" and self.name != "dye" and self.name != "singe":
                gerund = self.name[:length-1] + "ing"
            elif self.name[length-1] in consonants and self.name[length-1] != "x" and self.name[length-2] in vowels:
                gerund = self.name + self.name[length-1] + "ing"
            else:
                gerund = self.name + "ing"

            return gerund
        return self.name, standard_plural, es_plural, consonant_y_plural, ves_plural, irregular_plural, vowel_change_plural, first_plural, second_plural, genitive, plural_genitive, standard_ps_or_pp, final_e_ps_or_pp, ied_ps_or_pp, irregular_ps, irregular_pp, present_participle(self)

################## CLASSES END ####################

def user_string_to_list(user_text):
    # for c in string.punctuation:  # this removes punctuation
    #     user_text = user_text.replace(c, "")
    user_text = user_text.lower()
    user_text_as_list = user_text.split()
    return user_text_as_list

@csrf_exempt
def count_consonants_a(request):
    user_text = request.POST.dict()
    user_text = user_text['user_text']
    some_list = user_string_to_list(user_text)
    global consonant_count_a
    consonant_count_a = 0
    # HELPER DEFINITIONS START
    def one(bit):
        # takes a part of word as an argument
        # if the part of word in the word, then subtract 1 from count
        if bit in word:
            global consonant_count_a
            bit_iteration = re.findall(bit, word)
            bit_count = len(bit_iteration)
            if bit_count == 1:
                consonant_count_a -= 1
            if bit_count == 2:
                consonant_count_a -= 2
            if bit_count == 3:
                consonant_count_a -= 3
    def two(bit):
        # takes a part of word as an argument
        # if the part of word in the word, then subtract 2 from count
        if bit in word:
            global consonant_count_a
            consonant_count_a -= 2
    def add_one_exception(exception):
        # takes a whole word as an argument
        # if the word is present, add 1 to count
        if exception == word:
            global consonant_count_a
            consonant_count_a += 1
    def subtract_one_exception(word_forms):
        # takes a list of all the inflectional forms of a given class for a given instance
        # if one of the inflectional forms is present, add 1 to count
        for element in word_forms:
            if element == word:
                global consonant_count_a
                consonant_count_a -= 1
    def subtract_one_form(string):
        if string == word:
            global consonant_count_a
            consonant_count_a -= 1
    def add_two_exception(exception):
        # takes a whole word as an argument
        # if the word is present, add 2 to count
        if exception == word:
            global consonant_count_a
            consonant_count_a += 2
    # # HELPER DEFINITIONS STOP
    # BIG START
    for word in some_list:
        length = len(word)
        # ADDITIONAL AUXILIARY FUNCTION FOR RHOTIC DIALECTS START
        def r_before_suffix(suffix):
        # takes a suffix as an argument
        # if the suffix (which starts with a consonant) is before morpheme final r, subtracts 1 from the count
            global consonant_count_a
            suffix_length = len(suffix)
            suffix_beginning = (length - suffix_length)
            if word[suffix_beginning-1:suffix_beginning] == "r" and word[suffix_beginning:length] == suffix:
                consonant_count_a -= 1
            if word[suffix_beginning - 2:suffix_beginning] == "re" and word[suffix_beginning:length] == suffix:
                consonant_count_a -= 1
        # ADDITIONAL AUXILIARY FUNCTION FOR RHOTIC DIALECTS START
        for letter in word: # this iterates through each word
            if letter == "b":
                consonant_count_a += 1
            elif letter == "c":
                consonant_count_a += 1
            elif letter == "d":
                consonant_count_a += 1
            elif letter == "f":
                consonant_count_a += 1
            elif letter == "g":
                consonant_count_a += 1
            elif letter == "h":
                consonant_count_a += 1
            elif letter == "j":
                consonant_count_a += 1
            elif letter == "k":
                consonant_count_a += 1
            elif letter == "l":
                consonant_count_a += 1
            elif letter == "m":
                consonant_count_a += 1
            elif letter == "n":
                consonant_count_a += 1
            elif letter == "p":
                consonant_count_a += 1
            elif letter == "q":
                consonant_count_a += 1
            elif letter == "r":
                consonant_count_a += 1
            elif letter == "s":
                consonant_count_a += 1
            elif letter == "t":
                consonant_count_a += 1
            elif letter == "w":
                consonant_count_a += 1
            elif letter == "v":
                consonant_count_a += 1
            elif letter == "x":
                consonant_count_a += 2
            elif letter == "y" and word.startswith("y"):
                consonant_count_a += 1
            elif letter == "z":
                consonant_count_a += 1
        # the below deals with two letter and three letter symbols for consonants
        one("bb")
        one("cc")
        one("pp")
        one("th")
        one("tt")
        one("dd")
        one("ss")
        one("wh")
        one("ck")
        one("acq")
        one("gh")
        one("ff")
        one("kk")
        one("vv")
        one("rr")
        if "ch" in word and "sch" not in word:
            bit_iteration = re.findall("ch", word)
            bit_count = len(bit_iteration)
            if bit_count == 1:
                consonant_count_a -= 1
            if bit_count == 2:
                consonant_count_a -= 2
            if bit_count == 3:
                consonant_count_a -= 3
        if "mb" in word:
            if word[length-2:] == "mb" or word[length-4:] == "mbed" or word[length-5:] == "mbing" or word[length-6:] == "mbings"or word[length-3:] == "mbs" or word[length-4:] == "mber" or word[length-5:] == "mbers" or word[length-5:] == "mbest":
                consonant_count_a -= 1
        if "mn" in word:
            if word[length-2:] == "mn" or word[length-4:] == "mned" or word[length-5:] == "mning" or word[length-6:] == "mnings" or word[length-3:] == "mns" or word[length-4:] == "mner" or word[length-5:] == "mners" or word[length-5:] == "mnest":
                consonant_count_a -= 1
        one("sch")
        one("ow")
        one("dg")
        one("sh")
        one("gg")
        one("zz")
        one("mm")
        one("nn")
        one("ll")
        one("wr")
        one("ph")
        one("ght")
        if "xx" in word:
            consonant_count_a -= 2
        if "ew" in word:
            ew_beginning = word.find("ew")
            if word[ew_beginning:] != "ew" and word[ew_beginning:length - 1] != "ew":  # this is necessary because if such a condition is not set, the line below may return "index out of range"
                if word[ew_beginning + 2] != "h" and word[ew_beginning +2] not in vowels:
                    consonant_count_a -= 1
        one("ng") # this needs additional rules, such as for "singer"
        if "nger" in word and "ang" not in word:
            if word[length-4:] == "nger":
                consonant_count_a += 1
            elif word[length-5:] == "ngers":
                consonant_count_a += 1
        if "ang" in word:
            consonant_count_a += 1

        if word[0:2] == "pn":
            consonant_count_a -= 1
        if word[0:2] == "ps":
            consonant_count_a -= 1
        if word[0:2] == "pt":
            consonant_count_a -= 1
        if word[0:2] == "kn":
            consonant_count_a -= 1
        if word[length-2:length-1] == "gn":
            consonant_count_a -= 1
        if word[0:2] == "gn":
            consonant_count_a -= 1
        if "aw" in word:
            if word[0:2] != "aw":
                consonant_count_a -= 1
        if "sce" in word or "sci" in word:
            consonant_count_a -= 1
        if "qu" in word:
            consonant_count_a += 1
        if "mu" in word: # for additional /j/ in words like "muse"
            consonant_count_a += 1
        if "mu" in word: # for words like "must" in which /j/ is not inserted
            mu_beginning = word.find("mu")
            if word[mu_beginning:] != "mu" and word[mu_beginning:length-1] != "mu": # this is necessary because if such a condition is not set, the line below may return "index out of range"
                if word[mu_beginning+2] in consonants and word[mu_beginning+3] in consonants:
                    consonant_count_a -= 1
        if "few" in word or "new" in word or "view" in word or "stew" in word or "pew" in word: # these are a bit accidental - I do not know the exact rules
            consonant_count_a += 1
        # inserting additional /j/ end
        # the class Verb does not work properly - needs corrections...
        subtract_one_exception(Noun("singer").forms())
        subtract_one_exception(Noun("hanger").forms())
        subtract_one_exception(Noun("springer").forms())
        subtract_one_exception(Noun("stringer").forms())
        subtract_one_exception(Noun("winger").forms())
        subtract_one_exception(Noun("ringer").forms())
        subtract_one_exception(Noun("stinger").forms())
        subtract_one_exception(Noun("anxiety").forms())
        subtract_one_exception(Noun("receipt").forms())
        subtract_one_exception(Noun("raspberry").forms())
        subtract_one_exception(Noun("cupboard").forms())
        subtract_one_exception(Noun_and_Verb("muscle").forms())
        subtract_one_exception(Noun_and_Verb("attempt").forms())
        subtract_one_exception(Noun("individual").forms())
        subtract_one_exception(Noun_and_Verb("doubt").forms())
        subtract_one_exception(Noun("debt").forms())
        subtract_one_exception(Adjective("subtle").forms())
        subtract_one_exception(Noun("yacht").forms())
        subtract_one_exception(Verb("except").forms())
        subtract_one_form("through")
        subtract_one_form("though")
        subtract_one_form("although")
        subtract_one_form("Hugh")
        subtract_one_form("mud")
        subtract_one_form("should")
        subtract_one_form("would")
        subtract_one_form("could")
        add_one_exception("toward")
        add_two_exception("towards")
    data = {
        'result': consonant_count_a,
    }
    return JsonResponse(data)


@csrf_exempt
def count_consonants_b(request):
    user_text = request.POST.dict()
    user_text = user_text['user_text']
    some_list = user_string_to_list(user_text)
    global consonant_count_b
    consonant_count_b = 0
    # HELPER DEFINITIONS START
    def one(bit):
        # takes a part of word as an argument
        # if the part of word in the word, then subtract 1 from count
        if bit in word:
            global consonant_count_b
            bit_iteration = re.findall(bit, word)
            bit_count = len(bit_iteration)
            if bit_count == 1:
                consonant_count_b -= 1
            if bit_count == 2:
                consonant_count_b -= 2
            if bit_count == 3:
                consonant_count_b -= 3
    def two(bit):
        # takes a part of word as an argument
        # if the part of word in the word, then subtract 2 from count
        if bit in word:
            global consonant_count_b
            consonant_count_b -= 2
    def add_one_exception(exception):
        # takes a whole word as an argument
        # if the word is present, add 1 to count
        if exception == word:
            global consonant_count_b
            consonant_count_b += 1
    def subtract_one_exception(word_forms):
        # takes a list of all the inflectional forms of a given class for a given instance
        # if one of the inflectional forms is present, add 1 to count
        for element in word_forms:
            if element == word:
                global consonant_count_b
                consonant_count_b -= 1
    def subtract_one_form(string):
        if string == word:
            global consonant_count_b
            consonant_count_b -= 1
    def add_two_exception(exception):
        # takes a whole word as an argument
        # if the word is present, add 2 to count
        if exception == word:
            global consonant_count_b
            consonant_count_b += 2
    # # HELPER DEFINITIONS STOP
    # BIG START
    for word in some_list:
        length = len(word)
        # ADDITIONAL AUXILIARY FUNCTION FOR RHOTIC DIALECTS START
        def r_before_suffix(suffix):
        # takes a suffix as an argument
        # if the suffix (which starts with a consonant) is before morpheme final r, subtracts 1 from the count
            global consonant_count_b
            suffix_length = len(suffix)
            suffix_beginning = (length - suffix_length)
            if word[suffix_beginning-1:suffix_beginning] == "r" and word[suffix_beginning:length] == suffix:
                consonant_count_b -= 1
            if word[suffix_beginning - 2:suffix_beginning] == "re" and word[suffix_beginning:length] == suffix:
                consonant_count_b -= 1
        # ADDITIONAL AUXILIARY FUNCTION FOR RHOTIC DIALECTS START
        for letter in word: # this iterates through each word
            if letter == "b":
                consonant_count_b += 1
            elif letter == "c":
                consonant_count_b += 1
            elif letter == "d":
                consonant_count_b += 1
            elif letter == "f":
                consonant_count_b += 1
            elif letter == "g":
                consonant_count_b += 1
            elif letter == "h":
                consonant_count_b += 1
            elif letter == "j":
                consonant_count_b += 1
            elif letter == "k":
                consonant_count_b += 1
            elif letter == "l":
                consonant_count_b += 1
            elif letter == "m":
                consonant_count_b += 1
            elif letter == "n":
                consonant_count_b += 1
            elif letter == "p":
                consonant_count_b += 1
            elif letter == "q":
                consonant_count_b += 1
            elif letter == "r":
                consonant_count_b += 1
            elif letter == "s":
                consonant_count_b += 1
            elif letter == "t":
                consonant_count_b += 1
            elif letter == "w":
                consonant_count_b += 1
            elif letter == "v":
                consonant_count_b += 1
            elif letter == "x":
                consonant_count_b += 2
            elif letter == "y" and word.startswith("y"):
                consonant_count_b += 1
            elif letter == "z":
                consonant_count_b += 1
        # the below deals with two letter and three letter symbols for consonants
        one("bb")
        one("cc")
        one("pp")
        one("th")
        one("tt")
        one("dd")
        one("ss")
        one("wh")
        one("ck")
        one("acq")
        one("gh")
        one("ff")
        one("kk")
        one("vv")
        if "ch" in word and "sch" not in word:
            bit_iteration = re.findall("ch", word)
            bit_count = len(bit_iteration)
            if bit_count == 1:
                consonant_count_b -= 1
            if bit_count == 2:
                consonant_count_b -= 2
            if bit_count == 3:
                consonant_count_b -= 3
        if "mb" in word:
            if word[length-2:] == "mb" or word[length-4:] == "mbed" or word[length-5:] == "mbing" or word[length-6:] == "mbings"or word[length-3:] == "mbs" or word[length-4:] == "mber" or word[length-5:] == "mbers" or word[length-5:] == "mbest":
                consonant_count_b -= 1
        if "mn" in word:
            if word[length-2:] == "mn" or word[length-4:] == "mned" or word[length-5:] == "mning" or word[length-6:] == "mnings" or word[length-3:] == "mns" or word[length-4:] == "mner" or word[length-5:] == "mners" or word[length-5:] == "mnest":
                consonant_count_b -= 1
        one("sch")
        one("ow")
        one("dg")
        one("sh")
        one("gg")
        one("zz")
        one("mm")
        one("nn")
        one("ll")
        one("wr")
        one("ph")
        one("ght")
        if "xx" in word:
            consonant_count_b -= 2
        if "ew" in word:
            ew_beginning = word.find("ew")
            if word[ew_beginning:] != "ew" and word[ew_beginning:length - 1] != "ew":  # this is necessary because if such a condition is not set, the line below may return "index out of range"
                if word[ew_beginning + 2] != "h" and word[ew_beginning +2] not in vowels:
                    consonant_count_b -= 1
        one("ng") # this needs additional rules, such as for "singer"
        if "nger" in word and "ang" not in word:
            if word[length-4:] == "nger":
                consonant_count_b += 1
            elif word[length-5:] == "ngers":
                consonant_count_b += 1
        if "ang" in word:
            consonant_count_b += 1
        # dealing with non-rhotic dialects - start
        one("rb")
        one("rc")
        one("rd")
        one("rf")
        one("rg")
        one("rh")
        one("rj")
        one("rk")
        one("rl")
        one("rm")
        one("rn")
        one("rp")
        one("rq")
        one("rr")
        one("rs")
        one("rt")
        one("rv")
        one("rw")
        one("rx")
        one("rz")
        if word[length-2:length] == "re" or word[length-3:length] == "res": # this requires futher work - "fires" does not work
            consonant_count_b -= 1
        if word[length-1] == "r":
            consonant_count_b -= 1
        if "re" in word:
            if word[0:2] != "re":
                if word[length-6:] == "reless" or word[length-5:] == "redom" or word[length-6:] == "redoms" or word[length-5:] == "reful" or word[length-6:] == "refuls" or word[length-7:] == "refully" or word[length-6:] == "rehood" or word[length-7:] == "rehoods" or word[length-6:] == "rement" or word[length-7:] == "rements" or word[length-6:] == "reness" or word[length-8:] == "renesses" or word[length-6:] == "reship" or word[length-7:] == "reships" or word[length-4:] == "rely" or word[length-6:] == "refree":
                    consonant_count_b -= 1
        # dealing with non-rhotic dialects - end
        if word[0:2] == "pn":
            consonant_count_b -= 1
        if word[0:2] == "ps":
            consonant_count_b -= 1
        if word[0:2] == "pt":
            consonant_count_b -= 1
        if word[0:2] == "kn":
            consonant_count_b -= 1
        if word[length-2:length-1] == "gn":
            consonant_count_b -= 1
        if word[0:2] == "gn":
            consonant_count_b -= 1
        if "aw" in word:
            if word[0:2] != "aw":
                consonant_count_b -= 1
        if "sce" in word or "sci" in word:
            consonant_count_b -= 1
        if "qu" in word:
            consonant_count_b += 1
        # inserting additional /j/ start
        if "du" in word: # for additional /j/ in words like "duration"
            consonant_count_b += 1
        if "du" in word: # for words like "dusk" in which /j/ is not inserted
            du_beginning = word.find("du")
            if word[du_beginning:] != "du" and word[du_beginning:length-1] != "du": # this is necessary because if such a condition is not set, the line below may return "index out of range"
                if word[du_beginning+2] in consonants and word[du_beginning+3] in consonants:
                    consonant_count_b -= 1
        if "mu" in word: # for additional /j/ in words like "muse"
            consonant_count_b += 1
        if "mu" in word: # for words like "must" in which /j/ is not inserted
            mu_beginning = word.find("mu")
            if word[mu_beginning:] != "mu" and word[mu_beginning:length-1] != "mu": # this is necessary because if such a condition is not set, the line below may return "index out of range"
                if word[mu_beginning+2] in consonants and word[mu_beginning+3] in consonants:
                    consonant_count_b -= 1
        if "few" in word or "new" in word or "view" in word or "stew" in word or "pew" in word: # these are a bit accidental - I do not know the exact rules
            consonant_count_b += 1 ###############
        # inserting additional /j/ end
        if "-" in word:
            hyphen_index = 0
            for letter in word:
                if letter == "-":
                    break
                else:
                    hyphen_index += 1
            if word[hyphen_index-1] == "r" and word[hyphen_index+1] not in vowels:
                consonant_count_b -= 1
            elif word[hyphen_index-2:hyphen_index] == "re" and word[hyphen_index+1] not in vowels:
                consonant_count_b -= 1
        # the class Verb does not work properly - needs corrections...
        subtract_one_exception(Noun("singer").forms())
        subtract_one_exception(Noun("hanger").forms())
        subtract_one_exception(Noun("springer").forms())
        subtract_one_exception(Noun("stringer").forms())
        subtract_one_exception(Noun("winger").forms())
        subtract_one_exception(Noun("ringer").forms())
        subtract_one_exception(Noun("stinger").forms())
        subtract_one_exception(Noun("anxiety").forms())
        subtract_one_exception(Noun("receipt").forms())
        subtract_one_exception(Noun("raspberry").forms())
        subtract_one_exception(Noun("cupboard").forms())
        subtract_one_exception(Noun_and_Verb("muscle").forms())
        subtract_one_exception(Noun_and_Verb("attempt").forms())
        subtract_one_exception(Noun("individual").forms())
        subtract_one_exception(Noun_and_Verb("doubt").forms())
        subtract_one_exception(Noun("debt").forms())
        subtract_one_exception(Adjective("subtle").forms())
        subtract_one_exception(Noun("yacht").forms())
        subtract_one_exception(Verb("except").forms())
        subtract_one_form("through")
        subtract_one_form("though")
        subtract_one_form("although")
        subtract_one_form("Hugh")
        subtract_one_form("mud")
        subtract_one_form("should")
        subtract_one_form("would")
        subtract_one_form("could")
        add_one_exception("toward")
        add_two_exception("towards")
        # morphemes (only these beginning with a vowel - the ones beginning with a consonant are not needed)
        r_before_suffix("ed")
    data = {
        'result': consonant_count_b,
    }
    return JsonResponse(data)



@csrf_exempt
def count_vowels_a(request):
    user_text = request.POST.dict()
    user_text = user_text['user_text']
    some_list = user_string_to_list(user_text)
    global vowel_count_a
    vowel_count_a = 0
    # HELPER DEFINITIONS START
    def one(bit):
        # takes a part of word as an argument
        # if the part of word in the word, then subtract 1 from vowel_count_a
        if bit in word:
            global vowel_count_a
            bit_iteration = re.findall(bit, word)
            bit_count = len(bit_iteration)
            if bit_count == 1:
                vowel_count_a -= 1
            if bit_count == 2:
                vowel_count_a -= 2
            if bit_count == 3:
                vowel_count_a -= 3
    def two(bit):
        # takes a part of word as an argument
        # if the part of word in the word, then subtract 2 from vowel_count_a
        if bit in word:
            global vowel_count_a
            vowel_count_a -= 2
    def add_one_exception(exception):
        # takes a whole word as an argument
        # if the word is present, add 1 to vowel_count_a
        if exception == word:
            global vowel_count_a
            vowel_count_a += 1
    def subtract_one_exception(exception):
        # takes a whole word as an argument
        # if the word is present, add 1 to vowel_count_a
        if exception == word:
            global vowel_count_a
            vowel_count_a -= 1
    def add_two_exception(exception):
        # takes a whole word as an argument
        # if the word is present, add 2 to vowel_count_a
        if exception == word:
            global vowel_count_a
            vowel_count_a += 2
    # # HELPER DEFINITIONS STOP
    # BIG START
    for word in some_list:
        length = len(word)
        # ADDITIONAL HELPER FUNCTION START
        def e_before_suffix(suffix):
        # takes a suffix as an argument
        # if the suffix is before morpheme final e, subtracts 1 from the vowel_count_a
            global vowel_count_a
            suffix_length = len(suffix)
            suffix_beginning = (length - suffix_length)
            if word[suffix_beginning-2:suffix_beginning] == "ee" and word[suffix_beginning:length] == suffix:
                vowel_count_a += 1
            if word[suffix_beginning - 2:suffix_beginning] == "ie" and word[suffix_beginning:length] == suffix:
                vowel_count_a += 1
            if word[suffix_beginning - 2:suffix_beginning] == "ye" and word[suffix_beginning:length] == suffix:
                vowel_count_a += 1
            if word[suffix_beginning - 3:suffix_beginning] == "aye" and word[suffix_beginning:length] == suffix:
                vowel_count_a -= 1
            if word[suffix_beginning-3:suffix_beginning] == "oye" and word[suffix_beginning:length] == suffix:
                vowel_count_a -= 1
            if word[suffix_beginning - 2:suffix_beginning] == "oe" and word[suffix_beginning:length] == suffix:
                vowel_count_a += 1
            if word[suffix_beginning - 2:suffix_beginning] == "ue" and word[suffix_beginning:length] == suffix:
                vowel_count_a += 1
            if word[suffix_beginning:length] == suffix and word[suffix_beginning-1] == "e" and word[suffix_beginning-3:suffix_beginning] != "ire":
                vowel_count_a -= 1

        def syllabic_en_before_suffix(suffix):
            # takes a suffix as an argument
            # if the suffix is before morpheme final e, subtracts 1 from the vowel_count_a
            global vowel_count_a
            suffix_length = len(suffix)
            suffix_beginning = (length - suffix_length)
            if word[suffix_beginning - 3:suffix_beginning] == "ten" and word[suffix_beginning:length] == suffix:
                vowel_count_a -= 1
            if word[suffix_beginning - 3:suffix_beginning] == "den" and word[suffix_beginning:length] == suffix:
                vowel_count_a -= 1
            if word[suffix_beginning - 3:suffix_beginning] == "ven" and word[suffix_beginning:length] == suffix:
                vowel_count_a -= 1

        # ADDITIONAL HELPER FUNCTION STOP
        for letter in word: # this iterates through each word
            if letter == "e":
                vowel_count_a += 1
            elif letter == "a":
                vowel_count_a += 1
            elif letter == "u":
                vowel_count_a += 1
            elif letter == "i":
                vowel_count_a += 1
            elif letter == "y" and not word.startswith("y"):
                vowel_count_a += 1
            elif letter == "o":
                vowel_count_a += 1
        # the below deals with two letter and three letter symbols for vowels
        one("ee")
        if word[length - 2:length] == "ee" or word[length - 3:length] == "ees" or word[length-3:length] == "eed":
            vowel_count_a += 1
        one("ea")
        one("ie")
        if word[length-2:length] == "ie" or word[length-3:length] == "ies" or word[length-3:length] == "ied":
            vowel_count_a += 1
        one("ei")
        one("ey")
        one("ai")
        one("oo")
        if "ou" in word and "eou" not in word and "iou" not in word:
            vowel_count_a -= 1
        if "eo" in word and "eou" not in word:
            vowel_count_a -= 1
        if "io" in word and "iou" not in word:
            vowel_count_a -= 1
        two("eou")
        two("iou")
        # the rule for AmE where words ending in "er", "re" and "or" loose one vowel - instead the syllabic "r" is pronounced - FOR NOW THE ONLY DIFFERENCE FROM THE SAME FUNCTION FOR BrE
        if word.endswith("er") and word[length-3] in consonants and len(word) > 3:
            vowel_count_a -= 1
        # unfortunate case of -ye start...
        if "ay" in word and "aye" not in word:
            vowel_count_a -= 1
        if "oy" in word and "oye" not in word:
            vowel_count_a -= 1
        if "ye" in word and "aye" not in word and "oye" not in word and word[length-length:(length-length)+2] != "ye":
            vowel_count_a -= 1
        if word[length-2:length] == "ye" or word[length-3:length] == "yes" or word[length-3:length] == "yed":
            vowel_count_a += 1
        if word[length-3:length] == "aye" or word[length-3:length] == "oye" or word[length-4:length] == "ayes" or word[length-4:length] == "oyes" or word[length-4:length] == "ayed" or word[length-4:length] == "oyed":
            vowel_count_a -= 1
        one("aye")
        one("oye")
        # unfortunate case of -ye end...
        one("oe")
        if word[length-2:length] == "oe" or word[length-3:length] == "oes" or word[length-3:length] == "oed":
            vowel_count_a += 1
        one("au")
        one("oa")
        one("ue")
        if word[length - 2:length] == "ue" or word[length - 3:length] == "ues" or word[length-3:length] == "ued":
            vowel_count_a += 1
        one("ui")
        one("ua")
        one("oi")
        one("ia")
        one("eu")
        one("aa")
        # the below deals with the e in the word-final position - in a general way
        if word[length-1] == "e" and word[length-3:length] != "ire":
            vowel_count_a -= 1 # deals with final mute e in singular
        if word[length - 2:length] == "es" and word[length-4:length] != "ires" and word[length-3:length] != "ges" and word[length-3:length] != "ces" and word[length-3:length] != "ses" and word[length-3:length] != "zes" and word[length-4:length] != "ches" and word[length-4:length] != "shes" and word[length-4:length] != "sses" and word[length-3:length] != "xes":
            vowel_count_a -= 1  # deals with final mute e in plural
        # the below deals with simple past and past participle forms
        if word[length - 2:length] == "ed":
            if word[length-3] in consonants and length == 3:
                vowel_count_a += 1
            if word[length-3] in consonants and word[length-4] in consonants and length == 4:
                vowel_count_a += 1
            if word[length-3] in consonants and word[length-4] in consonants and word[length-5] in consonants and length == 5:
                vowel_count_a += 1
        if word[length - 2:length] == "ed" and word[length - 3:length] != "ted" and word[length - 3:length] != "ded":
            vowel_count_a -= 1
        # the below deals with syllabic n in "en" endings
        if word.endswith("en") and length > 3:
            if word[length-3] == "t" or word[length-3] == "d" or word[length-3] == "v":
                vowel_count_a -= 1
        # the below deals with syllabic n in "tton" endings
        if word.endswith("tton") and length > 4:
            vowel_count_a -= 1
        # implementing morpheme final e rules for compounds with "e"
        if "-" in word:
            hyphen_index = 0
            for letter in word:
                if letter == "-":
                    hyphen_index += 1
                    break
                else:
                    hyphen_index += 1
            if word[hyphen_index - 2:hyphen_index] == "e-" and word[hyphen_index-4:hyphen_index] != "ire-":
                vowel_count_a -= 1  # deals with final mute e when a) it is in singular, b) it is in a compound with - as the first word
            if word[hyphen_index - 3:hyphen_index] == "es-" and word[hyphen_index-5:hyphen_index] != "ires-" and word[hyphen_index - 4:hyphen_index] != "ges-" and word[hyphen_index - 4:hyphen_index] != "ces-" and word[hyphen_index - 4:hyphen_index] != "ses-" and word[hyphen_index - 4:hyphen_index] != "zes-" and word[hyphen_index - 5:hyphen_index] != "ches-" and word[hyphen_index - 5:hyphen_index] != "shes-" and word[hyphen_index - 5:hyphen_index] != "sses-" and word[hyphen_index - 4:hyphen_index] != "xes-":
                vowel_count_a -= 1  # deals with final mute e when a) it is in plural, b) it is in a compound with - as the first word
            if word[hyphen_index-3:hyphen_index] == "ee-" or word[hyphen_index-4:hyphen_index] == "ees-" or word[hyphen_index-4:hyphen_index] == "eed-":
                vowel_count_a += 1
            if word[hyphen_index-3:hyphen_index] == "ie-" or word[hyphen_index-4:hyphen_index] == "ies-" or word[hyphen_index-4:hyphen_index] == "ied-":
                vowel_count_a += 1
            # unfortunate case of -ye... start
            if word[hyphen_index-3:hyphen_index] == "ye-" or word[hyphen_index-4:hyphen_index] == "yes-" or word[hyphen_index-4:hyphen_index] == "yed-":
                vowel_count_a += 1
            if word[hyphen_index-4:hyphen_index] == "aye-" or word[hyphen_index-4:hyphen_index] == "oye-" or word[hyphen_index-5:hyphen_index] == "ayes-" or word[hyphen_index-5:hyphen_index] == "oyes-" or word[hyphen_index-5:hyphen_index] == "ayed-" or word[hyphen_index-5:hyphen_index] == "oyed-":
                vowel_count_a -= 1
            # unfortunate case of -ye... end
            if word[hyphen_index-3:hyphen_index] == "oe-" or word[hyphen_index-4:hyphen_index] == "oes-" or word[hyphen_index-4:hyphen_index] == "oed-":
                vowel_count_a += 1
            if word[hyphen_index-3:hyphen_index] == "ue-" or word[hyphen_index-4:hyphen_index] == "ues-" or word[hyphen_index-4:hyphen_index] == "ued-":
                vowel_count_a += 1
            # # the below deals with simple past and past participle forms before -
            if word[hyphen_index-3:hyphen_index] == "ed-" and word[hyphen_index-4:hyphen_index] != "ted-" and word[hyphen_index-4:hyphen_index] != "ded-":
                vowel_count_a -= 1
            pre_hyphen_length = len(word[:hyphen_index-1])
            if word[hyphen_index - 2:hyphen_index] == "e-" and pre_hyphen_length == 1: # deals with compounds such as e-book
                vowel_count_a += 1
            if word[hyphen_index-3:hyphen_index] == "re-" and pre_hyphen_length == 2:
                vowel_count_a += 1
            if word[hyphen_index - 4:hyphen_index] == "pre-" and pre_hyphen_length == 3:
                vowel_count_a += 1
        # removing morpheme-final e before derivational suffixes (but not in compounds with -)
        if "less" in word:
            e_before_suffix("less")
        if "dom" in word:
            e_before_suffix("dom")
        if "doms" in word:
            e_before_suffix("doms")
        if "ful" in word:
            e_before_suffix("ful")
        if "fuls" in word:
            e_before_suffix("fuls")
        if "fully" in word:
            e_before_suffix("fully")
        if "hood" in word:
            e_before_suffix("hood")
        if "hoods" in word:
            e_before_suffix("hoods")
        if "ment" in word:
            e_before_suffix("ment")
        if "ments" in word:
            e_before_suffix("ments")
        if "ness" in word:
            e_before_suffix("ness")
        if "nesses" in word:
            e_before_suffix("nesses")
        if "ship" in word:
            e_before_suffix("ship")
        if "ships" in word:
            e_before_suffix("ships")
        if "ly" in word:
            e_before_suffix("ly")
        if "free" in word:
            e_before_suffix("free")

        # dealing with syllabic "en" before  derivational suffixes (but not in compounds with -)
        if "less" in word:
            syllabic_en_before_suffix("less")
        if "dom" in word:
            syllabic_en_before_suffix("dom")
        if "doms" in word:
            syllabic_en_before_suffix("doms")
        if "ful" in word:
            syllabic_en_before_suffix("ful")
        if "fuls" in word:
            syllabic_en_before_suffix("fuls")
        if "fully" in word:
            syllabic_en_before_suffix("fully")
        if "hood" in word:
            syllabic_en_before_suffix("hood")
        if "hoods" in word:
            syllabic_en_before_suffix("hoods")
        if "ment" in word:
            syllabic_en_before_suffix("ment")
        if "ments" in word:
            syllabic_en_before_suffix("ments")
        if "ness" in word:
            syllabic_en_before_suffix("ness")
        if "nesses" in word:
            syllabic_en_before_suffix("nesses")
        if "ship" in word:
            syllabic_en_before_suffix("ship")
        if "ships" in word:
            syllabic_en_before_suffix("ships")
        if "ly" in word:
            syllabic_en_before_suffix("ly")
        if "free" in word:
            syllabic_en_before_suffix("free")

        # lexical exceptions
        add_one_exception("lion")
        if word[length - 1:length] == "e":
            if word[length-2] in consonants and length == 2:
                vowel_count_a += 1
            if word[length-2] in consonants and word[length-3] in consonants and length == 3:
                vowel_count_a += 1
            if word[length-2] in consonants and word[length-3] in consonants and word[length-4] in consonants and length == 4:
                vowel_count_a += 1
        add_two_exception("mediocre")
        subtract_one_exception("business")
        add_one_exception("free")
    data = {
        'result': vowel_count_a,
    }
    return JsonResponse(data)


@csrf_exempt
def count_vowels_b(request):
    user_text = request.POST.dict()
    user_text = user_text['user_text']
    some_list = user_string_to_list(user_text)
    global vowel_count_b
    vowel_count_b = 0
    # HELPER DEFINITIONS START
    def one(bit):
        # takes a part of word as an argument
        # if the part of word in the word, then subtract 1 from vowel_count_b
        if bit in word:
            global vowel_count_b
            bit_iteration = re.findall(bit, word)
            bit_count = len(bit_iteration)
            if bit_count == 1:
                vowel_count_b -= 1
            if bit_count == 2:
                vowel_count_b -= 2
            if bit_count == 3:
                vowel_count_b -= 3
    def two(bit):
        # takes a part of word as an argument
        # if the part of word in the word, then subtract 2 from vowel_count_b
        if bit in word:
            global vowel_count_b
            vowel_count_b -= 2
    def add_one_exception(exception):
        # takes a whole word as an argument
        # if the word is present, add 1 to vowel_count_b
        if exception == word:
            global vowel_count_b
            vowel_count_b += 1
    def subtract_one_exception(exception):
        # takes a whole word as an argument
        # if the word is present, add 1 to vowel_count_b
        if exception == word:
            global vowel_count_b
            vowel_count_b -= 1
    def add_two_exception(exception):
        # takes a whole word as an argument
        # if the word is present, add 2 to vowel_count_b
        if exception == word:
            global vowel_count_b
            vowel_count_b += 2
    # # HELPER DEFINITIONS STOP
    # BIG START
    for word in some_list:
        length = len(word)
        # ADDITIONAL HELPER FUNCTION START
        def e_before_suffix(suffix):
        # takes a suffix as an argument
        # if the suffix is before morpheme final e, subtracts 1 from the vowel_count_b
            global vowel_count_b
            suffix_length = len(suffix)
            suffix_beginning = (length - suffix_length)
            if word[suffix_beginning-2:suffix_beginning] == "ee" and word[suffix_beginning:length] == suffix:
                vowel_count_b += 1
            if word[suffix_beginning - 2:suffix_beginning] == "ie" and word[suffix_beginning:length] == suffix:
                vowel_count_b += 1
            if word[suffix_beginning - 2:suffix_beginning] == "ye" and word[suffix_beginning:length] == suffix:
                vowel_count_b += 1
            if word[suffix_beginning - 3:suffix_beginning] == "aye" and word[suffix_beginning:length] == suffix:
                vowel_count_b -= 1
            if word[suffix_beginning-3:suffix_beginning] == "oye" and word[suffix_beginning:length] == suffix:
                vowel_count_b -= 1
            if word[suffix_beginning - 2:suffix_beginning] == "oe" and word[suffix_beginning:length] == suffix:
                vowel_count_b += 1
            if word[suffix_beginning - 2:suffix_beginning] == "ue" and word[suffix_beginning:length] == suffix:
                vowel_count_b += 1
            if word[suffix_beginning:length] == suffix and word[suffix_beginning-1] == "e" and word[suffix_beginning-3:suffix_beginning] != "ire":
                vowel_count_b -= 1

        def syllabic_en_before_suffix(suffix):
            # takes a suffix as an argument
            # if the suffix is before morpheme final e, subtracts 1 from the vowel_count_a
            global vowel_count_b
            suffix_length = len(suffix)
            suffix_beginning = (length - suffix_length)
            if word[suffix_beginning - 3:suffix_beginning] == "ten" and word[suffix_beginning:length] == suffix:
                vowel_count_b -= 1
            if word[suffix_beginning - 3:suffix_beginning] == "den" and word[suffix_beginning:length] == suffix:
                vowel_count_b -= 1
            if word[suffix_beginning - 3:suffix_beginning] == "ven" and word[suffix_beginning:length] == suffix:
                vowel_count_b -= 1

        # ADDITIONAL HELPER FUNCTION STOP
        for letter in word: # this iterates through each word
            if letter == "e":
                vowel_count_b += 1
            elif letter == "a":
                vowel_count_b += 1
            elif letter == "u":
                vowel_count_b += 1
            elif letter == "i":
                vowel_count_b += 1
            elif letter == "y" and not word.startswith("y"):
                vowel_count_b += 1
            elif letter == "o":
                vowel_count_b += 1
        # the below deals with two letter and three letter symbols for vowels
        one("ee")
        if word[length - 2:length] == "ee" or word[length - 3:length] == "ees" or word[length-3:length] == "eed":
            vowel_count_b += 1
        one("ea")
        one("ie")
        if word[length-2:length] == "ie" or word[length-3:length] == "ies" or word[length-3:length] == "ied":
            vowel_count_b += 1
        one("ei")
        one("ey")
        one("ai")
        one("oo")
        if "ou" in word and "eou" not in word and "iou" not in word:
            vowel_count_b -= 1
        if "eo" in word and "eou" not in word:
            vowel_count_b -= 1
        if "io" in word and "iou" not in word:
            vowel_count_b -= 1
        two("eou")
        two("iou")
        # unfortunate case of -ye start...
        if "ay" in word and "aye" not in word:
            vowel_count_b -= 1
        if "oy" in word and "oye" not in word:
            vowel_count_b -= 1
        if "ye" in word and "aye" not in word and "oye" not in word and word[length-length:(length-length)+2] != "ye":
            vowel_count_b -= 1
        if word[length-2:length] == "ye" or word[length-3:length] == "yes" or word[length-3:length] == "yed":
            vowel_count_b += 1
        if word[length-3:length] == "aye" or word[length-3:length] == "oye" or word[length-4:length] == "ayes" or word[length-4:length] == "oyes" or word[length-4:length] == "ayed" or word[length-4:length] == "oyed":
            vowel_count_b -= 1
        one("aye")
        one("oye")
        # unfortunate case of -ye end...
        one("oe")
        if word[length-2:length] == "oe" or word[length-3:length] == "oes" or word[length-3:length] == "oed":
            vowel_count_b += 1
        one("au")
        one("oa")
        one("ue")
        if word[length - 2:length] == "ue" or word[length - 3:length] == "ues" or word[length-3:length] == "ued":
            vowel_count_b += 1
        one("ui")
        one("ua")
        one("oi")
        one("ia")
        one("eu")
        one("aa")
        # the below deals with the e in the word-final position - in a general way
        if word[length-1] == "e" and word[length-3:length] != "ire":
            vowel_count_b -= 1 # deals with final mute e in singular
        if word[length - 2:length] == "es" and word[length-4:length] != "ires" and word[length-3:length] != "ges" and word[length-3:length] != "ces" and word[length-3:length] != "ses" and word[length-3:length] != "zes" and word[length-4:length] != "ches" and word[length-4:length] != "shes" and word[length-4:length] != "sses" and word[length-3:length] != "xes":
            vowel_count_b -= 1  # deals with final mute e in plural
        # the below deals with simple past and past participle forms
        if word[length - 2:length] == "ed":
            if word[length-3] in consonants and length == 3:
                vowel_count_b += 1
            if word[length-3] in consonants and word[length-4] in consonants and length == 4:
                vowel_count_b += 1
            if word[length-3] in consonants and word[length-4] in consonants and word[length-5] in consonants and length == 5:
                vowel_count_b += 1
        if word[length - 2:length] == "ed" and word[length - 3:length] != "ted" and word[length - 3:length] != "ded":
            vowel_count_b -= 1
        # the below deals with syllabic n in "en" endings
        if word.endswith("en") and length > 3:
            if word[length-3] == "t" or word[length-3] == "d" or word[length-3] == "v":
                vowel_count_b -= 1
        # the below deals with syllabic n in "tton" endings
        if word.endswith("tton") and length > 4:
            vowel_count_b -= 1
        # implementing morpheme final e rules for compounds with "e"
        if "-" in word:
            hyphen_index = 0
            for letter in word:
                if letter == "-":
                    hyphen_index += 1
                    break
                else:
                    hyphen_index += 1
            if word[hyphen_index - 2:hyphen_index] == "e-" and word[hyphen_index-4:hyphen_index] != "ire-":
                vowel_count_b -= 1  # deals with final mute e when a) it is in singular, b) it is in a compound with - as the first word
            if word[hyphen_index - 3:hyphen_index] == "es-" and word[hyphen_index-5:hyphen_index] != "ires-" and word[hyphen_index - 4:hyphen_index] != "ges-" and word[hyphen_index - 4:hyphen_index] != "ces-" and word[hyphen_index - 4:hyphen_index] != "ses-" and word[hyphen_index - 4:hyphen_index] != "zes-" and word[hyphen_index - 5:hyphen_index] != "ches-" and word[hyphen_index - 5:hyphen_index] != "shes-" and word[hyphen_index - 5:hyphen_index] != "sses-" and word[hyphen_index - 4:hyphen_index] != "xes-":
                vowel_count_b -= 1  # deals with final mute e when a) it is in plural, b) it is in a compound with - as the first word
            if word[hyphen_index-3:hyphen_index] == "ee-" or word[hyphen_index-4:hyphen_index] == "ees-" or word[hyphen_index-4:hyphen_index] == "eed-":
                vowel_count_b += 1
            if word[hyphen_index-3:hyphen_index] == "ie-" or word[hyphen_index-4:hyphen_index] == "ies-" or word[hyphen_index-4:hyphen_index] == "ied-":
                vowel_count_b += 1
            # unfortunate case of -ye... start
            if word[hyphen_index-3:hyphen_index] == "ye-" or word[hyphen_index-4:hyphen_index] == "yes-" or word[hyphen_index-4:hyphen_index] == "yed-":
                vowel_count_b += 1
            if word[hyphen_index-4:hyphen_index] == "aye-" or word[hyphen_index-4:hyphen_index] == "oye-" or word[hyphen_index-5:hyphen_index] == "ayes-" or word[hyphen_index-5:hyphen_index] == "oyes-" or word[hyphen_index-5:hyphen_index] == "ayed-" or word[hyphen_index-5:hyphen_index] == "oyed-":
                vowel_count_b -= 1
            # unfortunate case of -ye... end
            if word[hyphen_index-3:hyphen_index] == "oe-" or word[hyphen_index-4:hyphen_index] == "oes-" or word[hyphen_index-4:hyphen_index] == "oed-":
                vowel_count_b += 1
            if word[hyphen_index-3:hyphen_index] == "ue-" or word[hyphen_index-4:hyphen_index] == "ues-" or word[hyphen_index-4:hyphen_index] == "ued-":
                vowel_count_b += 1
            # # the below deals with simple past and past participle forms before -
            if word[hyphen_index-3:hyphen_index] == "ed-" and word[hyphen_index-4:hyphen_index] != "ted-" and word[hyphen_index-4:hyphen_index] != "ded-":
                vowel_count_b -= 1
            pre_hyphen_length = len(word[:hyphen_index-1])
            if word[hyphen_index - 2:hyphen_index] == "e-" and pre_hyphen_length == 1: # deals with compounds such as e-book
                vowel_count_b += 1
            if word[hyphen_index-3:hyphen_index] == "re-" and pre_hyphen_length == 2:
                vowel_count_b += 1
            if word[hyphen_index - 4:hyphen_index] == "pre-" and pre_hyphen_length == 3:
                vowel_count_b += 1
        # removing morpheme-final e before derivational suffixes (but not in compounds with -)
        if "less" in word:
            e_before_suffix("less")
        if "dom" in word:
            e_before_suffix("dom")
        if "doms" in word:
            e_before_suffix("doms")
        if "ful" in word:
            e_before_suffix("ful")
        if "fuls" in word:
            e_before_suffix("fuls")
        if "fully" in word:
            e_before_suffix("fully")
        if "hood" in word:
            e_before_suffix("hood")
        if "hoods" in word:
            e_before_suffix("hoods")
        if "ment" in word:
            e_before_suffix("ment")
        if "ments" in word:
            e_before_suffix("ments")
        if "ness" in word:
            e_before_suffix("ness")
        if "nesses" in word:
            e_before_suffix("nesses")
        if "ship" in word:
            e_before_suffix("ship")
        if "ships" in word:
            e_before_suffix("ships")
        if "ly" in word:
            e_before_suffix("ly")
        if "free" in word:
            e_before_suffix("free")

        # dealing with syllabic "en" before  derivational suffixes (but not in compounds with -)
        if "less" in word:
            syllabic_en_before_suffix("less")
        if "dom" in word:
            syllabic_en_before_suffix("dom")
        if "doms" in word:
            syllabic_en_before_suffix("doms")
        if "ful" in word:
            syllabic_en_before_suffix("ful")
        if "fuls" in word:
            syllabic_en_before_suffix("fuls")
        if "fully" in word:
            syllabic_en_before_suffix("fully")
        if "hood" in word:
            syllabic_en_before_suffix("hood")
        if "hoods" in word:
            syllabic_en_before_suffix("hoods")
        if "ment" in word:
            syllabic_en_before_suffix("ment")
        if "ments" in word:
            syllabic_en_before_suffix("ments")
        if "ness" in word:
            syllabic_en_before_suffix("ness")
        if "nesses" in word:
            syllabic_en_before_suffix("nesses")
        if "ship" in word:
            syllabic_en_before_suffix("ship")
        if "ships" in word:
            syllabic_en_before_suffix("ships")
        if "ly" in word:
            syllabic_en_before_suffix("ly")
        if "free" in word:
            syllabic_en_before_suffix("free")

        # lexical exceptions
        add_one_exception("lion")
        if word[length - 1:length] == "e":
            if word[length-2] in consonants and length == 2:
                vowel_count_b += 1
            if word[length-2] in consonants and word[length-3] in consonants and length == 3:
                vowel_count_b += 1
            if word[length-2] in consonants and word[length-3] in consonants and word[length-4] in consonants and length == 4:
                vowel_count_b += 1
        add_two_exception("mediocre")
        subtract_one_exception("business")
        add_one_exception("free")
    data = {
        'result': vowel_count_b,
    }
    return JsonResponse(data)


@csrf_exempt
def count_phonemes_a(request):
    user_text = request.POST.dict()
    user_text = user_text['user_text']

    def count_consonants_a(user_text):
        some_list = user_string_to_list(user_text)
        global consonant_count_a
        consonant_count_a = 0

        # HELPER DEFINITIONS START
        def one(bit):
            # takes a part of word as an argument
            # if the part of word in the word, then subtract 1 from count
            if bit in word:
                global consonant_count_a
                bit_iteration = re.findall(bit, word)
                bit_count = len(bit_iteration)
                if bit_count == 1:
                    consonant_count_a -= 1
                if bit_count == 2:
                    consonant_count_a -= 2
                if bit_count == 3:
                    consonant_count_a -= 3

        def two(bit):
            # takes a part of word as an argument
            # if the part of word in the word, then subtract 2 from count
            if bit in word:
                global consonant_count_a
                consonant_count_a -= 2

        def add_one_exception(exception):
            # takes a whole word as an argument
            # if the word is present, add 1 to count
            if exception == word:
                global consonant_count_a
                consonant_count_a += 1

        def subtract_one_exception(word_forms):
            # takes a list of all the inflectional forms of a given class for a given instance
            # if one of the inflectional forms is present, add 1 to count
            for element in word_forms:
                if element == word:
                    global consonant_count_a
                    consonant_count_a -= 1

        def subtract_one_form(string):
            if string == word:
                global consonant_count_a
                consonant_count_a -= 1

        def add_two_exception(exception):
            # takes a whole word as an argument
            # if the word is present, add 2 to count
            if exception == word:
                global consonant_count_a
                consonant_count_a += 2

        # # HELPER DEFINITIONS STOP
        # BIG START
        for word in some_list:
            length = len(word)

            # ADDITIONAL AUXILIARY FUNCTION FOR RHOTIC DIALECTS START
            def r_before_suffix(suffix):
                # takes a suffix as an argument
                # if the suffix (which starts with a consonant) is before morpheme final r, subtracts 1 from the count
                global consonant_count_a
                suffix_length = len(suffix)
                suffix_beginning = (length - suffix_length)
                if word[suffix_beginning - 1:suffix_beginning] == "r" and word[suffix_beginning:length] == suffix:
                    consonant_count_a -= 1
                if word[suffix_beginning - 2:suffix_beginning] == "re" and word[suffix_beginning:length] == suffix:
                    consonant_count_a -= 1

            # ADDITIONAL AUXILIARY FUNCTION FOR RHOTIC DIALECTS START
            for letter in word:  # this iterates through each word
                if letter == "b":
                    consonant_count_a += 1
                elif letter == "c":
                    consonant_count_a += 1
                elif letter == "d":
                    consonant_count_a += 1
                elif letter == "f":
                    consonant_count_a += 1
                elif letter == "g":
                    consonant_count_a += 1
                elif letter == "h":
                    consonant_count_a += 1
                elif letter == "j":
                    consonant_count_a += 1
                elif letter == "k":
                    consonant_count_a += 1
                elif letter == "l":
                    consonant_count_a += 1
                elif letter == "m":
                    consonant_count_a += 1
                elif letter == "n":
                    consonant_count_a += 1
                elif letter == "p":
                    consonant_count_a += 1
                elif letter == "q":
                    consonant_count_a += 1
                elif letter == "r":
                    consonant_count_a += 1
                elif letter == "s":
                    consonant_count_a += 1
                elif letter == "t":
                    consonant_count_a += 1
                elif letter == "w":
                    consonant_count_a += 1
                elif letter == "v":
                    consonant_count_a += 1
                elif letter == "x":
                    consonant_count_a += 2
                elif letter == "y" and word.startswith("y"):
                    consonant_count_a += 1
                elif letter == "z":
                    consonant_count_a += 1
            # the below deals with two letter and three letter symbols for consonants
            one("bb")
            one("cc")
            one("pp")
            one("th")
            one("tt")
            one("dd")
            one("ss")
            one("wh")
            one("ck")
            one("acq")
            one("gh")
            one("ff")
            one("kk")
            one("vv")
            one("rr")
            if "ch" in word and "sch" not in word:
                bit_iteration = re.findall("ch", word)
                bit_count = len(bit_iteration)
                if bit_count == 1:
                    consonant_count_a -= 1
                if bit_count == 2:
                    consonant_count_a -= 2
                if bit_count == 3:
                    consonant_count_a -= 3
            if "mb" in word:
                if word[length - 2:] == "mb" or word[length - 4:] == "mbed" or word[length - 5:] == "mbing" or word[
                                                                                                               length - 6:] == "mbings" or word[
                                                                                                                                           length - 3:] == "mbs" or word[
                                                                                                                                                                    length - 4:] == "mber" or word[
                                                                                                                                                                                              length - 5:] == "mbers" or word[
                                                                                                                                                                                                                         length - 5:] == "mbest":
                    consonant_count_a -= 1
            if "mn" in word:
                if word[length - 2:] == "mn" or word[length - 4:] == "mned" or word[length - 5:] == "mning" or word[
                                                                                                               length - 6:] == "mnings" or word[
                                                                                                                                           length - 3:] == "mns" or word[
                                                                                                                                                                    length - 4:] == "mner" or word[
                                                                                                                                                                                              length - 5:] == "mners" or word[
                                                                                                                                                                                                                         length - 5:] == "mnest":
                    consonant_count_a -= 1
            one("sch")
            one("ow")
            one("dg")
            one("sh")
            one("gg")
            one("zz")
            one("mm")
            one("nn")
            one("ll")
            one("wr")
            one("ph")
            one("ght")
            if "xx" in word:
                consonant_count_a -= 2
            if "ew" in word:
                ew_beginning = word.find("ew")
                if word[ew_beginning:] != "ew" and word[
                                                   ew_beginning:length - 1] != "ew":  # this is necessary because if such a condition is not set, the line below may return "index out of range"
                    if word[ew_beginning + 2] != "h" and word[ew_beginning + 2] not in vowels:
                        consonant_count_a -= 1
            one("ng")  # this needs additional rules, such as for "singer"
            if "nger" in word and "ang" not in word:
                if word[length - 4:] == "nger":
                    consonant_count_a += 1
                elif word[length - 5:] == "ngers":
                    consonant_count_a += 1
            if "ang" in word:
                consonant_count_a += 1

            if word[0:2] == "pn":
                consonant_count_a -= 1
            if word[0:2] == "ps":
                consonant_count_a -= 1
            if word[0:2] == "pt":
                consonant_count_a -= 1
            if word[0:2] == "kn":
                consonant_count_a -= 1
            if word[length - 2:length - 1] == "gn":
                consonant_count_a -= 1
            if word[0:2] == "gn":
                consonant_count_a -= 1
            if "aw" in word:
                if word[0:2] != "aw":
                    consonant_count_a -= 1
            if "sce" in word or "sci" in word:
                consonant_count_a -= 1
            if "qu" in word:
                consonant_count_a += 1
            if "mu" in word:  # for additional /j/ in words like "muse"
                consonant_count_a += 1
            if "mu" in word:  # for words like "must" in which /j/ is not inserted
                mu_beginning = word.find("mu")
                if word[mu_beginning:] != "mu" and word[
                                                   mu_beginning:length - 1] != "mu":  # this is necessary because if such a condition is not set, the line below may return "index out of range"
                    if word[mu_beginning + 2] in consonants and word[mu_beginning + 3] in consonants:
                        consonant_count_a -= 1
            if "few" in word or "new" in word or "view" in word or "stew" in word or "pew" in word:  # these are a bit accidental - I do not know the exact rules
                consonant_count_a += 1
            # inserting additional /j/ end
            # the class Verb does not work properly - needs corrections...
            subtract_one_exception(Noun("singer").forms())
            subtract_one_exception(Noun("hanger").forms())
            subtract_one_exception(Noun("springer").forms())
            subtract_one_exception(Noun("stringer").forms())
            subtract_one_exception(Noun("winger").forms())
            subtract_one_exception(Noun("ringer").forms())
            subtract_one_exception(Noun("stinger").forms())
            subtract_one_exception(Noun("anxiety").forms())
            subtract_one_exception(Noun("receipt").forms())
            subtract_one_exception(Noun("raspberry").forms())
            subtract_one_exception(Noun("cupboard").forms())
            subtract_one_exception(Noun_and_Verb("muscle").forms())
            subtract_one_exception(Noun_and_Verb("attempt").forms())
            subtract_one_exception(Noun("individual").forms())
            subtract_one_exception(Noun_and_Verb("doubt").forms())
            subtract_one_exception(Noun("debt").forms())
            subtract_one_exception(Adjective("subtle").forms())
            subtract_one_exception(Noun("yacht").forms())
            subtract_one_exception(Verb("except").forms())
            subtract_one_form("through")
            subtract_one_form("though")
            subtract_one_form("although")
            subtract_one_form("Hugh")
            subtract_one_form("mud")
            subtract_one_form("should")
            subtract_one_form("would")
            subtract_one_form("could")
            add_one_exception("toward")
            add_two_exception("towards")
        return consonant_count_a


    def count_vowels_a(user_text):
        some_list = user_string_to_list(user_text)
        global vowel_count_a
        vowel_count_a = 0

        # HELPER DEFINITIONS START
        def one(bit):
            # takes a part of word as an argument
            # if the part of word in the word, then subtract 1 from vowel_count_a
            if bit in word:
                global vowel_count_a
                bit_iteration = re.findall(bit, word)
                bit_count = len(bit_iteration)
                if bit_count == 1:
                    vowel_count_a -= 1
                if bit_count == 2:
                    vowel_count_a -= 2
                if bit_count == 3:
                    vowel_count_a -= 3

        def two(bit):
            # takes a part of word as an argument
            # if the part of word in the word, then subtract 2 from vowel_count_a
            if bit in word:
                global vowel_count_a
                vowel_count_a -= 2

        def add_one_exception(exception):
            # takes a whole word as an argument
            # if the word is present, add 1 to vowel_count_a
            if exception == word:
                global vowel_count_a
                vowel_count_a += 1

        def subtract_one_exception(exception):
            # takes a whole word as an argument
            # if the word is present, add 1 to vowel_count_a
            if exception == word:
                global vowel_count_a
                vowel_count_a -= 1

        def add_two_exception(exception):
            # takes a whole word as an argument
            # if the word is present, add 2 to vowel_count_a
            if exception == word:
                global vowel_count_a
                vowel_count_a += 2

        # # HELPER DEFINITIONS STOP
        # BIG START
        for word in some_list:
            length = len(word)

            # ADDITIONAL HELPER FUNCTION START
            def e_before_suffix(suffix):
                # takes a suffix as an argument
                # if the suffix is before morpheme final e, subtracts 1 from the vowel_count_a
                global vowel_count_a
                suffix_length = len(suffix)
                suffix_beginning = (length - suffix_length)
                if word[suffix_beginning - 2:suffix_beginning] == "ee" and word[suffix_beginning:length] == suffix:
                    vowel_count_a += 1
                if word[suffix_beginning - 2:suffix_beginning] == "ie" and word[suffix_beginning:length] == suffix:
                    vowel_count_a += 1
                if word[suffix_beginning - 2:suffix_beginning] == "ye" and word[suffix_beginning:length] == suffix:
                    vowel_count_a += 1
                if word[suffix_beginning - 3:suffix_beginning] == "aye" and word[suffix_beginning:length] == suffix:
                    vowel_count_a -= 1
                if word[suffix_beginning - 3:suffix_beginning] == "oye" and word[suffix_beginning:length] == suffix:
                    vowel_count_a -= 1
                if word[suffix_beginning - 2:suffix_beginning] == "oe" and word[suffix_beginning:length] == suffix:
                    vowel_count_a += 1
                if word[suffix_beginning - 2:suffix_beginning] == "ue" and word[suffix_beginning:length] == suffix:
                    vowel_count_a += 1
                if word[suffix_beginning:length] == suffix and word[suffix_beginning - 1] == "e" and word[
                                                                                                     suffix_beginning - 3:suffix_beginning] != "ire":
                    vowel_count_a -= 1

            def syllabic_en_before_suffix(suffix):
                # takes a suffix as an argument
                # if the suffix is before morpheme final e, subtracts 1 from the vowel_count_a
                global vowel_count_a
                suffix_length = len(suffix)
                suffix_beginning = (length - suffix_length)
                if word[suffix_beginning - 3:suffix_beginning] == "ten" and word[suffix_beginning:length] == suffix:
                    vowel_count_a -= 1
                if word[suffix_beginning - 3:suffix_beginning] == "den" and word[suffix_beginning:length] == suffix:
                    vowel_count_a -= 1
                if word[suffix_beginning - 3:suffix_beginning] == "ven" and word[suffix_beginning:length] == suffix:
                    vowel_count_a -= 1

            # ADDITIONAL HELPER FUNCTION STOP
            for letter in word:  # this iterates through each word
                if letter == "e":
                    vowel_count_a += 1
                elif letter == "a":
                    vowel_count_a += 1
                elif letter == "u":
                    vowel_count_a += 1
                elif letter == "i":
                    vowel_count_a += 1
                elif letter == "y" and not word.startswith("y"):
                    vowel_count_a += 1
                elif letter == "o":
                    vowel_count_a += 1
            # the below deals with two letter and three letter symbols for vowels
            one("ee")
            if word[length - 2:length] == "ee" or word[length - 3:length] == "ees" or word[length - 3:length] == "eed":
                vowel_count_a += 1
            one("ea")
            one("ie")
            if word[length - 2:length] == "ie" or word[length - 3:length] == "ies" or word[length - 3:length] == "ied":
                vowel_count_a += 1
            one("ei")
            one("ey")
            one("ai")
            one("oo")
            if "ou" in word and "eou" not in word and "iou" not in word:
                vowel_count_a -= 1
            if "eo" in word and "eou" not in word:
                vowel_count_a -= 1
            if "io" in word and "iou" not in word:
                vowel_count_a -= 1
            two("eou")
            two("iou")
            # the rule for AmE where words ending in "er", "re" and "or" loose one vowel - instead the syllabic "r" is pronounced - FOR NOW THE ONLY DIFFERENCE FROM THE SAME FUNCTION FOR BrE
            if word.endswith("er") and word[length - 3] in consonants and len(word) > 3:
                vowel_count_a -= 1
            # unfortunate case of -ye start...
            if "ay" in word and "aye" not in word:
                vowel_count_a -= 1
            if "oy" in word and "oye" not in word:
                vowel_count_a -= 1
            if "ye" in word and "aye" not in word and "oye" not in word and word[length - length:(
                                                                                                         length - length) + 2] != "ye":
                vowel_count_a -= 1
            if word[length - 2:length] == "ye" or word[length - 3:length] == "yes" or word[length - 3:length] == "yed":
                vowel_count_a += 1
            if word[length - 3:length] == "aye" or word[length - 3:length] == "oye" or word[
                                                                                       length - 4:length] == "ayes" or word[
                                                                                                                       length - 4:length] == "oyes" or word[
                                                                                                                                                       length - 4:length] == "ayed" or word[
                                                                                                                                                                                       length - 4:length] == "oyed":
                vowel_count_a -= 1
            one("aye")
            one("oye")
            # unfortunate case of -ye end...
            one("oe")
            if word[length - 2:length] == "oe" or word[length - 3:length] == "oes" or word[length - 3:length] == "oed":
                vowel_count_a += 1
            one("au")
            one("oa")
            one("ue")
            if word[length - 2:length] == "ue" or word[length - 3:length] == "ues" or word[length - 3:length] == "ued":
                vowel_count_a += 1
            one("ui")
            one("ua")
            one("oi")
            one("ia")
            one("eu")
            one("aa")
            # the below deals with the e in the word-final position - in a general way
            if word[length - 1] == "e" and word[length - 3:length] != "ire":
                vowel_count_a -= 1  # deals with final mute e in singular
            if word[length - 2:length] == "es" and word[length - 4:length] != "ires" and word[
                                                                                         length - 3:length] != "ges" and word[
                                                                                                                         length - 3:length] != "ces" and word[
                                                                                                                                                         length - 3:length] != "ses" and word[
                                                                                                                                                                                         length - 3:length] != "zes" and word[
                                                                                                                                                                                                                         length - 4:length] != "ches" and word[
                                                                                                                                                                                                                                                          length - 4:length] != "shes" and word[
                                                                                                                                                                                                                                                                                           length - 4:length] != "sses" and word[
                                                                                                                                                                                                                                                                                                                            length - 3:length] != "xes":
                vowel_count_a -= 1  # deals with final mute e in plural
            # the below deals with simple past and past participle forms
            if word[length - 2:length] == "ed":
                if word[length - 3] in consonants and length == 3:
                    vowel_count_a += 1
                if word[length - 3] in consonants and word[length - 4] in consonants and length == 4:
                    vowel_count_a += 1
                if word[length - 3] in consonants and word[length - 4] in consonants and word[
                    length - 5] in consonants and length == 5:
                    vowel_count_a += 1
            if word[length - 2:length] == "ed" and word[length - 3:length] != "ted" and word[
                                                                                        length - 3:length] != "ded":
                vowel_count_a -= 1
            # the below deals with syllabic n in "en" endings
            if word.endswith("en") and length > 3:
                if word[length - 3] == "t" or word[length - 3] == "d" or word[length - 3] == "v":
                    vowel_count_a -= 1
            # the below deals with syllabic n in "tton" endings
            if word.endswith("tton") and length > 4:
                vowel_count_a -= 1
            # implementing morpheme final e rules for compounds with "e"
            if "-" in word:
                hyphen_index = 0
                for letter in word:
                    if letter == "-":
                        hyphen_index += 1
                        break
                    else:
                        hyphen_index += 1
                if word[hyphen_index - 2:hyphen_index] == "e-" and word[hyphen_index - 4:hyphen_index] != "ire-":
                    vowel_count_a -= 1  # deals with final mute e when a) it is in singular, b) it is in a compound with - as the first word
                if word[hyphen_index - 3:hyphen_index] == "es-" and word[
                                                                    hyphen_index - 5:hyphen_index] != "ires-" and word[
                                                                                                                  hyphen_index - 4:hyphen_index] != "ges-" and word[
                                                                                                                                                               hyphen_index - 4:hyphen_index] != "ces-" and word[
                                                                                                                                                                                                            hyphen_index - 4:hyphen_index] != "ses-" and word[
                                                                                                                                                                                                                                                         hyphen_index - 4:hyphen_index] != "zes-" and word[
                                                                                                                                                                                                                                                                                                      hyphen_index - 5:hyphen_index] != "ches-" and word[
                                                                                                                                                                                                                                                                                                                                                    hyphen_index - 5:hyphen_index] != "shes-" and word[
                                                                                                                                                                                                                                                                                                                                                                                                  hyphen_index - 5:hyphen_index] != "sses-" and word[
                                                                                                                                                                                                                                                                                                                                                                                                                                                hyphen_index - 4:hyphen_index] != "xes-":
                    vowel_count_a -= 1  # deals with final mute e when a) it is in plural, b) it is in a compound with - as the first word
                if word[hyphen_index - 3:hyphen_index] == "ee-" or word[
                                                                   hyphen_index - 4:hyphen_index] == "ees-" or word[
                                                                                                               hyphen_index - 4:hyphen_index] == "eed-":
                    vowel_count_a += 1
                if word[hyphen_index - 3:hyphen_index] == "ie-" or word[
                                                                   hyphen_index - 4:hyphen_index] == "ies-" or word[
                                                                                                               hyphen_index - 4:hyphen_index] == "ied-":
                    vowel_count_a += 1
                # unfortunate case of -ye... start
                if word[hyphen_index - 3:hyphen_index] == "ye-" or word[
                                                                   hyphen_index - 4:hyphen_index] == "yes-" or word[
                                                                                                               hyphen_index - 4:hyphen_index] == "yed-":
                    vowel_count_a += 1
                if word[hyphen_index - 4:hyphen_index] == "aye-" or word[
                                                                    hyphen_index - 4:hyphen_index] == "oye-" or word[
                                                                                                                hyphen_index - 5:hyphen_index] == "ayes-" or word[
                                                                                                                                                             hyphen_index - 5:hyphen_index] == "oyes-" or word[
                                                                                                                                                                                                          hyphen_index - 5:hyphen_index] == "ayed-" or word[
                                                                                                                                                                                                                                                       hyphen_index - 5:hyphen_index] == "oyed-":
                    vowel_count_a -= 1
                # unfortunate case of -ye... end
                if word[hyphen_index - 3:hyphen_index] == "oe-" or word[
                                                                   hyphen_index - 4:hyphen_index] == "oes-" or word[
                                                                                                               hyphen_index - 4:hyphen_index] == "oed-":
                    vowel_count_a += 1
                if word[hyphen_index - 3:hyphen_index] == "ue-" or word[
                                                                   hyphen_index - 4:hyphen_index] == "ues-" or word[
                                                                                                               hyphen_index - 4:hyphen_index] == "ued-":
                    vowel_count_a += 1
                # # the below deals with simple past and past participle forms before -
                if word[hyphen_index - 3:hyphen_index] == "ed-" and word[
                                                                    hyphen_index - 4:hyphen_index] != "ted-" and word[
                                                                                                                 hyphen_index - 4:hyphen_index] != "ded-":
                    vowel_count_a -= 1
                pre_hyphen_length = len(word[:hyphen_index - 1])
                if word[
                   hyphen_index - 2:hyphen_index] == "e-" and pre_hyphen_length == 1:  # deals with compounds such as e-book
                    vowel_count_a += 1
                if word[hyphen_index - 3:hyphen_index] == "re-" and pre_hyphen_length == 2:
                    vowel_count_a += 1
                if word[hyphen_index - 4:hyphen_index] == "pre-" and pre_hyphen_length == 3:
                    vowel_count_a += 1
            # removing morpheme-final e before derivational suffixes (but not in compounds with -)
            if "less" in word:
                e_before_suffix("less")
            if "dom" in word:
                e_before_suffix("dom")
            if "doms" in word:
                e_before_suffix("doms")
            if "ful" in word:
                e_before_suffix("ful")
            if "fuls" in word:
                e_before_suffix("fuls")
            if "fully" in word:
                e_before_suffix("fully")
            if "hood" in word:
                e_before_suffix("hood")
            if "hoods" in word:
                e_before_suffix("hoods")
            if "ment" in word:
                e_before_suffix("ment")
            if "ments" in word:
                e_before_suffix("ments")
            if "ness" in word:
                e_before_suffix("ness")
            if "nesses" in word:
                e_before_suffix("nesses")
            if "ship" in word:
                e_before_suffix("ship")
            if "ships" in word:
                e_before_suffix("ships")
            if "ly" in word:
                e_before_suffix("ly")
            if "free" in word:
                e_before_suffix("free")

            # dealing with syllabic "en" before  derivational suffixes (but not in compounds with -)
            if "less" in word:
                syllabic_en_before_suffix("less")
            if "dom" in word:
                syllabic_en_before_suffix("dom")
            if "doms" in word:
                syllabic_en_before_suffix("doms")
            if "ful" in word:
                syllabic_en_before_suffix("ful")
            if "fuls" in word:
                syllabic_en_before_suffix("fuls")
            if "fully" in word:
                syllabic_en_before_suffix("fully")
            if "hood" in word:
                syllabic_en_before_suffix("hood")
            if "hoods" in word:
                syllabic_en_before_suffix("hoods")
            if "ment" in word:
                syllabic_en_before_suffix("ment")
            if "ments" in word:
                syllabic_en_before_suffix("ments")
            if "ness" in word:
                syllabic_en_before_suffix("ness")
            if "nesses" in word:
                syllabic_en_before_suffix("nesses")
            if "ship" in word:
                syllabic_en_before_suffix("ship")
            if "ships" in word:
                syllabic_en_before_suffix("ships")
            if "ly" in word:
                syllabic_en_before_suffix("ly")
            if "free" in word:
                syllabic_en_before_suffix("free")

            # lexical exceptions
            add_one_exception("lion")
            if word[length - 1:length] == "e":
                if word[length - 2] in consonants and length == 2:
                    vowel_count_a += 1
                if word[length - 2] in consonants and word[length - 3] in consonants and length == 3:
                    vowel_count_a += 1
                if word[length - 2] in consonants and word[length - 3] in consonants and word[
                    length - 4] in consonants and length == 4:
                    vowel_count_a += 1
            add_two_exception("mediocre")
            subtract_one_exception("business")
            add_one_exception("free")
        return vowel_count_a


    phoneme_count_a = count_consonants_a(user_text) + count_vowels_a(user_text)
    data = {
        'result': phoneme_count_a,
    }
    return JsonResponse(data)





@csrf_exempt
def count_phonemes_b(request):
    user_text = request.POST.dict()
    user_text = user_text['user_text']

    def count_consonants_b(user_text):
        some_list = user_string_to_list(user_text)
        global consonant_count_b
        consonant_count_b = 0

        # HELPER DEFINITIONS START
        def one(bit):
            # takes a part of word as an argument
            # if the part of word in the word, then subtract 1 from count
            if bit in word:
                global consonant_count_b
                bit_iteration = re.findall(bit, word)
                bit_count = len(bit_iteration)
                if bit_count == 1:
                    consonant_count_b -= 1
                if bit_count == 2:
                    consonant_count_b -= 2
                if bit_count == 3:
                    consonant_count_b -= 3

        def two(bit):
            # takes a part of word as an argument
            # if the part of word in the word, then subtract 2 from count
            if bit in word:
                global consonant_count_b
                consonant_count_b -= 2

        def add_one_exception(exception):
            # takes a whole word as an argument
            # if the word is present, add 1 to count
            if exception == word:
                global consonant_count_b
                consonant_count_b += 1

        def subtract_one_exception(word_forms):
            # takes a list of all the inflectional forms of a given class for a given instance
            # if one of the inflectional forms is present, add 1 to count
            for element in word_forms:
                if element == word:
                    global consonant_count_b
                    consonant_count_b -= 1

        def subtract_one_form(string):
            if string == word:
                global consonant_count_b
                consonant_count_b -= 1

        def add_two_exception(exception):
            # takes a whole word as an argument
            # if the word is present, add 2 to count
            if exception == word:
                global consonant_count_b
                consonant_count_b += 2

        # # HELPER DEFINITIONS STOP
        # BIG START
        for word in some_list:
            length = len(word)

            # ADDITIONAL AUXILIARY FUNCTION FOR RHOTIC DIALECTS START
            def r_before_suffix(suffix):
                # takes a suffix as an argument
                # if the suffix (which starts with a consonant) is before morpheme final r, subtracts 1 from the count
                global consonant_count_b
                suffix_length = len(suffix)
                suffix_beginning = (length - suffix_length)
                if word[suffix_beginning - 1:suffix_beginning] == "r" and word[suffix_beginning:length] == suffix:
                    consonant_count_b -= 1
                if word[suffix_beginning - 2:suffix_beginning] == "re" and word[suffix_beginning:length] == suffix:
                    consonant_count_b -= 1

            # ADDITIONAL AUXILIARY FUNCTION FOR RHOTIC DIALECTS START
            for letter in word:  # this iterates through each word
                if letter == "b":
                    consonant_count_b += 1
                elif letter == "c":
                    consonant_count_b += 1
                elif letter == "d":
                    consonant_count_b += 1
                elif letter == "f":
                    consonant_count_b += 1
                elif letter == "g":
                    consonant_count_b += 1
                elif letter == "h":
                    consonant_count_b += 1
                elif letter == "j":
                    consonant_count_b += 1
                elif letter == "k":
                    consonant_count_b += 1
                elif letter == "l":
                    consonant_count_b += 1
                elif letter == "m":
                    consonant_count_b += 1
                elif letter == "n":
                    consonant_count_b += 1
                elif letter == "p":
                    consonant_count_b += 1
                elif letter == "q":
                    consonant_count_b += 1
                elif letter == "r":
                    consonant_count_b += 1
                elif letter == "s":
                    consonant_count_b += 1
                elif letter == "t":
                    consonant_count_b += 1
                elif letter == "w":
                    consonant_count_b += 1
                elif letter == "v":
                    consonant_count_b += 1
                elif letter == "x":
                    consonant_count_b += 2
                elif letter == "y" and word.startswith("y"):
                    consonant_count_b += 1
                elif letter == "z":
                    consonant_count_b += 1
            # the below deals with two letter and three letter symbols for consonants
            one("bb")
            one("cc")
            one("pp")
            one("th")
            one("tt")
            one("dd")
            one("ss")
            one("wh")
            one("ck")
            one("acq")
            one("gh")
            one("ff")
            one("kk")
            one("vv")
            if "ch" in word and "sch" not in word:
                bit_iteration = re.findall("ch", word)
                bit_count = len(bit_iteration)
                if bit_count == 1:
                    consonant_count_b -= 1
                if bit_count == 2:
                    consonant_count_b -= 2
                if bit_count == 3:
                    consonant_count_b -= 3
            if "mb" in word:
                if word[length - 2:] == "mb" or word[length - 4:] == "mbed" or word[length - 5:] == "mbing" or word[
                                                                                                               length - 6:] == "mbings" or word[
                                                                                                                                           length - 3:] == "mbs" or word[
                                                                                                                                                                    length - 4:] == "mber" or word[
                                                                                                                                                                                              length - 5:] == "mbers" or word[
                                                                                                                                                                                                                         length - 5:] == "mbest":
                    consonant_count_b -= 1
            if "mn" in word:
                if word[length - 2:] == "mn" or word[length - 4:] == "mned" or word[length - 5:] == "mning" or word[
                                                                                                               length - 6:] == "mnings" or word[
                                                                                                                                           length - 3:] == "mns" or word[
                                                                                                                                                                    length - 4:] == "mner" or word[
                                                                                                                                                                                              length - 5:] == "mners" or word[
                                                                                                                                                                                                                         length - 5:] == "mnest":
                    consonant_count_b -= 1
            one("sch")
            one("ow")
            one("dg")
            one("sh")
            one("gg")
            one("zz")
            one("mm")
            one("nn")
            one("ll")
            one("wr")
            one("ph")
            one("ght")
            if "xx" in word:
                consonant_count_b -= 2
            if "ew" in word:
                ew_beginning = word.find("ew")
                if word[ew_beginning:] != "ew" and word[
                                                   ew_beginning:length - 1] != "ew":  # this is necessary because if such a condition is not set, the line below may return "index out of range"
                    if word[ew_beginning + 2] != "h" and word[ew_beginning + 2] not in vowels:
                        consonant_count_b -= 1
            one("ng")  # this needs additional rules, such as for "singer"
            if "nger" in word and "ang" not in word:
                if word[length - 4:] == "nger":
                    consonant_count_b += 1
                elif word[length - 5:] == "ngers":
                    consonant_count_b += 1
            if "ang" in word:
                consonant_count_b += 1
            # dealing with non-rhotic dialects - start
            one("rb")
            one("rc")
            one("rd")
            one("rf")
            one("rg")
            one("rh")
            one("rj")
            one("rk")
            one("rl")
            one("rm")
            one("rn")
            one("rp")
            one("rq")
            one("rr")
            one("rs")
            one("rt")
            one("rv")
            one("rw")
            one("rx")
            one("rz")
            if word[length - 2:length] == "re" or word[
                                                  length - 3:length] == "res":  # this requires futher work - "fires" does not work
                consonant_count_b -= 1
            if word[length - 1] == "r":
                consonant_count_b -= 1
            if "re" in word:
                if word[0:2] != "re":
                    if word[length - 6:] == "reless" or word[length - 5:] == "redom" or word[
                                                                                        length - 6:] == "redoms" or word[
                                                                                                                    length - 5:] == "reful" or word[
                                                                                                                                               length - 6:] == "refuls" or word[
                                                                                                                                                                           length - 7:] == "refully" or word[
                                                                                                                                                                                                        length - 6:] == "rehood" or word[
                                                                                                                                                                                                                                    length - 7:] == "rehoods" or word[
                                                                                                                                                                                                                                                                 length - 6:] == "rement" or word[
                                                                                                                                                                                                                                                                                             length - 7:] == "rements" or word[
                                                                                                                                                                                                                                                                                                                          length - 6:] == "reness" or word[
                                                                                                                                                                                                                                                                                                                                                      length - 8:] == "renesses" or word[
                                                                                                                                                                                                                                                                                                                                                                                    length - 6:] == "reship" or word[
                                                                                                                                                                                                                                                                                                                                                                                                                length - 7:] == "reships" or word[
                                                                                                                                                                                                                                                                                                                                                                                                                                             length - 4:] == "rely" or word[
                                                                                                                                                                                                                                                                                                                                                                                                                                                                       length - 6:] == "refree":
                        consonant_count_b -= 1
            # dealing with non-rhotic dialects - end
            if word[0:2] == "pn":
                consonant_count_b -= 1
            if word[0:2] == "ps":
                consonant_count_b -= 1
            if word[0:2] == "pt":
                consonant_count_b -= 1
            if word[0:2] == "kn":
                consonant_count_b -= 1
            if word[length - 2:length - 1] == "gn":
                consonant_count_b -= 1
            if word[0:2] == "gn":
                consonant_count_b -= 1
            if "aw" in word:
                if word[0:2] != "aw":
                    consonant_count_b -= 1
            if "sce" in word or "sci" in word:
                consonant_count_b -= 1
            if "qu" in word:
                consonant_count_b += 1
            # inserting additional /j/ start
            if "du" in word:  # for additional /j/ in words like "duration"
                consonant_count_b += 1
            if "du" in word:  # for words like "dusk" in which /j/ is not inserted
                du_beginning = word.find("du")
                if word[du_beginning:] != "du" and word[
                                                   du_beginning:length - 1] != "du":  # this is necessary because if such a condition is not set, the line below may return "index out of range"
                    if word[du_beginning + 2] in consonants and word[du_beginning + 3] in consonants:
                        consonant_count_b -= 1
            if "mu" in word:  # for additional /j/ in words like "muse"
                consonant_count_b += 1
            if "mu" in word:  # for words like "must" in which /j/ is not inserted
                mu_beginning = word.find("mu")
                if word[mu_beginning:] != "mu" and word[
                                                   mu_beginning:length - 1] != "mu":  # this is necessary because if such a condition is not set, the line below may return "index out of range"
                    if word[mu_beginning + 2] in consonants and word[mu_beginning + 3] in consonants:
                        consonant_count_b -= 1
            if "few" in word or "new" in word or "view" in word or "stew" in word or "pew" in word:  # these are a bit accidental - I do not know the exact rules
                consonant_count_b += 1  ###############
            # inserting additional /j/ end
            if "-" in word:
                hyphen_index = 0
                for letter in word:
                    if letter == "-":
                        break
                    else:
                        hyphen_index += 1
                if word[hyphen_index - 1] == "r" and word[hyphen_index + 1] not in vowels:
                    consonant_count_b -= 1
                elif word[hyphen_index - 2:hyphen_index] == "re" and word[hyphen_index + 1] not in vowels:
                    consonant_count_b -= 1
            # the class Verb does not work properly - needs corrections...
            subtract_one_exception(Noun("singer").forms())
            subtract_one_exception(Noun("hanger").forms())
            subtract_one_exception(Noun("springer").forms())
            subtract_one_exception(Noun("stringer").forms())
            subtract_one_exception(Noun("winger").forms())
            subtract_one_exception(Noun("ringer").forms())
            subtract_one_exception(Noun("stinger").forms())
            subtract_one_exception(Noun("anxiety").forms())
            subtract_one_exception(Noun("receipt").forms())
            subtract_one_exception(Noun("raspberry").forms())
            subtract_one_exception(Noun("cupboard").forms())
            subtract_one_exception(Noun_and_Verb("muscle").forms())
            subtract_one_exception(Noun_and_Verb("attempt").forms())
            subtract_one_exception(Noun("individual").forms())
            subtract_one_exception(Noun_and_Verb("doubt").forms())
            subtract_one_exception(Noun("debt").forms())
            subtract_one_exception(Adjective("subtle").forms())
            subtract_one_exception(Noun("yacht").forms())
            subtract_one_exception(Verb("except").forms())
            subtract_one_form("through")
            subtract_one_form("though")
            subtract_one_form("although")
            subtract_one_form("Hugh")
            subtract_one_form("mud")
            subtract_one_form("should")
            subtract_one_form("would")
            subtract_one_form("could")
            add_one_exception("toward")
            add_two_exception("towards")
            # morphemes (only these beginning with a vowel - the ones beginning with a consonant are not needed)
            r_before_suffix("ed")
        return consonant_count_b

    def count_vowels_b(user_text):
        some_list = user_string_to_list(user_text)
        global vowel_count_b
        vowel_count_b = 0

        # HELPER DEFINITIONS START
        def one(bit):
            # takes a part of word as an argument
            # if the part of word in the word, then subtract 1 from vowel_count_b
            if bit in word:
                global vowel_count_b
                bit_iteration = re.findall(bit, word)
                bit_count = len(bit_iteration)
                if bit_count == 1:
                    vowel_count_b -= 1
                if bit_count == 2:
                    vowel_count_b -= 2
                if bit_count == 3:
                    vowel_count_b -= 3

        def two(bit):
            # takes a part of word as an argument
            # if the part of word in the word, then subtract 2 from vowel_count_b
            if bit in word:
                global vowel_count_b
                vowel_count_b -= 2

        def add_one_exception(exception):
            # takes a whole word as an argument
            # if the word is present, add 1 to vowel_count_b
            if exception == word:
                global vowel_count_b
                vowel_count_b += 1

        def subtract_one_exception(exception):
            # takes a whole word as an argument
            # if the word is present, add 1 to vowel_count_b
            if exception == word:
                global vowel_count_b
                vowel_count_b -= 1

        def add_two_exception(exception):
            # takes a whole word as an argument
            # if the word is present, add 2 to vowel_count_b
            if exception == word:
                global vowel_count_b
                vowel_count_b += 2

        # # HELPER DEFINITIONS STOP
        # BIG START
        for word in some_list:
            length = len(word)

            # ADDITIONAL HELPER FUNCTION START
            def e_before_suffix(suffix):
                # takes a suffix as an argument
                # if the suffix is before morpheme final e, subtracts 1 from the vowel_count_b
                global vowel_count_b
                suffix_length = len(suffix)
                suffix_beginning = (length - suffix_length)
                if word[suffix_beginning - 2:suffix_beginning] == "ee" and word[suffix_beginning:length] == suffix:
                    vowel_count_b += 1
                if word[suffix_beginning - 2:suffix_beginning] == "ie" and word[suffix_beginning:length] == suffix:
                    vowel_count_b += 1
                if word[suffix_beginning - 2:suffix_beginning] == "ye" and word[suffix_beginning:length] == suffix:
                    vowel_count_b += 1
                if word[suffix_beginning - 3:suffix_beginning] == "aye" and word[suffix_beginning:length] == suffix:
                    vowel_count_b -= 1
                if word[suffix_beginning - 3:suffix_beginning] == "oye" and word[suffix_beginning:length] == suffix:
                    vowel_count_b -= 1
                if word[suffix_beginning - 2:suffix_beginning] == "oe" and word[suffix_beginning:length] == suffix:
                    vowel_count_b += 1
                if word[suffix_beginning - 2:suffix_beginning] == "ue" and word[suffix_beginning:length] == suffix:
                    vowel_count_b += 1
                if word[suffix_beginning:length] == suffix and word[suffix_beginning - 1] == "e" and word[
                                                                                                     suffix_beginning - 3:suffix_beginning] != "ire":
                    vowel_count_b -= 1

            def syllabic_en_before_suffix(suffix):
                # takes a suffix as an argument
                # if the suffix is before morpheme final e, subtracts 1 from the vowel_count_a
                global vowel_count_b
                suffix_length = len(suffix)
                suffix_beginning = (length - suffix_length)
                if word[suffix_beginning - 3:suffix_beginning] == "ten" and word[suffix_beginning:length] == suffix:
                    vowel_count_b -= 1
                if word[suffix_beginning - 3:suffix_beginning] == "den" and word[suffix_beginning:length] == suffix:
                    vowel_count_b -= 1
                if word[suffix_beginning - 3:suffix_beginning] == "ven" and word[suffix_beginning:length] == suffix:
                    vowel_count_b -= 1

            # ADDITIONAL HELPER FUNCTION STOP
            for letter in word:  # this iterates through each word
                if letter == "e":
                    vowel_count_b += 1
                elif letter == "a":
                    vowel_count_b += 1
                elif letter == "u":
                    vowel_count_b += 1
                elif letter == "i":
                    vowel_count_b += 1
                elif letter == "y" and not word.startswith("y"):
                    vowel_count_b += 1
                elif letter == "o":
                    vowel_count_b += 1
            # the below deals with two letter and three letter symbols for vowels
            one("ee")
            if word[length - 2:length] == "ee" or word[length - 3:length] == "ees" or word[length - 3:length] == "eed":
                vowel_count_b += 1
            one("ea")
            one("ie")
            if word[length - 2:length] == "ie" or word[length - 3:length] == "ies" or word[length - 3:length] == "ied":
                vowel_count_b += 1
            one("ei")
            one("ey")
            one("ai")
            one("oo")
            if "ou" in word and "eou" not in word and "iou" not in word:
                vowel_count_b -= 1
            if "eo" in word and "eou" not in word:
                vowel_count_b -= 1
            if "io" in word and "iou" not in word:
                vowel_count_b -= 1
            two("eou")
            two("iou")
            # unfortunate case of -ye start...
            if "ay" in word and "aye" not in word:
                vowel_count_b -= 1
            if "oy" in word and "oye" not in word:
                vowel_count_b -= 1
            if "ye" in word and "aye" not in word and "oye" not in word and word[length - length:(
                                                                                                         length - length) + 2] != "ye":
                vowel_count_b -= 1
            if word[length - 2:length] == "ye" or word[length - 3:length] == "yes" or word[length - 3:length] == "yed":
                vowel_count_b += 1
            if word[length - 3:length] == "aye" or word[length - 3:length] == "oye" or word[
                                                                                       length - 4:length] == "ayes" or word[
                                                                                                                       length - 4:length] == "oyes" or word[
                                                                                                                                                       length - 4:length] == "ayed" or word[
                                                                                                                                                                                       length - 4:length] == "oyed":
                vowel_count_b -= 1
            one("aye")
            one("oye")
            # unfortunate case of -ye end...
            one("oe")
            if word[length - 2:length] == "oe" or word[length - 3:length] == "oes" or word[length - 3:length] == "oed":
                vowel_count_b += 1
            one("au")
            one("oa")
            one("ue")
            if word[length - 2:length] == "ue" or word[length - 3:length] == "ues" or word[length - 3:length] == "ued":
                vowel_count_b += 1
            one("ui")
            one("ua")
            one("oi")
            one("ia")
            one("eu")
            one("aa")
            # the below deals with the e in the word-final position - in a general way
            if word[length - 1] == "e" and word[length - 3:length] != "ire":
                vowel_count_b -= 1  # deals with final mute e in singular
            if word[length - 2:length] == "es" and word[length - 4:length] != "ires" and word[
                                                                                         length - 3:length] != "ges" and word[
                                                                                                                         length - 3:length] != "ces" and word[
                                                                                                                                                         length - 3:length] != "ses" and word[
                                                                                                                                                                                         length - 3:length] != "zes" and word[
                                                                                                                                                                                                                         length - 4:length] != "ches" and word[
                                                                                                                                                                                                                                                          length - 4:length] != "shes" and word[
                                                                                                                                                                                                                                                                                           length - 4:length] != "sses" and word[
                                                                                                                                                                                                                                                                                                                            length - 3:length] != "xes":
                vowel_count_b -= 1  # deals with final mute e in plural
            # the below deals with simple past and past participle forms
            if word[length - 2:length] == "ed":
                if word[length - 3] in consonants and length == 3:
                    vowel_count_b += 1
                if word[length - 3] in consonants and word[length - 4] in consonants and length == 4:
                    vowel_count_b += 1
                if word[length - 3] in consonants and word[length - 4] in consonants and word[
                    length - 5] in consonants and length == 5:
                    vowel_count_b += 1
            if word[length - 2:length] == "ed" and word[length - 3:length] != "ted" and word[
                                                                                        length - 3:length] != "ded":
                vowel_count_b -= 1
            # the below deals with syllabic n in "en" endings
            if word.endswith("en") and length > 3:
                if word[length - 3] == "t" or word[length - 3] == "d" or word[length - 3] == "v":
                    vowel_count_b -= 1
            # the below deals with syllabic n in "tton" endings
            if word.endswith("tton") and length > 4:
                vowel_count_b -= 1
            # implementing morpheme final e rules for compounds with "e"
            if "-" in word:
                hyphen_index = 0
                for letter in word:
                    if letter == "-":
                        hyphen_index += 1
                        break
                    else:
                        hyphen_index += 1
                if word[hyphen_index - 2:hyphen_index] == "e-" and word[hyphen_index - 4:hyphen_index] != "ire-":
                    vowel_count_b -= 1  # deals with final mute e when a) it is in singular, b) it is in a compound with - as the first word
                if word[hyphen_index - 3:hyphen_index] == "es-" and word[
                                                                    hyphen_index - 5:hyphen_index] != "ires-" and word[
                                                                                                                  hyphen_index - 4:hyphen_index] != "ges-" and word[
                                                                                                                                                               hyphen_index - 4:hyphen_index] != "ces-" and word[
                                                                                                                                                                                                            hyphen_index - 4:hyphen_index] != "ses-" and word[
                                                                                                                                                                                                                                                         hyphen_index - 4:hyphen_index] != "zes-" and word[
                                                                                                                                                                                                                                                                                                      hyphen_index - 5:hyphen_index] != "ches-" and word[
                                                                                                                                                                                                                                                                                                                                                    hyphen_index - 5:hyphen_index] != "shes-" and word[
                                                                                                                                                                                                                                                                                                                                                                                                  hyphen_index - 5:hyphen_index] != "sses-" and word[
                                                                                                                                                                                                                                                                                                                                                                                                                                                hyphen_index - 4:hyphen_index] != "xes-":
                    vowel_count_b -= 1  # deals with final mute e when a) it is in plural, b) it is in a compound with - as the first word
                if word[hyphen_index - 3:hyphen_index] == "ee-" or word[
                                                                   hyphen_index - 4:hyphen_index] == "ees-" or word[
                                                                                                               hyphen_index - 4:hyphen_index] == "eed-":
                    vowel_count_b += 1
                if word[hyphen_index - 3:hyphen_index] == "ie-" or word[
                                                                   hyphen_index - 4:hyphen_index] == "ies-" or word[
                                                                                                               hyphen_index - 4:hyphen_index] == "ied-":
                    vowel_count_b += 1
                # unfortunate case of -ye... start
                if word[hyphen_index - 3:hyphen_index] == "ye-" or word[
                                                                   hyphen_index - 4:hyphen_index] == "yes-" or word[
                                                                                                               hyphen_index - 4:hyphen_index] == "yed-":
                    vowel_count_b += 1
                if word[hyphen_index - 4:hyphen_index] == "aye-" or word[
                                                                    hyphen_index - 4:hyphen_index] == "oye-" or word[
                                                                                                                hyphen_index - 5:hyphen_index] == "ayes-" or word[
                                                                                                                                                             hyphen_index - 5:hyphen_index] == "oyes-" or word[
                                                                                                                                                                                                          hyphen_index - 5:hyphen_index] == "ayed-" or word[
                                                                                                                                                                                                                                                       hyphen_index - 5:hyphen_index] == "oyed-":
                    vowel_count_b -= 1
                # unfortunate case of -ye... end
                if word[hyphen_index - 3:hyphen_index] == "oe-" or word[
                                                                   hyphen_index - 4:hyphen_index] == "oes-" or word[
                                                                                                               hyphen_index - 4:hyphen_index] == "oed-":
                    vowel_count_b += 1
                if word[hyphen_index - 3:hyphen_index] == "ue-" or word[
                                                                   hyphen_index - 4:hyphen_index] == "ues-" or word[
                                                                                                               hyphen_index - 4:hyphen_index] == "ued-":
                    vowel_count_b += 1
                # # the below deals with simple past and past participle forms before -
                if word[hyphen_index - 3:hyphen_index] == "ed-" and word[
                                                                    hyphen_index - 4:hyphen_index] != "ted-" and word[
                                                                                                                 hyphen_index - 4:hyphen_index] != "ded-":
                    vowel_count_b -= 1
                pre_hyphen_length = len(word[:hyphen_index - 1])
                if word[
                   hyphen_index - 2:hyphen_index] == "e-" and pre_hyphen_length == 1:  # deals with compounds such as e-book
                    vowel_count_b += 1
                if word[hyphen_index - 3:hyphen_index] == "re-" and pre_hyphen_length == 2:
                    vowel_count_b += 1
                if word[hyphen_index - 4:hyphen_index] == "pre-" and pre_hyphen_length == 3:
                    vowel_count_b += 1
            # removing morpheme-final e before derivational suffixes (but not in compounds with -)
            if "less" in word:
                e_before_suffix("less")
            if "dom" in word:
                e_before_suffix("dom")
            if "doms" in word:
                e_before_suffix("doms")
            if "ful" in word:
                e_before_suffix("ful")
            if "fuls" in word:
                e_before_suffix("fuls")
            if "fully" in word:
                e_before_suffix("fully")
            if "hood" in word:
                e_before_suffix("hood")
            if "hoods" in word:
                e_before_suffix("hoods")
            if "ment" in word:
                e_before_suffix("ment")
            if "ments" in word:
                e_before_suffix("ments")
            if "ness" in word:
                e_before_suffix("ness")
            if "nesses" in word:
                e_before_suffix("nesses")
            if "ship" in word:
                e_before_suffix("ship")
            if "ships" in word:
                e_before_suffix("ships")
            if "ly" in word:
                e_before_suffix("ly")
            if "free" in word:
                e_before_suffix("free")

            # dealing with syllabic "en" before  derivational suffixes (but not in compounds with -)
            if "less" in word:
                syllabic_en_before_suffix("less")
            if "dom" in word:
                syllabic_en_before_suffix("dom")
            if "doms" in word:
                syllabic_en_before_suffix("doms")
            if "ful" in word:
                syllabic_en_before_suffix("ful")
            if "fuls" in word:
                syllabic_en_before_suffix("fuls")
            if "fully" in word:
                syllabic_en_before_suffix("fully")
            if "hood" in word:
                syllabic_en_before_suffix("hood")
            if "hoods" in word:
                syllabic_en_before_suffix("hoods")
            if "ment" in word:
                syllabic_en_before_suffix("ment")
            if "ments" in word:
                syllabic_en_before_suffix("ments")
            if "ness" in word:
                syllabic_en_before_suffix("ness")
            if "nesses" in word:
                syllabic_en_before_suffix("nesses")
            if "ship" in word:
                syllabic_en_before_suffix("ship")
            if "ships" in word:
                syllabic_en_before_suffix("ships")
            if "ly" in word:
                syllabic_en_before_suffix("ly")
            if "free" in word:
                syllabic_en_before_suffix("free")

            # lexical exceptions
            add_one_exception("lion")
            if word[length - 1:length] == "e":
                if word[length - 2] in consonants and length == 2:
                    vowel_count_b += 1
                if word[length - 2] in consonants and word[length - 3] in consonants and length == 3:
                    vowel_count_b += 1
                if word[length - 2] in consonants and word[length - 3] in consonants and word[
                    length - 4] in consonants and length == 4:
                    vowel_count_b += 1
            add_two_exception("mediocre")
            subtract_one_exception("business")
            add_one_exception("free")
        return vowel_count_b


    phoneme_count_b = count_consonants_b(user_text) + count_vowels_b(user_text)

    data = {
        'result': phoneme_count_b,
    }
    return JsonResponse(data)






@csrf_exempt
def count_syllables(request):
    user_text = request.POST.dict()
    user_text = user_text['user_text']
    some_list = user_string_to_list(user_text)
    global syllable_count
    syllable_count = 0
    # HELPER DEFINITIONS START
    def one(bit):
        # takes a part of word as an argument
        # if the part of word in the word, then subtract 1 from syllable_count
        if bit in word:
            global syllable_count
            bit_iteration = re.findall(bit, word)
            bit_count = len(bit_iteration)
            if bit_count == 1:
                syllable_count -= 1
            if bit_count == 2:
                syllable_count -= 2
            if bit_count == 3:
                syllable_count -= 3
    def two(bit):
        # takes a part of word as an argument
        # if the part of word in the word, then subtract 2 from syllable_count
        if bit in word:
            global syllable_count
            syllable_count -= 2
    def add_one_exception(exception):
        # takes a whole word as an argument
        # if the word is present, add 1 to syllable_count
        if exception == word:
            global syllable_count
            syllable_count += 1
    def subtract_one_exception(exception):
        # takes a whole word as an argument
        # if the word is present, add 1 to syllable_count
        if exception == word:
            global syllable_count
            syllable_count -= 1
    def add_two_exception(exception):
        # takes a whole word as an argument
        # if the word is present, add 2 to syllable_count
        if exception == word:
            global syllable_count
            syllable_count += 2
    # # HELPER DEFINITIONS STOP

    # BIG START
    for word in some_list:
        length = len(word)

        # ADDITIONAL HELPER FUNCTION START
        def e_before_suffix(suffix):
        # takes a suffix as an argument
        # if the suffix is before morpheme final e, subtracts 1 from the syllable_count
            global syllable_count
            suffix_length = len(suffix)
            suffix_beginning = (length - suffix_length)
            if word[suffix_beginning-2:suffix_beginning] == "ee" and word[suffix_beginning:length] == suffix:
                syllable_count += 1
            if word[suffix_beginning - 2:suffix_beginning] == "ie" and word[suffix_beginning:length] == suffix:
                syllable_count += 1
            if word[suffix_beginning - 2:suffix_beginning] == "ye" and word[suffix_beginning:length] == suffix:
                syllable_count += 1
            if word[suffix_beginning - 3:suffix_beginning] == "aye" and word[suffix_beginning:length] == suffix:
                syllable_count -= 1
            if word[suffix_beginning-3:suffix_beginning] == "oye" and word[suffix_beginning:length] == suffix:
                syllable_count -= 1
            if word[suffix_beginning - 2:suffix_beginning] == "oe" and word[suffix_beginning:length] == suffix:
                syllable_count += 1
            if word[suffix_beginning - 2:suffix_beginning] == "ue" and word[suffix_beginning:length] == suffix:
                syllable_count += 1
            if word[suffix_beginning:length] == suffix and word[suffix_beginning-1] == "e" and word[suffix_beginning-3:suffix_beginning] != "tle" and word[suffix_beginning-3:suffix_beginning] != "ple" and word[suffix_beginning-3:suffix_beginning] != "ble" and word[suffix_beginning-3:suffix_beginning] != "gle" and word[suffix_beginning-3:suffix_beginning] != "ire":
                syllable_count -= 1
        # ADDITIONAL HELPER FUNCTION STOP

        for letter in word: # this iterates through each word
            if letter == "e":
                syllable_count += 1
            elif letter == "a":
                syllable_count += 1
            elif letter == "u":
                syllable_count += 1
            elif letter == "i":
                syllable_count += 1
            elif letter == "y" and not word.startswith("y"):
                syllable_count += 1
            elif letter == "o":
                syllable_count += 1
        # the below deals with two letter and three letter symbols for vowels
        one("ee")
        if word[length - 2:length] == "ee" or word[length - 3:length] == "ees" or word[length-3:length] == "eed":
            syllable_count += 1
        one("ea")
        one("ie")
        if word[length-2:length] == "ie" or word[length-3:length] == "ies" or word[length-3:length] == "ied":
            syllable_count += 1
        one("ei")
        one("ey")
        one("ai")
        one("oo")
        if "ou" in word and "eou" not in word and "iou" not in word:
            syllable_count -= 1
        if "eo" in word and "eou" not in word:
            syllable_count -= 1
        if "io" in word and "iou" not in word:
            syllable_count -= 1
        two("eou")
        two("iou")
        # unfortunate case of -ye start...
        if "ay" in word and "aye" not in word:
            syllable_count -= 1
        if "oy" in word and "oye" not in word:
            syllable_count -= 1
        if "ye" in word and "aye" not in word and "oye" not in word and word[length-length:(length-length)+2] != "ye":
            syllable_count -= 1
        if word[length-2:length] == "ye" or word[length-3:length] == "yes" or word[length-3:length] == "yed":
            syllable_count += 1
        if word[length-3:length] == "aye" or word[length-3:length] == "oye" or word[length-4:length] == "ayes" or word[length-4:length] == "oyes" or word[length-4:length] == "ayed" or word[length-4:length] == "oyed":
            syllable_count -= 1
        one("aye")
        one("oye")
        # unfortunate case of -ye end...
        one("oe")
        if word[length-2:length] == "oe" or word[length-3:length] == "oes" or word[length-3:length] == "oed":
            syllable_count += 1
        one("au")
        one("oa")
        one("ue")
        if word[length - 2:length] == "ue" or word[length - 3:length] == "ues" or word[length-3:length] == "ued":
            syllable_count += 1
        one("ui")
        one("ua")
        one("oi")
        one("ia")
        one("eu")
        one("aa")
        # the below deals with the e in the word-final position - in a general way
        if word[length-1] == "e" and word[length-3:length] != "tle" and word[length-3:length] != "ple" and word[length-3:length] != "ble" and word[length-3:length] != "gle" and word[length-3:length] != "ire":
            syllable_count -= 1 # deals with final mute e in singular
        if word[length - 2:length] == "es" and word[length - 4:length] != "tles" and word[length - 4:length] != "ples" and word[length-4:length] != "bles" and word[length-4:length] != "gles" and word[length-4:length] != "ires" and word[length-3:length] != "ges" and word[length-3:length] != "ces" and word[length-3:length] != "ses" and word[length-3:length] != "zes" and word[length-4:length] != "ches" and word[length-4:length] != "shes" and word[length-4:length] != "sses" and word[length-3:length] != "xes":
            syllable_count -= 1  # deals with final mute e in plural
        # the below deals with simple past and past participle forms
        if word[length - 2:length] == "ed":
            if word[length-3] in consonants and length == 3:
                syllable_count += 1
            if word[length-3] in consonants and word[length-4] in consonants and length == 4:
                syllable_count += 1
            if word[length-3] in consonants and word[length-4] in consonants and word[length-5] in consonants and length == 5:
                syllable_count += 1
        if word[length - 2:length] == "ed" and word[length - 3:length] != "ted" and word[length - 3:length] != "ded":
            syllable_count -= 1
        # implementing morpheme final e rules for compounds with "e"
        if "-" in word:
            hyphen_index = 0
            for letter in word:
                if letter == "-":
                    hyphen_index += 1
                    break
                else:
                    hyphen_index += 1
            if word[hyphen_index - 2:hyphen_index] == "e-" and word[hyphen_index - 4:hyphen_index] != "tle-" and word[hyphen_index - 4:hyphen_index] != "ple-" and word[hyphen_index-4:hyphen_index] != "ble-" and word[hyphen_index-4:hyphen_index] != "gle-" and word[hyphen_index-4:hyphen_index] != "ire-":
                syllable_count -= 1  # deals with final mute e when a) it is in singular, b) it is in a compound with - as the first word
            if word[hyphen_index - 3:hyphen_index] == "es-" and word[hyphen_index - 5:hyphen_index] != "tles-" and word[hyphen_index - 5:hyphen_index] != "ples-" and word[hyphen_index-5:hyphen_index] != "bles-" and word[hyphen_index-5:hyphen_index] != "gles-" and word[hyphen_index-5:hyphen_index] != "ires-" and word[hyphen_index - 4:hyphen_index] != "ges-" and word[hyphen_index - 4:hyphen_index] != "ces-" and word[hyphen_index - 4:hyphen_index] != "ses-" and word[hyphen_index - 4:hyphen_index] != "zes-" and word[hyphen_index - 5:hyphen_index] != "ches-" and word[hyphen_index - 5:hyphen_index] != "shes-" and word[hyphen_index - 5:hyphen_index] != "sses-" and word[hyphen_index - 4:hyphen_index] != "xes-":
                syllable_count -= 1  # deals with final mute e when a) it is in plural, b) it is in a compound with - as the first word
            if word[hyphen_index-3:hyphen_index] == "ee-" or word[hyphen_index-4:hyphen_index] == "ees-" or word[hyphen_index-4:hyphen_index] == "eed-":
                syllable_count += 1
            if word[hyphen_index-3:hyphen_index] == "ie-" or word[hyphen_index-4:hyphen_index] == "ies-" or word[hyphen_index-4:hyphen_index] == "ied-":
                syllable_count += 1
            # unfortunate case of -ye... start
            if word[hyphen_index-3:hyphen_index] == "ye-" or word[hyphen_index-4:hyphen_index] == "yes-" or word[hyphen_index-4:hyphen_index] == "yed-":
                syllable_count += 1
            if word[hyphen_index-4:hyphen_index] == "aye-" or word[hyphen_index-4:hyphen_index] == "oye-" or word[hyphen_index-5:hyphen_index] == "ayes-" or word[hyphen_index-5:hyphen_index] == "oyes-" or word[hyphen_index-5:hyphen_index] == "ayed-" or word[hyphen_index-5:hyphen_index] == "oyed-":
                syllable_count -= 1
            # unfortunate case of -ye... end
            if word[hyphen_index-3:hyphen_index] == "oe-" or word[hyphen_index-4:hyphen_index] == "oes-" or word[hyphen_index-4:hyphen_index] == "oed-":
                syllable_count += 1
            if word[hyphen_index-3:hyphen_index] == "ue-" or word[hyphen_index-4:hyphen_index] == "ues-" or word[hyphen_index-4:hyphen_index] == "ued-":
                syllable_count += 1
            # # the below deals with simple past and past participle forms before -
            if word[hyphen_index-3:hyphen_index] == "ed-" and word[hyphen_index-4:hyphen_index] != "ted-" and word[hyphen_index-4:hyphen_index] != "ded-":
                syllable_count -= 1
            pre_hyphen_length = len(word[:hyphen_index-1])
            if word[hyphen_index - 2:hyphen_index] == "e-" and pre_hyphen_length == 1: # deals with compounds such as e-book
                syllable_count += 1
            if word[hyphen_index-3:hyphen_index] == "re-" and pre_hyphen_length == 2:
                syllable_count += 1
            if word[hyphen_index - 4:hyphen_index] == "pre-" and pre_hyphen_length == 3:
                syllable_count += 1
        # removing morpheme-final e before derivational suffixes (but not in compounds with -)
        if "less" in word:
            e_before_suffix("less")
        if "dom" in word:
            e_before_suffix("dom")
        if "doms" in word:
            e_before_suffix("doms")
        if "ful" in word:
            e_before_suffix("ful")
        if "fuls" in word:
            e_before_suffix("fuls")
        if "fully" in word:
            e_before_suffix("fully")
        if "hood" in word:
            e_before_suffix("hood")
        if "hoods" in word:
            e_before_suffix("hoods")
        if "ment" in word:
            e_before_suffix("ment")
        if "ments" in word:
            e_before_suffix("ments")
        if "ness" in word:
            e_before_suffix("ness")
        if "nesses" in word:
            e_before_suffix("nesses")
        if "ship" in word:
            e_before_suffix("ship")
        if "ships" in word:
            e_before_suffix("ships")
        if "ly" in word:
            e_before_suffix("ly")
        # lexical exceptions
        add_one_exception("lion")
        if word[length - 1:length] == "e":
            if word[length-2] in consonants and length == 2:
                syllable_count += 1
            if word[length-2] in consonants and word[length-3] in consonants and length == 3:
                syllable_count += 1
            if word[length-2] in consonants and word[length-3] in consonants and word[length-4] in consonants and length == 4:
                syllable_count += 1
        add_two_exception("mediocre")
        subtract_one_exception("business")
    data = {
        'result': syllable_count,
    }
    return JsonResponse(data)
