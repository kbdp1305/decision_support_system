-- Create Clubs Table
CREATE TABLE Clubs (
    id INT PRIMARY KEY,
    club_name VARCHAR(255) UNIQUE
);

-- Create Followers Table
CREATE TABLE Followers (
    id INT PRIMARY KEY,
    club_id INT,
    instagram_followers FLOAT,
    twitter_followers FLOAT,
    average_attendance FLOAT,
    FOREIGN KEY (club_id) REFERENCES Clubs(id)
);

-- Create ClubFinancial Table
CREATE TABLE ClubFinancial (
    id INT PRIMARY KEY,
    club_id INT,
    market_value DECIMAL(10, 2),
    income DECIMAL(10, 2),
    expenditure DECIMAL(10, 2),
    FOREIGN KEY (club_id) REFERENCES Clubs(id)
);

-- Create ClubHistory Table
CREATE TABLE ClubHistory (
    id INT PRIMARY KEY,
    club_id INT,
    trophies_won INT,
    manager_count INT,
    FOREIGN KEY (club_id) REFERENCES Clubs(id)
);

-- Create SeasonStats Table
CREATE TABLE SeasonStats (
    id INT PRIMARY KEY,
    club_id INT,
    goals_scored INT,
    goals_against INT,
    matches_won INT,
    matches_lost INT,
    matches_drawn INT,
    FOREIGN KEY (club_id) REFERENCES Clubs(id)
);
