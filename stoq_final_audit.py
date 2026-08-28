from pathlib import Path
import re
s=Path('index.html').read_text(encoding='utf-8')
terms=['report','relat','valor','price','preco','custo','total','conf','photo','foto','DOMContentLoaded','function render','function save','window.','addEventListener','toISOString().split','innerHTML','deleteItem','shoppingLists','currentList']
out=[]
for term in terms:
    out.append(f'\n===== {term} =====\n')
    hits=[m.start() for m in re.finditer(re.escape(term),s,re.I)]
    out.append(f'COUNT {len(hits)}\n')
    for pos in hits[:80]:
        a=max(0,pos-500); b=min(len(s),pos+1300)
        out.append(s[a:b].replace('\r','')+'\n---\n')
# duplicate named function declarations
names=re.findall(r'(?m)^\s*(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(',s)
from collections import Counter
out.append('\n===== DUPLICATE FUNCTIONS =====\n')
for n,c in sorted(Counter(names).items()):
    if c>1: out.append(f'{n}: {c}\n')
# storage keys and external APIs
out.append('\n===== STORAGE KEYS =====\n'+ '\n'.join(sorted(set(re.findall(r"(?:localStorage\.(?:getItem|setItem|removeItem)\(['\"]([^'\"]+)",s))))+'\n')
Path('stoq_final_audit_report.txt').write_text(''.join(out),encoding='utf-8')
