from environs import Env

from telegram.ext import Updater


env = Env()
env.read_env()


def main():
    tg_token = env.str('TELEGRAM_TOKEN')

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
