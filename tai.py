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
	if len(sections) < 3: # or re.match('.*[Cc]onclusion', sections[-1], re.DOTALL)
		sections = cleanStringList(re.split('(?<=[.?!])\n+', text)) # '(?<![A-Z][a-z]+(?: [A-Z][a-z]+)*)[\n\t]+'
	
	# No ending punctuation used at all; simply break into sections by newlines
	if len(sections) < 3:
		sections = cleanStringList(text.splitlines())
	
	# If a "section" has less than 5 words, it's most likely a title or heading; merge with the next section
	for i in range(len(sections) - 2, -1, -1):
		print(len(nltk.word_tokenize(sections[i])))
		if len(nltk.word_tokenize(sections[i])) < 5:
			sections[i] = sections[i] + '\n\n' + sections[i + 1]
			del sections[i + 1]

	# Remove the first section if it's a table of contents
	if re.match('.*[Tt]able [Oo]f [Cc]ontents', sections[0], re.DOTALL):
		sections = sections[1:]

	# Remove the last section if it's a glossary
	if re.match('.*[Gg]loss[ao]ry', sections[-1], re.DOTALL):
		sections = sections[:-1]

	return sections


# Extract nouns from a list of words
def findTopics(words):
	partOfSpeechTags = nltk.pos_tag(words)
	return [word.lower() for (word, partOfSpeech) in partOfSpeechTags if partOfSpeech in ('NN', 'NNP', 'NNS')]


# Get all the synonyms of a list of words
def findAllSynonyms(words, partOfSpeech = None):
	synonyms = words 
	synsets = []
	for w in words: 
		synsets.extend(wn.synsets(w)) # , partOfSpeech
	for syn in synsets:
		for l in syn.lemmas():
			synonyms.append(l.name().replace("_"," "))
	return synonyms


# Convert list of words to lowercase and remove duplicates
def uniqueWords(words):
	return set([word.lower() for word in words])


leadTopics = None

def scoreLead(lead):
	leadWords = nltk.word_tokenize(lead)
	leadSentences = nltk.sent_tokenize(lead)

	partOfSpeechTags = nltk.pos_tag(leadWords)

	global leadTopics
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

		print('Lead:')
		print(lead)
		print('Body:')
		print(body)
		print('Ending:')
		print(ending)
	
		print('Lead:', scoreLead(lead))
		print('Transitions:', scoreTransitions(text, lead, body, ending))
		print('Ending:', scoreEnding(ending))


if __name__ == '__main__':
	text = open(sys.argv[1]).read()
	scoreEssay(text)
