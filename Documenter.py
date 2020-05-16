#   Written By: Michael Cooper

from typing import List

import re
import json

class Documenter():

	def __init__(self, language, files):
		self.LANG = language
		self.FILES = files
		self.CURFILE = files[0]
		self.langFuncRegex = None

	def findFuncDec(self, fileContent):
		arrInds = []	#empty list

		curLine = 0
		for line in fileContent:
			ind = re.search(self.langFuncRegex, line)
			if ind is not None:
				arrInds.append(curLine)
			curLine += 1

		return arrInds

	# UPDATE TO TAKE LIST OF ALL COMMENTS WITH INDECES, dict of dicts? list of dicts?
	def comment(self, fileContent, comment, index):	# comment will be array of lines to comment
		comment.reverse()			# reverse comment to place comment in proper order
		for line in comment:
			fileContent.insert(index, line)
		return fileContent		# return new version of filecontent

	def getRegex(self):
		with open('languageRegexes.json', encoding='utf-8') as langInfo:
			data = json.loads(langInfo.read())

		regex = ""

		regex = data[self.LANG]

		return regex

	def getCommentFormat(self):
		with open('languageComments.json', encoding='utf-8') as comInfo:
			data = json.loads(comInfo.read())

		comments = data[self.LANG]

		return comments

	def getFileContent(self) -> List[str]:
		content = ""
		with open(self.CURFILE) as f:
			content = f.readlines()
		content = [tmp.strip('\n') for tmp in content]
		return content

	def getLines(self) -> dict:
		fileContent = getFileContent()
		lines = findFuncDec(fileContent)

		linesDict = dict()
		for line in lines:
			# print("Function Declared at line:", line)
			linesDict[line] = fileContent[line]

		# for key in linesDict:
		# print(key, linesDict[key])
		return linesDict

	# What exactly was this doing again?
	def addComment(self, comment, index) -> None:
		comChar = getCommentFormat(self.LANG)
		comContent = []
		comChar = comChar[0]

		for line in comment:
			comContent.append(comChar + line)

		newContent = comment(getFileContent(), comContent, index)
		f = open(self.CURFILE, 'w')

		newContent = "\n".join(newContent)
		if newContent != "machine broke error":
			f.write(newContent)



if __name__ == "__main__":
	pass