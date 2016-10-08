# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import FormRequest
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString, Comment


class WeiboSpider(scrapy.Spider):
    name = "weibo"

    def start_requests(self):
        # url = 'http://weibo.cn/search/mblog/?keyword=%23G20%23&vt=4&PHPSESSID=&page='
        url = 'http://s.weibo.com/weibo/G20&b=1&page='
        cookie_dict = {}
        
        cnt = 1
        while (cnt <= 50):
            yield FormRequest(url=url+str(cnt), callback=self.parse, cookies=cookie_dict)
            cnt += 1

    def parse(self, response):
        print response.body
        f = file('1.html', 'w')
        num = 0
        for item in response.body.split('<script>STK && STK.pageletM && STK.pageletM.view('):
            if(num==0):
                num=1
                continue
            real_html = json.loads(item.split('</script>')[0].strip().rstrip(")"))['html']
            soup = BeautifulSoup(real_html, 'lxml')
            self.finditem(soup)

    def finditem(self, soup):
        for item in soup.find_all('div', attrs={'class':'WB_cardwrap'}):
            if item.find('div', class_='feed_content'):
                f = file('1.txt', 'a+')
                comment_txt = item.find('p', class_='comment_txt').get_text().strip().split(u'展开全文')[0].strip('.').strip()
                f.write(comment_txt.encode('utf-8'))
                f.write('\t')
                date = item.find('div', class_='feed_from W_textb').find('a')['title']
                f.write(date)
                f.write('\t')
                timestamp = int(item.find('div', class_='feed_from W_textb').find('a')['date'])/1000
                f.write(str(timestamp))
                f.write('\t')
                cnt = 0
                element_list = ['转发', '评论', '赞']
                for element in item.find('ul', class_='feed_action_row4').find_all('li'):
                    if(cnt >= 1):
                        num = 0
                        if element.find('em') and element.find('em').get_text():
                            try:
                                num = int(element.find('em').get_text())
                            except ValueError:
                                num = 0
                        f.write(str(num))
                        f.write('\t')
                    cnt += 1
                f.write('\n')
                f.close()
        # print response.body
        # soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf8')
        # f.write(str(soup))
        # f.close
        # print soup.find_all('div', class_=)
        # print soup.find_all('div', attrs={'class':'WB_cardwrap'})
        # allow_element = [u'赞', u'转', u'评']
        # for item in soup.find_all('div', class_='c'):
        #     pos = 0
        #     for elements in item.children:
        #         try:
        #             if elements.find('span', class_='ctt'):
        #                 item_text = ''
        #                 for part in elements.find('span', class_='ctt').children:
        #                     if isinstance(part, NavigableString):
        #                         item_text += part
        #                     else:
        #                         item_text += part.get_text()
        #                 print item_text.lstrip(':'),
        #         except TypeError:
        #             continue
        #         if isinstance(elements, NavigableString):
        #             continue
        #         for element in elements.children:
        #             if isinstance(element, NavigableString):
        #                 continue
        #             if element.get_text()[0:1] in allow_element:
        #                 print element.get_text(),
        #         print
