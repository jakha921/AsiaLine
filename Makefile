# define the name of the virtual environment directory
VENV := venv

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

# venv is a shortcut target
venv: $(VENV)/bin/activate

# migrate the database with alembic
migrate:
    ./$(VENV)/bin/alembic upgrade head


run: venv
	./$(VENV)/bin/uvicorn main:app --reload

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete __pycache__

.PHONY: all venv run clean
# in db file change config_example.py to config.py and add your own config info