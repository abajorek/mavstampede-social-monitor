.PHONY: setup pipeline find parse classify export clean gui

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

pipeline: find parse classify export

find:
	python -m src.cli find --window 21d --out data/candidates.csv

parse:
	python -m src.cli parse-exports --in_dir data/raw --out data/comments_raw.csv

classify:
	python -m src.cli classify --in data/comments_raw.csv --out data/comments_classified.csv

export:
        python -m src.cli export --in data/comments_classified.csv --out data/mavstampede_monitor.csv

gui:
        FLASK_APP=src.webapp:create_app flask run --port 5001

clean:
        rm -f data/candidates.csv data/comments_raw.csv data/comments_classified.csv data/mavstampede_monitor.csv
        rm -rf data/webapp
