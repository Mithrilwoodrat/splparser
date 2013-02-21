#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
#from splparser.lexer import *
from splparser.startlexer import *
from splparser.exceptions import SPLSyntaxError, TerminatingSPLSyntaxError
from splparser.commandrules import *

start = 'start'

def p_pipeline_start(p):
    """start : pipeline"""
    p[0] = ParseTreeNode('ROOT')
    p[0].add_children(p[1].children)

def p_pipeline_stage(p):
    """pipeline : stage"""
    p[0] = ParseTreeNode('_PIPELINE')
    p[0].add_child(p[1])

def p_pipeline_pipe(p):
    """pipeline : pipeline PIPE stage"""
    p[0] = ParseTreeNode('_PIPELINE')
    p[0].add_children(p[1].children) 
    p[0].add_child(p[3])

def p_stage_cmdexpr(p):
    """stage : cmdexpr"""
    p[0] = ParseTreeNode('STAGE')
    p[0].add_child(p[1])

def p_stage_macro(p):
    """stage : MACRO"""
    p[0] = ParseTreeNode('STAGE')
    p[0].add_child(ParseTreeNode('MACRO', raw=p[1]))

def p_arglist(p):
    """arglist : args"""
    p[0] = p[1]

def p_args(p):
    """args : ARGS"""
    p[0] = p[1]

def p_args_fields(p):
    """args : FIELDS"""
    p[0] = p[1]

def p_arglist_arg(p):
    """arglist : arglist args"""
    p[0] = ' '.join(p[1:])

def p_arglist_macro(p):
    """arglist : arglist MACRO"""
    p[0] = ' '.join(p[1:])

def p_macro_arglist(p):
    """arglist : MACRO arglist"""
    p[0] = ' '.join(p[1:])

def p_error(p):
    raise TerminatingSPLSyntaxError("Syntax error in top-level parser input!")

logging.basicConfig(
    level = logging.DEBUG,
    filename = "splparser.log",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)

log = logging.getLogger()

def parse(data, ldebug=False, ldebuglog=log, pdebug=False, pdebuglog=log):
    #lexer = lex()
    lexer = ply.lex.lex()
    yp = ply.yacc.yacc(debug=pdebug, debuglog=pdebuglog, tabmodule="toplevel_parsetab")
    parsetree = None
    try:
        parsetree = yp.parse(data, debug=pdebuglog, lexer=lexer)
    except NotImplementedError:
        raise
    except Exception:
        raise
    return parsetree

if __name__ == "__main__":

    import sys
 
    lexer = ply.lex.lex()
    parser = ply.yacc.yacc()
                
    print parser.parse(sys.argv[1:], debug=log, lexer=lexer)
