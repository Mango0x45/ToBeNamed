import logging
import time
from threading import Lock, Thread

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
from xtypes import MintageJson


class MintageWatcher(FileSystemEventHandler):
	def __init__(self) -> None:
		self.__lock = Lock()
		self.__mintages: MintageJson = {}

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
		# TODO
		pass

	def on_deleted(self, event: FileDeletedEvent) -> None:
		# TODO
		pass

	def on_modified(self, event: FileModifiedEvent) -> None:
		# TODO
		pass

	def on_moved(self, event: FileMovedEvent) -> None:
		# TODO
		pass

	@property
	def mintages(self) -> MintageJson:
		with self.__lock:
			return self.__mintages.copy()

	def init_mintages(self, path: str) -> None:
		# TODO
		pass

	def _process(self):
		while True:
			time.sleep(1)


def setup() -> None:
	path = util.from_root("data/mintages")
	watcher.init_mintages(path)
	logging.root.debug(f"Watching for mintages in ‘{path}’")
	observer = Observer()
	observer.schedule(watcher, path=path)
	observer.start()
	logging.root.debug("Started mintage watcher")


watcher = MintageWatcher()
