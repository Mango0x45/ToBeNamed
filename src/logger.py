import logging.config


def setup(debug: bool) -> None:
	logging.config.dictConfig(
		{
			"version": 1,
			"formatters": {
				"default": {
					"format": "%(levelname)s in %(module)s: %(message)s",
				},
			},
			"handlers": {
				"console": {
					"class": "logging.StreamHandler",
					"formatter": "default",
					"stream": "ext://sys.stderr",
				},
				"syslog": {
					"class": "logging.handlers.SysLogHandler",
					"formatter": "default",
					"address": "/dev/log",
				},
			},
			"root": {
				"level": "DEBUG" if debug else "INFO",
				"handlers": ["console", "syslog"],
			},
		}
	)
