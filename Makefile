MAIN_PACKAGE_NAME=tag_space_tools

UIC=pyuic5
UI_DIR=lib/$(MAIN_PACKAGE_NAME)/ui
UI_FILES=$(wildcard $(UI_DIR)/*.ui)
COMPILED_UI_FILES=$(UI_FILES:$(UI_DIR)/%.ui=$(UI_DIR)/%_ui.py)

PYTHON=python3.9
ENV_NAME=tag_space_move_env
PYTHON_ENV=./$(ENV_NAME)/bin/python
####################################

.PHONY: all ui clean_env install_in_env setup_env

setup_env:
	$(PYTHON) -m venv $(ENV_NAME)

install_in_env:
	$(PYTHON_ENV) -m pip install --upgrade pip
	$(PYTHON_ENV) -m pip install -e .

clean_env:
	rm -r $(ENV_NAME)

all: ui
	@echo "Make all finished"

ui: $(COMPILED_UI_FILES)

$(UI_DIR)/%_ui.py : $(UI_DIR)/%.ui
	$(UIC) $< --from-imports -o $@
