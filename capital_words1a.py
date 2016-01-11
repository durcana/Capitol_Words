import json
import os
import sqlite3
from urllib2 import urlopen


KEY = os.environ.get('API_KEY')

STUB = "http://capitolwords.org/api/1/phrases.json"

print "Would you like to find the most frequent years within a specific date or month?"
Type = raw_input().lower()
while Type.lower() != 'month' and Type.lower() != 'date':
    Type = raw_input().lower()

print "Give the date as YYYYMMDD or the month as YYYYMM"
Value = raw_input()
#while isinstance(Value, int) == False and len(Value) != 6 and len(Value) != 8:
#    Value = raw_input()
#try?


params_dict = {'entity_type': Type,
               'entity_value': Value,
               'sort': 'count+desc',
               'apikey': KEY}


def main(params_dict):
    data = get_data(params_dict)
    manage_db(data)


def get_data(params_dict):
    api_dict = {'entity_type': 'month',
              'entity_value': '201007',
              'sort': 'count+desc',
              'apikey': KEY}

    api_dict.update(params_dict)

    # generator expression
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
        stub = "INSERT INTO records VALUES ({})".format(qmark_str)
        cur.execute(stub, values)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main({})