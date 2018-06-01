import sqlite3

class SQLighter:


    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM journal').fetchall()

    def select_single(self, rownum):
        with self.connection:
            return self.cursor.execute('SELECT * FROM journal WHERE id = ?', (rownum,)).fetchall()[0]

    def count_rows(self):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM journal').fetchall()
            return len(result)

    def close(self):
        self.connection.close()

    def set_id(self, ID, rownum):

            self.cursor.execute("UPDATE journal SET ID_of_Telegram=" + str(ID) + " WHERE Id=" + str(rownum) + ";")
            self.connection.commit()

    def del_id(self, rownum):
        with self.connection:
            self.cursor.execute("UPDATE journal SET ID_of_Telegram=" + "''" + " WHERE Id=" + str(rownum) + ";")
            self.connection.commit()
