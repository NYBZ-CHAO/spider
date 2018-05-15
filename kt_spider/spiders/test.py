import datetime

import pymysql

from kt_spider.items import KtSpiderItem


class dbTest:
    def __init__(self):
        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            passwd="123456",
            charset="utf8",
            db="dg_spider",
            use_unicode=True
        )

    def data_updata(self, item):
        try:
            cur = self.conn.cursor()
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql_fail = "update dg_spider_post set price='%s',update_time = '%s' where sku_id = '%s'" % (item['price'],dt,item['sku_id'])
            cur.execute(sql_fail)
            result = cur.rowcount
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


db = dbTest()

item = KtSpiderItem()
item['price'] ='2999'
item['sku_id'] = '4031578'
# result = db.data_sel(item)
result = db.data_updata(item)

