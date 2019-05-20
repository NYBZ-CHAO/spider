# spider
pip install Scrapy

#下载对应版本  
https://www.lfd.uci.edu/~gohlke/pythonlibs/ 
例如：python 3.6 --》 Twisted-17.9.0-cp36-cp36m-win_amd64.whl

python -m pip install pypiwin32

scrapy startproject projectName (创建scrapy项目)

格式：scrapy crawl+爬虫名  –nolog即不显示日志
example:scrapy crawl xiaohau --nolog 

//scrapy的暂停与重启
scrapy crawl jingdong -s JOBDIR=zant/001

linux python3.6.5 安装

确保系统中已经有了所有必要的开发依赖：
# yum -y groupinstall development
# yum -y install zlib-devel
在 Debian 中，我们需要安装 gcc、make 和 zlib 压缩/解压缩库：
# aptitude -y install gcc make zlib1g-dev

##################################
wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz 获取安装包
tar -zxf Python-3.6.5.tgz  解压缩
cd Python-3.6.5   定位到文件夹
./configure  添加配置
make && make install  编译源码 执行安装
##################################################

yum install gcc libffi-devel openssl-devel libxml2 libxslt-devel libxml2-devel python-devel -y   ##首先准备环境
 
pip  安装
phthon3 -m pip install scrapy

报错原因：没有安装Twisted
wget https://twistedmatrix.com/Releases/Twisted/17.9/Twisted-17.9.0.tar.bz2
tar -xvf Twisted-17.9.0.tar.bz2
cd Twisted-15.2.1
python3 setup.py install

################################################

phthon3 slqite3 安装问题
$ wget https://www.sqlite.org/2017/sqlite-autoconf-3170000.tar.gz --no-check-certificate
$ tar zxvf sqlite-autoconf-3170000.tar.gz
$ cd sqlite-autoconf-3170000
$ ./configure --prefix=/usr/local/sqlite3 --disable-static --enable-fts5 --enable-json1 CFLAGS="-g -O2 -DSQLITE_ENABLE_FTS3=1 -DSQLITE_ENABLE_FTS4=1 -DSQLITE_ENABLE_RTREE=1"

（2）对python3进行重新编译
$ cd Python-3.6.2
$ LD_RUN_PATH=/usr/local/sqlite3/lib ./configure LDFLAGS="-L/usr/local/sqlite3/lib" CPPFLAGS="-I /usr/local/sqlite3/include"
$ LD_RUN_PATH=/usr/local/sqlite3/lib make
$ LD_RUN_PATH=/usr/local/sqlite3/lib sudo make install
