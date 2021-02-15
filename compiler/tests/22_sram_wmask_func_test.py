#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import unittest
from testutils import *
import sys, os
sys.path.append(os.getenv("OPENRAM_HOME"))
import globals
from globals import OPTS
from sram_factory import factory
import debug


#@unittest.skip("SKIPPING sram_wmask_func_test")
class sram_wmask_func_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)
        OPTS.analytical_delay = False
        OPTS.netlist_only = True
        OPTS.trim_netlist = False

        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        import characterizer
        reload(characterizer)
        from characterizer import functional
        from sram_config import sram_config
        c = sram_config(word_size=8,
                        num_words=16,
                        write_size=4,
                        num_banks=1)
        c.words_per_row=1
        c.recompute_sizes()
        debug.info(1, "Functional test for sram with "
                   "{} bit words, {} words, {} words per row, {} bit writes, {} banks".format(c.word_size,
                                                                                              c.num_words,
                                                                                              c.words_per_row,
                                                                                              c.write_size,
                                                                                              c.num_banks))
        s = factory.create(module_type="sram", sram_config=c)
        tempspice = OPTS.openram_temp + "sram.sp"
        s.sp_write(tempspice)

        f = functional(s.s, tempspice)
        (fail, error) = f.run()
        self.assertTrue(fail, error)

        globals.end_openram()

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
