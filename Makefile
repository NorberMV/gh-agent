install-deps:
	pip install -r requirements.txt

run:
	python mcp_client.py

run.articles:
	python mcp_client.py articles "Research recent articles about Arkady Volozh"

run.podcast:
	python mcp_client.py podcast "Search for podcast episodes about Arkady Volozh"