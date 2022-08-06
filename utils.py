import requests
from bs4 import BeautifulSoup
import obj_comparison
import time

WEBHOOK_URL = "https://discordapp.com/api/webhooks/825435452256550922/VW8rXr0vWCXiI9GzF2iP12v_87OMrndekWOcH-0gODu5J4FIsypXYTLcfGjVrXQ_gnql"

class Roadmap:
    SELECTOR = "#rt-mainbody > div"
    def __init__(self, url):
        self.url = url
        self.soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        self.content = self.soup.select_one(self.SELECTOR)

        self.categories = [Category(c) for c in self.content.findChildren("div", recursive=False)]


class Category:
    def __init__(self, categoryElement):
        self.categoryElement = categoryElement
        self.name = self.getName()
        self.issues = self.getIssues()
    
    def getName(self):
        return self.categoryElement.find('div', {"class": "kheader"}).find('h2').text

    def getIssues(self):
        issues = self.categoryElement.find('div', {"class": "kbody"}).find_all('tr', {"class": "krow2"})
        return [Issue(issue) for issue in issues]

class Issue:
    def __init__(self, issueElement):
        self.issueElement = issueElement
        columns = self.issueElement.findChildren('td', recursive=False)

        self.id = columns[0].text
        self.assigneeImg = columns[1].find('img')['src']
        self.assignee = columns[2].text
        self.name = columns[3].text
        self.description = columns[4].text
        self.created = columns[5].text

    def __str__(self):
        return self.name
