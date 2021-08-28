from bs4 import BeautifulSoup
import requests

def searchOjad(word):
	searchBase = "http://www.gavo.t.u-tokyo.ac.jp/ojad/search/index/sortprefix:accent/narabi1:kata_asc/narabi2:accent_asc/narabi3:mola_asc/yure:visible/curve:invisible/details:visible/limit:100/word:"
	downloadBase = "http://www.gavo.t.u-tokyo.ac.jp/ojad/ajax/wave_download/"

	searchWord = searchBase + word
	response = requests.get(searchWord)

	wordPage = BeautifulSoup(response.content)
	results = wordPage.find_all('div', attrs={'id':'search_result'})

	if len(results) == 0:
		return "Error, no results found"

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

	downloadId = wordId + "_" + str(form) + "_1_male"
	downloadUrl = downloadBase + "/" + downloadId + "/" + downloadId
	response = requests.get(downloadUrl)

	toWrite = open(word + ".mp3", "w+b")
	toWrite.write(response.content)
	toWrite.flush()
	toWrite.close()

	return "Success"