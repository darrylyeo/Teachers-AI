import nltk, re
from nltk.tokenize import PunktSentenceTokenizer, sent_tokenize
from nltk.corpus import wordnet as wn


# Trim whitespace, delete empty strings, and fix some punctuation
def cleanStringList(strings):
	return [string for string in [
		re.sub(r"([.?!,;])(?=[A-Z][a-z])", r"\g<1> ", re.sub(r"’", "'", re.sub(r'[“”]|``', '"', string.strip()))) for string in strings
	] if string]


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
		#print(len(nltk.word_tokenize(sections[i])))
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
	return [word.lower() for (word, partOfSpeech) in partOfSpeechTags if partOfSpeech in ('NN', 'NNP', 'NNS', 'NNPS')]


# Extract nouns, verbs, and adjectives from a list of words
def findKeywords(words):
	partOfSpeechTags = nltk.pos_tag(words)
	#print(partOfSpeechTags)
	return [word.lower() for (word, partOfSpeech) in partOfSpeechTags if partOfSpeech in ('NN', 'NNP', 'NNS', 'NNPS', 'VB', 'VBG', 'VBD', 'VBN', 'VBZ', 'JJ', 'JJR', 'JJS')]


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


# Remove punctuation from a list of words
def removePunctuation(words):
	return [word for word in [re.sub(r"[^A-Za-z']", '', word) for word in words] if word]