import os

from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy_file.storage import StorageManager

from src.config_reader import settings


def configure_storage():
    os.makedirs(os.path.join(settings.STORAGE_PATH, settings.STORAGE_CONTAINER), 0o777, exist_ok=True)
    container = LocalStorageDriver(settings.STORAGE_PATH).get_container(settings.STORAGE_CONTAINER)
    StorageManager.add_storage("default", container)
