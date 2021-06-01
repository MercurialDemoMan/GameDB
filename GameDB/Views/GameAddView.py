#!/usr/bin/env python3
# coding=utf-8

import sys
import os
import urllib.request
import shutil
import ntpath

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QEvent
from PyQt5 import QtGui

from GameDB.Repositories.GameRepository import GameRepository
from GameDB.Entities.GameEntity import GameEntity
from GameDB.Configuration import Configuration
from GameDB.Views.Prompt import Prompt

class GameAddView(QtWidgets.QDialog):

    def _getUiPath(self, ui_file_name):
        """Get absolute ui path"""

        script_path = os.path.realpath(__file__)
        parent_dir = os.path.dirname(script_path)
        return os.path.join(parent_dir, ui_file_name)

    def __init__(self, model: GameEntity):

        super().__init__()
        
        self.setWindowIcon(Configuration.WindowIcon())

        uic.loadUi(self._getUiPath('GameAddView.ui'), self)
        
        self.model = model
        
        self.setAcceptDrops(True)
        
        self.saveButton.clicked.connect(lambda: self.save())
        self.cancelButton.clicked.connect(lambda: self.close())
        
        if self.model.ID is None:
            self.deleteButton.setEnabled(False)
            self.moveButton.setEnabled(False)
        else:
            self.deleteButton.clicked.connect(lambda: self.delete())
            self.moveButton.clicked.connect(lambda: self.moveTo())
       
        self.nameEdit.setText(self.model.name)
        self.platformEdit.setText(self.model.platform)
        self.ratingEdit.setText(self.model.rating)
        self.reviewEdit.setText(self.model.review)
        self.reviewEdit.setAlignment(Qt.AlignJustify)
        self.reviewEdit.setAcceptDrops(False)
        
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.setImage(self.model.image_url)
        
    def dragEnterEvent(self, event):
    
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
    
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        
        if len(files) != 0:
            
            src_path = files[0]
            dst_path = Configuration.ImageDatabasePath() + ntpath.basename(src_path)
            
            shutil.copyfile(src_path, dst_path)
            
            self.model.image_url = ntpath.basename(src_path)
            self.setImage(self.model.image_url)
    
    def setImage(self, image_path: str):
    
        self._pixmap = QtGui.QPixmap()
        
        if image_path is None:
            self._pixmap = Configuration.MissingPixmap()
        elif not self._pixmap.load(Configuration.ImageDatabasePath() + self.model.image_url):
            self._pixmap = Configuration.MissingPixmap()
        
        self.imageLabel.setPixmap(self._pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    
    def moveTo(self):
        
        res = Prompt.show("Move To", "Choose, where you want to move this record", Prompt.NoIcon, Prompt.Yes | Prompt.No | Prompt.Cancel)
    
    def resizeEvent(self, e):
    
        self.imageLabel.setPixmap(self._pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            
    def save(self):
    
        self.model.name     = self.nameEdit.text()
        self.model.platform = self.platformEdit.text()
        self.model.rating   = self.ratingEdit.text()
        self.model.review   = self.reviewEdit.toPlainText()
        self.close()
        
    def delete(self):
        
        res = Prompt.show("Warning", "Are you sure you want to delete this record?", Prompt.Warning, Prompt.Yes | Prompt.No)
        
        if res == Prompt.Yes:
            self.model.clear()
            self.close()