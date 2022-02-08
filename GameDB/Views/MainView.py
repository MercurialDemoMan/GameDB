#!/usr/bin/env python3
# coding=utf-8

from copy import copy
import time
import sys
import os

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QEvent, QSize, QObject, QThread, pyqtSignal, QMutex
from PyQt5 import QtGui

from GameDB.Repositories.GameRepository import GameRepository
from GameDB.Views.GameAddView import GameAddView
from GameDB.Entities.GameEntity import GameEntity

from GameDB.Configuration import Configuration

class ListLoader(QThread):
    
    finished = pyqtSignal()
    items = pyqtSignal(QtWidgets.QListWidgetItem)
    length = pyqtSignal(int)
    
    def __init__(self, widget, db):
        super(ListLoader, self).__init__()
        self.widget = widget
        self.db = db
        self.thread_active = True
    
    def run(self):
    
        db_items = self.db.getAll()
        
        self.length.emit(len(db_items))
        
        db_items.sort(key=lambda x: x.name)
        
        for item in db_items:
        
            if not self.thread_active:
                break
                
            qt_item = QtWidgets.QListWidgetItem()
            qt_item.setText(item.name)
            qt_item.setData(Qt.UserRole, item.ID)
            if(item.image_url != ""):
                qt_item.setIcon(QtGui.QIcon(QtGui.QPixmap(Configuration.ImageDatabasePath() + item.image_url)))
                
            self.widget.addItem(qt_item)
        
        self.finished.emit()
    
    def stop(self):
        self.thread_active = False
    
class MainView(QtWidgets.QMainWindow):

    def _getUiPath(self, ui_file_name):
        """Get absolute ui path"""

        script_path = os.path.realpath(__file__)
        parent_dir = os.path.dirname(script_path)
        return os.path.join(parent_dir, ui_file_name)

    def getDatabaseBasedOnTab(self):
        
        tab_index = self.tabWidget.currentIndex()
        
        tab_table = {
            0: self.finished_db,
            1: self.ongoing_db,
            2: self.dropped_db
        }
        
        if tab_index in tab_table:
            return tab_table[tab_index]
            
        return None
        
    def getListWidgetBasedOnTab(self):
        
        tab_index = self.tabWidget.currentIndex()
        
        tab_table = {
            0: self.finishedListWidget,
            1: self.ongoingListWidget, 
            2: self.droppedListWidget
        }
        
        if tab_index in tab_table:
            return tab_table[tab_index]
            
        return None
        
    def getTotalLabelBasedOnTab(self):
        
        tab_index = self.tabWidget.currentIndex()
        
        tab_table = {
            0: self.finishedTotalLabel,
            1: self.ongoingTotalLabel, 
            2: self.droppedTotalLabel
        }
        
        if tab_index in tab_table:
            return tab_table[tab_index]
            
        return None

    def fillListWidget(self):
    
        if hasattr(self, "load_thread"):
            self.load_thread.stop()
            
        current_widget = self.getListWidgetBasedOnTab()
        current_db     = self.getDatabaseBasedOnTab()
        
        current_widget.clear()
        
        self.load_thread = ListLoader(current_widget, current_db)
        self.load_thread.length.connect(lambda length: self.getTotalLabelBasedOnTab().setText("Total: {}".format(length)))
                
        self.load_thread.start()
        

    def __init__(self, finished_db, ongoing_db, dropped_db):

        super().__init__()

        self.finished_db = finished_db
        self.ongoing_db  = ongoing_db
        self.dropped_db  = dropped_db
        self.prompt = None
        self.add_item_mutex = QMutex()
        
        uic.loadUi(self._getUiPath('MainView.ui'), self)
        
        self.setWindowIcon(Configuration.WindowIcon())
        
        self.finishedNewButton.clicked.connect(lambda: self.addEditItem())
        self.ongoingNewButton.clicked.connect(lambda: self.addEditItem())
        self.droppedNewButton.clicked.connect(lambda: self.addEditItem())
        
        self.finishedListWidget.itemDoubleClicked.connect(self.addEditItem)
        self.ongoingListWidget.itemDoubleClicked.connect(self.addEditItem)
        self.droppedListWidget.itemDoubleClicked.connect(self.addEditItem)
        
        self.finishedListWidget.installEventFilter(self)
        self.ongoingListWidget.installEventFilter(self)
        self.droppedListWidget.installEventFilter(self)
        
        self.finishedListWidget.setDragEnabled(True)
        self.ongoingListWidget.setDragEnabled(True)
        self.droppedListWidget.setDragEnabled(True)
        
        self.tabWidget.currentChanged.connect(self.tabChanged)
        self.tabChanged(0)
                
        self.show()
            
    def closeEvent(self, event):
    
        if hasattr(self, "load_thread"):
            self.load_thread.stop()
            self.load_thread.wait()
            
        #event.ignore()
            
    def eventFilter(self, watched, event):
        
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                
                list_widget = self.getListWidgetBasedOnTab()
            
                if watched is list_widget:
                    self.addEditItem(list_widget.currentItem())
                    return True
        
        return super().eventFilter(watched, event)
    
    def addEditItem(self, item = None):
    
        db = self.getDatabaseBasedOnTab()
    
        new_model = None
        old_model = None
    
        if item is None:
            new_model = GameEntity()
            old_model = copy(new_model)
        else:
            new_model = db.getByID(item.data(Qt.UserRole))
            old_model = copy(new_model)
    
        self.prompt = GameAddView(new_model)
        
        self.prompt.setModal(True)
        self.prompt.exec()
        
        if new_model == old_model:
            return

        if new_model.isClear() and not item is None:
            db.delete(old_model)
        else:
            if db.save(new_model) is None:
                print("fuck")
        
        db.flush()
        
        self.tabChanged(self.tabWidget.currentIndex())
        
    def tabChanged(self, i):

        self.fillListWidget() 

        #num_items = self.fillListWidget(self.getListWidgetBasedOnTab(), self.getDatabaseBasedOnTab()) 
        
        #label = self.getTotalLabelBasedOnTab()
        
        #label.setText("Total: {}".format(num_items))
            
            
        