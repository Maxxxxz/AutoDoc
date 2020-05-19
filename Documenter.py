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
		self.content = None

	def findFuncDec(self, fileContent):
		arrInds = []	#empty list

		curLine = 0
		for line in fileContent:
			ind = re.search(self.langFuncRegex, line)
			if ind is not None:
				arrInds.append(curLine)
			curLine += 1

		return arrInds

	# update to use dict of lists of strings :)
	def comment(self, commentsDict):	# comment will be array of lines to comment
		keys = commentsDict.keys()		# logic to get keys in correct order we need them in
		keys.sort()
		keys.reverse()
		# keys are now in reverse order to document from bottom down, keeping other keys simple with no extra math
		for k in keys:		# begin looping over all keys (will be from bottom up)
			commentsDict[k].reverse()
			for c in commentsDict[k]:	# should work :)
				self.content.insert(k, c)		# insert comments in reverse order so they appear correctly

		# comment.reverse()			# reverse comment to place comment in proper order
		# for line in comment:
		# 	fileContent.insert(index, line)
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
		self.content = None
		with open(self.CURFILE) as f:
			self.content = f.readlines()
		self.content = [tmp.strip('\n') for tmp in self.content]
		return self.content

	def getLines(self) -> dict:
		fileContent = self.getFileContent()
		lines = self.findFuncDec(fileContent)

		linesDict = dict()
		for line in lines:
			# print("Function Declared at line:", line)
			linesDict[line] = fileContent[line]

		# for key in linesDict:
		# print(key, linesDict[key])
		return linesDict

	# What exactly was this doing again?
	def addComment(self, comment, index) -> None:
		comChar = self.getCommentFormat(self.LANG)
		comContent = []
		comChar = comChar[0]

		for line in comment:
			comContent.append(comChar + line)

		newContent = comment(self.getFileContent(), comContent, index)
		f = open(self.CURFILE, 'w')

		newContent = "\n".join(newContent)
		if newContent != "machine broke error":
			f.write(newContent)



if __name__ == "__main__":
	pass