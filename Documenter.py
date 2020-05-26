#   Written By: Michael Cooper

from typing import List
from os import rename

import re

from tkinter import messagebox

class Documenter():

	def __init__(self, language, files, rx, app):
		self.LANG = language
		self.FILES = files
		self.CURFILE = files[0]
		self.APP = app
		self.curFileCounter = 0
		self.langFuncRegex = rx
		self.content = None

		# self.getRegex()
		# self.getCommentFormat()

	def nextFile(self):
		self.curFileCounter += 1
		if self.curFileCounter < len(self.FILES):
			self.CURFILE = self.FILES[self.curFileCounter]
		else:
			self.CURFILE = "NO MORE FILES"
		# print(self.CURFILE)

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
		keys = list(commentsDict.keys())		# logic to get keys in correct order we need them in
		keys.sort()
		keys.reverse()
		# keys are now in reverse order to document from bottom down, keeping other keys simple with no extra math
		for k in keys:		# begin looping over all keys (will be from bottom up)
			commentsDict[k].reverse()
			############## add logic here to see how many whitespace characters are on line below ##############
			for c in commentsDict[k]:	# should work :)
				self.content.insert(k, c)		# insert comments in reverse order so they appear correctly

		# comment.reverse()			# reverse comment to place comment in proper order
		# for line in comment:
		# 	fileContent.insert(index, line)
		# return fileContent		# return new version of filecontent

	# def getRegex(self):
	# 	with open('./json/languageRegexes.json', encoding='utf-8') as langInfo:
	# 		data = json.loads(langInfo.read())

	# 	self.langFuncRegex = data[self.LANG]

	def getFileContent(self):
		self.content = None
		with open(self.CURFILE) as f:
			self.content = f.readlines()
		self.content = [tmp.strip('\n') for tmp in self.content]
		# print(self.content)

	def getLines(self) -> dict:
		self.getFileContent()
		lines = self.findFuncDec(self.content)

		linesDict = dict()
		for line in lines:
			# print("Function Declared at line:", line)
			linesDict[line] = self.content[line]

		# for key in linesDict:
		# print(key, linesDict[key])
		return linesDict

	def addComment(self, commentsDict) -> None:

		self.comment(commentsDict)

		# find SAFE way to rename with numbers if the file already exists.
		rename(self.CURFILE, self.CURFILE + ".ADbak") # autodoc bak
		f = open(self.CURFILE, 'w')

		self.content = "\n".join(self.content)
		if self.content is not None:
			# print(self.content)
			f.write(self.content)

if __name__ == "__main__":
	pass