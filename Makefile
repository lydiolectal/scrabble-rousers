default:
	python3 -m unittest tests/board_test.py
	python3 -m unittest tests/trie_test.py
	python3 -m unittest tests/bag_test.py
	python3 -m unittest tests/ai_test.py
	python3 -m unittest tests/start_seq_test.py

.PHONY: default
