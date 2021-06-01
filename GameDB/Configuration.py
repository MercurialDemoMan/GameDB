#!/usr/bin/env python3
# coding=utf-8

import getpass
import platform

from PyQt5 import QtCore, QtGui

class Configuration:

    WindowIconData = b"iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABhWlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9TS0UqInYQ6ZChioIFURFHqWIRLJS2QqsOJpd+QZOGpMXFUXAtOPixWHVwcdbVwVUQBD9A3NycFF2kxP8lhRYxHhz34929x907QGiUmWp2TQCqVjWSsaiYya6K/lf4EEI/RjEmMVOPpxbTcB1f9/Dw9S7Cs9zP/Tl6lZzJAI9IPMd0o0q8QTyzWdU57xMHWVFSiM+Jxw26IPEj12WH3zgXbBZ4ZtBIJ+eJg8RioYPlDmZFQyWeJg4rqkb5QsZhhfMWZ7VcY6178hcGctpKius0Q4hhCXEkIEJGDSWUUUWEVo0UE0naj7r4h2x/glwyuUpg5FhABSok2w/+B7+7NfNTk05SIAr4XizrYxjw7wLNumV9H1tW8wTwPgNXWttfaQCzn6TX21r4COjbBi6u25q8B1zuAINPumRItuSlKeTzwPsZfVMWGLgFetac3lr7OH0A0tTV8g1wcAiMFCh73eXd3Z29/Xum1d8P1BJyzjY3lXYAAAAGYktHRAD/AO4AAJBbgVkAAAAJcEhZcwAALiMAAC4jAXilP3YAAAAHdElNRQflBRwRLBEWF8XdAAAAGXRFWHRDb21tZW50AENyZWF0ZWQgd2l0aCBHSU1QV4EOFwAAAU9JREFUeNrtW0kSwzAIs5j+/8v02ksTmwBh8zkOkoy8jcHyaSzoAw9gCET4FaxIQNwUMxIRN8GOhMRVOcCJOILGMAWm6VWzmFAG4rF0qWJAMvLqWKAQ0JO4Oi4kJq+CD8nJP8YJwU8jEX+MmQJvcFwyhCKe0Dw3diiS+mIOVGTkxXipuPdvM4MKjr54I8SFyK9dXrSaN2ri/b9ZQQW9f8RjLNBdABSe/bdWg7HACDACjAAjwAgwAowAI8AIMAL0PQytRgeiX67omgEYC2xeinK3dMg8D7AU86fAZPZIDGz8FInIr1P8pBwsGvnb7ymZ51m7HxkHTrkVRicRyCkF30z/y/4kmTm7ZMCVFcrYIdtLUdbm+vSJDFe2wIkIXNkCJyOOoDaAJuA3KkbMzgKRa4Y0MMAaGAexp/g+IHLdYMrSWc4mQobaYWQUwHTpmqbYvow3R17YYQ5/AAAAAElFTkSuQmCC"
    MissingPixmapData = b"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"

    def WindowIcon():
    
        pixmap = QtGui.QPixmap()
        if pixmap.loadFromData(QtCore.QByteArray.fromBase64(Configuration.WindowIconData)):
            return QtGui.QIcon(pixmap)
        else:
            return None
        
    def MissingPixmap():
        pixmap = QtGui.QPixmap()
        if pixmap.loadFromData(QtCore.QByteArray.fromBase64(Configuration.MissingPixmapData)):
            return pixmap
        else:
            return None
        
    def DatabasePath():
        
        if platform.system() == "Windows":
            return "C:/users/" + getpass.getuser() + "/GameDB/"
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            return "~/GameDB/"
        else:
            raise OSError("Running on an unknown platform")
        
    def FinishedDatabasePath():
        return Configuration.DatabasePath() + "finished.csv"
        
    def OngoingDatabasePath():
        return Configuration.DatabasePath() + "ongoing.csv"
        
    def DroppedDatabasePath():
        return Configuration.DatabasePath() + "dropped.csv"
        
    def ImageDatabasePath():
        return Configuration.DatabasePath() + "img/"