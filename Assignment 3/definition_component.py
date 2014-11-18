#!/usr/bin/env python
import re
import sys
import subprocess
from wordnik.wordnik import *

ignore = ['a','able','about','above','across','after','again','against','aint','all','almost','also','am','among','an','and','any','are','arent','as','at','be','because','been','before','being','below','between','both','but','by','can','cant','cannot','could','couldve','couldnt','dear','did','didnt','do','does','doesnt','doing','dont','down','during','each','either','else','ever','every','few','for','from','further','get','got','had','hadnt','has','hasnt','have','havent','having','he','hed','hell','hes','her','here','heres','hers','herself','him','himself','his','how','howd','howll','hows','however','i','id','ill','im','ive','if','in','into','is','isnt','it','its','its','itself','just','least','let','lets','like','likely','may','me','might','mightve','mightnt','more','most','must','mustve','mustnt','my','myself','neither','no','nor','not','of','off','often','on','once','only','or','other','ought','our','ours','ourselves','out','over','own','rather','said','same','say','says','shall','shant','she','shed','shell','shes','should','shouldve','shouldnt','since','so','some','such','than','that','thatll','thats','the','their','theirs','them','themselves','then','there','theres','these','they','theyd','theyll','theyre','theyve','this','those','through','tis','to','too','twas','under','until','up','us','very','wants','was','wasnt','we','wed','well','were','weve','were','werent','what','whatd','whats','when','whend','whenll','whens','where','whered','wherell','wheres','which','while','who','whod','wholl','whos','whom','why','whyd','whyll','whys','will','with','wont','would','wouldve','wouldnt','yet','you','youd','youll','youre','youve','your','yours','yourself','yourselves']

def init():
    apiUrl = 'http://api.wordnik.com/v4'
    apiKey = '0447438b71e16b1fe640c0524220f075951133d14bb14890e'
    client = swagger.ApiClient(apiKey, apiUrl)
    return WordApi.WordApi(client)
    # wordApi = WordApi.WordApi(client)
    # definitions = wordApi.getDefinitions('badger',sourceDictionaries='wiktionary',limit=1)
    # print definitions[0].text

def find_def(clue,length,wordapi):   
    word_arr = clue.split()
    answer = []
    for word in word_arr:
        word = word.lower()
        if len(word)<2:
            continue
        if word in ignore:
            continue
        definition = wordapi.getDefinitions(word.lower(),sourceDictionaries='wiktionary',limit=1)
        if not definition:
            continue
        # print definition[0].text
        for words in definition[0].text.split():
            words = words.lower()
            if words in ignore:
                continue
            words = ''.join(c for c in words if c not in ' ()[]\/|.-,\'\"')
            if len(words) == int(length):
                answer.append(words.lower())
            # else:
            #     print "The word was {0} with length of {1} with size {2}".format(words,length,len(words))
    return answer

def run_bash(clue,length):
    clue = ''.join(c for c in clue if c not in '()[]\/|.-,\'\"')
    cmd ="for i in `../derek/search_wiki_paths.bash 100 \'{}\'`; do head -3 $i | tail -1; done".format(clue)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    output = output.split('\n')
    if len(output) > 40:
        return filter_words(output,length)
    return filter_words(output[0:40],length)

def filter_words(arr,length):
    def_dict = {}
    max_ans = float("-inf")
    for item in arr:
        for word in item.split():
            word = word.lower()
            #get rid of all blank spaces or quotations or dashes etc
            word = ''.join(c for c in word if c not in ' ()[]\/|.-,\'\"')
            if word in ignore:
                continue
            if not word:
                continue
            if len(word) != int(length):
                continue
            if word.lower() in def_dict:
                temp = def_dict[word.lower()] + 1
                def_dict[word.lower()] = temp
            else:
                temp = 1
                def_dict[word.lower()] = 1
            if temp > max_ans:
                max_ans = temp
    for key in def_dict:
        if max_ans < 3:
            max_ans = 3
        def_dict[key] = (def_dict[key]* 1.0) / ((max_ans + 1) * 1.0)
    return def_dict


def process_line(line,wordapi):
    if line != "":
        clueid,clue,length = '','',''
    try:
        temp = line.split('\t')
        clueid = temp[0]
        clue = temp [1]
        length = temp[2]
    except Exception as e:
        print line
    output = run_bash(clue,length)
    try:
        for word in find_def(clue,length,wordapi):
            if word.lower() in output:
                if output[word.lower()]+.4 < .9:
                    output[word.lower()] = output[word.lower()] +.2
                else:
                    output[word.lower()] = .9
            else:
                output[word.lower()] = .3
    except:
        pass
	# if match, then return the result
    for word in output:
        print "\t".join([clueid,word,str(output[word])])


if __name__ == "__main__":
    wordapi = init()
    if len(sys.argv) == 2:
        for line in open(sys.argv[1]).readlines():
            process_line(line,wordapi)
    elif len(sys.argv) == 1:
	   for line in sys.stdin:
	       process_line(line,wordapi)
