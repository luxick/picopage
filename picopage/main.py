import argparse
import errno
import os
import shutil

from pathlib import Path
from typing import Iterable, List, Union

from dataclasses import dataclass
import markdown
import yaml
from jinja2 import Template, Environment, FileSystemLoader

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
THEMES_PATH = Path(SCRIPT_PATH, "themes")
TEMPLATES_PATH = Path(SCRIPT_PATH, "templates")

ENV = Environment(loader=FileSystemLoader(str(TEMPLATES_PATH)))


@dataclass
class Article:
    stub: str
    title: str
    created: str
    content: str
    updated: str = None


@dataclass
class Page:
    name: str
    pos: int
    stub: str
    articles: List[Article] = None
    is_index: bool = False


@dataclass
class Site:
    title: str
    author: str
    theme: str
    pages: List[Page] = None


class PicoPage:
    def __init__(self, path, out_path=None):
        self.in_path = Path(path)

        if out_path is None:
            self.out_path = Path(self.in_path.parent / "publish")
        else:
            self.out_path = Path(out_path)

        conf = self.read_config(self.in_path)
        conf["theme"] = f"{conf.get('theme', 'default')}.css"

        pages = self.read_pages(self.in_path)
        self.site = Site(conf["title"], conf["author"], conf["theme"], pages)

        article_count = len([a for pages in self.site.pages for a in pages.articles])
        print(f"Read {len(self.site.pages)} pages with {article_count} articles")

    @staticmethod
    def parse_metadata(md: markdown.Markdown) -> Article:
        title = "No Title"
        try:
            title = md.Meta["title"][0]
        except KeyError:
            pass

        created = "Never"
        try:
            created = md.Meta["created"][0]
        except KeyError:
            pass

        updated = "Never"
        try:
            updated = md.Meta["updated"][0]
        except KeyError:
            pass

        return Article(content="",
                       stub="",
                       title=title,
                       created=created,
                       updated=updated)

    @staticmethod
    def load_template(path: Path) -> Template:
        with open(str(path), "r") as file:
            return Template(file.read())

    @staticmethod
    def read_config(path: Path) -> dict:
        conf_path = path / "config.yaml"

        if not conf_path.exists():
            print(f"Warning: No config file in '{conf_path}'")
            return {}

        with open(str(conf_path), "r") as file:
            try:
                return yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print(exc)

    def read_pages(self, path) -> List[Page]:
        pages = []
        root = Path(path)

        # Parse root page
        articles = list(self.read_articles(root))
        page = Page(name=root.stem,
                    stub="index",
                    pos=0,
                    is_index=True,
                    articles=sorted(articles, key=lambda a: a.stub))
        pages.append(page)

        # Parse sub pages
        for sub in root.glob("**/"):
            if sub == root:
                continue

            articles = list(self.read_articles(sub))
            # Ignore sub dirs without markdown files
            if len(articles) == 0:
                continue

            conf = self.read_config(sub)

            page = Page(name=conf.get("title", sub.stem),
                        stub=sub.stem,
                        pos=conf.get("position", 100),
                        articles=sorted(articles, key=lambda a: a.stub))
            pages.append(page)

        return sorted(pages, key=lambda p: p.pos)

    @staticmethod
    def read_files(path: Path):
        for file_name in path.glob('*.md'):
            yield file_name.stem, open(str(file_name)).read()

    def read_articles(self, path: Path) -> Iterable[Article]:
        md = markdown.Markdown(extensions=['meta', 'extra'])
        for name, data in self.read_files(path):
            html = md.convert(data)
            article = self.parse_metadata(md)
            article.stub = name.replace(" ", "").lower()
            article.content = html
            yield article

    def copy_static(self):
        src = str(self.in_path)
        dest = str(self.out_path)
        try:
            shutil.copytree(src, dest, ignore=shutil.ignore_patterns("*.md", "*.yaml"))
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.copy(src, dest)
            else:
                print('Directory not copied. Error: %s' % e)

    def write_output(self):
        if Path.exists(self.out_path):
            shutil.rmtree(self.out_path)
        # self.out_path.mkdir()
        self.copy_static()

        template = ENV.get_template("page.html")

        for page in self.site.pages:
            page_vars = {
                "site_title": self.site.title,
                "page_title": page.name,
                "theme": self.site.theme,
                "pages": self.site.pages,
                "current_page": page
            }
            html = template.render(page_vars)

            path = self.out_path
            if page.is_index:
                path = path / "index.html"
            else:
                path = path / page.stub / "index.html"

            if not Path(path.parent).exists():
                Path(path.parent).mkdir()

            with open(str(path), "w") as outfile:
                outfile.write(html)

        shutil.copyfile(THEMES_PATH / self.site.theme, self.out_path / self.site.theme)

        print(f"Finished. {len(self.site.pages)} HTML files written.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate static html pages.')
    parser.add_argument(
        'path',
        type=Path,
        default=Path('.'),
        help='Base path of the website files.')
    parser.add_argument(
        'out_path',
        type=Path,
        nargs='?',
        help='Output path for the generated website.')

    args = parser.parse_args()

    pico = PicoPage(args.path, args.out_path)
    pico.write_output()
