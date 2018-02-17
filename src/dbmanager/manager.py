class DBManager():

    def __init__(self, host="mysql", user="root", password="testing"):
        import MySQLdb
        self.connection = MySQLdb.connect(host=host, port=3306, user=user, passwd='pass')
        self.cursor = self.connection.cursor()


    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.cursor
        

    def create_db(self, dbname):
        self.connection.query('CREATE DATABASE {}'.format(dbname))

    def use_db(self, dbname):
        self.exec("USE {}".format(dbname))


    def create_table(self, query):
        self.cursor.execute('SET NAMES `utf8`')
        self.cursor.execute(query)


    def exec(self, query):
        self.cursor.execute(query)


    def get_rows(self, query):
        try:
            self.cursor.execute(query)
        except Exception as e:
            print(e)
            return None

        try: 
            res = self.cursor.fetchall()
            return res
        except TypeError as e:
            return None

    def close(self):
        self.cursor.close()
        self.connection.commit()
        self.connection.close()


# 1_1518814530_test_table

# 1_1518815888_test_table        |
# 1_1518815980_test_table