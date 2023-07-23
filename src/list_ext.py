import bisect
from abc import abstractmethod
from typing import Generic, Protocol, Self, TypeVar


class Comparable(Protocol):
	@abstractmethod
	def __lt__(self, value: Self) -> bool:
		...

	@abstractmethod
	def __eq__(self, value: Self) -> bool:
		...


T = TypeVar("T", bound=Comparable)


class ListExt(list, Generic[T]):
	def try_remove(self, value: T) -> None:
		try:
			super().remove(value)
		except ValueError:
			pass

	def sorted_insert(self, value: T) -> None:
		bisect.insort(self, value)
