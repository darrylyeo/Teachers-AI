import nltk, re
from nltk.tokenize import PunktSentenceTokenizer, sent_tokenize
from nltk.corpus import wordnet as wn
from helpers import cleanStringList, gradeLevelToScore, findTopics, findKeywords, findAllSynonyms, uniqueWords, removePunctuation


checkboxWeights = {
	'2-0_ending': 1,
	'3-0_ending': 1,
	'4-0_ending': 1/2,
	'4-1_ending': 1/2,
	'5-0_ending': 1,
}


def scoreEnding(lead, ending):
	leadWords = removePunctuation(nltk.word_tokenize(lead))

	endingWords = nltk.word_tokenize(ending)
	endingSentences = nltk.sent_tokenize(ending)

	uniqueEndingWords = uniqueWords(endingWords)

	hasQuestion = '?' in lead

	grade = 0

	# Wrote some sentences to wrap up
	grade += checkboxWeights['2-0_ending']
	
	# Drew conclusions, asked questions, or suggested ways readers might respond
	conclusionWords = findAllSynonyms(['in_conclusion', 'all_in_all', 'so', 'conclude'])
	if len(uniqueEndingWords.intersection(conclusionWords)) > 0 or hasQuestion:
		grade += checkboxWeights['3-0_ending']
	
	# Reminded readers of subject and either suggested a follow-up action or left readers with a final thought
	leadTopics = findTopics(leadWords)
	endingTopics = findTopics(endingWords)
	print('Ending topics:', endingTopics)
	commonTopics = uniqueWords(leadTopics).intersection(uniqueWords(endingTopics))
	print('Topics common to both lead and ending:', commonTopics)
	finalWords = findAllSynonyms(['hope', 'try', 'visit', 'learned'])
	if len(commonTopics) >= 3 and len(uniqueEndingWords.intersection(finalWords)) > 0:
		grade += checkboxWeights['4-0_ending']
	
	# Thoughts, feelings, and questions about the subject
	thoughtsAndFeelingsWords = findAllSynonyms(['think', 'believe', 'opinion', 'feel', 'issue', 'address'])
	if len(uniqueEndingWords.intersection(thoughtsAndFeelingsWords)) > 0 or hasQuestion:
		grade += checkboxWeights['4-1_ending']
	
	# Restated main points
	commonKeywords = uniqueWords(findKeywords(leadWords)).intersection(uniqueWords(findKeywords(endingWords))).difference(set(['is', 'are', 'were', 'was', 'has', 'had', 'have', 'be']))
	print('Keywords common to both lead and ending:', commonKeywords)
	if len(commonKeywords) >= 6:
		grade += checkboxWeights['5-0_ending']

	return gradeLevelToScore(grade)