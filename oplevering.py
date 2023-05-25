#
# oplevering.py
#
# Opdracht: Tekstidentificatie
#
# Naam: Antonio Mazzara
#
from collections import Counter

#import van stemming-bibliotheek Snowball
from nltk.stem.snowball import SnowballStemmer

#import van math om de log te gebruiken in de functie compare_dictionaries
import math



class TextModel:
    """A class supporting complex models of text."""

    def __init__(self):
        """Create an empty TextModel."""
        #
        # Maak dictionary's voor elke eigenschap
        #
        self.words = {}             # Om woorden te tellen
        self.word_lengths = {}      # Om woordlengtes te tellen
        self.stems = {}             # Om stammen te tellen
        self.sentence_lengths = {}  # Om zinslengtes te tellen
        #
        # Mijn eigen dictionary
        #
        self.my_feature = {}        # Om de leestekens te tellen

    def __repr__(self):
        """Display the contents of a TextModel."""
        s = 'Woorden:\n' + str(self.words) + '\n\n'
        s += 'Woordlengtes:\n' + str(self.word_lengths) + '\n\n'
        s += 'Stammen:\n' + str(self.stems) + '\n\n'
        s += 'Zinslengtes:\n' + str(self.sentence_lengths) + '\n\n'
        s += 'MIJN EIGENSCHAP (Leestekens):\n' + str(self.my_feature)
        return s



    def read_text_from_file(self, filename):
        
        with open(filename, encoding='utf-8') as f:
            self.text = f.read()

    def make_sentence_lengths(self):
        """
        De methode make_sentence_lengths(self) moet de tekst in self.text 
        gebruiken om de dictionary self.sentence_lengths te vullen.
        """
        
        LoW = self.text.split()
        self.sentence_lengths = {}
        sentence_counter = 0
        for w in LoW:
            sentence_counter +=1
            if w[-1] in '.?!':
                if sentence_counter not in self.sentence_lengths:
                    self.sentence_lengths[sentence_counter] = 1
                else:
                    self.sentence_lengths[sentence_counter] += 1
                sentence_counter = 0
        return self.sentence_lengths
        
        
    
    
    def clean_string(self, s):
        """
        De methode clean_string(self, s) krijgt een string s mee en geeft
        een opgeschoonde versie ervan terug zonder leestekens en zonder 
        hoofdletters.
        """
        new_string = ''
        for i in range(len(s)):
            if s[i] not in '.,?!':
                new_string+=s[i].lower()
        return new_string
        


    def make_word_lenghts(self):
        """
        Hier wordt een dictionary gemaakt van de woordlengtes
        van de opgeschoonde string.
        """
        clean_s = self.clean_string(self.text)
        Low = clean_s.split() 
        c = Counter(map(len, Low))
        self.word_lengths = dict(c)
        return self.word_lengths
        
    
    
    def make_words(self):
        """
        Hier wordt een dictionary van de opgeschoonde worden gemaakt.
        """
        clean_s = self.clean_string(self.text)
        LoW = clean_s.split()
        c = Counter(LoW)
        self.words = dict(c)
        return self.words
    

    def create_stem(self, w):
        dutchStemmer=SnowballStemmer("dutch", ignore_stopwords=True)
        clean_stem = self.clean_string(w)
        final_stem = dutchStemmer.stem(clean_stem)
        return final_stem

    
    def make_stems(self):
        """
        Wordt een dictionary gemaakt van de stammen van de opgeschoonde worden.
        """
        clean_s = self.clean_string(self.text)
        LoW = clean_s.split()
        c = Counter()      
        for word in LoW:
            c[self.create_stem(word)] +=1
        
        self.stems = dict(c)
                   
        return self.stems



    
    def make_punctuation(self):
        """
        Hier wordt een dictionary met leestekens gemaakt.
        """
        punctuation_dict = {}
        punc = ['.', '?', '!', "'", ',']

        for char in self.text:
            if char in punc:
                if char in punctuation_dict:
                    punctuation_dict[char] += 1
                else:
                    punctuation_dict[char] = 1
        self.my_feature = punctuation_dict
        return self.my_feature


    def normalize_dictionary(self, d):
        """
        De methode krijgt een van de dictionary's uit het model mee en geeft
        een genormaliseerde versie terug (een versie waar de som van alle waardes
        exact 1.0 is).
        """
        total = sum(d.values())
        for key in d:
          d[key] = d[key]/total
        return d


    def smallest_value(self, nd1, nd2):
        """
        De methode krijgt twee dictionary's (nd1 en nd2) mee uit het model en
        geeft de kleinste positieve waarde terug die in de dictionary's
        samen voorkomt.        
        """
        
        all_values = [value for value in nd1.values()] + [value for value in nd2.values()]
    
        all_positive_values = [value for value in all_values if value > 0]
    
        return min(all_positive_values)


    
        
        
    def compare_dictionaries(self, d, nd1, nd2):
        """
        De methode berekent de kans dat de dictionary d voorkomt uit de verdeling
        van de gegevens in de genormaliseerde dictionary nd1, en dezelfde kans
        voor nd2.
        """
        nd1 = self.normalize_dictionary(nd1)
        nd2 = self.normalize_dictionary(nd2)
        epsilon = self.smallest_value(nd1, nd2) / 2
        log1 = 0.0
        log2 = 0.0
        for key in d:
            if key in nd1:
                log1 += d[key] * math.log2(nd1[key])
            else:
                log1 += d[key] * math.log2(epsilon)
            if key in nd2:
                log2 += d[key] * math.log2(nd2[key])
            else:
                log2 += d[key] * math.log2(epsilon)
        return [log1, log2]


    def create_all_dictionaries(self):
        """Create out all five of self's
           dictionaries in full.
        """
        self.make_sentence_lengths()
        self.make_word_lenghts()
        self.make_words()
        self.make_stems()
        self.make_punctuation()



    def compare_text_with_two_models(self, model1, model2):
        """
        Vergelijk TextModel self met TextModels model1 en model2
        op basis van de vijf dictionaries.
        """
        properties = ['words', 'word_lengths', 'stems', 'sentence_lengths', 'my_feature']
        model1_results = []
        model2_results = []
        for prop in properties:
            model1_results.append(self.compare_dictionaries(getattr(self, prop), getattr(model1, prop), getattr(model2, prop)))
            model2_results.append(self.compare_dictionaries(getattr(self, prop), getattr(model2, prop), getattr(model1, prop)))

        print("-----------------------------------------------------------------------------------------------------------------")
        print("\n")
        print("           Vergelijkingsresultaten van tm_unknown met het getrainde_model1 en het getrainde_model2: \n")
        print("\n")
        print("-----------------------------------------------------------------------------------------------------------------")
        
        print(f"Resultaten voor model 1  vs  model 2 ( words,  word_lengths,  stems,  sentence_lengths,  my_feature(leestekens) ): \n\n")
        print(f"{model1_results}")
        print("\n"*3)
        
        print("Som van de log-waarschijnlijkheden")
        print("----------------------------------")
        totals = [sum(i) for i in zip(*model1_results)]
        print(totals)
        print("\n")


        if totals[0] > totals[1]:
            print('Model 1 is de betere match!')
        elif totals[0] < totals[1]:
            print('Model 2 is de betere match!')
        else:
            print('Het is een gelijkspel!')
        

   
    
    

tm = TextModel()
print('\n\n +++++++++++++++++++++++++++++++++++ Model 1 +++++++++++++++++++++++++++++++++++++\n ')
model1 = TextModel()
model1.read_text_from_file('Hamlet - shakespeare.txt')
model1.create_all_dictionaries()
print(model1)

print('\n\n +++++++++++++++++++++++++++++++++++ Model 2 +++++++++++++++++++++++++++++++++++++\n ')
model2 = TextModel()
model2.read_text_from_file('Oliver twist - dickens.txt')
model2.create_all_dictionaries()  
print(model2)


print('\n\n +++++++++++++++++++++++++++++++++++ Onbekende teks +++++++++++++++++++++++++++++++++++++\n ')
tm_unknown = TextModel()
tm_unknown.read_text_from_file('romeo and juliet -shakespeare.txt')
tm_unknown.create_all_dictionaries()  
print(tm_unknown)


print('\n\n +++++++++++++++++++++++++++++++++++ Vergelijkingsresultaten: +++++++++++++++++++++++++++++++++++++\n ')
tm_unknown.compare_text_with_two_models(model1,model2)


