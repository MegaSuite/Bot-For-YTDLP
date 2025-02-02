# Setup

- [Setup](#setup)
  - [Preliminary steps](#preliminary-steps)
  - [1. Docker](#1-docker)
  - [2. Ubuntu](#2-ubuntu)
  - [3. Windows](#3-windows)
  - [Search command](#search-command)
  - [Alternative ways to pass keys](#alternative-ways-to-pass-keys)


## Preliminary steps
1. Get a telegram bot key.
2. (optional) Get a youtube api key. [See search command](#Search-command)

## 1. Docker
1. Install Docker. [docker docs](https://docs.docker.com/engine/install/ubuntu/)
```shell
sudo apt update
sudo apt install docker.io -y
```
1. Run the container with your bot key. [ytdlp-tgbot docker image](https://hub.docker.com/r/megasuite/ytdlp-tgbot)
```shell
sudo docker run -d --name ytdlp-tgbot --restart unless-stopped -e TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY> megasuite/ytdlp-tgbot:latest
```

**Optional flags**

- To run bot with search feature
```shell
-e YOUTUBE_API_KEY=<YOUTUBE_API_KEY>
```
- Mapping config folder to a volume for setting custom configurations.
```shell
-v /home/can/configs:/app/configs
```
- Mapping logs to a volume.
```shell
-v /home/can/logs:/app/logs
```
- Example with all flags
```shell
sudo docker run -d --name ytdlp-tgbot --restart unless-stopped \
-e TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY> \
-e YOUTUBE_API_KEY=<YOUTUBE_API_KEY> \
-v <YOUR_CONFIGS_PATH>/configs:/app/configs \
-v <YOUR_LOGS_PATH>/logs:/app/logs \
megasuite/ytdlp-tgbot:latest
```

## 2. Ubuntu
- Tested with `Ubuntu 24` - `Python 3.12`
1. Install ffmpeg
```shell
sudo apt update
sudo apt upgrade -y
sudo apt install ffmpeg -y
```
2. Install python and virtualenv
```shell
sudo apt install python3 -y
sudo apt install python3-pip -y

sudo apt install python3-virtualenv -y
```
3. Add your bot key to environment. Also check the [alternative ways to pass keys](#Alternative-ways-to-pass-keys).
```shell
export TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY>
source ~/.bashrc
```
- (optional) To run bot with search feature
```shell
export YOUTUBE_API_KEY=<YOUTUBE_API_KEY>
source ~/.bashrc
```
4. Install the repository and run the bot 
```shell
# Install repository
git clone https://github.com/MegaSuite/ytdlp-tgbot.git
cd ytdlp-tgbot

# Create virtualenv
virtualenv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run
python ytdlp-tgbot
```

## 3. Windows
- Tested with `Windows 10` - `Python 3.12`
1. Download ffmpeg from [ffmpeg.org](https://ffmpeg.org/).
    - Add `ffmpeg` to path, or add the binary path to `configs\config.yaml`. [See configurations](https://github.com/MegaSuite/ytdlp-tgbot/blob/master/docs/CONFIGURATIONS.md).
2. Install python from [python.org](https://www.python.org/downloads/).
3. Install requirements.
```shell
pip install -r requirements.txt
```
1. Run on cmd/terminal. Also check [Alternative ways to pass keys](#Alternative-ways-to-pass-keys).

```shell
python ytdlp-tgbot -k <TELEGRAM_BOT_KEY>
```
- (optional) To run bot with search feature
```shell
python ytdlp-tgbot -k <TELEGRAM_BOT_KEY>,<YOUTUBE_API_KEY>
```

## Search command
- `/search` is an optional feature, and requires a youtube api key.
- With search enabled you can make youtube searches and download from search results that listed as a button menu. 
- **You can get the key from [console.developers.google.com](https://console.developers.google.com/)**

<br/>

## Alternative ways to pass keys
1. With environment (Default)
    - `TELEGRAM_BOT_KEY` key must be present on environment variables.
    - To use `/search`, `YOUTUBE_API_KEY` key must be present on environment variables.
```shell
python ytdlp-tgbot
```
2. With file
    - First line has to be <TELEGRAM_BOT_KEY>.
    - To use `/search`, <YOUTUBE_API_KEY> should be on the second line.
```shell
python ytdlp-tgbot -f <FILE_PATH_FOR_KEYS>
```
3. Directly
```shell
python ytdlp-tgbot -k <TELEGRAM_BOT_KEY>
```
```shell
python ytdlp-tgbot -k <TELEGRAM_BOT_KEY>,<YOUTUBE_API_KEY>
```