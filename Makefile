VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

REQUIREMENTS = requirements.txt

DATA_DIR = datasets
TRAIN_DATA = $(DATA_DIR)/dataset_train.csv
TEST_DATA = $(DATA_DIR)/dataset_test.csv
WEIGHTS = weights.json
PREDICTION = houses.csv

all: $(VENV)

$(VENV): $(REQUIREMENTS)
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQUIREMENTS)
	@touch $(VENV)

describe: $(VENV)
	$(PYTHON) describe.py $(TRAIN_DATA)

histogram: $(VENV)
	$(PYTHON) histogram.py $(TRAIN_DATA)

scatter: $(VENV)
	$(PYTHON) scatter_plot.py $(TRAIN_DATA)

pair_plot: $(VENV)
	$(PYTHON) pair_plot.py $(TRAIN_DATA)

train: $(VENV)
	$(PYTHON) logreg_train.py $(TRAIN_DATA)

predict: $(VENV)
	$(PYTHON) logreg_predict.py $(TEST_DATA) $(WEIGHTS)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

fclean: clean
	rm -rf $(WEIGHTS) $(PREDICTION) $(VENV)

re: fclean all
	
.PHONY: all describe histogram scatter pair_plot train predict clean fclean re