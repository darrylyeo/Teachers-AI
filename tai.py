import json, nltk, re, sys
from nltk.tokenize import PunktSentenceTokenizer, sent_tokenize
from nltk.corpus import wordnet as wn


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


# Trim whitespace and delete empty strings
def cleanStringList(strings):
	return [string for string in [string.strip() for string in strings] if string]


def gradeLevelToScore(grade):
	# Grade Level 4 = Score 3.0
	return max(grade - 1, 0)


def breakSections(text):
	sections = []

	# Attempt to break into sections by topic
	# https://www.nltk.org/api/nltk.tokenize.html#module-nltk.tokenize.texttiling
	try:
		sections = cleanStringList(nltk.tokenize.TextTilingTokenizer().tokenize(text))
	except:
		pass

	# Attempt to break into sections by newlines, as long the previous line ends with punctuation (i.e. not a heading)
	if len(sections) < 3: # or re.match('\n[Cc]onclusion', sections[-1])
		sections = cleanStringList(re.split('(?<=[.?!])\n+', text)) # '(?<![A-Z][a-z]+(?: [A-Z][a-z]+)*)[\n\t]+'
	
	# No ending punctuation used at all; simply break into sections by newlines
	if len(sections) < 3:
		sections = cleanStringList(text.splitlines())

	# Remove the last section if it's a glossary
	if re.match('[Gg]loss[ao]ry', sections[-1]):
		sections = sections[:-1]
	
	return sections


# Extract nouns from a list of words
def findTopics(words):
	partOfSpeechTags = nltk.pos_tag(words)
	return [word.lower() for (word, partOfSpeech) in partOfSpeechTags if partOfSpeech in ('NN', 'NNP', 'NNS')]


leadTopics = None
leadWords = ['learn', 'teach', 'know', 'guide']

def scoreLead(lead):
	leadWords = nltk.word_tokenize(lead)
	leadSentences = nltk.sent_tokenize(lead)

	partOfSpeechTags = nltk.pos_tag(leadWords)

	global leadTopics
	leadTopics = findTopics(leadWords)
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
 
def scoreTransitions(text, lead, body, ending):
	all_words = nltk.word_tokenize(text)
	print(all_words)
	sentences = nltk.sent_tokenize(text)

	grade = 0

	#include synsets of such as, and, also 
	synonyms =["and", "also"]
	synsets = []
	synsets.extend(wn.synsets("and"))
	synsets.extend(wn.synsets("also"))
	for syn in synsets:
		for l in syn.lemmas():
			synonyms.append(l.name().replace("_"," "))
	if len(set(all_words).intersection(synonyms)) > 0:
		grade += checkboxWeights['2-0_transitions']
	#include synsets of before, after, then, later
	synonyms =["before","after","then","later"]
	synsets = []
	synsets.extend(wn.synsets("before"))
	synsets.extend(wn.synsets("after"))
	synsets.extend(wn.synsets("then"))
	synsets.extend(wn.synsets("later"))
	for syn in synsets:
		for l in syn.lemmas():
			synonyms.append(l.name().replace("_"," "))
	if len(set(all_words).intersection(synonyms)) > 1:
		grade += checkboxWeights['3-0_transitions']
	#include synsets of however and but
	synonyms =["however", "but"]
	synsets = []
	synsets.extend(wn.synsets("however"))
	synsets.extend(wn.synsets("but"))
	for syn in synsets:
		for l in syn.lemmas():
			synonyms.append(l.name().replace("_"," "))
	if len(set(all_words).intersection(synonyms)) > 0:
		grade += checkboxWeights['3-1_transitions']
	'''
	if True:
		grade += checkboxWeights['4-0_transitions']
	if True:
		grade += checkboxWeights['4-1_transitions']
	if True:
		grade += checkboxWeights['4-2_transitions']
	if True:
		grade += checkboxWeights['5-0_transitions']
	if True:
		grade += checkboxWeights['5-1_transitions']
	if True:
		grade += checkboxWeights['5-2_transitions']
	if True:
		grade += checkboxWeights['5-3_transitions']
	'''
	print(grade)
	return gradeLevelToScore(grade)

def scoreEnding(ending):
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

# essays = json.load(open('tai-documents-v3.json').read())
# checkboxes = json.load(open('tai-checkboxes-v3.json').read())

def scoreEssay(text):
	sections = breakSections(text)

	print('Sections:', sections, '\n')
	
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
	
		# print('Lead:', scoreLead(lead))
		print('Transitions:', scoreTransitions(text, lead, body, ending))
		# print('Ending:', scoreEnding(ending))




if __name__ == '__main__':
	text = open(sys.argv[1]).read()
	scoreEssay(text)
