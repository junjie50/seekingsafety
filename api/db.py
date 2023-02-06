import sqlite3
from sqlite3 import Error

class Database():

    def __init__(self, db_file):
        self._conn = None
        try:
            self._conn = sqlite3.connect(db_file)
            self.create_database()
        except Error as e:
            print(e)
            self.close()

    def create_database(self):
        c = self._conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS person (person_id INTEGER PRIMARY KEY, name TEXT, nric TEXT, occupation TEXT)
            ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS worker (boss_id INTEGER, worker_id INTEGER, FOREIGN KEY(boss_id) REFERENCES PERSON(person_id), 
            FOREIGN KEY(WORKER_ID) REFERENCES PERSON(PERSON_ID))
            ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS manager (username TEXT, password TEXT, person_id TEXT, FOREIGN KEY(person_id) REFERENCES PERSON(person_id))
            ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS check_in
            (id INTEGER PRIMARY KEY, date TEXT, person_id INTEGER, img_uri TEXT, status BOOL)
            ''')
        c.close()

    def add_person(self, name, nric, occupation):
        c = self._conn.cursor()
        c.execute('''INSERT INTO person VALUES (?, ?, ?, ?)''', (None, name, nric, occupation))
        c.close()
        self._conn.commit()

    def get_id(self, nric):
        print(nric)
        c = self._conn.cursor()
        number = c.execute('''SELECT person_id FROM person WHERE nric=?''', (nric,)).fetchone()[0]
        c.close()
        return number
    
    def get_info(self, id):
        c = self._conn.cursor()
        info = c.execute('''SELECT name, nric, occupation FROM person WHERE person_id=?''', (id,)).fetchone()
        c.close()
        return info
    
    def add_worker(self, boss_id, worker_id):
        print(boss_id, worker_id)
        c = self._conn.cursor()
        c.execute('''INSERT INTO worker VALUES (?, ?)''', (boss_id, worker_id))
        c.close()
        self._conn.commit()

    def make_manager(self, nric, username, password):
        c = self._conn.cursor()
        id = self.get_id(nric)
        c.execute('''INSERT INTO manager VALUES (?, ?, ?)''', (username, password, id))
        c.close()
        self._conn.commit()
    
    def get_all_workers(self, id):
        c = self._conn.cursor()
        lst = list(map(lambda x: x, c.execute('''
        SELECT name, nric, occupation FROM person WHERE person_id in
        (SELECT worker_id FROM worker WHERE boss_id=?)
        ''', (id,)).fetchall()))
        print(lst)
        c.close()
        return lst
    
    def authenticate_admin(self, username, password):
        c = self._conn.cursor()
        usr = c.execute('''SELECT password, person_id FROM manager WHERE username=?''', (username,)).fetchone()
        c.close()
        print(usr)
        if usr == None:
            return '-1'
        elif password == usr[0]:
            return usr[1]
        else:
            return '-1'
    
    def get_checkin(self, date, nric):
        c = self._conn.cursor()
        id = self.get_id(nric)
        data = c.execute('''SELECT * FROM check_in WHERE date=? AND person_id=?''', (date, id)).fetchone()
        c.close()
        return data
    
    def is_user_checked_in(self, date, nric):
        c = self._conn.cursor()
        id = self.get_id(nric)
        data = c.execute('''SELECT * FROM check_in WHERE date=? AND person_id=?''', (date, id)).fetchone()
        print(data)
        if data and data[-1]:
            return True
        else:
            return False

    def add_checkin(self, date, nric, status):
        print("adding check in")
        c = self._conn.cursor()
        person_id = self.get_id(nric)
        data_id = self.get_checkin(date, nric)
        if not data_id:
            c.execute('''INSERT INTO check_in VALUES (?, ?, ?, ?, ?)''', (None, date, person_id, "", status))
        else:
            c.execute('''REPLACE INTO check_in (id, date, person_id, img_uri, status) VALUES (?, ?, ?, ?, ?)''', (data_id[0], date, person_id, "", status))
        c.close()
        self._conn.commit()

    def close(self):
        if self._conn:
                self._conn.close()

if __name__ == '__main__':
    db = Database('safetyseeker.db')
    # with open('../testing_data/worker.txt', 'r') as f:
    #     line = f.readline()
    #     line = f.readline()[:-1]
    #     while line:
    #         data = line.split(',')
    #         db.add_person(data[0], data[1], data[2])
    #         line = f.readline()[:-1]
    
    # with open('../testing_data/manager.txt', 'r') as f:
    #     line = f.readline()
    #     line = f.readline()[:-1]
    #     while line:
    #         data = line.split(',')
    #         db.add_worker(db.get_id(data[0]), db.get_id(data[1]))
    #         line = f.readline()[:-1]

    # db.make_manager("S4567890X", "peekingduck","password")
    # db.get_all_workers('5')
    db.close()