
from qgis.PyQt.QtWidgets import QAction, QMessageBox

class OhsomeDownloaderPlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.action = QAction("OhsomeDownlaoder", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        QMessageBox.Information(None, "Ohsome Downloader Plugin", "Tests")
