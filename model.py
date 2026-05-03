import os
from PIL import Image
from ffmpeg import probe
from dateutil.parser import parse
from datetime import datetime
import uuid

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tif", ".tiff"}
VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".wmv"}


class Medium:
    def __init__(self, path: str, perch_mount_name: str) -> None:
        self.id = uuid.uuid4()
        self.path = path
        self.perch_mount_name = perch_mount_name
        self.medium_type = self._find_medium_type(path)
        self.medium_datetime = self._get_datetime(path, self.medium_type)

    @property
    def str_medium_datetime(self):
        return datetime.strftime(self.medium_datetime, "%Y-%m-%d %H:%M:%S")

    @property
    def _str_datetime_for_filename(self):
        return datetime.strftime(self.medium_datetime, "%Y%m%d_%H%M%S")

    def _find_medium_type(self, path) -> str | None:
        _, ext = os.path.splitext(path)
        ext_lower = ext.lower()
        if ext_lower in IMAGE_EXTS:
            medium_type = "IMAGE"
        elif ext_lower in VIDEO_EXTS:
            medium_type = "VIDEO"
        else:
            return
        return medium_type

    def _get_datetime(self, path: str, medium_type: str) -> datetime | None:
        dt = None
        if medium_type == "IMAGE":
            dt = Image.open(path)._getexif()[36867]
            dt = datetime.strptime(dt, "%Y:%m:%d %H:%M:%S")
        elif medium_type == "VIDEO":
            dt = probe(path)["streams"][0]["tags"]["creation_time"]
            dt = parse(dt).replace(tzinfo=None)
        return dt

    @property
    def s3_file_name(self):
        _, ext = os.path.splitext(self.path)
        return "%s_%s_%s%s" % (
            self.perch_mount_name,
            self._str_datetime_for_filename,
            str(self.id)[:8],
            ext.lower(),
        )

    def json(self) -> dict:
        return {
            "id": str(self.id),
            "medium_datetime": self.str_medium_datetime,
            "medium_type": self.medium_type,
            "s3_file_name": self.s3_file_name,
        }
