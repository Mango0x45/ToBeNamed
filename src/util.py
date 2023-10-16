import os.path


def strip_jinja(s: str) -> str:
	"""
	Strip Jinja tags (‘{{’ & ‘}}’) and the translation function (‘_()’) from the
	given string.
	"""
	s = s.strip().removeprefix("{{").removesuffix("}}").strip()
	if s.startswith("_("):
		s = (
			s.removeprefix("_(")
			.removesuffix(")")
			.strip()
			.removeprefix('"')
			.removesuffix('"')
		)
	return s


def from_root(s: str) -> str:
	"""
	Get a file path for the file ‘s’ relative to the root of the ‘src/’
	directory.
	"""
	return os.path.join(os.path.dirname(__file__), s)
