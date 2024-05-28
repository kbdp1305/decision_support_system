import streamlit as st
import pandas as pd
from database.connector import connectDatabase
from database.dataset_generate import generate_dataset
from database.crud import Query
from model.profile_matching import profile_matching
from model.topsis import ProfileTopsis
# Create a DataFrame to hold the data
import streamlit as st

database=connectDatabase()
cursor,db=database.makeCursor()


# Define Streamlit layout

# Function to add data
def Suggest_Club() :
        st.title("CLUB SUGGESTION GENERATOR")
        input_values=[]
        market_value = st.number_input("Market Value", min_value=1, max_value=6)
        income = st.number_input("Income", min_value=1, max_value=6)
        expenditure = st.number_input("Expenditure", min_value=1, max_value=6)
        instagram_followers = st.number_input("Instagram Followers", min_value=1, max_value=6)
        twitter_followers = st.number_input("Twitter Followers", min_value=1, max_value=6)
        average_attendance = st.number_input("Average Attendance", min_value=1, max_value=6)
        trophies_won = st.number_input("Trophies Won", min_value=1, max_value=6)
        manager_count = st.number_input("Manager Count", min_value=1, max_value=6)
        goals_against = st.number_input("Goals Against", min_value=1, max_value=6)
        goals_scored = st.number_input("Goals Scored", min_value=1, max_value=6)
        matches_won = st.number_input("Matches Won", min_value=1, max_value=6)
        matches_lost = st.number_input("Matches Lost", min_value=1, max_value=6)
        matches_drawn = st.number_input("Matches Drawn", min_value=1, max_value=6)
        if st.button("Profile Topsis"):
            input_values.append(market_value)
            input_values.append(income)
            input_values.append(expenditure)
            input_values.append(instagram_followers)
            input_values.append(twitter_followers)
            input_values.append(average_attendance)
            input_values.append(trophies_won)
            input_values.append(manager_count)
            input_values.append(goals_against)
            input_values.append(goals_scored)
            input_values.append(matches_won)
            input_values.append(matches_lost)
            input_values.append(matches_drawn)
            market_value, income, expenditure, instagram_followers, twitter_followers, average_attendance, trophies_won, manager_count, goals_against, goals_scored, matches_won, matches_lost, matches_drawn = input_values
            pm=ProfileTopsis([instagram_followers,twitter_followers,average_attendance],[trophies_won,manager_count],[goals_scored,goals_against,matches_won,matches_lost,matches_drawn],[market_value,income,expenditure])
            s=pm.ranking()
            st.write(s)
        if st.button('Profile Matching') :
            input_values.append(market_value)
            input_values.append(income)
            input_values.append(expenditure)
            input_values.append(instagram_followers)
            input_values.append(twitter_followers)
            input_values.append(average_attendance)
            input_values.append(trophies_won)
            input_values.append(manager_count)
            input_values.append(goals_against)
            input_values.append(goals_scored)
            input_values.append(matches_won)
            input_values.append(matches_lost)
            input_values.append(matches_drawn)
            market_value, income, expenditure, instagram_followers, twitter_followers, average_attendance, trophies_won, manager_count, goals_against, goals_scored, matches_won, matches_lost, matches_drawn = input_values
            pm = profile_matching([instagram_followers, twitter_followers, average_attendance],
                               [trophies_won, manager_count],
                               [goals_scored, goals_against, matches_won, matches_lost, matches_drawn],
                               [market_value, income, expenditure])
            s = pm.ranking()
            st.write(s)






def insert(value) :
    team_name, market_value, income, expenditure, instagram_followers, twitter_followers, average_attendance, trophies_won, manager_count, goals_against, goals_scored, matches_won, matches_lost, matches_drawn = value
    Querying = Query(team_name, market_value, income, expenditure, instagram_followers, twitter_followers,
                     average_attendance, trophies_won, manager_count, goals_against, goals_scored, matches_won,
                     matches_lost, matches_drawn)
    Querying.insert()

def update_value(value,new_team):
        team_name, market_value, income, expenditure, instagram_followers, twitter_followers, average_attendance, trophies_won, manager_count, goals_against, goals_scored, matches_won, matches_lost, matches_drawn = value
        Querying = Query(team_name, market_value, income, expenditure, instagram_followers, twitter_followers,
                         average_attendance, trophies_won, manager_count, goals_against, goals_scored, matches_won,
                         matches_lost, matches_drawn)
        Querying.update(new_team)


def add_data():
    st.title("INSERT INTO DATABASE")
    input_values = []
    team_name = st.text_input("Team Name")
    market_value = st.number_input("Market Value")
    income = st.number_input("Income")
    expenditure = st.number_input("Expenditure")
    instagram_followers = st.number_input("Instagram Followers")
    twitter_followers = st.number_input("Twitter Followers")
    average_attendance = st.number_input("Average Attendance")
    trophies_won = st.number_input("Trophies Won")
    manager_count = st.number_input("Manager Count")
    goals_against = st.number_input("Goals Against")
    goals_scored = st.number_input("Goals Scored")
    matches_won = st.number_input("Matches Won")
    matches_lost = st.number_input("Matches Lost")
    matches_drawn = st.number_input("Matches Drawn")

    # Append input values to the list when "Add Data" button is clicked

    if st.button("Add Data"):
        input_values.append(team_name)
        input_values.append(market_value)
        input_values.append(income)
        input_values.append(expenditure)
        input_values.append(instagram_followers)
        input_values.append(twitter_followers)
        input_values.append(average_attendance)
        input_values.append(trophies_won)
        input_values.append(manager_count)
        input_values.append(goals_against)
        input_values.append(goals_scored)
        input_values.append(matches_won)
        input_values.append(matches_lost)
        input_values.append(matches_drawn)
        insert(input_values)

        st.write("data added")

def update() :
    st.title("UPDATE DATABASE")
    dataset,_=generate_dataset(cursor,db)
    input_values = []
    selected_club = st.selectbox("Team You Want to Change Name", dataset['club_name'])
    team_name = st.text_input("New Name")
    market_value = st.number_input("Market Value")
    income = st.number_input("Income")
    expenditure = st.number_input("Expenditure")
    instagram_followers = st.number_input("Instagram Followers")
    twitter_followers = st.number_input("Twitter Followers")
    average_attendance = st.number_input("Average Attendance")
    trophies_won = st.number_input("Trophies Won")
    manager_count = st.number_input("Manager Count")
    goals_against = st.number_input("Goals Against")
    goals_scored = st.number_input("Goals Scored")
    matches_won = st.number_input("Matches Won")
    matches_lost = st.number_input("Matches Lost")
    matches_drawn = st.number_input("Matches Drawn")

    if st.button("Update Data"):
        input_values.append(selected_club)
        input_values.append(market_value)
        input_values.append(income)
        input_values.append(expenditure)
        input_values.append(instagram_followers)
        input_values.append(twitter_followers)
        input_values.append(average_attendance)
        input_values.append(trophies_won)
        input_values.append(manager_count)
        input_values.append(goals_against)
        input_values.append(goals_scored)
        input_values.append(matches_won)
        input_values.append(matches_lost)
        input_values.append(matches_drawn)
        update_value(input_values,team_name)
        st.write("data changed")
def delete_team(value) :
    team_name, market_value, income, expenditure, instagram_followers, twitter_followers, average_attendance, trophies_won, manager_count, goals_against, goals_scored, matches_won, matches_lost, matches_drawn = value
    Querying = Query(team_name, market_value, income, expenditure, instagram_followers, twitter_followers,
                     average_attendance, trophies_won, manager_count, goals_against, goals_scored, matches_won,
                     matches_lost, matches_drawn)
    Querying.delete()

def delete() :
    st.title("DELETE DATABASE")
    dataset,_=generate_dataset(cursor,db)
    input_values = []
    team_name = st.selectbox("Team You Want to Delete", dataset['club_name'])
    market_value = 0
    income = 0
    expenditure = 0
    instagram_followers = 0
    twitter_followers = 0
    average_attendance = 0
    trophies_won = 0
    manager_count = 0
    goals_against = 0
    goals_scored = 0
    matches_won = 0
    matches_lost = 0
    matches_drawn = 0
    if st.button('Delete Data') :
        input_values.append(team_name)
        input_values.append(market_value)
        input_values.append(income)
        input_values.append(expenditure)
        input_values.append(instagram_followers)
        input_values.append(twitter_followers)
        input_values.append(average_attendance)
        input_values.append(trophies_won)
        input_values.append(manager_count)
        input_values.append(goals_against)
        input_values.append(goals_scored)
        input_values.append(matches_won)
        input_values.append(matches_lost)
        input_values.append(matches_drawn)
        delete_team(input_values)
        st.write("Data Deleted")



#
# # Add data
# # st.subheader("Add Data")
# # if st.button("Add Data"):
# #     st.write("Input Values:", input_values)
# #     team_name, market_value, income, expenditure, instagram_followers, twitter_followers, average_attendance, trophies_won, manager_count, goals_against, goals_scored, matches_won, matches_lost, matches_drawn = input_values
# #     Querying=Query(team_name, market_value, income, expenditure, instagram_followers, twitter_followers, average_attendance, trophies_won, manager_count, goals_against, goals_scored, matches_won, matches_lost, matches_drawn)
# #     Querying.insert()
#     #
# #
st.sidebar.title("Modify Data")
option = st.sidebar.selectbox("Choose operation", ["Insert", "Delete", "Update", "Generate Dataset", "Suggest Club"])

if option == "Insert":
    add_data()
elif option == "Delete":
    delete()
elif option == "Update":
    update()
elif option == "Generate Dataset":
    dataset_,_=generate_dataset(cursor,db)
    st.write(dataset_)
elif option == "Suggest Club" :
    Suggest_Club()

# # Function to delete data
# def delete_data():
#     index_to_delete = st.number_input("Index of the row to delete", min_value=0, max_value=len(data) - 1)
#     if st.button("Delete"):
#         data.drop(index=index_to_delete, inplace=True)
#         st.write("Data deleted successfully!")
#
#
# # Function to update data
# def update_data():
#     index_to_update = st.number_input("Index of the row to update", min_value=0, max_value=len(data) - 1)
#     column_to_update = st.selectbox("Column to update", data.columns)
#     new_value = st.text_input("New value")
#
#     if st.button("Update"):
#         data.at[index_to_update, column_to_update] = new_value
#         st.write("Data updated successfully!")
#
#
# # Function to display data
# def display_data():
#     st.write(data)
#
#
# # Define sidebar panel for modifying data
# st.sidebar.title("Modify Data")
# option = st.sidebar.selectbox("Choose operation", ["Insert", "Delete", "Update"])
#
# # Perform operation based on selection
# if option == "Insert":
#     add_data()
# elif option == "Delete":
#     delete_data()
# elif option == "Update":
#     update_data()
#
# # Display data
# st.subheader("Current Data")
# display_data()
