OS := $(shell uname)

.PHONY: setup install-package main main_no_proxy distclean load_config_rooted_phone load_config_jailed_phone load_config_2461 config_enable_trainer config_disable_trainer

ifeq ($(OS), Darwin)
install-package:
	brew install python pipx android-platform-tools jq
else
install-package:
	sudo apt install pipx adb jq
endif

setup: install-package
	pipx install poetry
	pipx run poetry install

main:
	pipx run poetry run main

main_no_proxy:
	pipx run poetry run main --no_proxy

distclean:
	-pipx run poetry env remove python
	-git clean -dfx

load_config:
	mkdir -p tmp
	jq --indent 4 '$(JQ_FILTER)' conf/config.json > tmp/config.json
	mv tmp/config.json conf/config.json

load_config_rooted_phone:
	$(MAKE) load_config JQ_FILTER='.use_su = true | .use_gadget = false'

load_config_jailed_phone:
	$(MAKE) load_config JQ_FILTER='.use_su = false | .use_gadget = true'

load_config_2461:
	$(MAKE) load_config JQ_FILTER='.use_su = false | .use_gadget = false'

config_enable_trainer:
	$(MAKE) load_config JQ_FILTER='.enable_trainer = true'

config_disable_trainer:
	$(MAKE) load_config JQ_FILTER='.enable_trainer = false'
