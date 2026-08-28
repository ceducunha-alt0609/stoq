from pathlib import Path
import re, json
s=Path('index.html').read_text(encoding='utf-8')
lines=s.splitlines()

def hits(pat, flags=re.I):
    rx=re.compile(pat, flags)
    return [(i+1,l.strip()) for i,l in enumerate(lines) if rx.search(l)]

def section(title, rows, limit=30):
    out=[f'\n## {title} ({len(rows)})\n']
    for n,l in rows[:limit]: out.append(f'{n}: {l[:420]}\n')
    return ''.join(out)

out=['STOQ concise audit findings\n']
checks={
'UTC_DATE_KEYS': r"toISOString\(\)\.split\(['\"]T['\"]\)\[0\]",
'LOCALSTORAGE_CLEAR': r'localStorage\.clear\s*\(',
'CACHE_DELETE_ALL': r'caches\.keys|caches\.delete',
'DEMO_SEED': r'\b(demo|sample|exemplo|seed)\b',
'DELETE_ITEM': r'\b(deleteItem|removeItem|excluir|deletar|apagar)\b',
'BACKUP_IMPORT': r'\b(backup|restore|import|export)\b',
'PRICE_COST_TOTAL': r'\b(price|pre[cç]o|custo|valor|total)\b',
'PHOTO': r'\b(photo|foto|imagem|image)\b',
'LIST_REFS': r'\b(shoppingLists|currentList|listId|itemId)\b',
}
for name,pat in checks.items(): out.append(section(name,hits(pat)))
# duplicate named funcs
names=[]
for i,l in enumerate(lines,1):
    m=re.search(r'\bfunction\s+([A-Za-z_$][\w$]*)\s*\(',l)
    if m: names.append((m.group(1),i,l.strip()))
from collections import Counter
cnt=Counter(n for n,_,_ in names)
out.append('\n## DUPLICATE_NAMED_FUNCTIONS\n')
for name,c in sorted(cnt.items()):
    if c>1:
        out.append(f'{name}: {c}\n')
        for _,ln,txt in [x for x in names if x[0]==name]: out.append(f'  {ln}: {txt[:300]}\n')
# storage keys
keys=sorted(set(re.findall(r"localStorage\.(?:getItem|setItem|removeItem)\(\s*['\"]([^'\"]+)['\"]",s)))
out.append('\n## STORAGE_KEYS\n'+'\n'.join(keys)+'\n')
# basic structural counts
out.append('\n## COUNTS\n')
for label,pat in [('DOMContentLoaded',r'DOMContentLoaded'),('addEventListener',r'addEventListener\s*\('),('innerHTML',r'\.innerHTML\s*='),('setInterval',r'setInterval\s*\('),('setTimeout',r'setTimeout\s*\(')]:
    out.append(f'{label}: {len(re.findall(pat,s))}\n')
Path('stoq_findings.txt').write_text(''.join(out),encoding='utf-8')
