import json
import os
import sqlite3
from urllib2 import urlopen


KEY = os.environ.get('API_KEY')

STUB = "http://capitolwords.org/api/1/phrases.json"


def main():
    api_dict = user_input()
    data = get_data(api_dict)
    manage_db(data)


def user_input():
    print "Search by specific date or month?"
    user_type = raw_input().lower()
    value = ""
    if user_type == 'month':
        print "Give the month as YYYYMM"
        value = raw_input()
    elif user_type == 'date':
        print "Give the date as YYYYMMDD"
        value = raw_input()
    else:
        user_input()

    params_dict = {'entity_type': user_type,
                   'entity_value': value,
                   'sort': 'count+desc',
                   'apikey': KEY}
    return params_dict


def get_data(api_dict):
    key_val_gen = (key + '=' + val for key, val in api_dict.items())
    query_string = '&'.join(key_val_gen)

    url = STUB + '?' + query_string

    response = urlopen(url)

    data = json.load(response)

    return data


def manage_db(data):
    keys = set()
    for d in data:
        for key in d:
            keys.add(key)
    keys = sorted(keys)

    qmark_str = ', '.join('?' * len(keys))

    conn = sqlite3.connect('sunlight.db')
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS records (" + ", ".join(keys) + ")")
    for item in data:
        values = [item.get(key) for key in keys]
        stub = "INSERT INTO records valueS ({})".format(qmark_str)
        cur.execute(stub, values)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
