from database.connector import connectDatabase


class Query:
    def __init__(self, team_name,market_value, income, expenditure, instagram_followers,
                 twitter_followers, average_attendance, trophies_won, manager_count,
                 goals_against, goals_scored, matches_won, matches_lost, matches_drawn):
        self.database = connectDatabase()
        self.team_name=team_name
        self.market_value = market_value
        self.income = income
        self.expenditure = expenditure
        self.instagram_followers = instagram_followers
        self.twitter_followers = twitter_followers
        self.average_attendance = average_attendance
        self.trophies_won = trophies_won
        self.manager_count = manager_count
        self.goals_against = goals_against
        self.goals_scored= goals_scored
        self.matches_won = matches_won
        self.matches_lost = matches_lost
        self.matches_drawn = matches_drawn
        self.club_id=0
        self.attributes = {
            'followers': (self.club_id,instagram_followers, twitter_followers, average_attendance),
            'clubfinancial': (self.club_id,market_value, income, expenditure),
            'clubhistory': (self.club_id,trophies_won, manager_count),
            'seasonstats': (self.club_id,goals_scored, goals_against, matches_won, matches_lost, matches_drawn)
        }
        self.attributes_names = {
            'followers': (self.club_id, "instagram_followers", "twitter_followers", "average_attendance"),
            'clubfinancial': (self.club_id, "market_value", "income", "expenditure"),
            'clubhistory': (self.club_id, "trophies_won", "manager_count"),
            'seasonstats': (self.club_id, "goals_scored", "goals_against", "matches_won", "matches_lost", "matches_drawn")
        }

        self.tables=["clubs","clubfinancial","followers","clubhistory","seasonstats"]



    def insert(self):
        try:
            self.cursor, self.db = self.database.makeCursor()
            self.cursor.execute("USE footballteams")

            # Insert into Data_tim table
            insert_query = "INSERT INTO Clubs (club_name) VALUES (%s)"
            team_data = (self.team_name,)
            self.cursor.execute(insert_query, team_data)
            self.db.commit()

            # Retrieve latest id from Data_tim table
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            self.club_id = self.cursor.fetchone()[0]
            self.attributes = {
                'followers': (self.club_id, self.instagram_followers, self.twitter_followers, self.average_attendance),
                'clubfinancial': (self.club_id, self.market_value, self.income, self.expenditure),
                'clubhistory': (self.club_id, self.trophies_won, self.manager_count),
                'seasonstats': (self.club_id, self.goals_scored, self.goals_against, self.matches_won, self.matches_lost, self.matches_drawn)
            }
            for table in self.tables[1:] :
                columns = ', '.join(map(str, self.attributes_names[table][1:]))
                values = ', '.join(['%s'] * (len(self.attributes[table])-1))
                insert_query = f"INSERT INTO {table} (club_id, {columns}) VALUES (%s, {values})"
                data = self.attributes[table]
                self.cursor.execute(insert_query, data)


            self.db.commit()
        except Exception as e:
            print("Error:", e)
            self.db.rollback()
        finally:
            if self.cursor:
                self.cursor.close()
            # if self.db:
            #     self.db.close()
    def update(self,new_name):
        try:
            self.cursor, self.db = self.database.makeCursor()
            self.cursor.execute("USE Footballteams")
            """First we update the main table clubs first"""
            self.cursor.execute(f"UPDATE Clubs SET club_name='{new_name}' WHERE club_name = '{self.team_name}'")
            self.cursor.execute(
                f"SELECT id FROM Clubs WHERE club_name = '{new_name}'" )
            team_id = self.cursor.fetchone()[0]
            """Updating Other Tables"""
            for table in self.tables[1:] :
                columns = ', '.join(map(str, self.attributes_names[table][1:]))
                set_clause = ', '.join([f"{column}='{value}'" if isinstance(value, str) else f"{column}={value}" for column, value in zip(list(self.attributes_names[table])[1:], list(self.attributes[table])[1:])])
                sql_query=f"UPDATE {table} SET {set_clause} WHERE club_id= {team_id}"
                self.cursor.execute(sql_query)

            self.db.commit()
        except Exception as e:
            print("Error:", e)
            self.db.rollback()
        # finally:
        #     if self.cursor:
        #         self.cursor.close()
        #     if self.db:
        #         self.db.close()
    def delete(self):
        try:
            self.cursor, self.db = self.database.makeCursor()
            self.cursor.execute("USE Footballteams")

            deleted_team_id = None  # Variable to store the deleted team ID

            # Retrieve the ID of the team to be deleted
            self.cursor.execute(
                "SELECT id FROM Clubs WHERE club_name = %s",
                (self.team_name,)
            )
            deleted_team_id = self.cursor.fetchone()[0]
            # Delete team from each table
            for table in self.tables[1:]:
                    self.cursor.execute(
                        f"DELETE FROM {table} WHERE club_id = %s",
                        (deleted_team_id,)
                    )
            self.cursor.execute(
                f"DELETE FROM Clubs WHERE id = %s",
                (deleted_team_id,)
            )


            self.db.commit()
            # return deleted_team_id  # Return the ID of the deleted team
        except Exception as e:
            print("Error:", e)
            self.db.rollback()
        # finally:
        #     if self.cursor:
        #         self.cursor.close()
        #     if self.db:
        #         self.db.close()