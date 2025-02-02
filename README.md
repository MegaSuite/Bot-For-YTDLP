# ytdlp-tgbot
![GitHub top language](https://img.shields.io/github/languages/top/MegaSuite/ytdlp-tgbot?color=blue&style=for-the-badge)  [![GitHub](https://img.shields.io/github/license/MegaSuite/ytdlp-tgbot?color=brightgreen&style=for-the-badge)](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/LICENSE) [![Docker Pulls](https://img.shields.io/docker/pulls/megasuite/ytdlp-tgbot?color=blue&style=for-the-badge)](https://hub.docker.com/r/megasuite/ytdlp-tgbot) [![Docker Image Size (tag)](https://img.shields.io/docker/image-size/megasuite/ytdlp-tgbot/latest?color=teal&style=for-the-badge)](https://hub.docker.com/r/megasuite/ytdlp-tgbot)

## What's new ?
- change `save_options` in `configs/configs.yaml` to change between `saving locally` and `send through telegram`.
- Use `/vc` command to download with the cookie you set.
- Use alpine as base image for smaller image size and optimized many details.

## Commands

### 1. Download
```shell
/video <download url>
/video <format> <download url>
/v <download url>
/vc <download url> #download with cookie
```
```shell
/audio <download url>
/audio <format> <download url>
/a <download url>
```
- You can set a [default command](https://github.com/MegaSuite/ytdlp-tgbot/blob/master/docs/CONFIGURATIONS.md#default_command) to run a download command on bare messages.

### 2. Search
Performs a YouTube search to download. [Also see setup/search](https://github.com//MegaSuite/ytdlp-tgbot/blob/master/docs/SETUP.md#search-command)
```shell
/search <query>
/s <query>
```

### 3. Utilities
[See configurations](https://github.com//MegaSuite/ytdlp-tgbot/blob/master/docs/CONFIGURATIONS.md) for command configurations.
```shell
/formats
/sites
/help
/about
```

## Running
You can also run the bot without Docker and with multiple other ways check [Setup](https://github.com//MegaSuite/ytdlp-tgbot/blob/master/docs/SETUP.md) for more information.
### Docker 
Example with all flags [Setup with Docker](https://github.com//MegaSuite/ytdlp-tgbot/blob/master/docs/SETUP.md#1-docker)
  - Search feature [Setup/search](https://github.com/MegaSuite/ytdlp-tgbot/blob/master/docs/SETUP.md#search-command)
  - Mapped logs
  - Custom configurations
```shell
docker run -d --name ytdlp-tgbot --restart unless-stopped \
-e TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY> \
-e YOUTUBE_API_KEY=<YOUTUBE_API_KEY> \
-v <YOUR_CONFIGS_PATH>/configs:/app/configs \
-v <LOCAL_SAVE_PATH>/app/downloads \
-v <YOUR_LOGS_PATH>/logs:/app/logs \
megasuite/ytdlp-tgbot:latest
```

## Docs
### Also see
- [Setup](https://github.com/MegaSuite/ytdlp-tgbot/blob/master/docs/SETUP.md) for more ways to run the bot.
- [Configurations](https://github.com//MegaSuite/ytdlp-tgbot/blob/master/docs/CONFIGURATIONS.md) for all configurable options.
- [Hardware Acceleration](https://github.com//MegaSuite/ytdlp-tgbot/blob/master/docs/HARDWARE_ACCELERATION.md) for using ffmpeg with hardware acceleration.
- [Api Server](https://github.com//MegaSuite/ytdlp-tgbot/blob/master/docs/API_SERVER.md) for using with custom telegram api server with increased download limits.
