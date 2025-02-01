import threading
import time
import os
import shutil

from telegram_media_sender import TelegramMediaSender
from youtube_downloader import YoutubeDownloader

from errors.download_error import DownloadError
from utils.logger_factory import LoggerFactory
from statics.content_type import ContentType
from errors.send_error import SendError
from utils.config_utils import ConfigUtils


class DownloadThread(threading.Thread):
    def __init__(self, downloader: YoutubeDownloader, media_sender: TelegramMediaSender, url: str, chat_id: int, content_type: ContentType, 
                 dl_format_name: "str | None", use_cookie: bool = False) -> None:
        super().__init__()
        self.__logger = LoggerFactory.get_logger(self.__class__.__name__)
        self.downloader = downloader
        self.media_sender = media_sender
        self.url = url
        self.chat_id = chat_id
        self.content_type = content_type
        self.dl_format_name = dl_format_name
        self.use_cookie = use_cookie


    def __get_extension_from_config(self, content_type: ContentType) -> str:
        """Get file extension from config based on content type"""
        config = ConfigUtils.read_cfg_file()["youtube_downloader_options"]
        
        if content_type == ContentType.AUDIO:
            # Get preferred codec for audio from postprocessors
            audio_options = config["audio_options"]
            if "postprocessors" in audio_options:
                for processor in audio_options["postprocessors"]:
                    if processor["key"] == "FFmpegExtractAudio":
                        return processor.get("preferredcodec", "mp3")
            return "mp3"  # Default fallback
            
        elif content_type == ContentType.VIDEO:
            # Get preferred format for video from postprocessors
            video_options = config["video_options"] 
            if "postprocessors" in video_options:
                for processor in video_options["postprocessors"]:
                    if processor["key"] == "FFmpegVideoConvertor":
                        return processor.get("preferedformat", "mkv")
            return "mkv"  # Default fallback
        
    def __run_for_audio(self) -> None:
        download_start = time.time()
        result = self.downloader.download(self.url, ContentType.AUDIO, self.dl_format_name)
        self.__logger.info(f"Download completed {result}, took {float(time.time() - download_start):.3f} seconds")

        # 获取配置
        save_options = ConfigUtils.read_cfg_file()["save_options"]
        
        if save_options["location"] == "telegram":
            # 原有的发送到Telegram的逻辑
            self.media_sender.send_text(self.chat_id, "⬆️🎧 Download finished, sending...")
            upload_start = time.time()
            self.media_sender.send_audio(
                chat_id=self.chat_id, 
                file_path=result.file_path,
                title=result.video_title,
                remove=True
            )
            self.media_sender.send_text(self.chat_id, "🥳")
            self.__logger.info(f"Upload completed, took {float(time.time() - upload_start):.3f} seconds")
            self.__logger.info(f"Total operation took {float(time.time() - download_start):.3f} seconds")
        
        elif save_options["location"] == "local":
            # Save to local with proper extension
            self.media_sender.send_text(self.chat_id, "⬆️🎧 Download finished, saving...")
            save_dir = save_options["directory"]
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            ext = self.__get_extension_from_config(ContentType.AUDIO)
            filename = f"{result.video_title}.{ext}"
            # Move file to specified directory
            shutil.move(result.file_path, os.path.join(save_dir, filename))
            self.media_sender.send_text(self.chat_id, f"✅ File saved to {save_dir}/{filename}")

    def __run_for_video(self) -> None:
        download_start = time.time()
        result = self.downloader.download(self.url, ContentType.VIDEO, self.dl_format_name)
        self.__logger.info(f"Download completed {result}, took {float(time.time() - download_start):.3f} seconds")

        save_options = ConfigUtils.read_cfg_file()["save_options"]
        
        if save_options["location"] == "telegram":
            # 原有的发送到Telegram的逻辑 
            self.media_sender.send_text(self.chat_id, "⬆️📽️ Download finished, sending...")
            upload_start = time.time()
            self.media_sender.send_video(
                chat_id=self.chat_id,
                file_path=result.file_path,
                title=result.video_title,
                remove=True
            )
            self.media_sender.send_text(self.chat_id, "🥳")
            self.__logger.info(f"Upload completed, took {float(time.time() - upload_start):.3f} seconds")
            self.__logger.info(f"Total operation took {float(time.time() - download_start):.3f} seconds")
            
        elif save_options["location"] == "local":
            # Save to local with proper extension
            self.media_sender.send_text(self.chat_id, "⬆️📽️ Download finished, saving...")
            save_dir = save_options["directory"]
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                
            ext = self.__get_extension_from_config(ContentType.VIDEO)
            filename = f"{result.video_title}.{ext}"
            # Move file to specified directory 
            shutil.move(result.file_path, os.path.join(save_dir, filename))
            self.media_sender.send_text(self.chat_id, f"✅ File saved to {save_dir}/{filename}")
            

    def run(self) -> None:
        self.__logger.info(f"Download started for url {self.url}")

        try:
            # TODO Might convert to inheritance later
            if(self.content_type == ContentType.AUDIO):
                self.__run_for_audio()
            elif(self.content_type == ContentType.VIDEO):
                result = self.downloader.download(
                    self.url, 
                    ContentType.VIDEO, 
                    self.dl_format_name,
                    use_cookie=self.use_cookie
                )
                self.__run_for_video()
            else:
                pass

        except (DownloadError, SendError) as e:
            self.__logger.warn(str(e))
            # Try to answer on error
            try:
                self.media_sender.send_text(chat_id=self.chat_id, text=f"💩 {str(e)}")
            except:
                self.__logger.error(f"User notifying attempt (via message) for an error failed due to another error during message sending, {str(e)}", exc_info=True)
        except Exception as e:
            self.__logger.error("Unknown error", exc_info=True)
            # Try to answer on error
            try:
                self.media_sender.send_text(chat_id=self.chat_id, text="🤷🏻‍♂️ Unknown error")
            except:
                self.__logger.error(f"User notifying attempt (via message) for an error failed due to another error during message sending, {str(e)}", exc_info=True)

