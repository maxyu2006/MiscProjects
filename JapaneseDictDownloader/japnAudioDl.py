#coding:utf8
from bs4 import BeautifulSoup
import requests
import hashlib
import re

FAIL_TEXT = "Error, no results found"
SUCCESS_TEXT = "Success"
ANKI_MEDIA = "C:\\Users\\maxyu\\AppData\\Roaming\\Anki2\\User 1\\collection.media"

def parseFile(filename, chapterToMatch):
	matchAudio = re.compile("ch_[0-9][0-9]_audio")
	audioFolder = "media"
	readFile = open(filename + ".txt", encoding="utf8")

	#split is to retrieve the text before the extension
	outputFile = open(filename + "_out.txt", "wt", encoding="utf8")
	logFile = open(filename + "_log.txt", "wt", encoding="utf8")

	# read each line of input file
	currentLine = readFile.readline()
	lineCounter = 1
	while (len(currentLine) != 0):
		lineElements = currentLine.rstrip('\n').split("\t")

		vocabWord = lineElements[0]
		chapterTags = lineElements[7].split(' ') # the entry may have more than one tag

		# checks to see if the desired chapter is in the tags list; if it isn't then skip
		if(chapterToMatch not in chapterTags):
			# end of loop tasks
			currentLine = readFile.readline()
			lineCounter = lineCounter + 1
			continue

		# attempt a search; if no match is found, then mark the vocab word
		logFile.write("Searching line\t" + str(lineCounter) + ": " + vocabWord + "\n")
		logFile.flush()
		searchResult = searchSequence(vocabWord, logFile)
		if(searchResult is None):
			# Mark the entry if it is not already
			if("marked" not in chapterTags):
				lineElements[7] = lineElements[7] + " marked"
		else:
			# The search succeeded, write the audio file
			audioFileName = chapterTags[0] + "_" + vocabWord + ".mp3"
			writeAudioFile(audioFolder, audioFileName, searchResult)

			# Update the sound entry
			lineElements[6] = "[sound:" + audioFileName + "]"

			outputFile.write("\t".join(lineElements)+"\n")
			outputFile.flush()

		# end of loop tasks
		currentLine = readFile.readline()
		lineCounter = lineCounter + 1

	readFile.close()
	logFile.close()
	outputFile.close()
	return SUCCESS_TEXT

# Searches the sources in order and returns the result if found
def searchSequence(word, logFile):
	# first try searching in ojad, returns the raw content of the audio file
	searchResult = searchOjad(word, logFile)
	#logFile.write(str(resultString) +"\n")

	# if failed Ojad, log and try Jdic
	if(searchResult is None):
		logFile.write("not found in ojad, trying jdic\n")
		logFile.flush()

		# update resultString with fallback source
		searchResult = searchJdic(word, logFile)

	# if failed again, log and mark the file, otherwise update the line entry
	if(searchResult is None):
		logFile.write("not found in jdic\n")
		logFile.flush() #ensure stuff is written for debugging

	return searchResult

def writeAudioFile(folder, filename, bytestr):
	toWrite = open(folder + "\\" + filename, "w+b")
	toWrite.write(bytestr)
	toWrite.flush()
	toWrite.close()
	return True

def searchOjad(word, logFile):
	searchBase = "http://www.gavo.t.u-tokyo.ac.jp/ojad/search/index/sortprefix:accent/narabi1:kata_asc/narabi2:accent_asc/narabi3:mola_asc/yure:visible/curve:invisible/details:visible/limit:100/word:"
	downloadBase = "http://www.gavo.t.u-tokyo.ac.jp/ojad/ajax/wave_download/"

	searchWord = searchBase + word
	response = requests.get(searchWord)

	wordPage = BeautifulSoup(response.content)
	results = wordPage.find_all('div', attrs={'id':'search_result'})

	if results[0].table is None:
		logFile.write("opjad table is none\n")
		return None

	# results parse tree looke like
	# <div id="search_result">
	#   <table id="word_table"
	#     <thead>
	#     <tfoot>
	#     <tbody>
	#       <tr id="word_####">
	wordId = results[0].table.tbody.tr['id'].split('_')[1]

	# do some processing on the the verb form of the word
	form = 1 #standard dictionary form
	if word.endswith("ます"):
		form = 2

	# build the request url for downloading the actual audio clip and get
	downloadId = wordId + "_" + str(form) + "_1_male"
	downloadUrl = downloadBase + "/" + downloadId + "/" + downloadId
	response = requests.get(downloadUrl)

	# checks to see if file not found
	if(response.content.find(b"file not found:") != -1):
		logFile.write("file not found\n")
		return None

	return response.content

def searchJdic(word, logFile):
	searchBase = "http://www.edrdg.org/cgi-bin/wwwjdic/wwwjdic?1MUQ"
	downloadBase = "http://assets.languagepod101.com/dictionary/japanese/audiomp3.php?"
	failedAudio = b"7E2C2F954EF6051373BA916F000168DC"

	searchWord = searchBase + word
	response = requests.get(searchWord)

	# get HTML tree for the result list and check if it is empty
	results = BeautifulSoup(response.content).find_all('div', attrs={'style':'clear: both;'})
	if(len(results) == 0):
		logFile.write("Results length is 0")
		return None

	# choose first result now; might need to modify later
	result = results[0]

	# html tree of result looks like this
	# <div style="clear:both;">
	#   <div style="...">
	#   <label for="...">
	#     <script>m("wordId we want")</script>
	# so we extract the script
	wordId = result.label.script
	if(wordId is None):
		logFile.write(FAIL_TEXT + " first result has no audio\n")
		return None
	else:
		wordId = wordId.string

	# remove the 'm("' and ');'
	wordId = wordId.replace("m(\"","")
	wordId = wordId.replace("\");","")

	# sanatize the unicode chars
	wordId = wordId.replace("%25", "%")
	wordId = wordId.replace("%26", "&")

	# build request url for downnloading audio file and get
	downloadUrl = downloadBase + wordId
	response = requests.get(downloadUrl)

	# check via hash to see if the audio is valid
	validCheck = hashlib.md5()
	validCheck.update(response.content)
	if(validCheck.digest() == failedAudio):
		logFile.write(FAIL_TEXT + " audio\n")
		return None

	return response.content
