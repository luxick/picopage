import argparse
import pathlib

import const


class PicoPage:
    def __init__(self, base_path):
        self.base_path = base_path

    def read_pages(self):
        pages_dir = self.base_path / const.DIR_PAGES
        for file_name in pages_dir.glob('*.md'):
            yield open(file_name).read()

    def main(self):
        print(list(self.read_pages()))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Generate static html pages.')
    parser.add_argument(
        'path',
        type=pathlib.Path,
        default=pathlib.Path('.'),
        help='Base path of the website files.')

    args = parser.parse_args()

    pico = PicoPage(args.path)
    pico.main()
