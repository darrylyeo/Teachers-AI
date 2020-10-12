import json, sys
from helpers import breakSections
from lead import scoreLead
from transitions import scoreTransitions
from ending import scoreEnding

def print_actual_grades(essays):
	outfile = open("actualgrades.txt", "w")
	outfile = open("actualgrades.txt", "w")
	for i in range(0, len(essays)):
		outfile.write("Title: "+str(essays[i]["doctitle"])+" ")
		outfile.write("Lead: "+str(essays[i]["grades"][1]["score"]["criteria"]["lead"])+" ")
		outfile.write("Ending: "+str(essays[i]["grades"][1]["score"]["criteria"]["ending"])+" ")
		outfile.write("Transitions: "+str(essays[i]["grades"][1]["score"]["criteria"]["transitions"])+" ")
		outfile.write("\n")
	outfile.close()

def scoreEssay(text):
	sections = breakSections(text)

	#print('Sections:', sections, '\n')
	
	if len(sections) < 3:
		print('No clear lead, body, or ending')
	else:
		lead = sections[0]
		body = sections[1:-2]
		ending = sections[-1]
		'''
		print('Lead:')
		print(lead)
		print('Body:')
		print(body)
		print('Ending:')
		print(ending)
		'''
		print('Lead:', scoreLead(lead))
		print('Transitions:', scoreTransitions(text, lead, body, ending))
		print('Ending:', scoreEnding(lead, ending))


if __name__ == '__main__':
	#with open('tai-documents-v3.json') as f:
  		#essays = json.load(f)
	#print_actual_grades(essays)
	text = open(sys.argv[1]).read()
	scoreEssay(text)
