__author__ = 'roopam'

# this script updates the following sets to be used while checking for fake owners
# fo_number_registered_brokers
# fo_number_query_c2v_dealers
# fo_ip_address_seller
# fo_number_sellers
# fo_number_crawled_broker

import constants99
import MySQLdb as mdb
import redis
import re
import csv

r_server = redis.Redis(constants99.redis_url)

def update_fo_email_list():
    offset = 0
    sql_delete = "delete from static_data.SELLER_BLACKLIST_WORDS where CATEGORY = 'EMAIL_BLACKLIST_ONE' and META is NULL"
    cur.execute(sql_delete)
    print "done deleting"
    while True:
        sql = "select URL from property.PROFILE where CLASS in ('A', 'B') and URL != '' limit "+str(offset*1000)+",1000"
        cur.execute(sql)
        rowCount = cur.rowcount
        print rowCount
        for row in cur.fetchall():
            url = row[0]
            url = re.sub(r"http|https|://|www.|", '', url).split(".")[0]
            if re.match(r'\S{3,}', url):
                sql_insert = "INSERT INTO static_data.SELLER_BLACKLIST_WORDS (`CATEGORY`, `VALUE`) " + \
                             "values ('EMAIL_BLACKLIST_TWO', '"+url+"')"
                cur.execute(sql_insert)
        if rowCount < 1000:
            break
        offset += 1


def update_fo_number_registered_brokers():
    offset = 0
    r_server.delete("fo_number_registered_brokers")
    while True:
        sql = "select PHONE,ALT_PHONE,MOBILE, MOBILE2, MOBILE3 from property.PROFILE " + \
              "where CLASS in ('A', 'B') and ACTIVATED='Y' limit "+str(offset*1000)+",1000"
        cur.execute(sql)
        rowCount = cur.rowcount
        print rowCount
        for row in cur.fetchall():
            numList = filter(lambda x: str(x).isdigit() == True, row)
            for element in numList:
                r_server.sadd("fo_number_registered_brokers", element)
        if rowCount < 1000:
            break
        offset += 1


def update_fo_number_query_c2v_dealers():
    r_server.delete("fo_number_query_c2v_dealers")
    tables = 'QUERY', 'QUERY_AGENT', 'QUERY_HOMEPAGE', 'QUERY_NEWPROJECTS', 'C2V_PROPERTY', 'C2V_AGENT', 'C2V_NEWPROJECT'
    for table in tables :
        offset = 0
        while True:
            sql = "select PHONE, IDENTITY from property.`"+table+"` limit "+str(offset*1000)+",1000"
            cur.execute(sql)
            rowCount = cur.rowcount
            print rowCount
            for row in cur.fetchall():
                if str(row[0]).isdigit() and row[1]=='D':
                    r_server.sadd("fo_number_query_c2v_dealers", row[0])
            if rowCount < 1000:
                break
            offset += 1


def update_fo_ip_address_seller() :
    r_server.delete("fo_ip_address_seller")
    offset = 0
    while True:
        sql = "select IPADD from property.SELLER limit "+str(offset*1000)+",1000"
        cur.execute(sql)
        rowCount = cur.rowcount
        print rowCount
        for row in cur.fetchall():
            r_server.hincrby("fo_ip_address_seller", row[0], 1)
        if rowCount < 1000:
            break
        offset += 1
        if offset > 1:
            break


def update_fo_number_seller() :
    r_server.delete("fo_number_seller")
    offset = 0
    while True :
        sql = "select p.PHONE,p.ALT_PHONE,p.MOBILE, p.MOBILE2, p.MOBILE3 from property.SELLER s " + \
              "left join property.PROFILE p on s.PROFILEID = p.PROFILEID limit "+str(offset*1000)+",1000"
        cur.execute(sql)
        rowCount = cur.rowcount
        print rowCount
        for row in cur.fetchall():
            numList = filter(lambda x: str(x).isdigit() == True, row)
            for element in numList:
                r_server.hincrby("fo_number_seller", element, 1)
        if rowCount < 1000:
            break
        offset += 1


def update_fo_number_crawled_broker():
    with open('AllCrawledDataBrokerPhones.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ',quotechar='|')
        for row in reader:
            r_server.sadd("fo_number_crawled_broker", row[0])

db = mdb.connect(host=constants99.db_host, user=constants99.db_user, passwd=constants99.db_pass)
cur = db.cursor()

#main script execution
update_fo_email_list()
update_fo_number_registered_brokers()
update_fo_number_query_c2v_dealers()
update_fo_ip_address_seller()
update_fo_number_seller()
update_fo_number_crawled_broker()