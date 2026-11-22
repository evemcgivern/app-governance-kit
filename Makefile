PY = PYTHONPATH=build python3
test:
	$(PY) -m unittest discover -s tests -v
build:
	$(PY) -m agk.build
scan:
	$(PY) -m agk.scan
journal-preview:
	$(PY) -m agk.journal --preview
.PHONY: test build scan journal-preview
