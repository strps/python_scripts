import sqlite3
import re
import os
import csv


file_path = os.path.join(os.path.dirname(__file__), 'files', 'WhatsApp Chat with NOTIFICATION.txt')

csv_file_path = os.path.join(os.path.dirname(__file__), 'files', 'log.csv')

connection = sqlite3.connect('db.db')
cursor = connection.cursor()

#clean table log
cursor.execute('''
    DELETE FROM log
''')

#delete table log
# cursor.execute('''
#     DROP TABLE IF EXISTS log
# ''')

#craete table log if not exists

cursor.execute('''
    CREATE TABLE IF NOT EXISTS log(
        date TEXT,
        time TEXT,
        user TEXT,
        flag TEXT,
        message TEXT,   
        datetime INTEGER, 
        PRIMARY KEY(date, time, user, flag)        
    )
''')

cursor.execute('''
               CREATE TABLE IF NOT EXISTS flag(
                    flag TEXT PRIMARY KEY,
                    description TEXT
                )   
''')

users ={
    "César": "César",
    "Jefferson": "Jefferson Soto Achia",
    "Orlando": "Orlando Flores",
}

flags = [
    {'flag': 'B1', 'description': 'Descanso 1'},
    {'flag': 'B2', 'description': 'Descanso 2'},
    {'flag': 'LCH', 'description': 'Almuerzo'},
    {'flag': 'OUT', 'description': 'Salida'},
    {'flag': 'EMR', 'description': 'Emergencia'},
    {'flag': 'COR', 'description': 'Corrección'},    
    {'flag': 'BTW', 'description': 'Back to work'},    
]              


flags_regex_str = '|'.join([f['flag'] for f in flags]) 
flags_regex_str = f'({flags_regex_str})'

notification_regex = re.compile(r'(\d{1,2}/\d{1,2}/\d{1,2}), (\d{2}:\d{2}) - (.*): (B1|B2|LCH|OUT|EMR|COR|BTW)([\s\S]*)')

file = open(file_path, "r")
for line in file:
    regex_match = notification_regex.match(line)
    if regex_match:
        date = regex_match.group(1)
        time = regex_match.group(2)
        user = regex_match.group(3)
        flag = regex_match.group(4)
        message = regex_match.group(5)
        # message = "mssg"
        message = message.strip()
        message = message.replace('\n', '')
        if message == '':
            message = "N/A"
        print(f'date: {date} time: {time} user: {user} flag: {flag} message: {message}')

        cursor.execute('''
            INSERT INTO log(date, time, user, flag, message)
            VALUES(?, ?, ?, ?, ?)
                    ON CONFLICT(date, time, user, flag) 
                    DO 
                       UPDATE SET message = excluded.message
        ''', (date, time, user, flag, message))
        connection.commit()

file.close()
#select all data from log table
res = cursor.execute('''
    SELECT 
        date AS date,
        time AS time,
        user AS user,
        flag AS flag,
        message AS message
    FROM log
''')


#write to csv
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file, dialect='excel', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['date', 'time', 'user', 'flag', 'message'])
    for row in res.fetchall():
        writer.writerow([row[0], row[1], row[2], row[3], row[4] ])
        # print(row)

connection.close()

