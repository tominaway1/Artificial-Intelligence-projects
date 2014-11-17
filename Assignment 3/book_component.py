import re
import sys
import subprocess

def run_bash(clue,length):
    temp = ''.join(c for c in clue if c not in ' ()[]\/|.-,\'\"')
    cmd ="for i in `../derek/search_wiki_paths.bash 100 \'{}\' \'books\'`; do head -3 $i | tail -1; done".format(temp)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    output = output.split('\n')
    if len(output) > 40:
        return filter_words(output,length,clue,temp)
    return filter_words(output[0:40],length,clue,temp)

def filter_words(arr,length,clue,temp):
    def_dict = {}
    #array of whole clue
    clue_arr = clue.split()
    clue_len = len(clue_arr)
    #array of all words without clue
    temp = temp.split()

    for item in arr:
        item_arr = item.split()
        if len(item_arr) != clue_len:
            continue
        #list of all possible words
        possible = []
        boolean = True
        max_frequency = 0
        for i in range(clue_len):
            temp_clue = ''.join(c for c in clue_arr[i] if c not in ' ()[]\/|.-,\'\"')
            temp_item = ''.join(c for c in item_arr[i] if c not in ' ()[]\/|.-,\'\"')
            if temp_clue in temp:
                if temp_clue.lower() != temp_item.lower():
                    boolean = False
                    break
            else:
                possible.append(temp_item.lower())
        if boolean:
            for word in possible:
                if word in def_dict:
                    t = def_dict[word] + 1
                    def_dict[word] = t
                    if t > max_frequency:
                        max_frequency = t
                else:
                    def_dict[word] = 1
                    if max_frequency < 1:
                        max_frequency = 1

    for key in def_dict:
        def_dict[key] = (def_dict[key] * 1.0) / (max_frequency * 1.0)
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
