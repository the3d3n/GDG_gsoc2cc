import requests
import json
from bs4 import BeautifulSoup as bsp
from flask import Flask

main_org_url = 'https://summerofcode.withgoogle.com/archive/2017/organizations/'
base_url = "https://summerofcode.withgoogle.com"
app = Flask(__name__)

@app.route('/org_info')
def org_info():
    fetch = requests.get(main_org_url)
    html = fetch.content
    b_soup1 = bsp(html, "html.parser")
    fetch_org = b_soup1.findAll("li", {'class': 'organization-card__container'})
    final_result = get_details(fetch_org)
    print(final_result)
    return json.dumps(final_result)


def get_details(fetch_org):
    extracted_result = list()
    count = 0
    for item in fetch_org:
        purl = item.find('a', {'class': 'organization-card__link'})
        organisation_name = item['aria-label']

        information = item.find('div', {'class': 'organization-card__tagline font-black-54'})
        information = information.text
        p_link = base_url + purl['href']
        page = requests.get(p_link)
        if page.status_code != 200:
            break
        p_link = base_url + purl['href']
        response1 = requests.get(p_link)
        html1 = response1.content
        b_soup2 = bsp(html1, "html.parser")
        organisation_link = b_soup2.find("a", {"class": "org__link"})
        organisation_link = organisation_link.text
        tech_info = b_soup2.findAll("li", {"class": "organization__tag organization__tag--technology"})
        technology = []
        for t_tech in tech_info:
            technology.append(t_tech.text)
        t_topics = b_soup2.findAll("li", {"class": "organization__tag organization__tag--topic"})
        topics = []
        for i in t_topics:
            topics.append(i.text)
        count += 1
        print(count)
        extracted_result.append({
            'organization_name': organisation_name,
            'description': information,
            'link': organisation_link,
            'technologies': technology,
            'topics': topics
        })
	#Extracting Only 15 organization details Change below count value to get details of more.
        if count == 15:
            return extracted_result


if __name__ == "__main__":
    app.run(debug=True)

