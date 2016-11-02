# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import FormRequest
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString, Comment


class WeiboSpider(scrapy.Spider):
    name = "weibo"

    def start_requests(self):
        urls = ['http://s.weibo.com/weibo/G20&typeall=1&suball=1&timescope=custom:2016-09-05-0:2016-09-19-21&page=', 'http://s.weibo.com/weibo/G20&typeall=1&suball=1&timescope=custom:2016-08-30-0:2016-09-06-15&page=', 'http://s.weibo.com/weibo/%25E4%25BA%25BA%25E6%25B0%2591%25E5%25B8%2581%2520SDR&xsort=hot&suball=1&timescope=custom:2016-10-01-0:2016-10-02-0&page=', 'http://s.weibo.com/weibo/G20&typeall=1&suball=1&timescope=custom:2016-07-25-0:2016-08-10-0&page=']
        cnts = [47, 45, 47, 47]

        cookie_dict = {}
        cookie_dict['_T_WM'] = '***'
        cookie_dict['WEIBOCN_FROM'] = 'feed'
        cookie_dict['ALF'] = '147919****'
        cookie_dict['SCF'] = '***'
        cookie_dict['SUBP'] = '***'
        cookie_dict['SUHB'] = '***
        cookie_dict['SSOLoginState'] = '147660****'
        cookie_dict['SUB'] = '***'
        cookie_dict['gsid_CTandWM'] = '***'

        i = 0
        while(i < len(urls)):
            cnt = 1
            while (cnt <= cnts[i]):
                yield FormRequest(url=urls[i]+str(cnt), callback=self.parse, cookies=cookie_dict)
                cnt += 1
            i += 1

    def parse(self, response):
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
                f = file('bu.txt', 'a+')
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
