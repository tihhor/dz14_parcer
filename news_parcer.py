import requests, pprint, json
from bs4 import BeautifulSoup

def pars_page(link):
    posts = []
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    pages = soup.find_all('div', class_='wp-block-post-date has-small-font-size')

    for page in pages:
        element1 = page.find("a")
        element2 = element1.get('href')
        posts.append([element1.text, element2])
    # print(posts)
    return posts

url = 'http://iprostak.ru/ru_RU/'

response = requests.get(url)

# Создаем суп для разбора html
soup = BeautifulSoup(response.content, 'html.parser')

posts =[]

pages = soup.find_all('div', class_='wp-block-post-date has-small-font-size')
# обрабатываем данные первой страницы (она же главаная страница сайта)

for page in pages:
    element1 = page.find("a")
    element2 = element1.get('href')
    posts.append([element1.text, element2])

# получаем список следующих страниц
next_pages = soup.find_all('a', class_='page-numbers')

for next_page in next_pages:
    # получаем сылку на следующую страницу
    link1 = next_page.get("href")
    # парсим страницу по ссылке
    next_posts = pars_page(link1)
    for next_post in next_posts:
        posts.append(next_post)

# печатаем итоги парсинга и ссылки на найденные страницы
print('Всего публикаций '+str(len(posts)))
for post in posts:
    print(post[0], post[1])

with open('parced_data.txt', 'w') as datafile:
    json.dump(posts, datafile)






