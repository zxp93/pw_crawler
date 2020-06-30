'''
@Description: 
@Version: 1.0
@Autor: ZhangXiangping
@Date: 2019-11-20 18:36:17
@LastEditors: ZhangXiangping
@LastEditTime: 2019-11-21 10:43:56
'''
import scrapy






pre = "https://www.programmableweb.com"

class web(scrapy.Spider): #需要继承scrapy.Spider类
    
    name = "api_links" # 定义蜘蛛名


    def start_requests(self): # 由此方法通过下面链接爬取页面
        
        # 定义爬取的链接
        urls = [
            'https://www.programmableweb.com/apis/directory?page=0']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse) #爬取到的页面如何处理？提交给parse方法处理

    def parse(self, response):

        f = open('./api_links.json', 'a')
        odd = response.css("tr.odd td.views-field.views-field-title.col-md-3 a::attr(href)").extract()
        even = response.css("tr.even td.views-field.views-field-title.col-md-3 a::attr(href)").extract()
        for item in odd:
            f.write(pre + item + "\n")
        for item in even:
            f.write(pre + item + "\n")

        next_page = response.css('li.pager-last a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)