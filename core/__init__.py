import eel

__version_info__ = ('1', '1', '0')
__version__ = '.'.join(__version_info__)
__release_date__ = "2024-10-30"


@eel.expose
def get_software_version():
    return {
        "status": "success",
        "data": {
            "version": __version__,
            "release_date": __release_date__
        }
    }