# Silencer

A Telegram bot that translates audio messages into text.

The bot is based on a [Transformers-based Whisper model](https://huggingface.co/openai/whisper-medium) via [a thin wrapper](https://github.com/Igor542/speech2text) and can translate audio messages to a different language.

## Usage

```sh
$ conda create -f environment.yml
$ conda activate telegram-bot-silencer
$ python3 silencer/silencer.py -t TOKEN
```

## TODO

- [ ] Docker image
- [ ] Limit the bot to answer only to a single user (the first user or pass uid as an argument)
