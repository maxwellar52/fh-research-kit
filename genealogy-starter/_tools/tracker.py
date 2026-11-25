"""tracker.py — add or replace a row in Research_Tracker.xlsx from data_<Name>.json.
Usage: python3 tracker.py Research_Tracker.xlsx data.json"""
import sys, json, openpyxl, copy
wb = openpyxl.load_workbook(sys.argv[1]); ws = wb['Tracker']
e = json.load(open(sys.argv[2], encoding='utf-8'))['tracker_entry']
head = [c.value for c in ws[1]]
row = next((r for r in range(2, ws.max_row + 1) if ws.cell(r, 2).value == e['PID']), ws.max_row + 1)
for ci, h in enumerate(head, 1):
    c = ws.cell(row, ci, e.get(h, ''))
    if row > 2:
        c._style = copy.copy(ws.cell(2, ci)._style)
wb.save(sys.argv[1]); print('tracker row', row)
