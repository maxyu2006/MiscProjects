from bs4 import BeautifulSoup
import requests

def searchJdic(word):
	searchBase = "http://www.edrdg.org/cgi-bin/wwwjdic/wwwjdic?1MUQ"
	downloadBase = "http://assets.languagepod101.com/dictionary/japanese/audiomp3.php?"

	searchWord = searchBase + word
	response = requests.get(searchWord)

	# get HTML tree for the result list and check if it is empty
	results = BeautifulSoup(response.content).find_all('div', attrs={'style':'clear: both;'})
	if(len(results) == 0):
		return "Error, no results found"

	# choose first result now; might need to modify later
	result = results[0]

	# html tree of result looks like this
	# <div style="clear:both;">
	#   <div style="...">
	#   <label for="...">
	#     <script>m("wordId we want")</script>
	# so we extract the script
	wordId = result.label.script.string

	# remove the 'm("' and ');'
	wordId = wordId.replace("m(\"","")
	wordId = wordId.replace("\");","")