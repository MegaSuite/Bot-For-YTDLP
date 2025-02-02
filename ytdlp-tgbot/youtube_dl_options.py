import pathlib
import uuid
import os

from statics.content_type import ContentType
from utils.config_utils import ConfigUtils
from utils.logger_factory import LoggerFactory

class YoutubeDlOptions:
    def __init__(self, use_cookie: bool = False):
        self.__youtube_dl_options = ConfigUtils.read_cfg_file()["youtube_downloader_options"]
        self.__logger = LoggerFactory.get_logger(self.__class__.__name__)

        save_dir = self.__get_random_dir_path()
        self.__audio_options = {
            # Spread values from config file
            **self.__youtube_dl_options["audio_options"],

            "outtmpl": os.path.join(save_dir, "TEMP" + ".%(ext)s"),

            # For custom downloader class 
            "content_type": ContentType.AUDIO,
            "save_dir": save_dir,
            "max_duration_seconds": self.__youtube_dl_options["max_audio_duration_seconds"]
        }

        self.__video_options = {
            # Spread values from config file
            **self.__youtube_dl_options["video_options"],

            "outtmpl": os.path.join(save_dir, "TEMP" + ".%(ext)s"),

            # For custom downloader class 
            "content_type": ContentType.VIDEO,
            "save_dir": save_dir,
            "max_duration_seconds": self.__youtube_dl_options["max_video_duration_seconds"]
        }

        # Add ffmpeg_location if exists
        if(self.__youtube_dl_options["ffmpeg_location"]):
            self.__audio_options["ffmpeg_location"] = self.__youtube_dl_options["ffmpeg_location"]
            self.__video_options["ffmpeg_location"] = self.__youtube_dl_options["ffmpeg_location"]

        if use_cookie:
            cookie = self.__get_cookie()
            if cookie:
                self.__audio_options["cookiefile"] = cookie
                self.__video_options["cookiefile"] = cookie

    def __get_random_dir_path(self):
        path = os.path.join("temp", str(uuid.uuid4()))
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        return path

    def set_format(self, content_type: ContentType, fmt: str):
        if(content_type == content_type.VIDEO):
            self.__video_options.update({"format": f'({fmt})'})
        if(content_type == content_type.AUDIO):
            self.__audio_options.update({"format": f'({fmt})'})

    def get_for_content_type(self, content_type: ContentType):
        if(content_type == ContentType.VIDEO):
            return self.__video_options
        if(content_type == ContentType.AUDIO):
            return self.__audio_options

    def __get_cookie(self) -> str | None:
        """Get cookie from file"""
        cookie_options = self.__youtube_dl_options.get("cookie_options", {})
        
        cookie_file = cookie_options.get("cookie_file")
        if cookie_file:
            if not os.path.isabs(cookie_file):
                cookie_file = os.path.join(os.getcwd(), cookie_file)
            if os.path.exists(cookie_file):
                return cookie_file
            
        return None