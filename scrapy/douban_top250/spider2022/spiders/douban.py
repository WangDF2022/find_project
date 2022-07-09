# 爬虫
import scrapy
from scrapy import Selector, Request
# url拼接
from scrapy.http import HtmlResponse

from spider2022.items import MovieItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    # start_urls = ['https://movie.douban.com/top250']

    # 完美的翻页爬取
    def start_requests(self):
        for page in range(1):
            yield Request(url=f'https://movie.douban.com/top250?start={page * 25}&filter=')  # meta={‘proxy’:''} 可以加代理,如果拒绝访问

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        # content > div > div.article > ol > li:nth-child(1) 找到要爬的内容
        list_items = sel.css('#content > div > div.article > ol > li')
        # sel.xpath('//*[@id="content"]/div/div[1]/ol/li[1]')
        for i in list_items:
            detail_url = i.css('div.info > div.hd > a::attr(href)').extract_first()
            movie_item = MovieItem()
            # movie_item['title'] = i.css('span.title::text').extract_first() or ''

            movie_item['title'] = i.css('span.title::text').extract_first() or ''
            movie_item['rank'] = i.css('span.rating_num::text').extract_first() or ''
            movie_item['subject'] = i.css('span.inq::text').extract_first() or ''
            movie_item['number'] = i.css('div > div.info > div.bd > div > span::text').extract()[-1] or ''
            yield Request(url=detail_url,callback=self.parse_detail,cb_kwargs={'item':movie_item})  # 爬第二页，回调，传入字典。

        # # 翻页继续爬 第一页会有问题。
        # href_list = sel.css('div.paginator > a::attr(href)')
        # for href in href_list:
        #     url = response.urljoin(href.extract())
        #     yield Request(url=url)

    def parse_detail(self, response: HtmlResponse, **kwargs):
        movie_item = kwargs['item']
        sel = Selector(response)
        # 直接使用extract（），在excel里输入会报错
        movie_item['duration'] = sel.css('span[property="v:runtime"]::attr(content)').extract_first() or ''
        # movie_item['duration'] = sel.css('span[property="v:runtime"]::attr(content)').get() or ''
        movie_item['intro'] = sel.css('span[property="v:summary"]::text').extract_first() or ''
        # movie_item['intro'] = sel.css('span[property="v:summary"]::text').get() or ''
        yield movie_item