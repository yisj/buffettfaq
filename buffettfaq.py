from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pprint

driver = webdriver.Chrome()
driver.get('https://buffettfaq.com')

s = BeautifulSoup(driver.page_source, 'lxml')

ps = s.ol.find_all('p')
questions = list()
for q in ps:
	a = q.find('a')
	if a:
		print(a.text, a['href'])
		if a['href'] != '#questions':
			questions.append({
				"text": a.text,
				"href": a['href']
			})


subquestions = list()

ToC = s.find('div', id="ToC")
h2s = ToC.find_all('h2')
lis = ToC.find_all('li')

for li in lis:
	a = li.find('a')
	if a:
		subquestions.append({
			"text": a.text,
			"href": a['href']
		})

h2 = ''
for c in ToC.children:
	if c.string != None:
		cstr = c.string.strip()
		for q in questions:
			if cstr == q['text']:
				h2 = cstr
		for sq in subquestions:
			if cstr == sq['text']:
				sq['h2'] = h2

print(subquestions)

'''
paragraphs = list()
ps = s.body.find_all('p')
for p in ps:
	paragraphs.append({
		"text": p.text,
		'h3': ''
	})

articles = list()

subquestion = ''
for c in s.body.children:
	if c.string != None:
		cstr = c.string.strip()
		for sq in subquestions:
			if cstr == sq['text'].strip():
				print(cstr)
				subquestion = cstr
				next_div = c.find_next('div')
				nexts = find_all_next()
				for n in nexts:
					if n == next_div:
						print('STOP')

# print(paragraphs)
'''
articles = list()
h3s = s.body.find_all('h3')
for h3 in h3s:
	article = {
		"text": h3.text.strip(),
		"id": h3['id'],
		"paragraphs": [],
		"source": []
	}
	next_node = h3
	while True:
		next_node = next_node.next_sibling
		try:
			tag_name = next_node.name
		except AttributeError:
			tag_name = ""
		if tag_name == "p":
			if next_node.string:
				article['paragraphs'].append(next_node.string.strip())

		elif tag_name == "div":
			lis = next_node.find("li")
			for li in lis:
				article['source'].append(li.string.strip())
			break
	articles.append(article)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(articles)


driver.quit()