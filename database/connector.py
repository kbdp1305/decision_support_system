import mysql.connector

# db=mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password=""
# )
# cursor=db.cursor()
# cursor.execute("USE TimSepakBola")
# insert_query = "INSERT INTO Data_tim (nama_tim, kota, tahun_berdiri, pelatih, warna_seragam) VALUES (%s, %s, %s, %s, %s)"
# team_data = ('Team F', 'City F', 2000, 'Coach F', 'Red')
#
#
# # Close the cursor and database connection
# cursor.close()
# db.close()
db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="S0kes0kk1pre1"
)


class connectDatabase() :
    def __init__(self):
        self.host="localhost"
        self.user="user"
        self.password=""
        self.db=None
    def openConnection(self):
        connection = db
        self.db=db
        return connection
    def makeCursor(self):
        return self.openConnection().cursor(),self.db
    # def query(self):
    #     cursor=self.makeCursor()
    #     cursor.execute("USE footballteams")
    #     cursor.execute("SELECT * FROM Data_tim")
    #
    #     # Fetch the first row
    #     row = cursor.fetchone()
    #
    #     # Loop through all rows and print them
    #     while row is not None:
    #         print(row)
    #         row = cursor.fetchone()
    #     cursor.close()
    #     self.db.close()
