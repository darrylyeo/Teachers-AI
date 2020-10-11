import nltk, re
from nltk.tokenize import PunktSentenceTokenizer, sent_tokenize
from nltk.corpus import wordnet as wn
from helpers import cleanStringList, gradeLevelToScore, findTopics, findAllSynonyms, uniqueWords


checkboxWeights = {
	'2-0_transitions': 1,
	'3-0_transitions': 1/2,
	'3-1_transitions': 1/2,
	'4-0_transitions': 1/3,
	'4-1_transitions': 1/3,
	'4-2_transitions': 1/3,
	'5-0_transitions': 1/4,
	'5-1_transitions': 1/4,
	'5-2_transitions': 1/4,
	'5-3_transitions': 1/4
}


def scoreTransitions(text, lead, body, ending):
	all_words = nltk.word_tokenize(text)
	lead_words = nltk.word_tokenize(lead)
	body_words = [word for section in body for word in nltk.word_tokenize(section)]
	ending_words = nltk.word_tokenize(ending)
	sentences = nltk.sent_tokenize(text)

	uniqueAllWords = uniqueWords(all_words)
	uniqueLeadWords = uniqueWords(lead_words)
	uniqueBodyWords = uniqueWords(body_words)
	uniqueEndingWords = uniqueWords(ending_words)

	grade = 0

	#include synsets of such as, and, also 
	synonyms = findAllSynonyms(["and","also"])
	if len(uniqueAllWords.intersection(synonyms)) > 0:
		grade += checkboxWeights['2-0_transitions']
	
	#include synsets of before, after, then, later
	synonyms = findAllSynonyms(["before","after","then","later"])
	if len(uniqueAllWords.intersection(synonyms)) > 1:
		grade += checkboxWeights['3-0_transitions']

	#include synsets of however and but
	synonyms = findAllSynonyms(["however", "but"])
	if len(uniqueAllWords.intersection(synonyms)) > 0:
		grade += checkboxWeights['3-1_transitions']

	'''
	if True:
		grade += checkboxWeights['4-0_transitions']
	'''

	#include synsets of before, after, then, later
	synonyms = findAllSynonyms(["before","after","then","later"])
	if len(uniqueLeadWords.intersection(synonyms)) > 1:
		grade += checkboxWeights['4-1_transitions']
	elif len(uniqueBodyWords.intersection(synonyms)) > 1:
		grade += checkboxWeights['4-1_transitions']
	elif len(uniqueEndingWords.intersection(synonyms)) > 1:
		grade += checkboxWeights['4-1_transitions']
	
	synonyms = findAllSynonyms(["also","another", "for_example"])
	if len(uniqueLeadWords.intersection(synonyms)) > 1:
		grade += checkboxWeights['4-2_transitions']
	elif len(uniqueBodyWords.intersection(synonyms)) > 1:
		grade += checkboxWeights['4-2_transitions']
	elif len(uniqueEndingWords.intersection(synonyms)) > 1:
		grade += checkboxWeights['4-2_transitions']

	synonyms = findAllSynonyms(["consequently","because", "result"])
	if len(uniqueEndingWords.intersection(synonyms)) > 1:
		grade += checkboxWeights['5-0_transitions']

	synonyms = findAllSynonyms(["especially","constrast", "comparison"])
	if len(uniqueAllWords.intersection(synonyms)) > 1:
		grade += checkboxWeights['5-1_transitions']

	synonyms = findAllSynonyms(["hours","later", "minutes"])
	if len(uniqueAllWords.intersection(synonyms)) > 1:
		grade += checkboxWeights['5-2_transitions']

	synonyms = findAllSynonyms(["reason","for_example", "consequently"])
	if len(uniqueAllWords.intersection(synonyms)) > 1:
		grade += checkboxWeights['5-3_transitions']
	
	print(grade)
	return gradeLevelToScore(grade)