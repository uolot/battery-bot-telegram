# Telegram battery bot.

Monitors laptop battery level and sends a message on Telegram when it drop below specified threshold.

To use it, register a new Telefram bot by talking to [@BotFather](https://core.telegram.org/bots#6-botfather). That will give you a new token, save it.
Then talk to @userinfobot to obtain your user id.
Pass the token and user id to the command invocation directly, or store then in the config file.

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
