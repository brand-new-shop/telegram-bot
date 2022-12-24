import pathlib

from config import Config


def main():
    config_file_path = pathlib.Path(__file__).parent.parent / 'config.ini'
    config = Config.from_file(config_file_path)


if __name__ == '__main__':
    main()
