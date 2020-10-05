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


leadWords = ['']

def scoreLead(text):
	sentences = nltk.sent_tokenize(text)

	partOfSpeechTags = [nltk.pos_tag(nltk.word_tokenize(sentence)) for sentence in sentences]

	topics = [word for (word, pos) in partOfSpeechTags if pos in ('NN', 'NNP')]
	print(topics)

	# https://www.nltk.org/api/nltk.tokenize.html#module-nltk.tokenize.texttiling
	topicalSections = nltk.tokenize.TextTilingTokenizer().tokenize(text)
	print(topicalSections)


	score = 0
	if ___:
		score += checkboxWeights['2-0_lead']
	if ___:
		score += checkboxWeights['3-0_lead']
	if ___:
		score += checkboxWeights['4-0_lead']
	if ___:
		score += checkboxWeights['4-1_lead']
	if ___:
		score += checkboxWeights['5-0_lead']
	if ___:
		score += checkboxWeights['5-1_lead']
	return score
 
def scoreTransitions(text):
	score = 0
	return score

def scoreEnding(text):
	score = 0
	return score
 

essays = json.load(open('tai-documents-v3.json'))
checkboxes = json.load(open('tai-checkboxes-v3.json'))

def scoreEssay(text):
	print('Lead:', scoreLead(text))
	print('Transitions:', scoreTransitions(text))
	print('Ending:', scoreEnding(text))




if __name__ == '__main__':
	text = open(sys.args[1])
	scoreEssay(text)
