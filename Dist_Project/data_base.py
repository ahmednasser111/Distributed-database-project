# pip install sqlalchemy
# pip install pyodbc
# pip install os
from sqlalchemy import create_engine, text
import pandas as pd
import os
from datetime import datetime

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
    a_engine = create_engine(conn_strs['alex'])
    a_con = a_engine.connect()
    # p_engine = create_engine(conn_strs['psaid'])
    # p_con = p_engine.connect()
    # c_r_engine = create_engine(conn_strs['cairo_replication'])
    # c_r_con = c_r_engine.connect()
    a_r_engine = create_engine(conn_strs['alex_replication'])
    a_r_con = a_r_engine.connect()
    p_r_engine = create_engine(conn_strs['port_replication'])
    p_r_con = p_r_engine.connect()

    connections = {
        "cairo": c_con,
        "alex": a_con,
        # "psaid": p_con
    }

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
        current_datetime = datetime.now()
        year = current_datetime.year
        month = current_datetime.month
        day = current_datetime.day
        hour = current_datetime.hour
        minute = current_datetime.minute
        second = current_datetime.second
        if count < 0:
            con.execute(text(f"update inventory set quantity -= {abs(count)} where pid = {pid}"))
            con.execute(text(f"insert into transactions (pid, quantity, p_state,p_timestamp) values ({pid}, {abs(count)}, 0, '{year}-{month}-{day}T{hour}:{minute}:{second}')"))
        elif count > 0:
            con.execute(text(f"update inventory set quantity += {abs(count)} where pid = {pid}"))
            con.execute(text(f"insert into transactions (pid, quantity, p_state,p_timestamp) values ({pid}, {abs(count)}, 1, '{year}-{month}-{day}T{hour}:{minute}:{second}')"))
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

    # def query(self , cities , products_id):
    #     results_cairo=[]

    #     results_alex=[]

    #     results_psaid=[]

    #     all_results=[]

    #     products_id=tuple(products_id)
    #     query=text(f'''
    #         SELECT p_name, sex, quantity
    #         FROM products
    #         JOIN inventory ON products.ID = inventory.pid
    #         WHERE products.ID IN {products_id}
    #     ''')
    #     if len(products_id) ==1:
    #         products_id=products_id[0]
    #         query=text(f'''
    #         SELECT p_name, sex, quantity
    #         FROM products
    #         JOIN inventory ON products.ID = inventory.pid
    #         WHERE products.ID = {products_id}
    #     ''')
        
        
    #     products_id=tuple(products_id)
    #     if "psaid" in cities:
    #         result=self.p_con.execute(query)
    #         results_psaid.append(result.fetchall())
    #         print(results_psaid) 
    #         all_results.append(results_psaid)
    #     if "cairo" in cities:
    #         result=self.c_con.execute(query)
    #         results_cairo.append(result.fetchall())
    #         print(results_cairo)
    #         all_results.append(results_cairo) 
    #     if "alex" in cities:
    #         result=self.a_con.execute(query)
    #         results_alex.append(result.fetchall())
    #         all_results.append(results_alex)
    #     return all_results

    def query(self , cities , products_id):
        result1 = []
        for j in products_id:
            result2 = []
            total = 0
            for i in cities:
                result3 = []
                rs = self.connections[i].execute(text(f"select * from inventory where pid={j}"))
                results = rs.fetchall()
                result3.append(results[0][0])
                result3.append(i)
                result3.append(results[0][1])
                result2.append(result3)
                total += results[0][1]
            result2.append(['total', total])
            result1.append(result2)
        print(result1)
        for i in result1:
            for j in i:
                print(j)
    
        # return
        return result1

    """This will look in what server to update"""
    def up(self, pid, count):
        if os.environ['server'] == 'cairo':
            self.cairo_update(pid, count)
        elif os.environ['server'] == 'alex':
            self.alex_update(pid, count)
        elif os.environ['server'] == 'psaid':
            self.psaid_update(pid, count)

    """This will look in what server to get transaction"""

    def get_transactions(self):
        server = os.environ['server']

        if server == 'cairo':
            return self.c_get_transactions()
        elif server == 'alex':
            return self.a_get_transactions()
        elif server == 'psaid':
            return self.p_get_transactions()

    """The connection function to connect to Cairo
    server and database"""

    def c_get_transactions(self):
        return self.get_transactions_from_db(self.c_con)

    """The connection function to connect to Alexandria
    server and database"""

    def a_get_transactions(self):
        return self.get_transactions_from_db(self.a_con)

    """The connection function to connect to Port-Said
    server and database"""

    def p_get_transactions(self):
        return self.get_transactions_from_db(self.p_con)

    """The function to get data from transactions"""

    def get_transactions_from_db(self, connection):
        # Execute SQL query to select transactions
        result = connection.execute(text('SELECT  p_name,p_state,quantity,p_timestamp FROM transactions JOIN products ON pid = ID;'))
        transactions = result.fetchall()
        return transactions

    
    """Since There will never be a wrong id
    therefore we don't need id validation"""
    # def validate_id(sef, val, con):
    #     val = int(val)