#!/usr/bin/python

import constants99
import MySQLdb as mdb
import re
import pycurl
import redis
import checkOwner
from datetime import date

# local constants
#log_date = "'" + str(date.today()) + "'"
log_date = "'" + str(date(2014, 8, 8)) + "'"
r_server = redis.Redis(constants99.redis_url)
list_one = []
list_two = []


def log_description_ength(description):
    description_length = len(re.sub(r'\s+', '', description))
    if description_length > constants99.fo_description_threshold:
        log_it("Description", "CharLimit", str(description_length))


def log_photo_count(prop_id):
    cur.execute("SELECT count(*) as CNT FROM property.PICTURE where PROP_ID = '" + str(prop_id) + "'")
    picture_row = cur.fetchone()
    photo_count = picture_row[0]
    if photo_count > constants99.fo_photo_count_threshold:
        log_it("Property_Photo", "CountLimit", str(photo_count))


def log_email_check(profile_id):
    cur.execute("SELECT EMAIL FROM property.PROFILE where PROFILEID = '" + str(profile_id) + "'")
    email_row = cur.fetchone()
    email = str(email_row[0])
    black_list_one, black_list_two = get_black_list_words()
    for ele in black_list_one:
        if ele in email:
            log_it("Email_Id", "Email_List1", str(ele))
    for ele in black_list_two:
        if ele in email:
            log_it("Email_Id", "Email_List2", str(ele))


def log_ipadd_check(ipadd):
    count = r_server.hget('fo_ip_address_seller', str(ipadd))
    if count > constants99.fo_ipadd_theshold:
        log_it("IP_Address","PropLimit", str(count))
    r_server.hincrby("fo_ip_address_seller", str(ipadd), 1)


def log_phone_number_check(profile_id):
    cur.execute("SELECT PHONE, ALT_PHONE, MOBILE, MOBILE2, MOBILE3 FROM property.PROFILE where PROFILEID = '" + str(profile_id) + "'")
    profile_row = cur.fetchone()
    for i in range(len(profile_row)):
        if i == 0:
            label = "Phone"
        elif i == 1:
            label = "Alt_Phone"
        elif i == 2:
            label = "Mobile"
        elif i == 3:
            label = "Mobile2"
        elif i == 4:
            label = "Mpbile3"

        number = profile_row[i]
        if str(number).isdigit():
            is_registered_broker = r_server.sismember("fo_number_registered_brokers", number)
            is_crawled_broker = r_server.sismember("fo_number_crawled_broker", number)
            is_c2v_broker = r_server.sismember("fo_number_query_c2v_dealers", number)
            count_listings_with_this_number = r_server.hget('fo_number_seller', str(number))
            if is_registered_broker:
                log_it(str(label), "99BrokerProfile", str(number))
            if is_crawled_broker:
                log_it(str(label), "CrawledBrokerProfile", str(number))
            if is_c2v_broker:
                log_it(str(label), "99Identity", str(number))
            if count_listings_with_this_number > constants99.fo_listings_with_same_number_threhold:
                log_it(str(label), "TotalPosted", str(count_listings_with_this_number))


def get_black_list_words():
    if len(list_one) == 0:
        print "calculating list one"
        sql_one = "SELECT VALUE FROM static_data.SELLER_BLACKLIST_WORDS where CATEGORY = 'EMAIL_BLACKLIST_ONE'"
        cur.execute(sql_one)
        for word_row in cur.fetchall():
            list_one.append(word_row[0])

    if len(list_two) == 0:
        print "calculating list two"
        sql_two = "SELECT VALUE FROM static_data.SELLER_BLACKLIST_WORDS where CATEGORY = 'EMAIL_BLACKLIST_TWO'"
        cur.execute(sql_two)
        for word_row in cur.fetchall():
            list_two.append(word_row[0])

    return list_one, list_two


def log_it(column, reason, reason_detail):
    content = "|" + str(column) + "|" + str(reason) + "|" + str(reason_detail) + "|"
    post_data = {'headers': {'tracking': constants99.fo_flume_url}, 'body': content}
    c = pycurl.Curl()
    c.setopt(c.URL, constants99.flume_url)
    c.setopt(c.POST, True)
    c.setopt(c.RETURNTRANSFER, True)
    c.setopt(c.HTTPHEADER, array(['Content-Type: application/json']))
    c.setopt(c.POSTFIELDS, post_data)
    c.perform()


# main script execution starts here
db = mdb.connect(host=constants99.db_host, user=constants99.db_user, passwd=constants99.db_pass)
cur = db.cursor()
sql = "select PROP_ID, CLASS, DESCRIPTION, PROFILEID, IPADD from property.SELLER where " + \
      "ACTIVATED in ('Y','S')  and DATE(REGISTER_DATE) = " + log_date
cur.execute(sql)
checkowner = checkOwner.CheckOwner()
for row in cur.fetchall():
    if row[1] == 'O':  # do this only for owners
        #log_description_ength(row[2])
        #log_photo_count(row[0])
        #log_email_check(row[3])
        #log_ipadd_check(row[4])
        #log_phone_number_check(row[3])
        checkowner.addPd(row[2])
        ownerStatus = checkowner.check()
        #print(ownerStatus)

