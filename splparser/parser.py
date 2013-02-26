#!/usr/bin/env python

import imp
import logging
import os
import ply.yacc

class SPLParser(object):

    def __init__(self, lexermod, parsetab_name, parsetab_dir, rulesmod, optimize=False):
        self.lexer = lexermod.lex()
        self.parsetab_name = parsetab_name
        self.parsetab_dir = parsetab_dir
        self.parsetab = self.setup_parsetab()
        self.log = self.setup_log()
        self.rules = rulesmod
        self.parser = ply.yacc.yacc(module=self.rules, 
                                    debuglog=self.log, 
                                    tabmodule=self.parsetab_name, 
                                    outputdir=self.parsetab_dir,
                                    optimize=optimize)

    def setup_parsetab(self):
        
        loaded = False
        try: # check for parsetabs in current installation
            here = os.path.dirname(__file__)
            path_to_parsetab = os.path.join(here, self.parsetab_dir, self.parsetab_name + '.py')
            parsetab = imp.load_source(self.parsetab_name, path_to_parsetab)
            loaded = True
        except IOError:
            parsetab = self.parsetab_name

        if not loaded:
            try: # check for parsetabs in current directory 
                path_to_parsetab = os.path.join(self.parsetab_dir, self.parsetab_name + '.py')
                parsetab = imp.load_source(self.parsetab_name, path_to_parsetab)
            except IOError:
                parsetab = self.parsetab_name

        if not loaded:
            try: # in case the above failed, create dir for PLY to write parsetabs in
                os.stat(self.parsetab_dir)
            except:
                try:
                    os.makedirs(self.parsetab_dir)
                except OSError:
                    sys.stderr.write("ERROR: \
                                      Need permission to write to ./" + self.parsetab_dir + "\n")
                    raise

        return parsetab
    
    def setup_log(self):
        logging.basicConfig(
            level = logging.DEBUG,
            filename = "splparser.log",
            filemode = "w",
            format = "%(filename)10s:%(lineno)4d:%(message)s"
        )
        return logging.getLogger()
    
    def parse(self, data):
        parsetree = None
        try:
            parsetree = self.parser.parse(data, lexer=self.lexer)
        except NotImplementedError:
            raise
        except Exception:
            raise
        return parsetree
