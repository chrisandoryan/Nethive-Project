# -*- coding: utf8 -*-

"""
This file contains the exceptions used in this project.
"""

class Error(Exception):
    pass

class UtilError(Exception):
    """General errors raised by command modules to user scripts.
    
    This exception class is used to report errors from MySQL utilities
    command modules and are used to communicate known errors to the user.
    """
    
    def __init__(self, message, errno=0):
        self.args = (message, errno)
        self.errmsg = message
        self.errno = errno


class UtilDBError(UtilError):
    """Database errors raised when the mysql database server operation fails.
    """
    
    def __init__(self, message, errno=0, db=None):
        UtilError.__init__(self, message, errno)
        self.db = db


class UtilRplError(UtilError):
    """Replication errors raised during replication operations.
    """
    
    def __init__(self, message, errno=0, master=None, slave=None):
        UtilError.__init__(self, message, errno)
        self.master = master
        self.slave = slave


class UtilBinlogError(UtilError):
    """Errors raised during binary log operations.
    """
    
    def __init__(self, message, errno=0, file=None, pos=0):
        UtilError.__init__(self.message, errno)
        self.file = file
        self.pos = pos


class UtilTestError(UtilError):
    """Errors during test execution of command or common module tests.
    
    This exception is used to raise and error and supply a return value for
    recording the test result.
    """
    def __init__(self, message, errno=0, result=None):
        UtilError.__init__(self, message, errno)
        self.result = result
    

class FormatError(Error):
    """An entity was supplied in the wrong format."""
    pass

class EmptyResultError(Error):
    """An entity was supplied in the wrong format."""
    pass

class MUTLibError(Exception):
    """MUT errors
    
    This exception class is used to report errors from the testing subsystem.
    """
    
    def __init__(self, message, options=None):
        self.args = (message, options)
        self.errmsg = message
        self.options = options
    
class LogParserError(UtilError):
    def __init__(self, message=''):
        super(LogParserError,self).__init__(message)
