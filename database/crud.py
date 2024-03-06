from database.connector import connectDatabase

# class query() :
#     def __init__(self):
#         database=connectDatabase()
#         self.cursor,self.db=database.makeCursor()
#         self.Kota="Kota Z"
#         self.tahun_berdiri=2020
#         self.pelatih="Coach Z"
#         self.warna_seragam="Blue"
#     def insert(self,nama_tim,Jumlah_fans,Jumlah_piala, Jumlah_followers):
#         """Inserting to primary table first Data_tim"""
#         self.cursor.execute("USE TimSepakBola")
#         insert_query = "INSERT INTO Data_tim (nama_tim, kota, tahun_berdiri, pelatih, warna_seragam) VALUES (%s, %s, %s, %s, %s)"
#         team_data = (nama_tim, 'City F', 2000, 'Coach F', 'Red')
#         self.cursor.execute(insert_query, team_data)
#         self.db.commit()
#         self.cursor.execute("SELECT MAX(id) FROM Data_tim")
#         latest_tim_id = self.cursor.fetchone()[0]
#         "Inserting to other Jumlah_Fans"
#         # insert_query
#         insert_query="INSERT INTO Jumlah_fans(tim_id,jumlah) VALUES(%s, %s)"
#         data=(latest_tim_id,Jumlah_fans)
#         self.cursor.execute(insert_query, data)
#         self.db.commit()
#         insert_query = "INSERT INTO Jumlah_piala (tim_id, jumlah_piala) VALUES(%s, %s)"
#         data=(latest_tim_id,Jumlah_piala)
#         self.cursor.execute(insert_query, data)
#         self.db.commit()
#         insert_query = "INSERT INTO Jumlah_followers_instagram (tim_id, jumlah_followers)  VALUES(%s, %s)"
#         data = (latest_tim_id, Jumlah_followers)
#         self.cursor.execute(insert_query, data)
#         self.db.commit()
#         self.cursor.close()
#         self.db.close()

class Query:
    def __init__(self):
        self.database = connectDatabase()
        self.tables=["Data_tim","Jumlah_fans","Jumlah_piala","Jumlah_followers_instagram"]

    def insert(self, nama_tim, Jumlah_fans, Jumlah_piala, Jumlah_followers):
        try:
            self.cursor, self.db = self.database.makeCursor()
            self.cursor.execute("USE TimSepakBola")

            # Insert into Data_tim table
            insert_query = "INSERT INTO Data_tim (nama_tim, kota, tahun_berdiri, pelatih, warna_seragam) VALUES (%s, %s, %s, %s, %s)"
            team_data = (nama_tim, 'City F', 2000, 'Coach F', 'Red')
            self.cursor.execute(insert_query, team_data)
            self.db.commit()

            # Retrieve latest id from Data_tim table
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            latest_tim_id = self.cursor.fetchone()[0]

            # Insert into Jumlah_fans table
            insert_query = "INSERT INTO Jumlah_fans(tim_id, jumlah) VALUES (%s, %s)"
            data = (latest_tim_id, Jumlah_fans)
            self.cursor.execute(insert_query, data)

            # Insert into Jumlah_piala table
            insert_query = "INSERT INTO Jumlah_piala (tim_id, jumlah_piala) VALUES (%s, %s)"
            data = (latest_tim_id, Jumlah_piala)
            self.cursor.execute(insert_query, data)

            # Insert into Jumlah_followers_instagram table
            insert_query = "INSERT INTO Jumlah_followers_instagram (tim_id, jumlah_followers) VALUES (%s, %s)"
            data = (latest_tim_id, Jumlah_followers)
            self.cursor.execute(insert_query, data)

            self.db.commit()
        except Exception as e:
            print("Error:", e)
            self.db.rollback()
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()
    def update(self, Nama_Tim, Jumlah_fans, Jumlah_piala, Jumlah_followers):
        try:
            self.cursor, self.db = self.database.makeCursor()
            self.cursor.execute("USE TimSepakBola")

            for table in self.tables:
                if table == "Data_tim":
                    self.cursor.execute(
                        f"UPDATE {table} SET nama_tim = %s WHERE nama_tim = %s",
                        (Nama_Tim, "Team A")
                    )
                    self.cursor.execute(
                        "SELECT id FROM Data_tim WHERE nama_tim = %s",
                        (Nama_Tim,)
                    )
                    updated_team_id = self.cursor.fetchone()[0]
                    print(updated_team_id)
                elif table == "Jumlah_fans":
                    self.cursor.execute(
                        f"UPDATE {table} SET jumlah = %s WHERE tim_id = {updated_team_id}",
                        (Jumlah_fans,)
                    )
                elif table == "Jumlah_piala":
                    self.cursor.execute(
                        f"UPDATE {table} SET jumlah_piala = %s WHERE tim_id = {updated_team_id}",
                        (Jumlah_piala,)
                    )
                elif table == "Jumlah_followers_instagram":
                    self.cursor.execute(
                        f"UPDATE {table} SET jumlah_followers = %s WHERE tim_id = {updated_team_id}",
                        (Jumlah_followers,)
                    )

            self.db.commit()
        except Exception as e:
            print("Error:", e)
            self.db.rollback()
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()
    def delete(self, nama_tim):
        try:
            self.cursor, self.db = self.database.makeCursor()
            self.cursor.execute("USE TimSepakBola")

            deleted_team_id = None  # Variable to store the deleted team ID

            # Retrieve the ID of the team to be deleted
            self.cursor.execute(
                "SELECT id FROM Data_tim WHERE nama_tim = %s",
                (nama_tim,)
            )
            deleted_team_id = self.cursor.fetchone()[0]
            # Delete team from each table
            for table in self.tables:
                if table=="Data_tim" :
                    continue
                else :
                    self.cursor.execute(
                        f"DELETE FROM {table} WHERE tim_id = %s",
                        (deleted_team_id,)
                    )
            self.cursor.execute(
                f"DELETE FROM Data_tim WHERE id = %s",
                (deleted_team_id,)
            )


            self.db.commit()
            return deleted_team_id  # Return the ID of the deleted team
        except Exception as e:
            print("Error:", e)
            self.db.rollback()
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()