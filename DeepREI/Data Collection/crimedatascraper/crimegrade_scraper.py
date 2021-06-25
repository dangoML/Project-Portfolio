import os
import time
import log
import config
import globals
import requests
from database.postgresql import PostgreSQL
from scraping_manager.automate import Web_scraping

def scraper (): 
    """
    Main function of the scraper. 
    Extract data and save it in database
    """ 
    
    # First instance of data base class
    server = config.get_credential("db_server")
    database = config.get_credential("db_name")
    user = config.get_credential("db_user")
    password = config.get_credential("db_password")

    globals.db_manager = PostgreSQL(server,
                                    database,
                                    user,
                                    password)
    
    # Create table
    output_table = str(config.get_credential ("output_table")).lower() 
    tables = globals.db_manager.get_tables_names()
    
    if (output_table,) in tables: 
        globals.db_manager.truncate_table(output_table)
        log.info(f"Table {output_table} truncated", print_text=True)
    else: 
        
        columns = [
            ["Assault", "numeric"],
            ["Robbery", "numeric"],
            ["Rape", "numeric"],
            ["Murder", "numeric"],
            ["Total_Violent_Crime", "varchar"],
            ["Theft", "numeric"],
            ["Vehicle_Theft", "numeric"],
            ["Burglary", "numeric"],
            ["Arson", "numeric"],
            ["Total_Property_Crime", "varchar"],
            ["Kidnapping", "numeric"],
            ["Drug_Crimes", "numeric"],
            ["Vandalism", "numeric"],
            ["Identity_Theft", "numeric"],
            ["Animal_Cruelty", "numeric"],
            ["Total_Other_Rate", "varchar"],
            ["zipcode", "integer"]
        ]
        
        globals.db_manager.create_table(f"{output_table}", columns)   
        log.info(f"Table {output_table} created", print_text=True)      
    

    # Get zip codes
    zipcodes = []
    zipcodes_path = os.path.join(os.path.dirname(__file__), "zipcodes.txt")
    with open (zipcodes_path, "r") as file:
        zipcodes = file.readlines()
        
    # Loop for each zip code in list
    valid_rows = 0
    zipcodes_num = len(zipcodes)
    for zipcode in zipcodes: 
        
        # End program if global status is not running
        if not globals.loading: 
            break
        
        # Instance of selenium and load page
        zipcode_formated = zipcode.replace("\n", "")
        page = f"https://crimegrade.org/safest-places-in-{zipcode_formated}/"
        scraper = Web_scraping(page, headless=True, user_agent=True)
        
        # Logs and status
        index = zipcodes.index(zipcode) + 1
        log.update_status(f'Scraping zipcode {zipcode_formated} ({index} / {zipcodes_num})')
        
        # Skip no found pages
        h1 = scraper.get_text("h1")
        if h1 == "No Results Found": 
            continue
        
        tables_selectors = [
            "p + .one_third", 
            ".one_third + .one_third", 
            ".one_third.et_column_last"
        ]
        
        columns = []
        values = []
        for table_selector in tables_selectors: 

            #  Get data for each table
            selector_row_vcr = f"{table_selector} > .SummaryStats.mtr-table.mtr-tr-th tr"
            rows_vcr = scraper.get_elems(selector_row_vcr)
            
            # Loopf ro each row in table
            for index_row in range(0, len(rows_vcr)+1): 
                title_selector = selector_row_vcr + f":nth-child({index_row}) > *:nth-child(1)"
                value_selector = selector_row_vcr + f":nth-child({index_row}) > *:nth-child(2)"
                
                title = str(scraper.get_text(title_selector)).strip().replace('"', "")
                value = str(scraper.get_text(value_selector)).strip().replace('"', "")
            
                # Clean data
                sktip_tiles = [None, "Crime Type", "None"]
                if title and value and not title in sktip_tiles:
                    
                    title_formated = str(title).lower().replace(" ", "_")
                    title_formated = title_formated.replace('”', "").replace('“', "")
                    
                    columns.append(title_formated)
                    values.append(value)
        
        # Send data to database
        columns.append("zipcode")
        values.append(zipcode_formated)
        globals.db_manager.insert_rows (output_table, columns, [values], nstring=False)
        valid_rows += 1
                
        # End browser
        scraper.end_browser()
        
    # End loading
    globals.loading = False
    globals.status += f"\nRows in database: {valid_rows}"
            
if __name__ == "__main__":
    globals.loading = True
    scraper()