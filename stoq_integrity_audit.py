from pathlib import Path
import re
s=Path('index.html').read_text(encoding='utf-8')
need=['function syncGithubSave','async function syncGithubLoad','function syncSupabaseSave','async function syncSupabaseLoad','function confirmReset','function deleteItem','function saveMov','function swipeQuickMov','function handlePhotoUpload']
out=[]
for key in need:
    i=s.find(key)
    out.append('\n=== '+key+' ===\n')
    if i<0:
        out.append('NOT FOUND')
        continue
    j=s.find('\nfunction ', i+10)
    ja=s.find('\nasync function ', i+10)
    cand=[x for x in [j,ja] if x!=-1]
    end=min(cand) if cand else min(len(s),i+6000)
    out.append(s[i:end][:7000])
Path('stoq_integrity_report.txt').write_text('\n'.join(out),encoding='utf-8')
