from controller import Controller
from loguru import logger


def main():
    app = Controller()
    app.run()
    logger.add("file.log",
               format="{time:YYYY-MM-DD at HH-MM-SS} | {level} | {message}",
               rotation="3 days",
               backtrace=True,
               diagnose=True)


if __name__ == "__main__":
    main()
