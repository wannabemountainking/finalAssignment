"""
Flask를 사용해 잡 스크래퍼의 프론트엔드를 구축합니다.
유저는 python, javascript, java 등과 같은 용어를 검색할 수 있어야 합니다.
스크래퍼는 berlinstartupjobs.com, weworkremotely.com 및 web3.career의 결과를 표시해야 합니다.
우리는 이미 berlinstartupjobs.com 스크래퍼에 대한 코드가 있으므로 weworkremotely.com 및 web3.career를 스크래핑하는 코드를 작성해야 합니다.
검색 URL은 다음과 같습니다:
https://berlinstartupjobs.com/skill-areas// where <s> is the search term (i.e https://berlinstartupjobs.com/skill-areas/python/)
https://web3.career/-jobs where <s> is the search term (i.e https://web3.career/python-jobs)
https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term= where <s> is the search term (i.e https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term=python)
"""

import re
import requests
from bs4 import BeautifulSoup
from pprint import pprint

URL = "https://berlinstartupjobs.com"
berlin_jobs_db = []

headers = {
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'Accept':
      'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5',
}

def get_berlin_job_skill_db(url, area):
	response = requests.get(f"{url}/engineering/", headers=headers)
	soup = BeautifulSoup(response.text, 'html.parser')
	berlin_job_db = []
	job_pages = soup.find_all(class_="page-numbers")
	number_of_pages = 0
	if job_pages:
		number_of_pages = len(job_pages)
	else:
		number_of_pages = 2

	for i in range(1, number_of_pages):
		if i != 1:
			new_response = requests.get(f"{url}/{area}/page/{i}", headers=headers)
			soup = BeautifulSoup(new_response.text, "html.parser")
		jobs = soup.find_all("li", class_="bjs-jlid")
		for job in jobs:
			raw_link = job.find("a")
			title = raw_link.text
			link = raw_link["href"]
			company = job.find("a", class_="bjs-jlid__b").text
			job_description = re.sub("\n|\t", "", job.find("div", class_="bjs-jlid__description").text)
			job_data = dict(
				company=company,
				job_title=title,
				job_description = job_description,
				link = link
			)
			berlin_job_db.append(job_data)
		pprint(berlin_job_db)
	return berlin_job_db

pprint(len(get_berlin_job_skill_db(URL, "engineering")))