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
    usedTables_list = list()
    usedTables_handler = open('MapTable.txt', 'r')
    lines = usedTables_handler.read().split()
    # usedTables_list = usedTables_handler.read().split() # ficheiro carregado como uma string
    for line in lines:
        if line not in usedTables_list:
            # print line
            usedTables_list.append(line)
    usedTables_handler.close()
    
    return usedTables_list
        
def main(directory):
    
    print os.path.basename(directory)
    
    result_extract = ''
    tablesInUse = usedTables()
    # print directory
    
    # Search for HTML files in: C:\blah\*.html
    for f in glob.glob(os.path.join(directory, '*.html')):
        f_name = os.path.basename(f).replace('_1.html','')
        if f_name in tablesInUse:
            # print 4*' ' + f_name
            result_extract += extractBody(f)

    # Build filename path: C:\blah\merged\merged_table.html
    # merged_table_file = os.path.join(directory, 'merged', 'merged_'+os.path.basename(directory).replace(' ', '_')+'.html')
    merged_table_file = os.path.join(os.path.dirname(__file__), 'merged_results', 'merged_'+os.path.basename(directory).replace(' ', '_')+'.html')
    
    # Check the existence of path: C:\blah\merged\
    if not os.path.isdir(os.path.dirname(merged_table_file)):
        os.makedirs(os.path.dirname(merged_table_file))
    
    merged_table_handler = open(merged_table_file, 'w')
    merged_table_handler.write(TEMPLATE_HTML % result_extract)
    merged_table_handler.close()
    if not merged_table_handler.closed:
        sys.exit('Error on closing file.')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for d in sys.argv[1:]:
            if os.path.isdir(d):
                main(os.path.abspath(d))
    else:
        main(os.path.dirname(__file__))
