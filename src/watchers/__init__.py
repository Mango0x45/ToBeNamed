from .articles import setup as article_setup
from .mintages import setup as mintage_setup

SETUP_FUNCS = (
	article_setup,
	mintage_setup,
)
