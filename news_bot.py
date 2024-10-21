import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json


# Getting G1 Politics News HTML and creating a BeautifulSoup object
with requests.session() as s:
    url = 'https://g1.globo.com/politica/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    req = s.get(url, headers=headers)
soup = BeautifulSoup(req.content, 'html.parser')

# Extracting the main news and saving on a list
news_part1 = soup.select('._evt .bastian-feed-item h2 a')
# Extracting older news that loads from a javascript after scroll
news_part2 = json.loads(soup.find_all('script', id='bstn-launcher-bundle')[0].get_text().split('"items":')[1].split(']')[0]+']')


# Searching for the URL and title of each news on both lists and saving in a dictionary
news_list = []

for news_info in news_part1:
    news_dict = {}
    news_dict['url'] = news_info['href']
    news_dict['title'] = news_info.text.strip()
    news_list.append(news_dict)
    
for news_info in news_part2:
    news_dict = {}
    news_dict['url'] = news_info['content']['url']
    news_dict['title'] = news_info['content']['title'].strip()
    news_list.append(news_dict)

#removing news that are only video
news_list = [news for news in news_list if not '/video/' in news['url']]


#selecting the latest 15 news and extracting its content, and saving on the dictionary
news_for_summary = 15
for news in news_list[:news_for_summary]:

    print(news['title'])

    with requests.session() as s:
        news_url = news['url']
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        news_req = s.get(news_url, headers=headers)
    news_soup = BeautifulSoup(news_req.content, 'html.parser')
    news_content = "\n".join([content_box.text.strip() for content_box in news_soup.select('.content-text__container')])
    news['content'] = news_content

# creating a txt file with each news title and its content
all_news = ''
for news in news_list[:news_for_summary]:
    title = news['title']
    content = news['content']
    all_news += (f'''
### {title}
{content}
#######
\n
''')
    
# creating a txt file with each news title and its url
news_source = ''
for news in news_list[:news_for_summary]:
    title = news['title']
    url = news['url']
    news_source += (f'''
*{title}*
{url}
''')

#saving both files
with open('news.txt', 'w', encoding='utf-8') as file:
    file.write(all_news)
with open('source.txt', 'w', encoding='utf-8') as file:
    file.write(news_source)