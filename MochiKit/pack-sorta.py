# This script was ganked from MochiKit's scripts section (pack.py).
# It's used to generate a single-file unpacked version of MochiKit,
# useful for debugging purposes.

import re

mk = file('lib/MochiKit/MochiKit.js').read()
SUBMODULES = map(str.strip, re.search(
    r"""(?mxs)MochiKit.MochiKit.SUBMODULES\s*=\s*\[([^\]]+)""",
    mk
).group(1).replace(' ', '').replace('"', '').split(','))
SUBMODULES.append('MochiKit')
alltext = '\n'.join(
    [file('lib/MochiKit/%s.js' % m).read() for m in SUBMODULES])

outf = open('packed/MochiKit/MochiKit.js', 'w')
outf.write(alltext)
outf.close()
