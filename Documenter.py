#   Written By: Michael Cooper

from typing import List
from os import rename

import re
import json

class Documenter():

	def __init__(self, language, files):
		self.LANG = language
		self.FILES = files
		self.CURFILE = files[0]
		self.langFuncRegex = None
		self.content = None
		self.langCommTemplate = None

		self.getRegex()
		self.getCommentFormat()



	def findFuncDec(self, fileContent):
		arrInds = []	#empty list

		curLine = 0
		for line in fileContent:
			# print(self.langFuncRegex)
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

		self.langFuncRegex = regex

	def getCommentFormat(self):
		with open('languageComments.json', encoding='utf-8') as comInfo:
			data = json.loads(comInfo.read())

		comments = data[self.LANG]

		self.langCommTemplate = comments

	def getFileContent(self) -> List[str]:
		self.content = None
		with open(self.CURFILE) as f:
			self.content = f.readlines()
		self.content = [tmp.strip('\n') for tmp in self.content]
		print(self.content)

	def getLines(self) -> dict:
		self.getFileContent()
		lines = self.findFuncDec(self.content)

		linesDict = dict()
		for line in lines:
			print("Function Declared at line:", line)
			linesDict[line] = self.content[line]

		# for key in linesDict:
		# print(key, linesDict[key])
		return linesDict

	# What exactly was this doing again?
	# update to use dict of lists of strings :)
	def addComment(self, commentsDict) -> None:
		self.getCommentFormat()
		comContent = []
		comChar = self.langCommTemplate[0]

		# get list of comments (already in order from top of file to bottom)
		# -> create dict where key=linenumber val=listitem
		# -> reverse list -> create filecontent string with comments
		# maybe try using generators in the future? https://youtu.be/6QyJVF4buE0

		

		for line in comment:
			comContent.append(comChar + line)

		newContent = comment(comContent, index)

		rename(self.CURFILE, self.CURFILE + ".bak")
		f = open(self.CURFILE, 'w')

		newContent = "\n".join(newContent)
		if newContent != "machine broke error":
			print(newContent)
			f.write(newContent)


if __name__ == "__main__":
	pass