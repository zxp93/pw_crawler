import scrapy
from bs4 import BeautifulSoup
import re
import json

pre = "https://www.programmableweb.com"


def parse_attr(html):
    bs = BeautifulSoup(html, 'lxml')  # 初始化BeautifulSoup库,并设置解析器
    temp = bs.find_all(name='div', attrs={"class": "field"})
    print('+++++++++++++++++++++',type(temp))
    dr = re.compile(r'<[^>]+>', re.S)
    temp_dict = {}

    for i in temp:
        k = i.find_all(name="label")
        v = i.find_all(name="span")
        k = dr.sub('', str(k)).replace('[','').replace(']','')
        v = dr.sub('', str(v)).replace('[','').replace(']','')
        if k != '':
            temp_dict[k] = v

    sdks = bs.find_all(name="a", attrs={"class": "sdks"})
    articles = bs.find_all(name="a", attrs={"class": "articles"})
    how_to = bs.find_all(name="a", attrs={"class": "how-to"})
    sample_source_code = bs.find_all(name="a", attrs={"class": "sample-source-code"})
    libraries = bs.find_all(name="a", attrs={"class": "libraries"})
    developers = bs.find_all(name="a", attrs={"class": "developers"})
    followers = bs.find_all(name="a", attrs={"class": "followers"})
    changelog = bs.find_all(name="a", attrs={"class": "changelog"})
    description = bs.find_all(name="div", attrs={"class": "api_description tabs-header_description"})
    api_name = bs.find_all(name='div', attrs={"class": "node-header"})
    try:
        temp_dict['api_name'] = re.search(r'<h1.*>(.*)<\/h1>', str(api_name)).group(1).replace("(", '').replace(")", '')
    except:
        pass

    try:
        temp_dict['description'] = description[0].get_text()
    except:
        pass

    try:
        temp_dict['articles'] = int(
            re.search(r'<span.*>(.*)<\/span>', str(articles)).group(1).replace("(", '').replace(")", ''))
    except:
        pass

    try:
        temp_dict['how_to'] = int(
            re.search(r'<span.*>(.*)<\/span>', str(how_to)).group(1).replace("(", '').replace(")", ''))
    except:
        pass

    try:
        temp_dict['sdks'] = int(
            re.search(r'<span.*>(.*)<\/span>', str(sdks)).group(1).replace("(", '').replace(")", ''))
    except:
        pass

    try:
        temp_dict['sample_source_code'] = int(
            re.search(r'<span.*>(.*)<\/span>', str(sample_source_code)).group(1).replace("(", '').replace(")", ''))
    except:
        pass

    try:
        temp_dict['libraries'] = int(
            re.search(r'<span.*>(.*)<\/span>', str(libraries)).group(1).replace("(", '').replace(")", ''))
    except:
        pass

    try:
        temp_dict['developers'] = int(
            re.search(r'<span.*>(.*)<\/span>', str(developers)).group(1).replace("(", '').replace(")", ''))
    except:
        pass

    try:
        temp_dict['followers'] = int(
            re.search(r'<span.*>(.*)<\/span>', str(followers)).group(1).replace("(", '').replace(")", ''))
    except:
        pass

    try:
        temp_dict['changelogs'] = int(
            re.search(r'<span.*>(.*)<\/span>', str(changelog)).group(1).replace("(", '').replace(")", ''))
    except:
        pass
    print('===================================\n',temp_dict)
    return temp_dict


def write_data(file, data):
    w = open(file, 'a')
    w.write(data + '\n')


class web(scrapy.Spider):  # 需要继承scrapy.Spider类

    name = "api_data"  # 定义蜘蛛名

    def start_requests(self):  # 由此方法通过下面链接爬取页面

        # 定义爬取的链接
        f = open('./api_links.json', 'r')
        urls = f.readlines()
        # urls = [
        #     'https://www.programmableweb.com/apis/directory?page=0']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)  # 爬取到的页面如何处理？提交给parse方法处理

    def parse(self, response):
        '''
        start_requests已经爬取到页面，那如何提取我们想要的内容呢？那就可以在这个方法里面定义。
        这里的话，并木有定义，只是简单的把页面做了一个保存，并没有涉及提取我们想要的数据，后面会慢慢说到
        也就是用xpath、正则、或是css进行相应提取，这个例子就是让你看看scrapy运行的流程：
        1、定义链接；
        2、通过链接爬取（下载）页面；
        3、定义规则，然后提取数据；
        就是这么个流程，似不似很简单呀？
        '''
        html = response.text
        # print(html.encode('gbk', 'ignore').decode('gbk'))
        data = parse_attr(html)
        write_data('./api_data_new.json', json.dumps(data))
