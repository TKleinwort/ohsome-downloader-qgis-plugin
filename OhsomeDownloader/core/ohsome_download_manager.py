import json
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtNetwork import QNetworkRequest
from qgis.core import QgsBlockingNetworkRequest, QgsVectorLayer
from osgeo import gdal


class OhsomeDownloadManager:
    OHSOME_BASE_URL = "https://api.heigit.org/ohsome-api/v2-rc"
    EXTRACTION_ENDPOINT = "extraction/features.parquet"
    HARDCODE_BODY = {
        "aoi": [8.622, 49.380, 8.802, 49.440],
        "filter": "building=* and building!=no and geometry:polygon",
        "time": "latest",
        "clip": True,
    }

    def __init__(self, base_url=OHSOME_BASE_URL):
        self.base_url = base_url
        self._request_counter = 0

    def fetch_data(self, api_key):
        complete_url = f"{self.OHSOME_BASE_URL}/{self.EXTRACTION_ENDPOINT}"

        request = QNetworkRequest(QUrl(complete_url))
        request.setHeader(
            QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json"
        )
        request.setRawHeader(b"accept", b"application/octet-stream")

        request.setRawHeader(b"authorization", api_key.encode("utf-8"))

        payload = json.dumps(self.HARDCODE_BODY).encode("utf-8")

        blocking_request = QgsBlockingNetworkRequest()
        blocking_request.post(request, payload)

        return bytes(blocking_request.reply().content())

    def reply_to_layer(self, reply_data, layer_name):
        self._request_counter += 1
        vsi_path = f"/vsimem/ohsome_temp_extraction{self._request_counter}.parquet"
        gdal.FileFromMemBuffer(vsi_path, reply_data)

        layer = QgsVectorLayer(vsi_path, layer_name, "ogr")
        if not layer.isValid():
            gdal.Unlink(vsi_path)
            raise RuntimeError("Could not read GeoParquet response; unlink vsimem.")

        layer.willBeDeleted.connect(lambda p=vsi_path: gdal.Unlink(p))

        return layer
