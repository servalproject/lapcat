#!/usr/bin/env python

#
#  Simple ASCII client to Serval Mesh to demonstrate some of the APIs.
#

import urllib2
import os
import sys

# UUDECODE implementation from:
# Copyright 1994 by Lance Ellinghouse
# Cathedral City, California Republic, United States of America.
#                        All Rights Reserved
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Lance Ellinghouse
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
# LANCE ELLINGHOUSE DISCLAIMS ALL WARRANTIES WITH REGARD TO
# THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS, IN NO EVENT SHALL LANCE ELLINGHOUSE CENTRUM BE LIABLE
# FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
# Modified by Jack Jansen, CWI, July 1995:
# - Use binascii module to do the actual line-by-line conversion
#   between ascii and binary. This results in a 1000-fold speedup. The C
#   version is still 5 times faster, though.
# - Arguments more compliant with python standard

"""Implementation of the UUdecode functions.

decode(in_file [, out_file, mode])
"""

import binascii

class Error(Exception):
    pass

def uudecode(in_file, out_file=None, mode=None, quiet=0):
    """Decode uuencoded file"""
    #
    # Open the input file, if needed.
    #
    opened_files = []
    if in_file == '-':
        in_file = sys.stdin
    elif isinstance(in_file, basestring):
        in_file = open(in_file)
        opened_files.append(in_file)
    try:
        #
        # Read until a begin is encountered or we've exhausted the file
        #
        while True:
            hdr = in_file.readline()
            if not hdr:
                raise Error('No valid begin line found in input file')
            if not hdr.startswith('begin'):
                continue
            hdrfields = hdr.split(' ', 2)
            if len(hdrfields) == 3 and hdrfields[0] == 'begin':
                try:
                    int(hdrfields[1], 8)
                    break
                except ValueError:
                    pass
        if out_file is None:
            out_file = hdrfields[2].rstrip()
            if os.path.exists(out_file):
                raise Error('Cannot overwrite existing file: %s' % out_file)
        if mode is None:
            mode = int(hdrfields[1], 8)
        #
        # Open the output file
        #
        if out_file == '-':
            out_file = sys.stdout
        elif isinstance(out_file, basestring):
            fp = open(out_file, 'wb')
            try:
                os.path.chmod(out_file, mode)
            except AttributeError:
                pass
            out_file = fp
            opened_files.append(out_file)
        #
        # Main decoding loop
        #
        s = in_file.readline()
        while s and s.strip() != 'end':
	    s = s.replace('\\"\\"\\"','"""')
            try:
                data = binascii.a2b_uu(s)
            except binascii.Error, v:
                # Workaround for broken uuencoders by /Fredrik Lundh
                nbytes = (((ord(s[0])-32) & 63) * 4 + 5) // 3
                data = binascii.a2b_uu(s[:nbytes])
                if not quiet:
                    sys.stderr.write("Warning: %s\n" % v)
            out_file.write(data)
            s = in_file.readline()
        if not s:
            raise Error('Truncated input file')
    finally:
        for f in opened_files:
            f.close()

###################################
	    
#  Create instance path with default config if not already existing.
#
instance_path = os.environ['HOME'] + '/.org.servalproject.lapcat'

# Create instance path
if os.path.exists(instance_path) == False:
	os.mkdir(instance_path)
if os.path.exists(instance_path + '/rhizome') == False:
	os.mkdir(instance_path+'/rhizome')
# Write default config if no config file
if os.path.exists(instance_path + '/serval.conf') == False:
	f = open(instance_path + '/serval.conf','w');
	f.write("""interfaces.1.match=+
interfaces.1.type=wifi
log.console.show_time=on
log.file.directory_path="""+instance_path+"""/log
log.file.level=fatal
rhizome.datastore_path="""+instance_path+"""/rhizome
rhizome.idle_timeout=30000
rhizome.rhizome_mdp_block_size=100
""");
	f.close();
	
if os.path.exists(instance_path + '/servald') == False:
	uudecode(sys.argv[0],instance_path+'/servald.gz',0755);
	os.system('gunzip '+instance_path+'/servald.gz');
if os.path.exists(instance_path + '/servald') == False:
	print 'Could not extract servald binary.'
	sys.exit(1);
	
downloaded_data  = urllib2.urlopen('http://www.google.com').read()
print downloaded_data

sys.exit(0);

servaldbinary="""
