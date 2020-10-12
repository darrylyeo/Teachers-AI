import json

def print_actual_grades(essays):
	outfile = open("actual-grades.txt", "w")
	for essay in essays:
		outfile.write("Title: " + str(essay["doctitle"]) + " ")
		outfile.write("Lead: " + str(essay["grades"][1]["score"]["criteria"]["lead"]) + " ")
		outfile.write("Ending: " + str(essay["grades"][1]["score"]["criteria"]["ending"]) + " ")
		outfile.write("Transitions: " + str(essay["grades"][1]["score"]["criteria"]["transitions"]) + " ")
		outfile.write("\n")
	outfile.close()

with open('tai-documents-v3.json') as data:
    essays = json.load(data)
    print_actual_grades(essays)