commit-notes:
	python3 scripts/normalize_notebooks.py notes
	git add notes && git commit -m "fix"
normalize-notebooks:
	python3 scripts/normalize_notebooks.py notes