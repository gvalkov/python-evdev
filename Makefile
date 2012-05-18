SHELL := "/bin/bash"

.PHONY: zipdoc ghpages

zipdoc:
	[ -f evdev/_ecodes.so ] || python setup.py develop
	(cd doc/ && make html)
	(cd doc/_build/html && zip -x \*.zip -r evdev-doc.zip .)
	echo `readlink -f doc/_build/html/evdev-doc.zip`

ghpages: zipdoc
	cp doc/_build/html/evdev-doc.zip /tmp/
	git co gh-pages
	rm .git/index
	git clean -fdx
	touch .nojekyll
	unzip -x /tmp/evdev-doc.zip
	git add -A ; git commit -m 'sphinxdoc update'


#vim:set ft=make ai noet sw=8 sts=8:

