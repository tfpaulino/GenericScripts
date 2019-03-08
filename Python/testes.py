#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# Date: 2017.12.19
# Author: Tony Paulino
# Description: 
# Modified by: Tony Paulino
# Version: 0.1

import os
import sys
import time
import glob
import re

TEMPLATE_HTML = """<HTML>
<HEAD>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html;charset=windows-1252">
<TITLE>Merged Tables</TITLE>
</HEAD>
<BODY>
%s
</BODY>
</HTML>
"""

def extractBody(filename):
    file_handler = open(filename, 'r')
    file_content = file_handler.read() # ficheiro carregado como uma string
    file_handler.close()
    if not file_handler.closed:
        sys.exit('Error on closing file.')
    # find_body = re.search('<body>(.*)</body>', file_content.replace('\n', ''), re.IGNORECASE | re.MULTILINE)
    find_body = re.findall('<body>(.*?)</body>', file_content, re.IGNORECASE | re.DOTALL)
    # print find_body
    if find_body:
        return find_body[0]
        # return find_body.groups()[0].replace('><', '>\n<')
    else:
        return ''

def usedTables():
    usedTables_content = list()
    usedTables_handler = open('MapTable.txt', 'r')
    lines = usedTables_handler.read().split()
    # usedTables_content = usedTables_handler.read().split() # ficheiro carregado como uma string
    for line in lines:
        if line not in usedTables_content:
            print line
            usedTables_content.append(line)
    usedTables_handler.close()
    
    return usedTables_content
    
# C:\Documents and Settings\Administrator\My Documents\
        
def main():
    
    a = usedTables()

    return


if __name__ == '__main__':
    main()
