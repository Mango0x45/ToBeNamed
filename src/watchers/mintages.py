import json
import logging
import os
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
from xtypes import CaseInsensitiveString, MintageJson

MintageDict = dict[CaseInsensitiveString, MintageJson]


class MintageWatcher(FileSystemEventHandler):
	def __init__(self) -> None:
		self.__lock = Lock()
		self.__mintages: MintageDict = {}

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
		logging.root.debug(f"Detected mintage creation event ‘{event!r}’")
		self._add_mintage(event.src_path)

	def on_deleted(self, event: FileDeletedEvent) -> None:
		logging.root.debug(f"Detected mintage deletion event ‘{event!r}’")
		self._del_mintage(event.src_path)

	def on_modified(self, event: FileModifiedEvent) -> None:
		logging.root.debug(f"Detected mintage modification event ‘{event!r}’")
		self._add_mintage(event.src_path)

	def on_moved(self, event: FileMovedEvent) -> None:
		logging.root.debug(f"Detected mintage move event ‘{event!r}’")
		self._del_mintage(event.src_path)
		self._add_mintage(event.dest_path)

	def _add_mintage(self, path: str) -> None:
		code, ext = path_parts(path)
		if ext != ".json":
			return
		with self.__lock:
			with open(path, "r") as f:
				self.__mintages[code] = json.load(f)

	def _del_mintage(self, path: str) -> None:
		code, ext = path_parts(path)
		if ext != ".json":
			return
		with self.__lock:
			del self.__mintages[code]

	@property
	def mintages(self) -> MintageDict:
		with self.__lock:
			return self.__mintages.copy()

	def init_mintages(self, path: str) -> None:
		for file in os.listdir(path):
			code, _ = os.path.splitext(file)
			code = CaseInsensitiveString(code)

			with open(os.path.join(path, file), "r") as f:
				self.__mintages[code] = json.load(f)
				logging.root.debug(f"Initialized mintages for ‘{code}’")

	def _process(self):
		while True:
			time.sleep(1)


def path_parts(path: str) -> tuple[CaseInsensitiveString, str]:
	basename = os.path.basename(path)
	code, ext = os.path.splitext(basename)
	return CaseInsensitiveString(code), ext


def setup() -> None:
	path = util.from_root("data/mintages")
	watcher.init_mintages(path)
	logging.root.debug(f"Watching for mintages in ‘{path}’")
	observer = Observer()
	observer.schedule(watcher, path=path)
	observer.start()
	logging.root.debug("Started mintage watcher")


watcher = MintageWatcher()
