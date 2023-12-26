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
        'alex_replication': f"mssql+pyodbc://{username}:{password}@{servers['cairo']}/{'alex_replication'}?driver={driver}",
        'psaid': f"mssql+pyodbc://{username}:{password}@{servers['psaid']}/{'portsaid'}?driver={driver}",
        'cairo_replication': f"mssql+pyodbc://{username}:{password}@{servers['psaid']}/{'cairo_replication'}?driver={driver}",
        'alex': f"mssql+pyodbc://{username}:{password}@{servers['alex']}/{'Alexandria'}?driver={driver}",
        'port_replication': f"mssql+pyodbc://{username}:{password}@{servers['alex']}/{'port_replication'}?driver={driver}",
    }

    """
    Server : Alex => port_replication
    Server : Cairo => alex_replication
    Server : Psaid => cairo_replication
    """

    """Uncomment if all the servers are running
    as it will give an error and the code won't
    run if else"""
    c_engine = create_engine(conn_strs['cairo'])
    c_con = c_engine.connect()
    # a_engine = create_engine(conn_strs['alex'])
    # a_con = a_engine.connect()
    p_engine = create_engine(conn_strs['psaid'])
    p_con = p_engine.connect()

    """The connection function to connect to Cairo
    server and database"""
    def cairo_update(self, pid, count):
        self.update(pid, count, self.c_con)
        self.update(pid, count, self.c_r_con)

    """The connection function to connect to Port-Said
    server and database"""
    def psaid_update(self, pid, count):
        self.update(pid, count, self.p_con)
        self.update(pid, count, self.p_r_con)

    """The connection function to connect to Alexandria
    server and database"""
    def alex_update(self, pid, count):
        self.update(pid, count, self.a_con)
        self.update(pid, count, self.a_r_con)

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
            con.execute(text(f'insert into transactions (pid, quantity, p_state) values ({pid}, {abs(count)}, 0)'))
        elif count > 0:
            con.execute(text(f'update inventory set quantity += {abs(count)} where pid = {pid}'))
            con.execute(text(f'insert into transactions (pid, quantity, p_state) values ({pid}, {abs(count)}, 1)'))
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

    def query(self , cities , products_id):
        results_cairo=[]

        results_alex=[]

        results_psaid=[]

        all_results=[]

        products_id=tuple(products_id)
        query=text(f'''
            SELECT p_name, sex, quantity
            FROM products
            JOIN inventory ON products.ID = inventory.pid
            WHERE products.ID IN {products_id}
        ''')
        if len(products_id) ==1:
            products_id=products_id[0]
            query=text(f'''
            SELECT p_name, sex, quantity
            FROM products
            JOIN inventory ON products.ID = inventory.pid
            WHERE products.ID = {products_id}
        ''')
        
        
        products_id=tuple(products_id)
        if "psaid" in cities:
            result=self.p_con.execute(query)
            results_psaid.append(result.fetchall())
            print(results_psaid) 
            all_results.append(results_psaid)
        if "cairo" in cities:
            result=self.c_con.execute(query)
            results_cairo.append(result.fetchall())
            print(results_cairo)
            all_results.append(results_cairo) 
        if "alex" in cities:
            result=self.a_con.execute(query)
            results_alex.append(result.fetchall())
            all_results.append(results_alex)
        return all_results
    
    """Since There will never be a wrong id
    therefore we don't need id validation"""
    # def validate_id(sef, val, con):
    #     val = int(val)