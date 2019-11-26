import spacy
from spacy import displacy

nlp = spacy.load('en_core_web_sm')
#These functions will check if a noun modifier is a licensor or not  

#The next two functions check for words to omit like "friend of ours", "his ones",etc
def not_preceded_by_of(i,sentence) :
    if i != 0 :
        if sentence[i-1].text.lower() != "of" :
            return True
        else :
            return False
    return True

def not_followed_by_one(i,sentence) :
    if i != len(sentence) - 1 :
        if sentence[i+1].text.lower() in ["one","ones"] :
            return False
        else :
            return True
    return True

#to check if a previous word is a determiner or a possesive pronoun or a personal pronoun 
def check_DT_prev(i,sentence):
    if i > 0 :
        if sentence[i-1].tag_ in ["DT","POS","PRP$"]  :
            return True
        if i > 1 :
            if sentence[i-2].tag_ in ["DT","POS","PRP$"] :
                return True

    return False


#check for punctuation
def check_for_punc(i,sentence_parse):
    if i != len(sentence_parse) - 1 :
        if sentence_parse[i+1].pos_ in ["PUNCT"] : 
            return True
    return False


#check for preposition
def check_for_prep(i,sentence_parse):
    if i != len(sentence_parse) - 1 :
        if sentence_parse[i+1].tag_ in ["IN","CC"]:
            return True
        if i != len(sentence_parse) - 2:
            if sentence_parse[i+2].tag_ in ["IN","CC"] and sentence_parse[i+1].pos_ in ["ADV"]:
                return True
    return False

#used for searching noun modifiers, if not there return True
def check_next_3_words(i,sentence):
    if i != len(sentence) - 1 :
        if sentence[i+1].tag_ in ["NNP","NN","NNS"] :
            return False
        if i != len(sentence) - 2 :
            if sentence[i+2].tag_ in ["NNP","NN","NNS"] :
                return False
            if i != len(sentence) - 3 :
                if sentence[i+3].tag_ in ["NNP","NN","NNS"] :
                    return False
    return True

#to check if the word to the left is a noun modifer
def check_prev_1_words(i,sentence):
    if i > 0 :
        if sentence[i-1].tag_ in ["NNP","NN","NNS"]  :
            return False
    return True


def find_licensor(sentence_parse):
    licensors = []
    displacy.render(sentence_parse, style="dep")
    ordinals = []
    for ent in sentence_parse.ents:
        if ent.label_ == "ORDINAL":
            ordinals.append(ent.text)
    
    for i,word in enumerate(sentence_parse) :
        #for sentences like "I don't like mine[my dog]"
        if word.text.lower() in ["mine","hers","theirs","yours","ours"] :
            if not_preceded_by_of(i,sentence_parse) == True :
                if not_followed_by_one(i,sentence_parse) == True :
                    licensors.append([word.text,i,word.pos_,word.tag_])

        #for cardinal numbers("four [chapters]"), demonstrative determiner("these [candidates]") and quantifiers("some [students]")
        elif word.tag_ in ["DT", "CD", "POS", "RBR"] :
            if check_for_punc(i,sentence_parse) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])
            elif check_for_prep(i,sentence_parse) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])
            elif check_next_3_words(i,sentence_parse) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])

        #for ordinal numbers, like "second [position]"
        elif word.text in ordinals:
            if check_for_punc(i,sentence_parse) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])
            elif check_for_prep(i,sentence_parse) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])
            elif check_next_3_words(i,sentence_parse) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])

        #for interrogative determiners like "which [pages]"
        elif word.tag_ in ["WDT"] :
            if check_for_punc(i,sentence_parse) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])
            elif check_for_prep(i,sentence_parse) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])
            elif check_prev_1_words(i,sentence_parse) == True and check_next_3_words(i,sentence_parse) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])

        #for pronoun possesives like "I am reading my book and he is reading his[book]."
        elif word.text.lower() in ["these","those","his"] :
            if check_for_punc(i,sentence_parse) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])
            elif check_next_3_words(i,sentence_parse) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])

        #for superlative adjectives like "the weirdest [guy]"
        elif word.tag_ in ["JJ",'JJR','JJS'] :
            if check_DT_prev(i,sentence_parse) == True:
                if check_next_3_words(i,sentence_parse) == True:
                    licensors.append([word.text,i,word.pos_,word.tag_])

        #for one-anaphora
        

    return licensors    


def find_antecedent(licensor, sentence_parse):
    #search based on POS tag
    tag_to_search = licensor[2]
    antecedents = []
    for i,word in enumerate(sentence_parse):
        if word.text.lower() != licensor[0].lower():
            if word.pos_ == tag_to_search:
                antecedents.append([sentence_parse[i+1].text,i+1,sentence_parse[i+1].pos_,sentence_parse[i+1].tag_])

    return antecedents


if __name__ == '__main__':

    f = open("data.txt","r")
    contents = f.readlines()
    
    for content in contents:
        print(content)
        sentence_parse = nlp(content)
        licensors = find_licensor(sentence_parse)
        for licensor in licensors:
            antecedent = find_antecedent(licensor,sentence_parse)
            print("Licensor:",licensor)
            print("Antecedent:",antecedent)

    f.close()
