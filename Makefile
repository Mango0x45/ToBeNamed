PROJECT = TO-BE-NAMED

all:

format:
	find src -name '*.py' -exec black -l 80 {} +
	find src -name '*.py' -exec isort -l 80 {} +

trans-update:
	pybabel extract -w 80 -F babel.cfg -o src/messages.pot --no-location \
		--project='${PROJECT}' src/
	if [ -d src/translations ]; then                                  \
		pybabel update -w 80 -i src/messages.pot -d src/translations; \
	fi

trans-new:
	@if [ -z "${LOCALE}" ]; then                                     \
		echo 'Specify a locale: “make trans-new LOCALE=xx_YY”' 2>&1; \
		exit 1;                                                      \
	fi
	pybabel init -i src/messages.pot -d src/translations -w 80 -l ${LOCALE}

trans-comp:
	pybabel compile -d src/translations

serve:
	pipenv run python src/app.py -d
