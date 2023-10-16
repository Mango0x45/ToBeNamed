PROJECT = TO-BE-NAMED

TRANSDIR = src/translations
TRANSPOT = src/messages.pot

all:

format:
	find src -name '*.py' -exec black -l 80 {} +
	find src -name '*.py' -exec isort -l 80 {} +

trans-update:
	pybabel extract -w 80 -F babel.cfg -o ${TRANSPOT} --no-location --project='${PROJECT}' src/
	[ -d src/translations ] && pybabel update -w 80 -i ${TRANSPOT} -d ${TRANSDIR}

trans-new:
	@if [ -z "${LOCALE}" ]; then \
		echo 'Specify a locale: “make trans-new LOCALE=xx_YY”' 2>&1; \
		exit 1; \
	fi
	pybabel init -w 80 -i ${TRANSPOT} -d ${TRANSDIR} -l ${LOCALE}

trans-comp:
	pybabel compile -d ${TRANSDIR}

serve:
	pipenv run python src/app.py -d
