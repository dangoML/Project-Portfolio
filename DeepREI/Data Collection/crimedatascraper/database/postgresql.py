import os
import sys
import psycopg2
from database._db_manager import _DB_manager

currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir) 

import globals
import log

class PostgreSQL (_DB_manager): 
    
    def credentials_error (self, err): 
        """
        Print credential error and update status
        """
        
        error_formated = "Database conecction error."
        error_formated += "\nPlease check your credentials.\n"
        
        # Logs and status 
        log.update_status(error_formated)
        globals.loading = False
        
        log.error(err)
        
    
    def get_cursor_connector (self): 
        """
        Connect to postgresql database and return cursor
        """
        
        try: 
            self.connection.cursor()
        except AttributeError: 
            
            try: 
                self.connection = psycopg2.connect(host=self.server, 
                                            database=self.database, 
                                            user=self.username, 
                                            password=self.password)
            except Exception as err: 
                
                self.credentials_error(err)

                return None
        
        return self.connection.cursor() 
                
    def run_sql (self, sql): 
        """ Exceute sql code
        
        Run sql code in the current data base, and commit it
        """
        
        cursor = self.get_cursor_connector()
           
        # Try to run sql  
        try: 
            cursor.execute (sql)
        except Exception as err:
            
            self.credentials_error(err)
            
            return None
        
        # try to get returned part
        try: 
            results = cursor.fetchall() 
        except: 
            results = None
        
        self.connection.commit()
        return results