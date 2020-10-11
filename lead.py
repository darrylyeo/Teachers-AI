import nltk, re
from nltk.tokenize import PunktSentenceTokenizer, sent_tokenize
from nltk.corpus import wordnet as wn
from helpers import cleanStringList, gradeLevelToScore, findTopics, findAllSynonyms, uniqueWords

checkboxWeights = {
	'2-0_lead': 1,
	'3-0_lead': 1,
	'4-0_lead': 1/2,
	'4-1_lead': 1/2,
	'5-0_lead': 1/2,
	'5-1_lead': 1/2
}

def scoreLead(lead):
	leadWords = nltk.word_tokenize(lead)
	leadSentences = nltk.sent_tokenize(lead)

	partOfSpeechTags = nltk.pos_tag(leadWords)

	leadTopics = findTopics(leadWords)
	print('Lead topics:', leadTopics)
	
	uniqueLeadWords = uniqueWords(leadWords)

	grade = 0

	# Named a subject, tried to interest readers
	if len(set(leadTopics)) > 0:
		grade += checkboxWeights['2-0_lead']

	# Got readers ready to learn a lot of information about the subject
	learnWords = findAllSynonyms(['learn', 'teach', 'know', 'guide'])
	if len(uniqueLeadWords.intersection(learnWords)) > 0:
		print(uniqueLeadWords.intersection(learnWords))
		grade += checkboxWeights['3-0_lead']

	# Hooked readers by explaining why subject matters, telling surprising fact, or giving a big picture
	hookWords = findAllSynonyms(['important', 'amazing', 'interesting', 'many', 'several', 'unique'])
	hasQuestion = '?' in lead
	if len(uniqueLeadWords.intersection(hookWords)) > 0 or hasQuestion:
		print(uniqueLeadWords.intersection(hookWords), hasQuestion)
		grade += checkboxWeights['4-0_lead']

	# Told reader that they will learn different things about a subject
	if len(set(leadTopics)) >= 4:
		grade += checkboxWeights['4-1_lead']

	# Helped readers get interested in and understand the subject
	if len(uniqueLeadWords.intersection(hookWords)) >= 2:
		grade += checkboxWeights['5-0_lead']

	# Let readers know the subtopics to be developed and their sequence
	sequenceWords = findAllSynonyms(['first', 'second', 'third', 'fourth', 'fifth', 'next', 'then', 'finally', 'after', 'step', 'reason', 'lastly', 'also', 'example'])
	if len(set(leadTopics)) >= 4 and len(uniqueLeadWords.intersection(sequenceWords)) > 0:
		print(uniqueLeadWords.intersection(sequenceWords))
		grade += checkboxWeights['5-1_lead']

	print(grade)

	return gradeLevelToScore(grade)
