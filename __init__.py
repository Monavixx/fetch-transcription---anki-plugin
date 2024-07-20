from aqt import mw
from aqt.qt import QAction, QInputDialog, QMessageBox, QWidget, QVBoxLayout, QLabel, QDialog
from aqt.browser import Browser
from anki.hooks import wrap
import requests
import re
from bs4 import BeautifulSoup
import os
from .setup import setup

setup()
