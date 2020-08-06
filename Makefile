# Self-Documented Makefile
.DEFAULT_GOAL := help

.PHONY: help

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


anagram_example_one: ## [Runs the anagram program using the example one file.]
	@python3 anagram_parser/anagram_parser.py data/example1.txt

anagram_example_two: ## [Runs the anagram program using the example two file.]
	@python3 anagram_parser/anagram_parser.py data/example2.txt

run_tests: ## [Runs the entire unit test suite.]
	@python3 -m unittest discover
