#   Written By: Michael Cooper

import re

#langdef: function def for language; ind: line to search from
def findFuncDec(fileContent, langDef):

	arrInds = []	#empty list

	curLine = 0
	for line in fileContent:
		ind = re.search(langDef, line)
		if ind is not None:
			arrInds.append(curLine)
		curLine += 1

	return arrInds

def comment(filecontent, comment, index):	#comment will be array of lines to comment
	comment.reverse()			#reverse comment to place comment in proper order
	for line in comment:
		filecontent.insert(index, line)
	return filecontent		#return new version of filecontent


if __name__ == "__main__":
	pass