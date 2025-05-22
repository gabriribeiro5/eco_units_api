# Dealing with ImportError: attempted relative import with no known parent package
import sys
sys.path.append('.')

# logging setup
import logging
import inspect
from pathlib import Path
import os
from datetime import datetime, timedelta
import functools
from config import Definitions
    
class LogSetup():
    '''
    Key features
    Dynamic Log Directory and File Creation:
        The **createLogDir** method ensures that the specified log directory is created if it doesn't already exist. This is critical for ensuring the logging system works seamlessly without manual intervention.

    Configuring the Logging System:
        The **logFileCreateAndConfig** method sets up the basic configuration for logging and writes an initial headline to the log file, showing the calling module that enabled the logger.

    Comprehensive Logging Tests:
        The **runTests** method writes test messages to the log file for all log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) to ensure the logger is functioning correctly.

    User-Friendly API:
        The **enableLog** method provides a simple interface to initialize logging. It takes in a directory name and a log file name, sets up the directory, configures logging, and runs the tests.

    Robust Error Handling:
        Several **try-except blocks** handle exceptions that might occur during directory creation, logging configuration, or file writing.
        
    Inspector-Based Calling Module Identification:
        The use of inspect to determine and log the calling module is a nice touch for **traceability and debugging**.
    '''
    def __init__(self) -> None:
        self.logDir:Path
        self.logFile:Path

    def createLogDir(self): # create log directory if not exists
        try:
            self.logDir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            msg = f"could not create log directory.\n {e}"
            raise msg
            
    def logFileCreateAndConfig(self):
        # create log file and set basic logging config
        logFilePathAndName = self.logDir / self.logFile

        # Check if enableLog has been recently activated
        try:
            modification_time = os.path.getmtime(logFilePathAndName)
            current_datetime = datetime.now()
            time_delta = current_datetime - datetime.fromtimestamp(modification_time)
        except Exception as e:
            time_delta = timedelta(seconds=5) # total_seconds > 2
        if time_delta.total_seconds() > 2:
            run_tests = True
        else:
            run_tests = False

        # Create file if doesn't exist
        f = open(logFilePathAndName, "a")
        
        # Apply configuration
        try:
            logging.basicConfig(filename=logFilePathAndName,
                            format='%(levelname)s[%(asctime)s] - %(module)s (%(funcName)s): %(message)s',
                            datefmt='%Y/%m/%d %I:%M:%S %p',
                            filemode='a',
                            level=logging.DEBUG)
                            
            
            # enable logfile to find value for keyword %(method)s at logging.basicConfig(format='... %(method)s ...')
            # logger = logging.getLogger()
            # logger.addFilter(MethodFilter())
        except:
            msg = "could not apply basiCofig to logging service"
            raise msg
        
        # Write a special headline to the log file, asigning enableLogs's client file
        try:
            with open(logFilePathAndName, 'a') as l:
                # find the calling module
                frm = inspect.stack()[1] # the call's frame: filepath, code line, etc
                mod = inspect.getmodule(frm[0])
                callingModule = inspect.getmodulename(mod.__file__)

                # append first line of the process
                l.write(f"\n -- Logger enabled by {callingModule}.py --\n")
        except:
            msg = f"could not open and write to {logFilePathAndName}"
            raise msg
        
        # Run tests while avoiding multiple test executions
        if run_tests:
            self.runTests(logFilePathAndName)

    def runTests(self, logFilePathAndName):
        try:
            logging.debug('logging lib test for debug level is ok, running into info level')
            logging.info('logging lib test for info level is ok, running into warining level')
            logging.warning('logging lib test for warning level is ok, running into error level')
            logging.error('logging lib test for error level is ok, running into critical level')
            logging.critical('logging lib test for critical level is ok, all levels have been tested')
            logging.info('------------------- All logging levels successfully tested -------------------')
        except Exception as e:
            msg = "failed writing test logs to log file. Error: {e}"
            raise msg
        
        try:
            # Write a success message to log file
            with open(logFilePathAndName, 'a') as l:
                # append success line
                l.write(f"-- Waiting application logs...\n")
        except Exception as e:
            msg = "could not write to logFile. Error: {e}"
            raise msg
        
    def enableLog(self, dirName:str=".", logFileName:str="logfile"):
        """
        Create a log file if it does not exist, then test logging methods

        dirName: where must the lofile be saved?
        logFileName: what is the logfile name (usually the application name)?
        """
        # remove .py from appName then normalize variables into paths
        if ".py" in logFileName:
            logFileName = logFileName[0:(len(logFileName)-3)]
        self.logDir = Path(dirName)
        self.logFile = Path(f"{logFileName}.log")
        
        self.createLogDir()
        self.logFileCreateAndConfig()
        

config = Definitions()
def async_log_running_and_done(func):
    """
    This is meant to be used as a @decorator for asyncronous methods
    It simply logs the begining and end of its decorated method
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if config.LOGGING_ENABLED:
            try:
                # select filename name in a complex module name
                func_module = func.__module__.split(".")[-1]
            except:
                # filename is the module
                func_module = func.__module__
            logging.info(f"{func_module} - ({func.__name__}): running")
            kwargs = await func(*args, **kwargs)  # Call the decorated method
            logging.info(f"{func_module} - ({func.__name__}): done")
            return kwargs
        else:
            try:
                # select filename name in a complex module name
                func_module = func.__module__.split(".")[-1]
            except:
                # filename is the module
                func_module = func.__module__
            print(f"{func_module} - ({func.__name__}): running")
            kwargs = await func(*args, **kwargs)  # Call the decorated method
            print(f"{func_module} - ({func.__name__}): done")
            return kwargs
    return wrapper

def log_running_and_done(func):
    """
    This is meant to be used as a @decorator
    It simply logs the begining and end of its decorated method
    """
    def wrapper(*args, **kwargs):
        try:
            # select filename name in a complex module name
            func_module = func.__module__.split(".")[-1]
        except:
            # filename is the module
            func_module = func.__module__

        if config.LOGGING_ENABLED:
            logging.info(f"{func_module} - ({func.__name__}): running")
            kwargs = func(*args, **kwargs)  # Call the decorated method
            logging.info(f"{func_module} - ({func.__name__}): done")
            return kwargs
        else:
            kwargs = func(*args, **kwargs)  # Call the decorated method
            return kwargs
    return wrapper