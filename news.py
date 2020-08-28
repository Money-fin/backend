from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import csv
import os


chemistry_url = "https://www.yna.co.kr/search/index?query=%ED%99%94%ED%95%99&ctype=A&scope=title&page_no="
# https://www.yna.co.kr/search/index?query=%ED%99%94%ED%95%99&ctype=A&scope=title&page_no=10
#(1~50)
it_url = "https://www.yna.co.kr/search/index?query=IT&ctype=A&scope=title&page_no="
#(1~27)
bio_url = "https://www.yna.co.kr/search/index?query=%EB%B0%94%EC%9D%B4%EC%98%A4&ctype=A&scope=title&page_no="
#(1~50)

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.maximize_window()

def crawlChemistry(url):
    driver.implicitly_wait(3)
    if (url == chemistry_url):
        for i in range(1,51):
            article_links = []
            tmp = url+str(i)
            print(tmp)
            driver.get(tmp)
            articles = driver.find_element_by_class_name("cts_atclst").find_elements_by_tag_name("a")
            for article in articles:
                article_links.append(article.get_attribute("href"))
            print(article_links)
            getArticleInfo(article_links)
    elif (url == bio_url):
        for i in range(1,51):
            article_links = []
            tmp = url+str(i)
            driver.get(tmp)
            articles = driver.find_element_by_class_name("cts_atclst").find_elements_by_tag_name("a")
            for article in articles:
                article_links.append(article.get_attribute("href"))
            getArticleInfo(article_links)
    else:
        for i in range(1,28):
            article_links = []
            tmp = url+str(i)
            driver.get(tmp)
            articles = driver.find_element_by_class_name("cts_atclst").find_elements_by_tag_name("a")
            for article in articles:
                article_links.append(article.get_attribute("href"))
            getArticleInfo(article_links)

def getArticleInfo(article_links):
    for link in article_links:
        driver.implicitly_wait(3)
        driver.get(link)
        try:
            title = driver.find_element_by_class_name("tit").text
        except:
            title = ""
        try:
            time = driver.find_element_by_class_name("update-time").text
        except:
            time = ""

        try:
            image = driver.find_element_by_class_name("image-zone").find_element_by_tag_name("img").get_attribute("src")
        except:
            image = ""
        try:
            contents = ""
            total = driver.find_element_by_class_name("story-news")
            content_tag = total.find_elements_by_tag_name("p")
            for content in content_tag:
                contents+=content.text
        except:
            contents=""

        with open('chemistry.csv','a', encoding='utf-8-sig', newline='\n') as f:
            wr = csv.writer(f)
            wr.writerow([link,title,time,image,contents])
        f.close()


crawlChemistry(chemistry_url)