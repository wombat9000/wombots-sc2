help:
	$(info Targets ----------------------------------------------------------------------)
	$(info   )
	$(info test                            | run all tests)
	$(info   )
	$(info run                             | run a bot match)


test:
	pytest

run:
	./run.py