#!/usr/bin/env python3
import csv,sys
from pathlib import Path
file=Path(sys.argv[1] if len(sys.argv)>1 else 'results/jacoco-final.csv')
with file.open(newline='',encoding='utf-8') as f:
  rows=[r for r in csv.DictReader(f) if r['CLASS']=='DataFlowTargets']
assert len(rows)==1, f'Expected one DataFlowTargets row, got {len(rows)}'
r=rows[0]
for metric in ('LINE','BRANCH','INSTRUCTION'):
  n=int(r[metric+'_COVERED']); missed=int(r[metric+'_MISSED'])
  print(f'{metric}: {n}/{n+missed} = {100*n/(n+missed):.2f}% (MISSED={missed})')
if len(sys.argv)>2 and sys.argv[2]=='final':
  assert int(r['BRANCH_MISSED'])==0, 'Final BRANCH_MISSED must be 0'
  assert int(r['BRANCH_COVERED'])==16, 'Expected 16 covered branch outcomes'
  assert int(r['LINE_MISSED'])==1, 'Teacher allows exactly 1 missed line (implicit constructor)'
  print('PASS: final branch=16/16, line missed=1 (implicit constructor)')
