.PHONY: bash-autocomplete update-authors

bash-autocomplete:
	make -C scripts/shell_completion/

update-authors:
	git shortlog -s -e -n | \
		sed -e "s/\t/  /" | \
		sed -e "s/^\s*//" > \
		AUTHORS

tags:
	ctags -V -R --language-force=python papis env
