import json, nltk, sys
from nltk.tokenize import PunktSentenceTokenizer, sent_tokenize


checkboxWeights = {
	'2-0_lead': 1,
	'3-0_lead': 1,
	'4-0_lead': 1/2,
	'4-1_lead': 1/2,
	'5-0_lead': 1/2,
	'5-1_lead': 1/2,
	'2-0_transitions': 1,
	'3-0_transitions': 1/2,
	'3-1_transitions': 1/2,
	'4-0_transitions': 1/3,
	'4-1_transitions': 1/3,
	'4-2_transitions': 1/3,
	'5-0_transitions': 1/4,
	'5-1_transitions': 1/4,
	'5-2_transitions': 1/4,
	'5-3_transitions': 1/4,
	'2-0_ending': 1,
	'3-0_ending': 1,
	'4-0_ending': 1/2,
	'4-1_ending': 1/2,
	'5-0_ending': 1,
}


leadWords = ['learn', 'teach', 'know', 'guide']


def gradeLevelToScore(grade):
	# Grade Level 4 = Score 3.0
	return max(grade - 1, 0)

leadTopics = None

def scoreLead(text):
	words = nltk.word_tokenize(text)
	sentences = nltk.sent_tokenize(text)

	partOfSpeechTags = nltk.pos_tag(words)

	global leadTopics
	leadTopics = [word for (word, partOfSpeech) in partOfSpeechTags if partOfSpeech in ('NN', 'NNP')]
	print('Lead topics:', leadTopics)


	grade = 0
	if True:
		grade += checkboxWeights['2-0_lead']
	if True:
		grade += checkboxWeights['3-0_lead']
	if True:
		grade += checkboxWeights['4-0_lead']
	if True:
		grade += checkboxWeights['4-1_lead']
	if True:
		grade += checkboxWeights['5-0_lead']
	if True:
		grade += checkboxWeights['5-1_lead']

	
	return gradeLevelToScore(grade)
 
def scoreTransitions(text):
	grade = 0
	return gradeLevelToScore(grade)

def scoreEnding(text):
	words = nltk.word_tokenize(text)
	sentences = nltk.sent_tokenize(text)

	partOfSpeechTags = nltk.pos_tag(words)

	endingTopics = [word for (word, partOfSpeech) in partOfSpeechTags if partOfSpeech in ('NN', 'NNP')]
	print('Ending topics:', endingTopics)

	commonTopics = set(leadTopics).intersection(set(endingTopics))
	print('Topics common to both lead and ending:', commonTopics)

	grade = 0
	return gradeLevelToScore(grade)
 

# essays = json.load(open('tai-documents-v3.json').read())
# checkboxes = json.load(open('tai-checkboxes-v3.json').read())

def scoreEssay(text):
	# Break into sections
	# https://www.nltk.org/api/nltk.tokenize.html#module-nltk.tokenize.texttiling
	topicalSections = nltk.tokenize.TextTilingTokenizer().tokenize(text)

	# Trimp whitespace
	topicalSections = [section.strip() for section in topicalSections]
	print(topicalSections)

	lead = topicalSections[0]
	body = topicalSections[1:-2]
	ending = topicalSections[-1]

	# print('Lead:')
	# print(lead)
	# print('Body:')
	# print(body)
	# print('Ending:')
	# print(ending)

	print('Lead:', scoreLead(lead))
	print('Transitions:', scoreTransitions(body))
	print('Ending:', scoreEnding(ending))




if __name__ == '__main__':
	text = open(sys.argv[1]).read()
	scoreEssay(text)
