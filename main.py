import logging
from bot import TelegramBot

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    bot = TelegramBot()
    bot.run()

if __name__ == '__main__':
    main()