import os
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog
from ..core.ohsome_download_manager import OhsomeDownloadManager


FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "ohsome_dialog.ui")
)

class OhsomeDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.iface = iface