"""
File: student.csv
1,Adam Kent,35.5
2,Bob,38.5
3,Chalie,40
4,Dom,25
5,Emma,30
6,Frank,40.5
7,Golder,30
8,Homy,43
9,Inna,48
10,Jacob,39
"""
from clickhouse_driver import Client, connect
import pandas as pd
import time

config = {
    'host': 'localhost',
    'database': 'myDB',
    'user': 'default',
    'password': ''
}

def read_file():
    file_data = 'student.csv'
    read_chunk = pd.read_csv(file_data, names=['id','name', 'marks'])
    return read_chunk


## Way 1 -  Client API
class ClientAPI(object):
    def __init__(self):
        self.client = Client(**config)

    def create_table(self):
        try:
            drop_query = '''drop table if exists students'''
            self.client.execute(drop_query)
            create_query = f''' CREATE TABLE students ( id Int64, name String, marks Float64 ) Engine = ReplacingMergeTree() Order by id '''
            self.client.execute(create_query)
        except Exception as err:
            print(err)

    def read_table(self):
        query = ''' Select * from students '''
        if condition:
            query += f' where {condition} '
        print(query)
        res = self.client.execute(query)
        return res

    def insert_table(self, value):
        """
        value : [[1, 'Adam Kent', 35.5], [2, 'Bob', 38.5], [3, 'Chalie', 40.0],...]
        """
        query = '''Insert into students (id, name, marks) values '''
        self.client.execute(query, value)

    def update_table(self, value):
        query =f'''Alter table students update marks=marks+5 where id in {value}'''
        print(query)
        res = self.client.execute(query)
        return res

    def main_funct(self):
        ## CREATE Table
        self.create_table()

        ## Read student.csv file
        file_data = read_file()

        ## INSERT data
        data = file_data.values.tolist()    #   [[1,'Adam',30.5],[2,'Bob',40],[3,'Cheng',45]...]
        self.insert_table(data)

        ## UPDATE data
        update_data = (3,4,5)
        self.update_table(update_data)

        ## SELECT data
        data = self.read_table()
        print(data)


## Way 2 -  DB API
class DBAPI(object):
    def __init__(self):
        self.conn = connect(**config)
        self.cursor = self.conn.cursor()

    def create_table(self):
        try:
            query = '''drop table if exists students'''
            self.cursor.execute(query)
            query = '''CREATE TABLE students ( id Int64, name String, marks Float64 ) Engine = ReplacingMergeTree() Order by id'''
            self.cursor.execute(query)
            print('Created Table: students')
        except Exception as err:
            print(err)

    def read_table(self):
        query = '''Select * from students '''
        print(query)
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    def insert_table(self, value):
        query = '''Insert into students (id, name, marks) values '''
        print(query)
        self.cursor.executemany(query, value)

    def update_table(self, value):
        query =f'''Alter table students update marks=marks+5 where id in {value}'''
        print(query)
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    def main_funct(self):
        ## CREATE Table
        self.create_table()

        ## Read student.csv file
        file_df = read_file()

        # INSERT data
        data = file_df.values.tolist()    #   [[1,'Adam',30.5],[2,'Bob',40],[3,'Cheng',45]...]
        self.insert_table(data)

        ## UPDATE data
        update_data = (1,2,3)
        self.update_table(update_data)

        ## SELECT data
        data = self.read_table()
        print(data)


# Main Function
if __name__ == '__main__':
    ## Way 1 - Client API
    client_obj = ClientAPI()
    client_obj.main_funct()

    ## Way 2 - DB API
    db_obj = DBAPI()
    db_obj.main_funct()
