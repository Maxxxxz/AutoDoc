#   Written By: Michael Cooper

import Documenter as dc
import json

#implement into backend class


def getFileContent(file):
	content = ""
	with open(file) as f:
		content = f.readlines()
	content = [tmp.strip('\n') for tmp in content]
	return content

# this function can be improved when fit into a class
def addComment(file, comment, index, lang):
	comChar = getComments(lang)
	comContent = []
	comChar = comChar[0]
	
	for line in comment:
		comContent.append(comChar + line)
	
	newContent = dc.comment(getFileContent(file), comContent, index)
	f = open(file, 'w')

	newContent = "\n".join(newContent)
	if newContent != "machine broke error":
		f.write(newContent)

def getRegex(lang):
	with open('languageRegexes.json', encoding='utf-8') as langInfo:
		data = json.loads(langInfo.read())

	regex = ""

	regex = data[lang]

	return regex

def getComments(lang):
	with open('languageComments.json', encoding='utf-8') as comInfo:
		data = json.loads(comInfo.read())

	comments = data[lang]

	return comments

#call from GUI in child window process while asking to comment (NEEDS DONE)
def getLines(file, definers):
	fileContent = getFileContent(file)
	lines = dc.findFuncDec(fileContent, definers)	#will return lines OF declaration, work BACKWARDS with these to avoid doing

	linesDict = dict()
	for line in lines:
		#print("Function Declared at line:", line)
		linesDict[line] = fileContent[line]

	#for key in linesDict:
		#print(key, linesDict[key])
	return linesDict   #returns dictionary of lines indexed by number so GUI can

if __name__ == "__main__":
	getRegex("Python")