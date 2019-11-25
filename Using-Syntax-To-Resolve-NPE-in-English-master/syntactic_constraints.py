def not_preceded_by_of(i,sentence) :
    if i != 0 :
        if sentence[i-1].text.lower() != "of" :
            return True
        else :
            return False
    return True

def check_DT_prev(i,sentence):
    if i > 0 :
        if sentence[i-1].tag_ in ["DT","POS","PRP$"]  :
            return True
        if i > 1 :
            if sentence[i-2].tag_ in ["DT","POS","PRP$"] :
                return True

    return False

def not_followed_by_one(i,sentence) :
    if i != len(sentence) - 1 :
        if sentence[i+1].text.lower() in ["one","ones"] :
            return False
        else :
            return True
    return True

def check_for_punct(i,sentence):
    if i != len(sentence) - 1 :
        if sentence[i+1].pos_ in ["PUNCT"] : 
            return True
    return False   

def check_for_prep(i,sentence):
    if i != len(sentence) - 1 :
        if sentence[i+1].tag_ in ["IN","CC"] :
            return True
        if i != len(sentence) - 2 :
            if sentence[i+2].tag_ in ["IN","CC"] and sentence[i+1].pos_ in ["ADV"] :
                return True
    return False

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

def check_prev_1_words(i,sentence):
    if i > 0 :
        if sentence[i-1].tag_ in ["NNP","NN","NNS"]  :
            return False
    return True
