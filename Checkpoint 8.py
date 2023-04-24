import requests
import string
from bs4 import BeautifulSoup

#Get and parse HTML content
def get_html_content(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    return soup

#Extract article title
def get_article_title(soup):
    title = soup.find('title').get_text()
    return title

#Extract article text
def get_article_content(soup):
    content = {}
    for i, header in enumerate(soup.select('h2, h3, h4, h5, h6')):
        section = header.get_text().strip()
        content[section] = []
        next_node = header
        while True:
            next_node = next_node.next_sibling
            if next_node is None:
                break
            try:
                tag_name = next_node.name
            except AttributeError:
                tag_name = ""
            if tag_name in ["h2", "h3", "h4", "h5", "h6"]:
                break
            elif tag_name == "p":
                content[section].append(next_node.get_text())
    return content


#Collect links
def get_links(soup):
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('/wiki/') and not href.startswith('/wiki/File:'):
            links.append('https://en.wikipedia.org' + href)
    return links

#Wrap all the functions into a single one
def scrape_wikipedia(url):
    soup = get_html_content(url)
    title = get_article_title(soup)
    content = get_article_content(soup)
    links = get_links(soup)
    return {"title": title, "content": content, "links": links}

#Test
url = 'https://en.wikipedia.org/wiki/Algeria'
result = scrape_wikipedia(url)
print(result["title"])
print(result["content"])
print(result["links"])
