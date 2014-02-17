all:	lapcat

servald.bin:
	cd ../serval-dna ; autoconf && ./configure && make  && cp servald ../ascii-client/servald.bin

lapcat:	lapcat-ascii.py servald.bin Makefile
	cp servald.bin s
	strip s
	rm s.gz
	gzip -9 s
	( cat lapcat-ascii.py ; uuencode s.gz servald.gz | sed 's/"""/\\"\\"\\"/g' ; echo \"\"\" ) > lapcat
	chmod 755 lapcat
	rm s.gz

