#!/usr/bin/env python3
# coding=utf-8

import sys
import os
from PyQt5 import QtWidgets

from GameDB.Views.MainView import MainView
from GameDB.Repositories.GameRepository import GameRepository
from GameDB.Configuration import Configuration

def main(args):
    """main entry point"""
    
    # initialize database path
    if not os.path.exists(Configuration.DatabasePath()):
        os.makedirs(Configuration.DatabasePath())

    if not os.path.exists(Configuration.ImageDatabasePath()):
        os.makedirs(Configuration.ImageDatabasePath())

    if not os.path.exists(Configuration.FinishedDatabasePath()):
        GameRepository.create("finished.csv")
        
    if not os.path.exists(Configuration.OngoingDatabasePath()):
        GameRepository.create("ongoing.csv")
        
    if not os.path.exists(Configuration.DroppedDatabasePath()):
        GameRepository.create("dropped.csv")
        
    # open databases
    finished_rep = GameRepository("finished.csv")
    ongoing_rep = GameRepository("ongoing.csv")
    dropped_rep = GameRepository("dropped.csv")
    
    # create and launch main window
    app = QtWidgets.QApplication(sys.argv)
    window = MainView(finished_rep, ongoing_rep, dropped_rep)
    app.exec()
    
    # close database
    finished_rep.close()
    ongoing_rep.close()
    dropped_rep.close()

if __name__ == '__main__':
    main(sys.argv)
