#    Copyright 2007 Trond Danielsen <trond.danielsen@gmail.com>
#
#    This file is part of OpenGNSS.
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Boston, MA  02110-1301  USA

from gnuradio import gr,window
from numpy import *
from gps import ca_code

class local_code(gr.hier_block2):
    def __init__(self, svn, fs, fd):

        # aliases:
        c = lambda i, o: self.connect(i,0,o,0)
        d = lambda n, f: self.define_component( n, f)

        code = ca_code(svn=svn, fs=fs)
        fd = array( [ e**(2j*pi*fd*n/fs) for n in range(len(code))] )
        lc = conj(fft.fft(code * fd))

        gr.hier_block2.__init__(self,
            "local_code",
            gr.io_signature(0,0,0),
            gr.io_signature(1,1, len(lc)*gr.sizeof_gr_complex))

        d( "code", gr.vector_source_c(lc, True))
        d( "s2v", 
            gr.stream_to_vector(gr.sizeof_gr_complex, len(lc)))
        c( "code", "s2v" )
        c( "s2v", "self" )

