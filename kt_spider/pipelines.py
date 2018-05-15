# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import logging

import pymysql
from scrapy.exceptions import DropItem


class KtSpiderPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host="10.106.0.88",
            user="root",
            passwd="dbtest",
            charset="utf8",
            db="tshop",
            use_unicode=True
        )

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            result = self.data_sel(item)
            if result and result[0]:
                self.data_update(item)
            else:
                self.data_add(item)
        return item

    def data_update(self, item):
        try:
            cur = self.conn.cursor()
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql_fail = "update dg_spider_post set price='%s',update_time = '%s' where sku_id = '%s'" % (item['price'], dt, item['sku_id'])
            cur.execute(sql_fail)
            result = cur.rowcount  # 返回影响行数
            self.conn.commit()
            return result
        except Exception as err:
            print(err)
        finally:
            cur.close()

    def data_sel(self, item):
        try:
            cur = self.conn.cursor()
            sql_fail = "select count(*) from dg_spider_post where sku_id = '%s'" % (item['sku_id'])
            cur.execute(sql_fail)
            result = cur.fetchone()  # 接收全部的返回结果行.
            self.conn.commit()
            return result
        except Exception as err:
            print(err)
        finally:
            cur.close()

    def data_add(self, item):
        try:
            cur = self.conn.cursor()
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql_fail = "insert into dg_spider_post (sku_id,parameters,name,price,brand,create_time,update_time,shop_flag)" \
                       'values("%s", "%s", "%s", "%s", "%s", "%s" , "%s" ,"%s")' % \
                       (item['sku_id'], item['parameters'], item['name'], item['price'],
                        item['brand'], dt, dt, '1')
            cur.execute(sql_fail)
            cur.fetchone()
            self.conn.commit()
        except Exception as err:
            print(err)
            self.conn.rollback()
            raise DropItem("Duplicated Item: {}".format(item['name']))
        finally:
            cur.close()
