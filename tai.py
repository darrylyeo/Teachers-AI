import json, nltk, re, sys
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


# Trim whitespace and delete empty strings
def cleanStringList(strings):
	return [string for string in [string.strip() for string in strings] if string]


def gradeLevelToScore(grade):
	# Grade Level 4 = Score 3.0
	return max(grade - 1, 0)


leadTopics = None
leadWords = ['learn', 'teach', 'know', 'guide']

def scoreLead(text):
	words = nltk.word_tokenize(text)
	sentences = nltk.sent_tokenize(text)

	partOfSpeechTags = nltk.pos_tag(words)

	global leadTopics
	leadTopics = [word.lower() for (word, partOfSpeech) in partOfSpeechTags if partOfSpeech in ('NN', 'NNP', 'NNS')]
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

	endingTopics = [word.lower() for (word, partOfSpeech) in partOfSpeechTags if partOfSpeech in ('NN', 'NNP', 'NNS')]
	print('Ending topics:', endingTopics)

	commonTopics = set(leadTopics).intersection(set(endingTopics))
	print('Topics common to both lead and ending:', commonTopics)

	if len(commonTopics) == 0:
		# Doesn't reference topic from lead; not a conclusion
		pass

	grade = 0
	return gradeLevelToScore(grade)

# essays = json.load(open('tai-documents-v3.json').read())
# checkboxes = json.load(open('tai-checkboxes-v3.json').read())

def scoreEssay(text):
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
	
	# No ending punctuation used; simply break into sections by newlines
	if len(sections) < 3:
		sections = cleanStringList(text.splitlines())

	# Remove the last section if it's a glossary
	if re.match('[Gg]loss[ao]ry', sections[-1]):
		sections = sections[:-1]


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

		print('Lead:', scoreLead(lead))
		print('Transitions:', scoreTransitions(body))
		print('Ending:', scoreEnding(ending))




if __name__ == '__main__':
	text = open(sys.argv[1]).read()
	scoreEssay(text)
