import os
import json
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog
from qgis.core import QgsCoordinateReferenceSystem, QgsProject, QgsSettings
from qgis.PyQt.QtCore import QDate, Qt
from ..core.ohsome_download_manager import OhsomeDownloadManager

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), "ohsome_dialog.ui"))


class OhsomeDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.manager = OhsomeDownloadManager()
        self.get_topics()

        self.LineEditApiKey.setText(QgsSettings().value("ohsome/api_key", ""))
        self.DateEdit.setDate(QDate.currentDate())
        self.DateEdit.setMaximumDate(QDate.currentDate())
        self.ExtentWidget.setMapCanvas(self.iface.mapCanvas())
        self.ExtentWidget.setOutputCrs(QgsCoordinateReferenceSystem("EPSG:4326"))
        self.ExtentWidget.setCurrentExtent(
            self.iface.mapCanvas().extent(),
            self.iface.mapCanvas().mapSettings().destinationCrs(),
        )

        self.PushButtonDownload.clicked.connect(self.pushed_download)
        self.PushButtonClose.clicked.connect(self.close)

    def get_topics(self):
        settings = QgsSettings()
        today = QDate.currentDate().toString(Qt.DateFormat.ISODate)

        if settings.value("ohsome/topics_date", "") != today:
            try:
                topics = self.manager.request_topics()
                settings.setValue("ohsome/topics", json.dumps(topics))
                settings.setValue("ohsome/topics_date", today)
            except RuntimeError:
                pass

        topics = json.loads(settings.value("ohsome/topics", "{}"))
        self.ComboBoxTopic.clear()
        for topic in sorted(topics.values(), key=lambda t: t["name"]):
            self.ComboBoxTopic.addItem(topic["name"], topic["filter"])
            self.ComboBoxTopic.setItemData(
                self.ComboBoxTopic.count() - 1,
                topic["description"],
                Qt.ItemDataRole.ToolTipRole,
            )

    def get_extent(self):
        extent = self.ExtentWidget.outputExtent()
        if extent.isNull() or extent.isEmpty():
            raise ValueError("Please select a correct Extent!")
        return [extent.xMinimum(), extent.yMinimum(), extent.xMaximum(), extent.yMaximum()]

    def pushed_download(self):
        api_key_entry = self.LineEditApiKey.text().strip()
        QgsSettings().setValue("ohsome/api_key", api_key_entry or "")
        inserted_extent = self.get_extent()
        inserted_ohsome_filter = self.ComboBoxTopic.currentData()
        time_value_selection = self.DateEdit.date().toString("yyyy-MM-dd")
        try:
            request_body = self.manager.construct_request_body(
                ohsome_filter=inserted_ohsome_filter,
                time_value=time_value_selection,
                extent=inserted_extent,
            )
            data = self.manager.fetch_data(request_body=request_body, api_key=api_key_entry)
            layer = self.manager.reply_to_layer(
                data, layer_name=f"{inserted_ohsome_filter} ({time_value_selection})"
            )
            QgsProject.instance().addMapLayer(layer)
        except Exception as exc:
            self.iface.messageBar().pushCritical("ohsome", str(exc))
