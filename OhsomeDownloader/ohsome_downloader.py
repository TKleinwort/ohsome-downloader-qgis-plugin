
import os
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox

class OhsomeDownloaderPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.ohsome_downloader_dir = os.path.dirname(__file__)

    def initGui(self):
        icon = QIcon(os.path.join(self.ohsome_downloader_dir, 'resources', 'img', 'icon.png'))
        self.action = QAction(icon, "OhsomeDownlaoder", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        QMessageBox.information(None, "Ohsome Downloader Plugin", "Tests")
