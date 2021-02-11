import sys

from .mocker import Mocker
from .mocker_config import MockerConfig


def main(is_test: bool):
    mocker_config = MockerConfig()
    mocker = Mocker(mocker_config)
    if is_test:
        print("All good, the mocker could start.")
        return
    mocker.start()


if __name__ == '__main__':
    is_test = len(sys.argv) >= 2 and sys.argv[1] == 'test'
    main(is_test)
