# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
"""
管道：处理数据
钩子函数 --> 回调函数（方法） --> callback
"""
import openpyxl
import pymysql


class DbPipeline:
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',#衣地数落席
            user='root',
            password='123456',
            db='spider',
            charset='utf8')
        self.cursor = self.conn.cursor()
        self.data = []

    def open_spider(self,spider):
        pass

    def close_spider(self,spider):
        if len(self.data) > 0:
            self._wirte_to_db()
        self.cursor.close()



    def process_item(self, item, spider):
        # title = item.get('title','')
        # rank = item.get('rank','')
        # subject = item.get('subject','')
        # self.data.append((title,rank,subject))
        self.data.append((item['title'], item['rank'], item['subject'], item['duration'], item['intro']))
        if len(self.data) == 100:
            self._wirte_to_db()
            self.data.clear()
        # 给其他类数据
        return item

    # 批处理
    def _wirte_to_db(self):
        self.cursor.executemany(
            'insert into tb_top_movie(title, rating,subject,duration,intro) '
            'values (%s,%s,%s,%s,%s);',
            self.data
        )
        self.conn.commit()


class ExcelPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()  # 创建工作溥对象
        # self.ws = self.wb.create_sheet()  # 创建新的工作表
        self.ws = self.wb.active  # 默认工作表
        self.ws.title = 'Top250'
        self.ws.append(('标题','评分','主题','片长','简介'))

    def open_spider(self,spider):
        pass

    def close_spider(self,spider):
        self.wb.save('电影数据.xlsx')

    # 处理数据方法 每次获得数据就执行一次，250条数据就执行250此
    def process_item(self, item, spider):
        # get 去除空值
        # title = item.get('title','')
        # rank = item.get('rank','')
        # subject = item.get('subject','')
        # 需要正则表达式处理简介
        self.ws.append((item['title'],item['rank'],item['subject'],item['duration'],item['intro'],item['number']))
        return item
