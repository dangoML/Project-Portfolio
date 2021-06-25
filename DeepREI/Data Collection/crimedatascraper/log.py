import os
import sys
import logging
import globals

# Login file path
file_log = os.path.join (os.path.dirname (__file__), ".log")
format_log = "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s"
logging.basicConfig(filename=file_log, level=logging.DEBUG, format=format_log)

# Max lines in log file
max_lines = 2000

# logging.disable(logging.DEBUG)) 

def update_status (new_status): 
    globals.status = new_status
    info(new_status, print_text=True)

def info (text, file="", print_text=False): 
    """
    Make a logging info in log file
    """
    
    clean_file()
    text_formated = clean_text (text)

    logging.info ("Module: {} - message: {}".format (file, text_formated))
    if print_text: 
        print (text_formated)

def debug (text, file="", print_text=False): 
    """
    Make a loggin debug in log file
    """
    
    clean_file()
    text_formated = clean_text (text)
    
    logging.debug ("Module: {} - message: {}".format (file, text_formated))
    if print_text: 
        print (text_formated)

def error (text, file="", print_text=False): 
    """
    Make a loggin debug in log file
    """
    
    clean_file()
    text_formated = clean_text (text)
    
    logging.error ("Module: {} - message: {}".format (file, text_formated))
    if print_text: 
        print (text_formated)

def warning (text, file="", print_text=False): 
    """
    Make a loggin debug in log file
    """
    
    clean_file()
    text_formated = clean_text (text)
    
    logging.warning ("Module: {} - message: {}".format (file, text_formated))
    if print_text: 
        print (text_formated)

def clean_file (): 
    """
    Clean the log file when I exceed a certain number of lines
    """
    
    file = open(file_log, "r")
    lines = file.readlines()
    file.close()
    lines_num = len(lines)
    
    if lines_num >= max_lines: 
        file = open(file_log, "w")
        file.write ("")
        file.close()

def clean_text (text): 
    """
    Replace breack lines in text
    """

    return str(text).replace ("\n", " | ")
    
def clean_terminal ():
    """
    Clean terminal in windows and linux 
    """ 
    
    os.system('cls||clear')

def catch_errors (function_get): 
        """
        Decorator for add log to each function
        """
        
        def function_with_logs (*args, **kwargs): 
            
            current_file = function_get.__module__
            
            try: 
                result = function_get(*args, **kwargs)
                message = "Function: '{}' executed. ".format (function_get.__name__)
                info (message, current_file, False)
                return result
            except Exception as err: 
                message = "Error in function: '{}': {}".format (function_get.__name__, err)
                error(message, current_file, False)
                raise Exception(err)
                
        return function_with_logs
    
def debug (function_get): 
        """
        Decorator for add log to each function from web scraping module, take screendhots and send
            emails when the program fails
        """
        
        def function_with_logs (*args, **kwargs): 
            
            current_file = function_get.__module__

            # Take the Screenshot A
            args[0].screenshot("screenshotA")

            try: 
                result = function_get(*args, **kwargs)
                
                # Save info line
                message = "Function: '{}' executed. ".format (function_get.__name__)
                info (message, current_file, False)
                
                return result
            except Exception as err: 

                # SEND MENSSAGE AND SAVE SCREENSHOTS

                # Take the Screenshot B
                args[0].screenshot("screenshotB")
                
                # # Save error
                # message = "Error in function: '{}': {}".format (function_get.__name__, err)
                # error(message, current_file, False)

                # # Get debug files 
                # current_dir = os.path.dirname(__file__)
                # file_list = [ os.path.join(current_dir, ".log"),
                #             os.path.join(current_dir, "screenshotA.png"),
                #             os.path.join(current_dir, "screenshotB.png")]

                # # Send files by email
                # debug_email(file_list)

                # Print status
                print ("\nSomething is wrong.")

                # Try to end browser
                try: 
                    args[0].end_browser()
                except: 
                    pass

                sys.exit()
          
        return function_with_logs
    
