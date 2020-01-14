# Telegram battery bot.

Monitors laptop battery level and sends a message on Telegram when it drop below specified threshold.

## Usage:

    batbottg -t TELEGRAM_TOKEN -u TELEGRAM_USER [-b BATTERY_THRESHOLD] [-f CHECK_FREQUENCY]
    batbottg -c CONFIG_FILE
    batbottg --help

## Options:

    -t, --telegram-token=TELEGRAM_TOKEN         Telegram bot token
    -u, --telegram-user=TELEGRAM_USER           Telegram user ID
    -b, --battery-threshold=BATTERY_THRESHOLD   Battery level alert threshold [default: 10]
    -f, --check-frequency=CHECK_FREQUENCY       Level check frequency [default: 60]
    -c, --config=CONFIG_FILE                    Read config from file
    --help                                      Show this screen

## Config file format:

    [bot]
    telegram_token = TELEGRAM_TOKEN
    telegram_user = TELEGRAM_USER
    battery_threshold = BATTERY_THRESHOLD
    check_frequency = CHECK_FREQUENCY
