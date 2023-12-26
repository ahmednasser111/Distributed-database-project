# pip install sqlalchemy
# pip install pyodbc
# pip install os
from sqlalchemy import create_engine, text
import pandas as pd
import os

"""
A class for us to use to access the database
"""
class data_base():
    servers = {
        'cairo': '20.25.37.239',
        'alex': '172.203.249.249',
        'psaid': '20.216.4.130'
    }
    username = "sa"
    password = "SQLServer123"
    driver = "ODBC Driver 17 for SQL Server"
    conn_strs = {
        'cairo': f"mssql+pyodbc://{username}:{password}@{servers['cairo']}/{'cairo'}?driver={driver}",
        'psaid': f"mssql+pyodbc://{username}:{password}@{servers['psaid']}/{'portsaid'}?driver={driver}",
        'alex': f"mssql+pyodbc://{username}:{password}@{servers['alex']}/{'Alexandria'}?driver={driver}"
    }

    """Uncomment if all the servers are running
    as it will give an error and the code won't
    run if else"""
    # c_engine = create_engine(conn_strs['cairo'])
    # c_con = c_engine.connect()
    # a_engine = create_engine(conn_strs['alex'])
    # a_con = a_engine.connect()
    # p_engine = create_engine(conn_strs['psaid'])
    # p_con = p_engine.connect()

    """The connection function to connect to Cairo
    server and database"""
    def cairo_update(self, pid, count):
        self.update(pid, count, self.c_con)

    """The connection function to connect to Port-Said
    server and database"""
    def psaid_update(self, pid, count):
        self.update(pid, count, self.p_con)

    """The connection function to connect to Alexandria
    server and database"""
    def alex_update(self, pid, count):
        self.update(pid, count, self.a_con)

    """General updating method to be used for all
    servers and databases"""
    def update(self, pid, count, connection):
        pid = int(pid)
        con = connection
        count = self.validate_count(pid, count, con)
        if type(count) != int:
            print("can't remove number higher than original number")
            return
        if count < 0:
            con.execute(text(f'update inventory set quantity -= {abs(count)} where pid = {pid}'))
        elif count > 0:
            con.execute(text(f'update inventory set quantity += {abs(count)} where pid = {pid}'))
        con.commit()

    """The validation for the count in order not to
    remove number more than the number in inventory"""
    def validate_count(sef, id, val, con):
        if type(val).__name__ != 'int':
            val = int(val)
        rs = con.execute(text(f'select quantity from inventory where pid={id}'))
        results = rs.fetchall()
        if val < 0:
            if abs(val) > results[0][0]:
                return ""
        return val

    """This will look in what server to update"""
    def up(self, pid, count):
        if os.environ['server'] == 'cairo':
            self.cairo_update(pid, count)
        elif os.environ['server'] == 'alex':
            self.alex_update(pid, count)
        elif os.environ['server'] == 'psaid':
            self.psaid_update(pid, count)

    """Since There will never be a wrong id
    therefore we don't need id validation"""
    # def validate_id(sef, val, con):
    #     val = int(val)
