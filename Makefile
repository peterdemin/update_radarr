.PHONY: build clean

build: clean
	python setup.py sdist
	pex -o update-radarr -c update-radarr dist/update_radarr-*.tar.gz

clean:
	rm -rf ~/.pex
	rm -rf dist
	rm -rf *.egg-info
