from pyspider.libs.base_handler import *
import pymysql

class Handler(BaseHandler):
    crawl_config = {

    }
    #
    # def __init__(self):
    #     self.db = pymysql.Connect('localhost', 'localhost', '123456', data=)


    start_url = 'http://www.zhuanzhuan.com/'
    grab_url = 'http://zhuanzhuan.58.com/detail/744782895816835076z.shtml'
    @every(minutes=24*60)
    def on_start(self):
        self.crawl(self.start_url, callback=self.channel_page)

    @config(age=10*24*60*60)
    def channel_page(self, response):
        for each in response.doc('a[href^="http://cd.58.com/"').items():
            self.crawl(each.attr.href, callback=self.grab_index)

    @config(age=10*24*60*60)
    def grab_index(self, response):
        for each in response.doc('a[href^="http://zhuanzhuan.58.com/detail/"').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(age=10*24*60*60)
    def detail_page(self, response):
        title = response.doc('h1').text()
        place = response.doc('div.palce_li > span > i').text()
        price = response.doc('div.price_li > span > i').text()
        quality = response.doc('div.info_massege.left > div.biaoqian_li').text()

        # self.add_question(title, content)
        return {
            'title': title,
            'place': place,
            'price': price,
            'quality': quality,
        }
