#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Regression tests for Bard's Way
'''

import gspread
import sys
from oauth2client.service_account import ServiceAccountCredentials \
    as SAC


def choose_worksheet(filename, branch):
    try:
        return filename.worksheet(branch)
    except Exception:
        return filename.add_worksheet(branch, 500, 100)


def auth():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    cred = SAC.from_json_keyfile_name('../.serviceAccount.json', scope)
    gc = gspread.authorize(cred)
    filename = gc.open('Regression_tests')
    return filename


def find_commit(ws, commit, coverage):
    i = 1
    while ws.cell(i, 1).value and ws.cell(i, 1).value != commit:
        i += 1
    ws.update_cell(i, 1, commit)
    ws.update_cell(i, 2, coverage)
    return i


def update_cell(ws, line, col):
    trigger = False
    nb = 0
    percentage = 0
    for lines in sys.stdin:
        if trigger is True and (lines.startswith('OK')
                                or lines.startswith('FAILED')):
            if lines.startswith('OK'):
                ws.update_cell(line, 3 + (2 * col), nb)
                ws.update_cell(line, 3 + (2 * col) + 1, '100%')
                return
            ws.update_cell(line, 3 + (2 * col), str(nb))
            fails = int(lines.split('=')[1].split(')')[0])
            ws.update_cell(line, 3 + (2 * col) + 1,
                           str(round((nb - fails) / nb * 100)) + '%')
            return
        if lines.startswith('Ran '):
            trigger = True
            nb = int(lines.split(' ')[1])


if __name__ == '__main__':
    if len(sys.argv) != 5:
        exit(1)
    filename = auth()
    worksheet = choose_worksheet(filename, sys.argv[1])
    line = find_commit(worksheet, sys.argv[2], sys.argv[3])
    update_cell(worksheet, line, int(sys.argv[4]))
