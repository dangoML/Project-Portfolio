import os
import subprocess
import log
import config
import globals
import crimegrade_scraper
import PySimpleGUI as sg
from gui_manager import gui
from database.postgresql import PostgreSQL

def main (): 
    """Main function of the project with gui
    """
    
    # Get credentials for main gui
    output_table = config.get_credential("output_table")
    
    # Get theme from config file
    theme = config.get_credential("theme")
                
    # Set theme
    sg.theme(theme)

    # Main screedn layout
    layout = [
        [
            sg.Text("Output table:"),  
        ],
        [
            sg.Input(size=(50,1), default_text=output_table, key="output_table"),  
        ],
        [
            sg.Button("Run", size=(43,1), key="run"),  
        ],
        [
            sg.Button("Theme", size=(8,1), key="Theme"), 
            sg.Button("Database", size=(10,1), key="database"),  
            sg.Button("Zip Codes", size=(10,1), key="zipcodes"),  
            sg.Button("Exit", size=(8,1), key="Quit"),
        ]
    ]
    
    # Create window
    window = sg.Window("CRIMGRADE SCRAPER", layout, no_titlebar=False)
    
    while True:
        
        
        reopen = False
    
        event, values = window.read()
        
        # Update credentials 
        config.update_credential("output_table", values["output_table"])
        
        # RUN BUTTONS                 
                   
        # End program when close windows
        if event == sg.WIN_CLOSED or event == 'Quit':
            break
            
        if event == "Theme": 
            
            # Select new theme
            gui.theme_selector()
            
            # Update theme in current window
            theme = config.get_credential("theme")
            sg.theme(theme)
            reopen = True
            break  
        
        if event == "run": 
            
            # Show loading status and run main function in thread
            
            gui.loading(crimegrade_scraper.scraper)            
            gui.show_status("Program end. Final status:")
            
        if event == "config":
            
            log.info ("Credentials and options updated")
            
            # Show config gui
            config_gui()
            
        if event == "database": 
            
            # Update credentials
            gui.database(PostgreSQL)
            
            # table = "table_2"
            # columns = ["usuario", "contraseña"]
            # data = [["d", "a"]]
            
            # globals.db_manager.insert_rows (table, columns, data)
            
            
        if event == "zipcodes": 
            
            zipcodes_file = os.path.join (os.path.dirname(__file__), "zipcodes.txt")
            subprocess.Popen(zipcodes_file, shell=True)
            
                    
    # End window
    window.close()
    
    # Reopen window after changes
    if reopen: 
        main()

if __name__ == "__main__":
    main()