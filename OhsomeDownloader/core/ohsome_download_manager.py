
class OhsomeDownloadManager:
    OHSOME_BASE_URL = "https://api.heigit.org/ohsome-api/v2-rc"      
    EXTRACTION_ENDPOINT = "extraction/features.parquet"

    def __init__(self, base_url=OHSOME_BASE_URL):
        self.base_url = base_url

        