VENV_DIR = venv

PYTHON = python3
ACTIVATE = . $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate:
	$(PYTHON) -m venv $(VENV_DIR) && \
	$(ACTIVATE)

# Install dependencies
install: $(VENV_DIR)/bin/activate .env
	pip install --upgrade pip setuptools wheel uv
	$(ACTIVATE) && uv pip install -r requirements.txt
	@echo '-------------------------------------------------------------'
	@echo 'run ". $(VENV_DIR)/bin/activate" to activate the virtual environment'
	@echo '-------------------------------------------------------------'

# Clean the virtual environment
clean:
	rm -rf $(VENV_DIR)

test:
	$(ACTIVATE) && python -m unittest discover -s tests -p "*_test.py"


coverage:
	$(ACTIVATE) && coverage run --source=app -m unittest discover -s tests -p "*_test.py"
	$(ACTIVATE) && coverage report -m --include="app/*" --omit="venv/*"
	$(ACTIVATE) && coverage html -d coverage_html

run:
	$(ACTIVATE) && uvicorn app.main:application --workers 10 --port 8001

.env:
	cp .env.example .env

docker-build:
	docker build -t chat_summarizer_bot .

lint:
	$(ACTIVATE) && flake8 app tests

format:
	$(ACTIVATE) && isort --profile black app tests
	$(ACTIVATE) && black app tests
	$(ACTIVATE) && autoflake --in-place --remove-all-unused-imports --recursive app tests

format-check:
	$(ACTIVATE) && isort --check-only --profile black app tests
	$(ACTIVATE) && black --check app tests
	$(ACTIVATE) && autoflake --check --remove-all-unused-imports --recursive app tests

console:
	$(ACTIVATE) &&  pip show ipython > /dev/null 2>&1 || pip install ipython
	$(ACTIVATE) && ipython