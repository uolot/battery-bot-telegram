"""Telegram battery bot.

Usage:
    batbot -t TELEGRAM_TOKEN -u TELEGRAM_USER [-b BATTERY_THRESHOLD] [-f CHECK_FREQUENCY]
    batbot -c CONFIG_FILE
    batbot --help

Options:
    -t, --telegram-token=TELEGRAM_TOKEN         Telegram bot token
    -u, --telegram-user=TELEGRAM_USER           Telegram user ID
    -b, --battery-threshold=BATTERY_THRESHOLD   Battery level alert threshold [default: 10]
    -f, --check-frequency=CHECK_FREQUENCY       Level check frequency [default: 60]
    -c, --config=CONFIG_FILE                    Read config from file
    --help                                      Show this screen

Config file format:
    [bot]
    telegram_token = TELEGRAM_TOKEN
    telegram_user = TELEGRAM_USER
    battery_threshold = BATTERY_THRESHOLD
    check_frequency = CHECK_FREQUENCY
"""

import configparser
from functools import lru_cache
import logging
import socket
from typing import NamedTuple, Tuple

from docopt import docopt
import psutil
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater


def get_logger(name=__name__):
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log = logging.getLogger(name)
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    return log


log = get_logger()


class Config(NamedTuple):
    telegram_token: str
    telegram_user: str
    battery_threshold: int
    check_frequency: int
    hostname: str


def _get_battery_status() -> Tuple[bool, int]:
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = int(battery.percent)
    log.info("Battery plugged: %s percent: %s", plugged, percent)
    return plugged, percent


def start(update: Update, context: CallbackContext):
    config = get_config()
    start_msg = "\n".join(
        [
            f"Hello, I'm a battery bot @ {config.hostname}.",
            "Use /battery to check the status.",
            f"I'll update you every {config.check_frequency} seconds if the battery level drops below {config.battery_threshold}.",
        ]
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=start_msg)


def battery(update: Update, context: CallbackContext):
    config = get_config()
    plugged, percent = _get_battery_status()
    plugged_str = "plugged" if plugged else "unplugged"
    context.bot.send_message(
        chat_id=config.telegram_user,
        text=f"Battery of {config.hostname} is at {percent}%. The charger is {plugged_str}.",
    )


def battery_callback(context: CallbackContext):
    config = get_config()
    plugged, percent = _get_battery_status()
    if not plugged and percent < config.battery_threshold:
        context.bot.send_message(
            chat_id=config.telegram_user,
            text=f"Battery of {config.hostname} is at {percent}%",
        )


@lru_cache()
def get_config() -> Config:
    args = docopt(__doc__)

    if args["--config"]:
        cp = configparser.ConfigParser()
        cp.read(args["--config"])
        telegram_token = cp["bot"]["telegram_token"]
        telegram_user = cp["bot"]["telegram_user"]
        battery_threshold = cp["bot"]["battery_threshold"]
        check_frequency = cp["bot"]["check_frequency"]
    else:
        telegram_token = args["--telegram-token"]
        telegram_user = args["--telegram-user"]
        battery_threshold = args["--battery-threshold"]
        check_frequency = args["--check-frequency"]

    config = Config(
        telegram_token,
        telegram_user,
        int(battery_threshold),
        int(check_frequency),
        socket.gethostname(),
    )
    log.info("Config: %s", config)
    return config


def run_bot():
    config = get_config()

    updater = Updater(config.telegram_token, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("battery", battery))

    updater.job_queue.run_repeating(
        battery_callback, interval=config.check_frequency, first=0
    )

    updater.start_polling()
    updater.idle()
