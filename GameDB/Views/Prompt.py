#!/usr/bin/env python3
# coding=utf-8

from PyQt5 import QtWidgets

from GameDB.Configuration import Configuration

class Prompt:

    NoIcon      = QtWidgets.QMessageBox.NoIcon
    Question    = QtWidgets.QMessageBox.Question
    Information = QtWidgets.QMessageBox.Information
    Warning     = QtWidgets.QMessageBox.Warning
    Critical    = QtWidgets.QMessageBox.Critical

    Yes    = QtWidgets.QMessageBox.Yes
    No     = QtWidgets.QMessageBox.No
    Ok     = QtWidgets.QMessageBox.Ok
    Cancel = QtWidgets.QMessageBox.Cancel
    Save   = QtWidgets.QMessageBox.Save
    Close  = QtWidgets.QMessageBox.Close

    def show(title: str = "Prompt", content: str = "Prompt", prompt_type = QtWidgets.QMessageBox.Information, buttons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel):
    
        message = QtWidgets.QMessageBox()
        message.setIcon(prompt_type)
        message.setText(content)
        message.setWindowTitle(title)
        message.setWindowIcon(Configuration.WindowIcon())
        message.setStandardButtons(buttons)
        
        return message.exec()