
import json
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtNetwork import QNetworkRequest
from qgis.core import QgsBlockingNetworkRequest


class OhsomeDownloadManager:
    OHSOME_BASE_URL = "https://api.heigit.org/ohsome-api/v2-rc"      
    EXTRACTION_ENDPOINT = "extraction/features.parquet"
    HARDCODE_BODY = {"aoi": [8.622,8.802,49.380,49.440], 
                     "filter": "building=* and building!=no and geometry:polygon", 
                     "time": "latest",
                     "clip": True}

    def __init__(self, base_url=OHSOME_BASE_URL):
        self.base_url = base_url

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
        