import re
import sys
import subprocess

def word_dictionary():
    definition_of = dict()
    definition_of["Alabama"] = "Montgomery"   
    definition_of["Alaska"] = "Juneau"   
    definition_of["Arizona"] = "Phoenix"
    definition_of["Arkansas"] = "Little Rock"
    definition_of["California"] = "Sacramento"
    definition_of["Colorado"] = "Denver"
    definition_of["Connecticut"] = "Hartford"
    definition_of["Delaware"] = "Dover"
    definition_of["Florida"] = "Tallahassee"
    definition_of["Georgia"] = "Atlanta"
    definition_of["Hawaii"] = "Honolulu"
    definition_of["Idaho"] = "Boise"
    definition_of["Illinois"] = "Springfield"
    definition_of["Indiana"] = "Indianapolis"
    definition_of["Iowa"] = "Des Moines"
    definition_of["Kansas"] = "Topeka"
    definition_of["Kentucky"] = "Frankfort"
    definition_of["Louisiana"] = "Baton Rouge"
    definition_of["Maine"] = "Augusta"
    definition_of["Maryland"] = "Annapolis"
    definition_of["Massachusetts"] = "Boston"
    definition_of["Michigan"] = "Lansing"
    definition_of["Minnesota"] = "Saint Paul"
    definition_of["Mississippi"] = "Jackson"
    definition_of["Missouri"] = "Jefferson City"
    definition_of["Montana"] = "Helena"
    definition_of["Nebraska"] = "Lincoln"
    definition_of["Nevada"] = "Carson City"
    definition_of["New Hampshire"] = "Concord"
    definition_of["New Jersey"] = "Trenton"
    definition_of["New Mexico"] = "Santa Fe"
    definition_of["New York"] = "Albany"
    definition_of["North Carolina"] = "Raleigh"
    definition_of["North Dakota"] = "Bismarck"
    definition_of["Ohio"] = "Columbus"
    definition_of["Oklahoma"] = "Oklahoma City"
    definition_of["Oregon"] = "Salem"
    definition_of["Pennsylvania"] = "Harrisburg"
    definition_of["Rhode Island"] = "Providence"
    definition_of["South Carolina"] = "Columbia"
    definition_of["South Dakota"] = "Pierre"
    definition_of["Tennessee"] = "Nashville"
    definition_of["Texas"] = "Austin"
    definition_of["Utah"] = "Salt Lake City"
    definition_of["Vermont"] = "Montpelier"
    definition_of["Virginia"] = "Richmond"
    definition_of["Washington"] = "Olympia"
    definition_of["West Virginia"] = "Charleston"
    definition_of["Wisconsin"] = "Madison"
    definition_of["Wyoming"] = "Cheyenne"
  
    return definition_of 

def get_answers(state, length, definition_of):
    if definition_of.has_key(state):
        return definition_of[state]
    else:
        return ""

def run_bash():
    cmd ="for i in `../derek/search_wiki_paths.bash 100 \' one of two extant subspecies of Equus ferus\'`; do head -3 $i | tail -1; done"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    print output.split('\n')

def process_line(line,definition_of):
    if line != "":
        clueid,clue,length = '','',''
	try:
	    clueid,clue,length = line.split('\t')
	except Exception as e:
	    print line
	output = []
	clue_words = re.split(r"\W+",clue)
	# if match, then return the result
	if (clue_words[0].lower() == "capital" and clue_words[1].lower() == "of"):
            state = ' '.join(clue_words[2:])
	    answer = get_answers(state,length,definition_of)
	    if answer != "":
	        output.append(answer)
        #print output
	for word in output:
	    print "\t".join([clueid,word,str(1)])

if __name__ == "__main__":
    run_bash()
 #    definition_of = word_dictionary()
 #    if len(sys.argv) == 2:
 #        for line in open(sys.argv[1]).readlines():
 #            process_line(line,definition_of)
 #    elif len(sys.argv) == 1:
	# for line in sys.stdin:
	#     process_line(line,definition_of)
