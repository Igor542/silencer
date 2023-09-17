import argparse
import logging

from bot import Bot


class Silencer:
    def __init__(self, token_file, data_dir, lang):
        self.bot = Bot(token_file, data_dir, lang)

    def run(self):
        self.bot.run()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="A Telegram bot to convert audio messages into text",
    )
    parser.add_argument(
        "-t",
        "--token",
        type=str,
        default="__data/secrets/TOKEN",
        help="path to telegram bot token file",
    )
    parser.add_argument(
        "-d",
        "--data",
        type=str,
        default="__data/storage",
        help="path for data storage directory",
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default="english",
        help="language",
    )
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    LOG_LEVELS = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    log_level = LOG_LEVELS[min(args.verbose, len(LOG_LEVELS) - 1)]

    logging.basicConfig(
        format="%(asctime)s - %(name)s" "- %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    silencer = Silencer(args.token, args.data, args.language)
    silencer.run()


if __name__ == "__main__":
    main()
