"""OhsomeDownloader plugin init."""


def classFactory(iface):
    """Launch of the plugin."""
    from .ohsome_downloader import OhsomeDownloaderPlugin
    return OhsomeDownloaderPlugin(iface)
