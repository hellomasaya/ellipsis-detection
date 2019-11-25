import spacy
#import pickle
from spacy import displacy
# import xlwt
# from xlwt import Workbook
debug = False
nlp = spacy.load('en')

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

def find_antecedent(licensor, sentence):
	#licensor is a list : [word, position_in_the_sentence, Tag pos_, Tag tag_]

	sentence = nlp(sentence)
	tag_to_search = licensor[2] #search based on pos_ tag
	# tag_to_search = licensor[3] #search based on tag_ tag

	antecedents = []
	for i,word in enumerate(sentence):
		if word.text.lower() != licensor[0].lower():

			#search based on pos_
			if word.pos_ == tag_to_search :
				antecedents.append([sentence[i+1].text,i+1,sentence[i+1].pos_,sentence[i+1].tag_])

			#search based on tag_
			# if word.tag_ == licensor[3] :
			# 	antecedents.append([word.text,i,word.pos_,word.tag_])

	return antecedents
			


def find_licensors(sentence):

    licensors = []
    sentence = nlp(sentence)
    potential_licensors = []
    displacy.render(sentence, style="dep")
    ordinals = []
    for ent in sentence.ents:
        if ent.label_ == "ORDINAL":
            #print(ent)
            #print("-----------")
            ordinals.append(ent.text)

    #for i,word in enumerate(sentence) :
        #print(word.text)
        #print(word.pos_)
        #print(word.tag_)
        #print(word.dep_)
        #print()
    debug_word_tags = []
    debug_noun_chunks = []
    
    for i,word in enumerate(sentence) :

        debug_word_tags.append((word,word.tag_))

        if word.text.lower() in ["mine","hers","theirs","yours","ours"] :
            if not_preceded_by_of(i,sentence) == True :
                if not_followed_by_one(i,sentence) == True :
                    licensors.append([word.text,i,word.pos_,word.tag_])

        elif word.tag_ in ["DT", "CD", "POS", "RBR"] :
            if check_for_punct(i,sentence) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])
            elif check_for_prep(i,sentence) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])
            elif check_next_3_words(i,sentence) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])

        elif word.text in ordinals:
            if check_for_punct(i,sentence) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])
            elif check_for_prep(i,sentence) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])
            elif check_next_3_words(i,sentence) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])

        elif word.tag_ in ["WDT"] :
            if check_for_punct(i,sentence) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])
            elif check_for_prep(i,sentence) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])
            elif check_prev_1_words(i,sentence) == True and check_next_3_words(i,sentence) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])


        elif word.text.lower() in ["these","those","his"] :
            if check_for_punct(i,sentence) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])
            elif check_next_3_words(i,sentence) == True:
                licensors.append([word.text,i,word.pos_,word.tag_])

        elif word.tag_ in ["JJ",'JJR','JJS'] :
            if check_DT_prev(i,sentence) == True:
                if check_next_3_words(i,sentence) == True:
                    licensors.append([word.text,i,word.pos_,word.tag_])

    refined_licensors = []
    for i,tup in enumerate(licensors):
        if i != len(licensors)-1 :
            if licensors[i+1][1] -tup[1] != 1 :
                refined_licensors.append(tup)
        else :
            refined_licensors.append(tup)

    index_dict = {} 

    for tup in refined_licensors:
        index_dict[tup[1]] = tup[0]
   
    ellided_sentence = []
    for i,word in enumerate(sentence) :
        if i in index_dict.keys():
            licensor_word = index_dict[i]
            if licensor_word.lower() == "mine" :
                ellided_sentence.append("my")
                ellided_sentence.append("[e]")

            elif licensor_word.lower() == "hers" :
                ellided_sentence.append("her")
                ellided_sentence.append("[e]")

            elif licensor_word.lower() == "theirs" :
                ellided_sentence.append("their")
                ellided_sentence.append("[e]")

            elif licensor_word.lower() == "yours" :
                ellided_sentence.append("your")
                ellided_sentence.append("[e]")

            elif licensor_word.lower() == "ours" :
                ellided_sentence.append("our")
                ellided_sentence.append("[e]")

            else:
                ellided_sentence.append(word.text)
                ellided_sentence.append("[e]")
        else :
            ellided_sentence.append(word.text)

    #print(licensors)
    #print(" ".join(ellided_sentence))

    return licensors    
    

#if __name__=="__main__" :
    

sentence="Mary got three keys and John got five"
licensors=find_licensors(sentence)
for i in licensors:
    print("Licensor :")
    print(i)
    print()
    antecedents = find_antecedent(i,sentence)
    print("Antecedents found : ")
    for j in antecedents :
        print(j)
        print()   

    
     
    
    
    
    
    
    
    
