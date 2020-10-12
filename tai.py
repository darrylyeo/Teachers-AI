import sys
from helpers import breakSections
from lead import scoreLead
from transitions import scoreTransitions
from ending import scoreEnding

def scoreEssay(text):
	sections = breakSections(text)

	# print('Sections:', sections, '\n')
	
	if len(sections) < 3:
		print('No clear lead, body, or ending')
	else:
		lead = sections[0]
		body = sections[1:-2]
		ending = sections[-1]
		
		# print('Lead:')
		# print(lead)
		# print('Body:')
		# print(body)
		# print('Ending:')
		# print(ending)

		print('Lead:', scoreLead(lead))
		print('Transitions:', scoreTransitions(text, lead, body, ending))
		print('Ending:', scoreEnding(lead, ending))


if __name__ == '__main__':
	text = open(sys.argv[1]).read()
	scoreEssay(text)
