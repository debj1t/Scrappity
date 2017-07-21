import logging
import logging.handlers
import time
import os

logValueMap = { 'CRITICAL' : logging.CRITICAL,
                'ERROR'    : logging.ERROR,
                'WARNING'  : logging.WARNING,
                'INFO'     : logging.INFO,
                'DEBUG'    : logging.DEBUG, }

ScrappityLogger = logging.getLogger("scrappity")

def InitializeLoggerModule():

    # Set log file name and log level
    logDirectory = 'logs'
    if not os.path.exists(logDirectory):
        os.makedirs(logDirectory)
    logFileName = logDirectory+'/scrappity.log'
    logLevel    = 'INFO'

    # WatchedFilehandler will create the log file if deleted
    ch = logging.handlers.WatchedFileHandler( logFileName )
    ScrappityLogger.setLevel ( logValueMap[logLevel] )

    ch.createLock()

    # create formatter
    if logLevel == "DEBUG":
        formatter = logging.Formatter('%(asctime)20s.%(msecs)03d | %(levelname)8s | %(module)10s | ' \
        '%(message)s ( %(filename)s , %(lineno)d )', "%d-%b-%Y %H:%M:%S")
    else:
        formatter = logging.Formatter('%(asctime)20s.%(msecs)03d | %(levelname)8s | %(module)10s | ' \
        '%(message)s', "%d-%b-%Y %H:%M:%S")

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    ScrappityLogger.addHandler(ch)
