from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s

# 1) Remove the earlier dead renderAlertas declaration. A later enhanced declaration is the effective one.
pat=r"function renderAlertas\(\)\{\n.*?\n\}\n\nfunction updateThreshLabel\(type\)\{"
m=re.search(pat,s,re.S)
assert m, 'first renderAlertas block not found'
block=m.group(0)
# Guard: this must be the early implementation, not the later budget override.
assert "const tl=document.getElementById('threshList')" in block and "renderBudgetInputs" not in block
s=s[:m.start()] + "// renderAlertas is defined once below, together with the budget controls.\n\nfunction updateThreshLabel(type){" + s[m.end():]

# 2) Fix the enhanced alert renderer: no mutation/save while merely rendering, and use the real threshold setter.
old="""  const tw = document.getElementById('threshWarn');
  if(tw){ tw.value = S.settings.threshWarn||150; updateThreshLabel('warn'); }
  const cf = document.getElementById('confFreq');"""
new="""  const tw = document.getElementById('threshWarn');
  if(tw){
    tw.value = S.settings.threshWarn ?? 150;
    const twLbl = document.getElementById('threshWarnLbl');
    if(twLbl) twLbl.textContent = tw.value+'%';
  }
  const cf = document.getElementById('confFreq');"""
assert old in s, 'alert render side-effect anchor not found'
s=s.replace(old,new,1)
assert "onchange=\"setThresh('${it.id}',this.value)\"" in s, 'broken setThresh anchor not found'
s=s.replace("onchange=\"setThresh('${it.id}',this.value)\"","onchange=\"setItemThresh('${it.id}',this.value)\"",1)

# 3) Snapshot unit price on new movements so historical reports do not drift after product price edits.
oldpush="S.movs.push({id:uid(),itemId,type,qty,resp,obs,valor,ts:Date.now()});"
newpush="S.movs.push({id:uid(),itemId,type,qty,resp,obs,valor,precoSnapshot:S.items[idx].preco||0,ts:Date.now()});"
assert oldpush in s, 'movement push anchor not found'
s=s.replace(oldpush,newpush,1)

oldcalc="return s+(it&&it.preco?(it.preco*mv.qty):0);"
newcalc="const unitPrice = Number.isFinite(mv.precoSnapshot) ? mv.precoSnapshot : (it&&it.preco?it.preco:0);\n      return s+(unitPrice*mv.qty);"
assert oldcalc in s, 'month spend fallback anchor not found'
s=s.replace(oldcalc,newcalc,1)

oldbudget="const v=m.valor>0?m.valor:(it.preco||0)*m.qty;"
newbudget="const unitPrice = Number.isFinite(m.precoSnapshot) ? m.precoSnapshot : (it.preco||0);\n    const v=m.valor>0?m.valor:unitPrice*m.qty;"
assert oldbudget in s, 'budget fallback anchor not found'
s=s.replace(oldbudget,newbudget,1)

assert s != orig
# Structural guards
assert s.count('function renderAlertas(){') == 1, s.count('function renderAlertas(){')
assert "setThresh('${it.id}'" not in s
assert 'precoSnapshot:S.items[idx].preco||0' in s
p.write_text(s,encoding='utf-8')

# Bump SW cache so installed PWA receives the patch rather than retaining cached index.html.
sw=Path('sw.js')
w=sw.read_text(encoding='utf-8')
old="const CACHE_NAME = 'stoq-pro-v2-5-reset-cleanup';"
new="const CACHE_NAME = 'stoq-pro-v2-6-final-integrity';"
assert old in w, 'SW cache anchor not found'
sw.write_text(w.replace(old,new,1),encoding='utf-8')
