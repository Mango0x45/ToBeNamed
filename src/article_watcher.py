import datetime
import logging
import os
import time
from threading import Lock, Thread
from typing import NamedTuple, Self

from flask_babel import _
from selectolax.parser import HTMLParser
from watchdog.events import (
	FileCreatedEvent,
	FileDeletedEvent,
	FileModifiedEvent,
	FileMovedEvent,
	FileSystemEvent,
	FileSystemEventHandler,
)
from watchdog.observers import Observer

import util
from xtypes import ListExt


class RawArticle(NamedTuple):
	headline: str
	date: datetime.date

	def __lt__(self, value: Self) -> bool:
		# We make the bisect module work with our list in descending order by
		# tricking it into thinking it’s ascending.
		return self.date > value.date

	def __eq__(self, value: Self) -> bool:
		return self.date == value.date


class ArticleWatcher(FileSystemEventHandler):
	def __init__(self) -> None:
		self.__lock = Lock()
		self.__xs: ListExt[RawArticle] = ListExt()

		super().__init__()

	def start(self) -> None:
		self._thread = Thread(target=self._process)
		self._thread.daemon = True
		self._thread.start()

	def dispatch(self, event: FileSystemEvent) -> None:
		match event:
			case FileCreatedEvent():
				self.on_created(event)
			case FileDeletedEvent():
				self.on_deleted(event)
			case FileModifiedEvent():
				self.on_modified(event)
			case FileMovedEvent():
				self.on_moved(event)

	def on_created(self, event: FileCreatedEvent) -> None:
		logging.root.debug(f"Detected article creation event ‘{event!r}’")

		headline = extract_header(event.src_path)
		date = file_to_date(event.src_path)
		if not headline or not date:
			return
		ra = RawArticle(headline=headline, date=date)

		with self.__lock:
			self.__xs.sorted_insert(ra)

	def on_deleted(self, event: FileDeletedEvent) -> None:
		logging.root.debug(f"Detected article deletion event ‘{event!r}’")

		if (date := file_to_date(event.src_path)) is None:
			return

		with self.__lock:
			self.__xs.try_remove(RawArticle(headline="", date=date))

	def on_modified(self, event: FileModifiedEvent) -> None:
		logging.root.debug(f"Detected article modification event ‘{event!r}’")

		headline = extract_header(event.src_path)
		date = file_to_date(event.src_path)
		if not headline or not date:
			return
		ra = RawArticle(headline=headline, date=date)

		with self.__lock:
			self.__xs.try_remove(ra)
			self.__xs.sorted_insert(ra)

	def on_moved(self, event: FileMovedEvent) -> None:
		logging.root.debug(f"Detected article move event ‘{event!r}’")

		headline = extract_header(event.dest_path)
		old = file_to_date(event.src_path)
		new = file_to_date(event.dest_path)
		if not headline or not new:
			return

		ra = RawArticle(headline=headline, date=new)

		with self.__lock:
			if old is not None:
				self.__xs.try_remove(RawArticle(headline="", date=old))
			self.__xs.try_remove(ra)
			self.__xs.sorted_insert(ra)

	@property
	def articles(self) -> list[RawArticle]:
		with self.__lock:
			return self.__xs.copy()

	def init_articles(self, path: str) -> None:
		for f in os.listdir(path):
			headline = extract_header(os.path.join(path, f))
			date = file_to_date(f)

			if headline and date:
				ra = RawArticle(headline=headline, date=date)
				self.__xs.sorted_insert(ra)

	def _process(self) -> None:
		while True:
			time.sleep(1)


def extract_header(filename: str) -> str | None:
	try:
		with open(filename, "r", encoding="UTF-8") as f:
			p = HTMLParser(f.read())
	except FileNotFoundError:
		return

	return (
		util.strip_jinja(s.text())
		if (s := p.css_first("h1"))
		else _("No headline found")
	)


def file_to_date(filename: str) -> datetime.date | None:
	base = os.path.basename(filename)
	parts: tuple[str, str] = os.path.splitext(base)
	name, _ = parts
	try:
		y, m, d = map(int, name.split("-"))
	except ValueError:
		return
	return datetime.date(year=y, month=m, day=d)


def setup() -> None:
	path = os.path.join(os.path.dirname(__file__), "templates/news/articles")
	watcher.init_articles(path)
	logging.root.debug(f"Watching for articles in ‘{path}’")
	observer = Observer()
	observer.schedule(watcher, path=path)
	observer.start()
	logging.root.debug("Started article watcher")


watcher = ArticleWatcher()
