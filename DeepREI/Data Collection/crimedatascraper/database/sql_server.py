import os
import sys
import pymssql
from database._db_manager import _DB_manager

currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir) 

import globals
import log

class SQL_Server (_DB_manager): 
    
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
                self.connection = pymssql.connect(server=self.server, user=self.username, password=self.password, database=self.database)
            except Exception as err:
                error_mensssage = "ERROR TO CONNECT TO DATABASE\n\nDetails: \n\n"
                
                # Clean error mensaje
                err = str(err).replace("\\n", "\n")
                chars = ["(", ")", 'b"', '"']
                
                for char in chars:
                    err = str(err).replace(char, "")           
                
                error_mensssage += err
                
                # Logs and status 
                log.update_status(error_mensssage)
                globals.loading = False
                
                return None, None
        
        return  self.connection, self.connection.cursor()
                
    def run_sql (self, sql): 
        """ Exceute sql code
        
        Run sql code in the current data base, and commit it
        """
        
        connection, cursor = self.get_cursor_connector()
           
        # Try to run sql  
        try: 
            cursor.execute (sql)
        except Exception as err:
            
            error_mensssage = "ERROR TO RUN SQL\n\nDetails: \n\n"
            
            # Clean error mensaje
            err = str(err).replace("\\n", "\n")
            chars = ["(", ")", 'b"', '"']
            
            for char in chars:
                err = str(err).replace(char, "")           
            
            error_mensssage += err
            
            # Logs and status 
            log.update_status(error_mensssage)
            globals.loading = False
            
            return None
        
        # try to get returned part
        try: 
            results = cursor.fetchall() 
        except: 
            results = None
            
        connection.commit()    
        return results