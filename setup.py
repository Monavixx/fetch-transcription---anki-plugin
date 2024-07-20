from aqt.qt import QAction, QMenu
from aqt.browser import Browser
from anki.hooks import wrap
from .automatically_set_transcription import automatically_set_transcription

def setup_menu(browser: Browser):
    browser.form.menuEdit.addSeparator()
    menu = QMenu('Transcription', browser)

    action = QAction("Fetch transcription(s) manually", browser)
    action.triggered.connect(lambda: automatically_set_transcription(browser, useLocalIfAny=False, manually=True))
    menu.addAction(action)

    action = QAction("Fetch transcription(s)", browser)
    action.triggered.connect(lambda: automatically_set_transcription(browser, useLocalIfAny=False))
    menu.addAction(action)

    action = QAction("Load transcription(s) or fetch manually", browser)
    action.triggered.connect(lambda: automatically_set_transcription(browser, useLocalIfAny=True, manually=True))
    menu.addAction(action)

    action = QAction("Load transcription(s)", browser)
    action.triggered.connect(lambda: automatically_set_transcription(browser, useLocalIfAny=True))
    menu.addAction(action)

    browser.form.menuEdit.addMenu(menu)
    

def setup():
    Browser.setupMenus = wrap(Browser.setupMenus, setup_menu, "after")