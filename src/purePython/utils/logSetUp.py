# Dealing with ImportError: attempted relative import with no known parent package
import sys
sys.path.append('.')

# logging setup
import logging
import inspect
from pathlib import Path

class LogSetUp():
    def __init__(self) -> None:
        self.logDir:Path
        self.logFile:Path

    def createLogDir(self): # create log directory if not exists
            try:
                self.logDir.mkdir(parents=True, exist_ok=True)
            except:
                msg = "could not create log directory"
                raise msg
            
    def logFileCreateAndConfig(self):
        # create log file and set basic logging config
        logFilePathAndName = self.logDir / self.logFile
        try:
            logging.basicConfig(filename=logFilePathAndName,
                            format='%(levelname)s[%(asctime)s] - %(module)s: %(message)s',
                            datefmt='%Y/%m/%d %I:%M:%S %p',
                            filemode='a',
                            level=logging.DEBUG)
        except:
            msg = "could not apply basiCofig to logging service"
            raise msg
        
        # Write a headline to the log file, asigning enableLogs's client file
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
        
        return logFilePathAndName

    def runTests(self, logFilePathAndName):
        try:
            logging.debug('logging lib test for debug level is ok, running into level')
            logging.info('logging lib test for info level is ok, running into warining level')
            logging.warning('logging lib test for warning level is ok, running into warning level')
            logging.error('logging lib test for error level is ok, running into critical level')
            logging.critical('logging lib test for critical level is ok, all levels have been tested')
            logging.info('------------------- All logging levels successfully tested -------------------')
        except:
            msg = "failed writing logs to log file"
            return msg
        
        try:
            # Write a success message to log file
            with open(logFilePathAndName, 'a') as l:
                # append success line
                l.write(f"-- Logging levels successfully tested by loSetUp.py --\n")
                l.write(f"-- Waiting logs... --\n\n")
        except:
            msg = "could not write to logFile"
            return msg
        
    def enableLog(self, dirName:str=".", logFileName:str="logfile"):
        """
        dirName: where must the lofile be saved?
        logFileName: what is the logfile name (usually the application name)?
        """
        # remove .py from appName then normalize variables into paths
        if ".py" in logFileName:
            logFileName = logFileName[0:(len(logFileName)-3)]
        self.logDir = Path(dirName)
        self.logFile = Path(f"{logFileName}.log")
        
        self.createLogDir()
        logFilePathAndName = self.logFileCreateAndConfig()
        
        self.runTests(logFilePathAndName)