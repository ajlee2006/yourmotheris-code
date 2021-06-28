from github import Github
from twython import Twython
import requests, datetime, json, os

def push(path, message, content, branch, update=False):
	g = Github(os.environ.get('GITHUB_TOKEN'))
	repo = g.get_repo("ajlee2006/yourmotheris-data")
	source = repo.get_branch("main")
	if update:  # If file already exists, update it
		contents = repo.get_contents(path, ref=branch)
		repo.update_file(contents.path, message, content, contents.sha, branch=branch)
	else:  # If file doesn't exist, create it
		repo.create_file(path, message, content, branch=branch)

def bold(input_text):
	chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
	bold_chars = "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"

	output = ""

	for character in input_text:
		if character in chars:
			output += bold_chars[chars.index(character)]
		else:
			output += character 

	return output

def cronjob():
	g = Github(os.environ.get('GITHUB_TOKEN'))
	repo = g.get_repo("ajlee2006/yourmotheris-data")

	response = requests.get("https://wordsapiv1.p.rapidapi.com/words/?partOfSpeech=adjective&random=true",
		headers = {
		'x-rapidapi-key': os.environ.get('API_KEY'),
		'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"
		})

	data = response.json()

	for i in data['results']:
		if i['partOfSpeech'] == "adjective":
			result = i
			break

	randomFact = ""
	if 'pronunciation' in data:
		if 'adjective' in data['pronunciation']:
			randomFact = "Pronunciation: /" + data['pronunciation']['adjective'] + "/"
		elif 'all' in data['pronunciation']:
			randomFact = "Pronunciation: /" + data['pronunciation']['all'] + "/"
		else:
			randomFact = "Pronunciation: /" + data['pronunciation'] + "/"
		randomFact = randomFact.replace("_","-").replace(",","ˌ").replace("'","ˈ")
	else:
		try:
			randomFact = "Similar to: " + result['similarTo'][0]
		except:
			try:
				randomFact = "Deriviation: " + result['deriviation'][0]
			except:
				pass
	randomFact = randomFact.replace("'","’").replace("`","‘")
	if 'synonyms' in result:
		synonym = "Synonyms: " + ", ".join(result['synonyms'])
	else:
		synonym = ""
		
	pastdata = requests.get("https://raw.githubusercontent.com/ajlee2006/yourmotheris-data/main/past.txt").json()['data']

	newnum = len(pastdata)+1
	time = datetime.datetime.now().astimezone().isoformat()
	
	thedata = [time, newnum, 'Your mother is', data['word'], randomFact, "Definition: " + result['definition'], synonym]

	for i in thedata:
		print(i)

	msg = json.dumps({'data': thedata})
	push("current.txt", "Update " + thedata[0] + " " + str(thedata[1]) + " " + thedata[3], msg, "main", update=True)
	
	pastdata.append(thedata)
	newpastdata = json.dumps({'data': pastdata})
	push("past.txt", "Update " + thedata[0] + " " + str(thedata[1]) + " " + thedata[3], newpastdata, "main", update=True)
	
	requests.post(os.environ.get('WEBHOOK'), data={"content":msg})
	
	twitter = Twython(os.environ.get('TWYTHON_A'),os.environ.get('TWYTHON_B'),os.environ.get('TWYTHON_C'),os.environ.get('TWYTHON_D'))
	formattedmessage = '#{}\n{}\n{}\n{}\n{}\n{}'.format(thedata[1], thedata[2], bold(thedata[3]), thedata[4], thedata[5], thedata[6])
	twitter.update_status(status=formattedmessage)

if __name__ == "__main__":
	cronjob()
