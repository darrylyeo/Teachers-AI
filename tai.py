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

topics = None

def scoreLead(text):
	sentences = nltk.sent_tokenize(text)

	partOfSpeechTags = [nltk.pos_tag(nltk.word_tokenize(sentence)) for sentence in sentences]

	topics = [[word for (word, partOfSpeech) in sentence if partOfSpeech in ('NN', 'NNP')] for sentence in partOfSpeechTags]
	print('Topics:', topics)


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
	grade = 0
	return gradeLevelToScore(grade)
 

# essays = json.load(open('tai-documents-v3.json').read())
# checkboxes = json.load(open('tai-checkboxes-v3.json').read())

def scoreEssay(text):
	# Break into sections??
	# https://www.nltk.org/api/nltk.tokenize.html#module-nltk.tokenize.texttiling
	topicalSections = nltk.tokenize.TextTilingTokenizer().tokenize(text)
	print(topicalSections)

	print('Lead:', scoreLead(text))
	print('Transitions:', scoreTransitions(text))
	print('Ending:', scoreEnding(text))




if __name__ == '__main__':
	text = open(sys.argv[1]).read()
	scoreEssay(text)
