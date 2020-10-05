checkbox_weights = {
	"2-0_lead": 1,
	"3-0_lead": 1,
	"4-0_lead": 1/2,
	"4-1_lead": 1/2,
	"5-0_lead": 1/2,
	"5-1_lead": 1/2,
	"2-0_transitions": 1,
	"3-0_transitions": 1,
	"3-1_transitions": 1,
	"4-0_transitions": 1/2,
	"4-1_transitions": 1/2,
	"5-0_transitions": 1/2,
	"5-1_transitions": 1/2,

}
def scoreLead(text): 
	if ___:
		Score = score + checkbox_weights["2-0_lead"]
	if ___:
		Score = score + checkbox_weights["3-0_lead"]
	if ___:
		Score = score + checkbox_weights["4-0_lead"]
	if ___:
		Score = score + checkbox_weights["4-1_lead"]
	if ___:
		Score = score + checkbox_weights["5-0_lead"]
	if ___:
		Score = score + checkbox_weights["5-1_lead"]
	return Score
 
def scoreTransitions():

def scoreEnding(): 

 
def score_essay(text):
	print(scoreLead(text))
	print(scoreTransitions(text))
	print(scoreEnding(text))
 
text = open(sys.args[1], "r")
score_essay(text)
