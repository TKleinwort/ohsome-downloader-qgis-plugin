import os
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog
from qgis.core import QgsProject, QgsSettings
from ..core.ohsome_download_manager import OhsomeDownloadManager

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "ohsome_dialog.ui")
)

class OhsomeDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.manager = OhsomeDownloadManager

        self.LineEditApiKey.setText(QgsSettings().value("ohsome/api_key", ""))
        self.PushButtonDownload.clicked.connect(self.pushed_download)
        self.PushButtonClose.clicked.connect(self.close)

    def pushed_download(self):
        api_key_entry = self.LineEditApiKey.text().strip() or None
        QgsSettings().setValue("ohsome/api_key", api_key_entry or "")
        try:
            data = self.manager.fetch_data(api_key = api_key_entry)
            layer = self.manager.reply_to_layer(data)
            QgsProject.instance().addMapLayer(layer)
        except Exception as exc:
            self.iface.messageBar().pushCritical("ohsome", str(exc))