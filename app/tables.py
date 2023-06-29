# Importing functions necessary to connect with the database
import os
from sqlalchemy import create_engine
from sqlite3 import connect
import psycopg2
from config import basedir

import pandas as pd

import datetime


today = datetime.date.today()

class Tabledf:
    def __init__(self, table_df, poultry, pork, beef, total, database):
        self.table_df = table_df
        self.poultry = poultry
        self.pork = pork
        self.beef = beef
        self.total = total
        self.database = database

    def create_table(self):
        # Connect to the PSQL database if the app is hosted or to the SQLite3 database if run locally.
        if os.getenv('DATABASE_URL'):
            engine = create_engine(os.getenv('DATABASE_URL').replace("postgres://", "postgresql+psycopg2://", 1))
            dbConnection = engine.connect()
        else:
            dbConnection = connect(os.path.join(basedir, 'app.db'))

        # Turns a given database into a pandas dataframe.
        self.table_df = pd.read_sql(f"SELECT date, {self.poultry}, {self.pork}, {self.beef}, {self.total} FROM {self.database};", dbConnection)

        # Check if the created dataframe is empty, if it is create one entry for the current day where every value is 0.
        # This prevents an error when the app is first opened.
        empty = self.table_df.empty
        if empty == True:
            initialSeries = pd.Series({"date":today, self.poultry:0, self.pork:0, self.beef:0, self.total:0})
            self.table_df = pd.concat([self.table_df, initialSeries.to_frame().T], ignore_index=True)

        # Renaming the column names, so they can be used for the chart labels.
        self.table_df=self.table_df.rename(columns={self.poultry:"Poultry",self.beef:"Beef",self.pork:"Pork",self.total:"Total"})

        # Combining individual entries for duplicate dates, to deal with days the user inputs multiple times.
        self.table_df=self.table_df.groupby(self.table_df['date'], as_index=False).sum()

        # The dates for which the user makes no entries are assumed to be meatless days, so entries of 0 are automatically generated.
        idx = pd.date_range(min(self.table_df.date), today)
        self.table_df['date'] = pd.to_datetime(self.table_df['date'])
        self.table_df = self.table_df.set_index('date').reindex(idx).rename_axis('date').fillna(0).reset_index()

        # Returns the formatted table to be used for further calculations.
        return self.table_df


class Savedstats:
    def __init__(self, table_df, constant, reference1, reference2):
        self.table_df = table_df
        self.constant = constant
        self.reference1 = reference1
        self.reference2 = reference2

    def calculate_stats(self):
        """
        This method calculates the total saved amount of a chosen variable.
        It does so by determining how much the user has consumed, then determining how much the average person consumes in the same time frame.
        The difference of the two values is the amount the user has saved.
        If reference values are given as arguments, the method also calculates what the saved amount would be equal to in the referenced unit, for example water to bath tubs.
        """
        totalrows = len(self.table_df.index)
        userAbsolute = self.table_df['Total'].sum()/1000
        averageCurrent = self.constant * totalrows
        savedAmount = averageCurrent - userAbsolute
        if self.reference1 != 0:
            self.reference1 = savedAmount/self.reference1
            self.reference2 = savedAmount/self.reference2
            return savedAmount, self.reference1, self.reference2
        else:
            return savedAmount
