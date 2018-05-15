from scrapy import cmdline

name = 'kt_spider'
cmd = 'scrapy crawl {0} -s JOBDIR=zant/002'.format(name)
cmd = 'scrapy crawl {0} '.format(name)
cmdline.execute(cmd.split())