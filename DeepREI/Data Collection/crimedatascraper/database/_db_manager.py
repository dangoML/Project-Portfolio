import os
import sys
import datetime

currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir) 

import globals
import log

class _DB_manager (): 
    """ Connect to data base and save data
    
    Read data from json files. 
    Connect to sql server and save data
    """
    
    def __init__ (self, server, database, username, password, tables={}): 
        """ Constructor of the class
        
        Connect to data base and set data
        
        Tables need the follow structure: dictionary with name of table as key
            and name of columns as a list in value. Sample: 
            {"table": [row1, row2, etc], }
        """
        
        # self.connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        
        # Set class variables
        self.server=server
        self.username=username
        self.password=password
        self.database=database
        
        self.tables = tables  
        
        self.connection = None
    
    def get_cursor_connector (self): 
        """
        Connect to database and return cursor
        """
        
        raise NotImplementedError("Please Implement this method")
    
    def run_sql (self, sql): 
        """ Exceute sql code
        
        Run sql code in the current data base, and commit it
        """
        
        raise NotImplementedError("Please Implement this method")
            
    
    def truncate_table (self, table): 
        """
        Truncate all twitter tables
        """
        
        # truncate specific table
        sql = "TRUNCATE TABLE {}".format(table)
        
        # Logs
        log.info(f"Table truncate: {table}")
        
        # run sql and commit changes
        self.run_sql(sql)
    
    def truncate_tables (self): 
        """
        Truncate all twitter tables
        """
        
        # truncate each table in instance
        for table in self.tables: 
            sql = "TRUNCATE TABLE {}".format(table)
            
            # run sql and commit changes
            self.run_sql(sql)
        
        # Logs
        log.info("All tables truncated")
    
    def insert_rows (self, table="", columns=[], data=[], nstring=True): 
        """
        Insert a list of rows in specific table
        """
        
        
        # Generate sql
        for row in data:
            
            columns_query = self.__get_sql_from_list__ (columns, nstring=False, quotes=False)
            values_query = self.__get_sql_from_list__ (row, nstring=nstring, quotes=True)
            
            sql = "INSERT INTO {} ({}) VALUES ({})".format (table, columns_query, values_query)
            
            # print (sql)
                                    
            # run sql and commit changes
            self.run_sql (sql)
            
        # Logs
        num_rows = len (data)
        log.info(f"Inserted {num_rows} rows in table {table}")
    
    def __get_sql_from_list__ (self, values, nstring, quotes): 
        """
        Convert a list of items to sql list
        """
        
        sql = ' '
        
        counter_values = 0
        for value in values: 
            
            counter_values += 1
            
            value = str(value).replace("\'", "").replace("[", "")
            value = str(value).replace("]", "").replace('', "")
            
            if nstring: 
                sql += " N"
            
            if quotes:                
                sql += "'{}' ".format (value)
            else: 
                sql += "{} ".format (value)
            
            # Add commas
            if counter_values < len (values): 
                sql += ','
        
        return sql
    
    def get_columns (self, table): 
        """ Get column names from specific table
        """
        
        sql = ""
        sql += "SELECT COLUMN_NAME, DATA_TYPE "
        sql += "FROM INFORMATION_SCHEMA.COLUMNS "
        sql += f"WHERE TABLE_NAME = N'{table}'"
        
        columns = self.run_sql (sql)
        
        # Logs
        log.info(f"Returned columns of table {table}")
        
        return columns
    
    def get_rows (self, table, top_rows=0): 
        """ Get column names from specific table
        """
        
        sql = ""
        
        if top_rows > 0: 
            sql += f"SELECT TOP ({top_rows}) *"
        else: 
            sql += f"SELECT * "
            
        sql += f"FROM {table}"
        
        rows = self.run_sql (sql)
        
        # Logs
        log.info(f"Returned rows of table {table}")
        
        return rows
    
    def get_tables_names (self): 
        """ Return all table name sin current data base
        """
        
        sql = ""
        sql += "SELECT TABLE_NAME "
        sql += "FROM INFORMATION_SCHEMA.TABLES "
        sql += "WHERE TABLE_TYPE = 'BASE TABLE'"
        
        tables = self.run_sql(sql)
        
        # Logs
        log.info(f"Returned table names")
        
        return tables

    def create_table (self, table_name, columns): 
        """Create table with a list of columns and datatypes
        """
        
        columns_formated = []
        for column in columns: 
            column_formated = f"{column[0]} {column[1]}"
            columns_formated.append(column_formated)
            
        columns_formated_sql = self.__get_sql_from_list__(columns_formated, 
                                                          nstring=False, 
                                                          quotes=False)
                
        sql = ""
        sql += f"CREATE TABLE {table_name} ("
        sql += columns_formated_sql
        sql += ")"
                
        self.run_sql(sql)

        # Logs
        log.info(f"Table created: {table_name}")
   