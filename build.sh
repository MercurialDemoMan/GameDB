#!/bin/bash

set -xe

pyinstaller -y App.pyw
cp -r GameDB/Views dist/App/GameDB/Views
