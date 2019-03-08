#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# Data: 2017.02.20
# Autor: Luís Cardoso

import os, sys

def printMessage(title='Dummy Title', message='Dummy message!', error_status=0):
    print title.title() + ':'
    print message

    if error_status > 0:
        sys.exit(error_status)

    print 80*'-'

def checkData(search_list=[], search_value=''):
    is_detected = True
    print search_value.replace('\r', '').replace('\n', ''), '...',
    try:
        search_list.index(search_value)
        print 'exists'
    except ValueError:
        is_detected = False
        print 'to be added'
    return is_detected

def procData(file_lines=[]):
    result_lines = []
    file_line_list = []
    for file_line in file_lines:
        # Limpeza de caracteres para fim de linha
        # Windows: \r\n
        # Mac: \r
        # Unix: \n
        file_line_clean = file_line.replace('\r', '').replace('\n', '')
        file_line_list = file_line_clean.split(',')
        for i in range(len(file_line_list) - 1):
            file_line_str = ','.join(file_line_list[i:i+2]) + '\r\n'
            if len(result_lines) < 1 or not checkData(result_lines, file_line_str):
                result_lines.append(file_line_str)
    return result_lines

def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    printMessage('Current Path', current_path)
    csv_file = os.path.join(current_path, 'teste.csv')
    csv_file_lines = []

    if not os.path.isfile(csv_file):
        printMessage('File IO', 'I can\'t find the required file...', 0x10)

    try:
        csv_file_handler = open(csv_file, 'r')
    except:
        e = sys.exc_info()
        printMessage('File IO', '\n'.join(e), 0x11)

    csv_file_lines = csv_file_handler.readlines()
    csv_file_handler.close()

    if not csv_file_handler.closed:
        printMessage('File IO', 'I can\'t close the file.', 0x12)

    result_file_lines = procData(csv_file_lines)
    csv_file = os.path.join(current_path, 'result.csv')

    try:
        csv_file_handler = open(csv_file, 'w')
    except:
        e = sys.exc_info()
        printMessage('File IO', '\n'.join(e), 0x11)

    csv_file_handler.writelines(result_file_lines)
    csv_file_handler.close()

    if not csv_file_handler.closed:
        printMessage('File IO', 'I can\'t close the file.', 0x12)

if __name__ == '__main__':
    main()
