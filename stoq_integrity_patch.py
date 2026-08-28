from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

anchor="""function saveSettings() {
  S.settings.confFreq = parseInt(document.getElementById('confFreq').value);
  save();
}
"""
insert=anchor+"""
function buildOperationalSnapshot() {
  return {
    app:'Stoq', version:4,
    items:S.items, movs:S.movs, settings:S.settings,
    confChecked:S.confChecked,
    shoppingLists:S.shoppingLists,
    currentList:S.currentList,
    photos:S.photos||{},
    exportedAt:new Date().toISOString()
  };
}
function validateOperationalSnapshot(d) {
  return !!(d && typeof d==='object' && !Array.isArray(d) &&
    Array.isArray(d.items) && Array.isArray(d.movs) &&
    d.settings && typeof d.settings==='object' && !Array.isArray(d.settings));
}
function applyOperationalSnapshot(d) {
  if(!validateOperationalSnapshot(d)) throw new Error('Estrutura de backup inválida');
  S.items=d.items;
  S.movs=d.movs;
  S.settings={...S.settings,...d.settings};
  if(Array.isArray(d.shoppingLists)) S.shoppingLists=d.shoppingLists;
  if(Array.isArray(d.currentList)) S.currentList=d.currentList;
  if(d.photos && typeof d.photos==='object' && !Array.isArray(d.photos)) S.photos=d.photos;
  if(d.confChecked && typeof d.confChecked==='object' && !Array.isArray(d.confChecked)) S.confChecked=d.confChecked;
  save();
}
"""
assert anchor in s
s=s.replace(anchor,insert,1)

# Validate manual item values
old="""  const preco=parseFloat(document.getElementById('fPreco').value)||0;
  const obj={"""
new="""  const preco=parseFloat(document.getElementById('fPreco').value)||0;
  if(qty<0 || min<0 || preco<0 || (thresh!=='' && (isNaN(parseInt(thresh)) || parseInt(thresh)<0))){
    toast('Quantidade, mínimo, alerta e preço não podem ser negativos','err'); return;
  }
  const obj={"""
assert old in s
s=s.replace(old,new,1)

# Clean dependent live references when product is deleted; historical shopping lists remain self-contained.
old="""  S.items=S.items.filter(i=>i.id!==S.editId);
  S.movs=S.movs.filter(m=>m.itemId!==S.editId);
  save();closeModal('modalAdd');"""
new="""  const deletedId=S.editId;
  S.items=S.items.filter(i=>i.id!==deletedId);
  S.movs=S.movs.filter(m=>m.itemId!==deletedId);
  S.currentList=S.currentList.filter(i=>i.itemId!==deletedId);
  delete S.confChecked[deletedId];
  delete S.photos[deletedId];
  save();closeModal('modalAdd');"""
assert old in s
s=s.replace(old,new,1)

# GitHub complete snapshot
old="const payload={description:'Stoq Backup',public:false,files:{'stoq-data.json':{content:JSON.stringify({items:S.items,movs:S.movs,settings:S.settings},null,2)}}};"
new="const payload={description:'Stoq Backup',public:false,files:{'stoq-data.json':{content:JSON.stringify(buildOperationalSnapshot(),null,2)}}};"
assert old in s
s=s.replace(old,new,1)
old="""    const parsed=JSON.parse(file.content);
    if(parsed.items) S.items=parsed.items;
    if(parsed.movs)  S.movs=parsed.movs;
    if(parsed.settings) S.settings=parsed.settings;
    save(); renderDashboard(); updateBanners();"""
new="""    const parsed=JSON.parse(file.content);
    applyOperationalSnapshot(parsed);
    renderDashboard(); updateBanners();"""
assert old in s
s=s.replace(old,new,1)

# JSONBin complete snapshot
old="const payload={items:S.items,movs:S.movs,settings:S.settings,savedAt:Date.now()};"
new="const payload={...buildOperationalSnapshot(),savedAt:Date.now()};"
assert old in s
s=s.replace(old,new,1)
old="""    const rec=data.record;
    if(rec?.items){ S.items=rec.items; S.movs=rec.movs||S.movs; S.settings=rec.settings||S.settings; }
    save(); renderDashboard(); updateBanners();"""
new="""    const rec=data.record;
    applyOperationalSnapshot(rec);
    renderDashboard(); updateBanners();"""
assert old in s
s=s.replace(old,new,1)

# Supabase: preserve existing table schema by carrying extra state inside settings JSON.
old="const payload={id:'stoq-main',items:JSON.stringify(S.items),movs:JSON.stringify(S.movs),settings:JSON.stringify(S.settings),updated_at:new Date().toISOString()};"
new="const cloudSettings={...S.settings,__stoqBackupExtras:{confChecked:S.confChecked,shoppingLists:S.shoppingLists,currentList:S.currentList,photos:S.photos||{}}};\n  const payload={id:'stoq-main',items:JSON.stringify(S.items),movs:JSON.stringify(S.movs),settings:JSON.stringify(cloudSettings),updated_at:new Date().toISOString()};"
assert old in s
s=s.replace(old,new,1)
old="""      const r=rows[0];
      if(r.items) S.items=JSON.parse(r.items);
      if(r.movs) S.movs=JSON.parse(r.movs);
      if(r.settings) S.settings=JSON.parse(r.settings);
      save(); renderDashboard(); updateBanners();"""
new="""      const r=rows[0];
      const items=JSON.parse(r.items||'null');
      const movs=JSON.parse(r.movs||'null');
      const rawSettings=JSON.parse(r.settings||'null');
      const extras=rawSettings && rawSettings.__stoqBackupExtras ? rawSettings.__stoqBackupExtras : {};
      const settings=rawSettings && typeof rawSettings==='object' ? {...rawSettings} : rawSettings;
      if(settings && typeof settings==='object') delete settings.__stoqBackupExtras;
      applyOperationalSnapshot({items,movs,settings,...extras});
      renderDashboard(); updateBanners();"""
assert old in s
s=s.replace(old,new,1)

# Local export/import use same canonical snapshot.
old="JSON.stringify({app:'Stoq',version:3,items:S.items,movs:S.movs,settings:S.settings,confChecked:S.confChecked,shoppingLists:S.shoppingLists,currentList:S.currentList,photos:S.photos||{},exportedAt:new Date().toISOString()},null,2)"
assert old in s
s=s.replace(old,"JSON.stringify(buildOperationalSnapshot(),null,2)",1)
old="""      const d=JSON.parse(ev.target.result);
      if(!d || typeof d!=='object' || !Array.isArray(d.items) || !Array.isArray(d.movs) || !d.settings || typeof d.settings!=='object' || Array.isArray(d.settings)) throw new Error('backup');
      S.items=d.items;
      S.movs=d.movs;
      S.settings={...S.settings,...d.settings};
      if(Array.isArray(d.shoppingLists)) S.shoppingLists=d.shoppingLists;
      if(Array.isArray(d.currentList)) S.currentList=d.currentList;
      if(d.photos && typeof d.photos==='object' && !Array.isArray(d.photos)) S.photos=d.photos;
      if(d.confChecked && typeof d.confChecked==='object' && !Array.isArray(d.confChecked)) S.confChecked=d.confChecked;
      save(); renderDashboard(); updateBanners();"""
new="""      const d=JSON.parse(ev.target.result);
      applyOperationalSnapshot(d);
      renderDashboard(); updateBanners();"""
assert old in s
s=s.replace(old,new,1)

# Copy complete operational data too.
old="navigator.clipboard.writeText(JSON.stringify({items:S.items,movs:S.movs,settings:S.settings},null,2))"
assert old in s
s=s.replace(old,"navigator.clipboard.writeText(JSON.stringify(buildOperationalSnapshot(),null,2))",1)

# Fix reset: previous code removed an obsolete key and left real ec2_* data untouched.
old="""    localStorage.removeItem('estoqueCP');
    location.reload();"""
new="""    ['ec2_items','ec2_movs','ec2_set','ec2_conf','ec2_lists','ec2_clist','ec2_photos'].forEach(k=>localStorage.removeItem(k));
    location.reload();"""
assert old in s
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')

# bump app cache
p=Path('sw.js'); w=p.read_text(encoding='utf-8')
assert "stoq-pro-v2-3-audit-safety" in w
w=w.replace("stoq-pro-v2-3-audit-safety","stoq-pro-v2-4-integrity",1)
p.write_text(w,encoding='utf-8')
