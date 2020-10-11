import nltk, re
from nltk.tokenize import PunktSentenceTokenizer, sent_tokenize
from nltk.corpus import wordnet as wn
from helpers import cleanStringList, gradeLevelToScore, findTopics, findAllSynonyms, uniqueWords


checkboxWeights = {
	'2-0_ending': 1,
	'3-0_ending': 1,
	'4-0_ending': 1/2,
	'4-1_ending': 1/2,
	'5-0_ending': 1,
}


def scoreEnding(lead, ending):
	leadWords = nltk.word_tokenize(lead)
	leadTopics = findTopics(leadWords)

	endingWords = nltk.word_tokenize(ending)
	endingSentences = nltk.sent_tokenize(ending)

	endingTopics = findTopics(endingWords)
	print('Ending topics:', endingTopics)

	commonTopics = set(leadTopics).intersection(set(endingTopics))
	print('Topics common to both lead and ending:', commonTopics)

	if len(commonTopics) == 0:
		# Doesn't reference topic from lead; not a conclusion
		pass


	grade = 0

	if True:
		grade += checkboxWeights['2-0_ending']
	if True:
		grade += checkboxWeights['3-0_ending']
	if True:
		grade += checkboxWeights['4-0_ending']
	if True:
		grade += checkboxWeights['4-1_ending']
	if True:
		grade += checkboxWeights['5-0_ending']

	return gradeLevelToScore(grade)