import os, sys
import logging, re

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/thirdparty"
)

import speech2text
from speech2text.speech2text.model import Whisper as Model
from speech2text.speech2text.utils import read_audio


class Bot:
    def __init__(self, token_file, data_dir, lang):
        self.data_dir = data_dir
        if not os.path.isdir(self.data_dir):
            os.makedirs(self.data_dir)
        self.bot = telegram.Bot(token=self.__read_token(token_file))
        self.updater = Updater(
            bot=self.bot, use_context=True, user_sig_handler=self.exit
        )
        self.m = Model(lang=lang)
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(MessageHandler(filters.Filters.all, self.echo))

    def echo(self, update, context):
        update.message.reply_text("Received a message. Working on it...")
        voice = update.message.voice
        if voice != None:
            file_id = voice.file_id
            custom_path = self.data_dir + "/" + file_id
            voice.get_file().download(custom_path=custom_path)
            speech = read_audio(custom_path, Model.sampling_rate)
            transcription = self.m.process(speech)
            update.message.reply_text(transcription[0])
        else:
            update.message.reply_text("There was no voice data found.")

    def __read_token(self, token_file):
        def complain(s):
            logging.critical(f"{s}. Exiting...")
            exit(2)

        if not os.path.isfile(token_file):
            complain(f'Token file "{token_file}" is not found')
        with open(token_file, "r") as f:
            token = f.readlines()

        if len(token) != 1:
            complain(f"Token file should have exactly one line (now has {len(token)})")
        token = token[0].strip()

        if not re.match(r"^\d+:\w+$", token):
            complain(f"Token has wrong format")
        return token

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

    def exit(self, signo, stack_frame):
        logging.info(f"Stopping the bot...")
        self.updater.stop()
