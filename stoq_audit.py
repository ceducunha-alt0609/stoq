from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
terms=['localStorage','sessionStorage','indexedDB','supabase','firebase','addSample','demo','seed','backup','restore','import','export','toISOString().split','serviceWorker.register','caches.delete','location.reload','setItem(','removeItem(','clear()']
out=[]
out.append(f'index bytes={len(s.encode())} lines={s.count(chr(10))+1}')
for t in terms:
    out.append(f'{t}: {s.lower().count(t.lower())}')
# contexts for high-risk terms
for pat in ['localStorage','demo','seed','backup','restore','import','export','toISOString\\(\\)\\.split','serviceWorker\\.register']:
    out.append('\n=== '+pat+' ===')
    for m in list(re.finditer(pat,s,re.I))[:40]:
        a=max(0,m.start()-180); b=min(len(s),m.end()+260)
        out.append(s[a:b].replace('\n',' ')[:500])
Path('stoq_audit_report.txt').write_text('\n'.join(out),encoding='utf-8')
