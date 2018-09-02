import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

connect = 'mysql+pymysql://root:@localhost/finance'