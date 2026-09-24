PY = PYTHONPATH=build python3
test:
	$(PY) -m unittest discover -s tests -v
build:
	$(PY) -m agk.build
scan:
	$(PY) -m agk.scan
.PHONY: test build scan
