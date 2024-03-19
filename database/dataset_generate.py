from database.connector import connectDatabase

import csv

# Open the CSV file
import pandas as pd
def generate_dataset(cursor,db) :
    cursor, db = cursor,db
    cursor.execute("USE footballteams")

    sql_query = """
        SELECT 
            t1.id as club_id,
            t1.club_name,
            t2.market_value,
            t2.income,
            t2.expenditure,
            t3.instagram_followers,
            t3.twitter_followers,
            t3.average_attendance,
            t4.trophies_won,
            t4.manager_count,
            t5.goals_scored,
            t5.goals_against,
            t5.matches_won,
            t5.matches_lost,
            t5.matches_drawn
        FROM Clubs t1
        INNER JOIN clubfinancial t2 ON t1.id = t2.club_id
        INNER JOIN followers t3 ON t1.id = t3.club_id
        INNER JOIN clubhistory t4 ON t1.id = t4.club_id
        INNER JOIN seasonstats t5 ON t1.id = t5.club_id
    """

    cursor.execute(sql_query)


    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Get the column names from the cursor description for all five tables
    column_names_table1 = [column[0] for column in
                           cursor.description[:len(cursor.description) // 5]]  # Columns for table1
    column_names_table2 = [column[0] for column in cursor.description[len(cursor.description) // 5:len(
        cursor.description) // 5 * 2]]  # Columns for table2
    column_names_table3 = [column[0] for column in cursor.description[len(cursor.description) // 5 * 2:len(
        cursor.description) // 5 * 3]]  # Columns for table3
    column_names_table4 = [column[0] for column in cursor.description[len(cursor.description) // 5 * 3:len(
        cursor.description) // 5 * 4]]  # Columns for table4
    column_names_table5 = [column[0] for column in
                           cursor.description[len(cursor.description) // 5 * 4:]]  # Columns for table5

    # Combine the column names
    column_names = column_names_table1 + column_names_table2 + column_names_table3 + column_names_table4 + column_names_table5

    # Create a DataFrame using pandas
    df = pd.DataFrame(rows, columns=column_names)
    # Close the cursor and database connection
    # cursor.close()
    # db.close()
    return df,db