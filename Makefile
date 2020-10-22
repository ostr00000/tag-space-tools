MAIN_PACKAGE_NAME=tag_space_tools

UIC=pyuic5
RCC=pyrcc5

UI_DIR=src/ui
COMPILED_UI_DIR=lib/$(MAIN_PACKAGE_NAME)/ui
RESOURCES=src/resources.qrc


PYTHON=python3.9
ENV_NAME=tag_space_move_env
PYTHON_ENV=./$(ENV_NAME)/bin/python
####################################

UI_FILES=$(wildcard $(UI_DIR)/*.ui)
COMPILED_UI_FILES=$(UI_FILES:$(UI_DIR)/%.ui=$(COMPILED_UI_DIR)/ui_%.py)
RESOURCES_SRC=$(shell grep '^ *<file' $(RESOURCES) | sed 's@</file>@@g;s@.*>@src/@g' | tr '\n' ' ')



setup_env:
	$(PYTHON) -m venv $(ENV_NAME)

install_in_env:
	$(PYTHON_ENV) -m pip install --upgrade pip
	$(PYTHON_ENV) -m pip install -e .

clean_env:
	rm -r $(ENV_NAME)

all: ui resources
	@echo "Make all finished"


ui: $(COMPILED_UI_FILES)

$(COMPILED_UI_DIR)/ui_%.py : $(UI_DIR)/%.ui
	$(UIC) $< --from-imports -o $@

resources: $(COMPILED_UI_DIR)/resources_rc.py

$(COMPILED_UI_DIR)/resources_rc.py: $(RESOURCES) $(RESOURCES_SRC)
	$(RCC) -o $(COMPILED_UI_DIR)/resources_rc.py  $<


.PHONY: all ui resources compile clean_env install_in_env setup_env
