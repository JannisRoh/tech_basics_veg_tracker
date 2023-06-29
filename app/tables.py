import os
from sqlalchemy import create_engine
from sqlite3 import connect
import psycopg2
import pandas as pd
import datetime
from config import basedir

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
        if os.getenv('DATABASE_URL'):
            engine = create_engine(os.getenv('DATABASE_URL').replace("postgres://", "postgresql+psycopg2://", 1))
            dbConnection = engine.connect()
        else:
            dbConnection = connect(os.path.join(basedir, 'app.db'))

        self.table_df = pd.read_sql(f"SELECT date, {self.poultry}, {self.pork}, {self.beef}, {self.total} FROM {self.database};", dbConnection)
        empty = self.table_df.empty
        if empty == True:
            initialSeries = pd.Series({"date":today, self.poultry:0, self.pork:0, self.beef:0, self.total:0})
            self.table_df = pd.concat([self.table_df, initialSeries.to_frame().T], ignore_index=True)
        self.table_df=self.table_df.rename(columns={self.poultry:"Poultry",self.beef:"Beef",self.pork:"Pork",self.total:"Total"})
        self.table_df=self.table_df.groupby(self.table_df['date'], as_index=False).sum()

        idx = pd.date_range(min(self.table_df.date), today)

        self.table_df['date'] = pd.to_datetime(self.table_df['date'])
        self.table_df = self.table_df.set_index('date').reindex(idx).rename_axis('date').fillna(0).reset_index()

        print("after:")
        print(self.table_df)
        return self.table_df

class Savedstats:
    def __init__(self, table_df, constant, reference1, reference2):
        self.table_df = table_df
        self.constant = constant
        self.reference1 = reference1
        self.reference2 = reference2

    def calculate_stats(self):
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
