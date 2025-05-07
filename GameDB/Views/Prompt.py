#!/usr/bin/env python3
# coding=utf-8

from PyQt6 import QtWidgets

from GameDB.Configuration import Configuration

class Prompt:

    NoIcon      = QtWidgets.QMessageBox.Icon.NoIcon
    Question    = QtWidgets.QMessageBox.Icon.Question
    Information = QtWidgets.QMessageBox.Icon.Information
    Warning     = QtWidgets.QMessageBox.Icon.Warning
    Critical    = QtWidgets.QMessageBox.Icon.Critical

    Yes    = QtWidgets.QMessageBox.StandardButton.Yes
    No     = QtWidgets.QMessageBox.StandardButton.No
    Ok     = QtWidgets.QMessageBox.StandardButton.Ok
    Cancel = QtWidgets.QMessageBox.StandardButton.Cancel
    Save   = QtWidgets.QMessageBox.StandardButton.Save
    Close  = QtWidgets.QMessageBox.StandardButton.Close

    def show(title: str = "Prompt", content: str = "Prompt", prompt_type = QtWidgets.QMessageBox.Icon.Information, buttons = QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel):
    
        message = QtWidgets.QMessageBox()
        message.setIcon(prompt_type)
        message.setText(content)
        message.setWindowTitle(title)
        message.setWindowIcon(Configuration.WindowIcon())
        message.setStandardButtons(buttons)
        
        return message.exec()
