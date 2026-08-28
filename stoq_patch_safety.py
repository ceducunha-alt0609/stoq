from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
assert "if (!S.items.length) seedData();" in s
s=s.replace("if (!S.items.length) seedData();", "if (localStorage.getItem('ec2_items') === null) seedData();", 1)
old="JSON.stringify({items:S.items,movs:S.movs,settings:S.settings,exportedAt:new Date().toISOString()},null,2)"
new="JSON.stringify({app:'Stoq',version:3,items:S.items,movs:S.movs,settings:S.settings,confChecked:S.confChecked,shoppingLists:S.shoppingLists,currentList:S.currentList,photos:S.photos||{},exportedAt:new Date().toISOString()},null,2)"
assert old in s
s=s.replace(old,new,1)
old="""      const d=JSON.parse(ev.target.result);
      if(d.items) S.items=d.items;
      if(d.movs) S.movs=d.movs;
      if(d.settings) S.settings=d.settings;
      save(); renderDashboard(); updateBanners();"""
new="""      const d=JSON.parse(ev.target.result);
      if(!d || typeof d!=='object' || !Array.isArray(d.items) || !Array.isArray(d.movs) || !d.settings || typeof d.settings!=='object' || Array.isArray(d.settings)) throw new Error('backup');
      S.items=d.items;
      S.movs=d.movs;
      S.settings={...S.settings,...d.settings};
      if(Array.isArray(d.shoppingLists)) S.shoppingLists=d.shoppingLists;
      if(Array.isArray(d.currentList)) S.currentList=d.currentList;
      if(d.photos && typeof d.photos==='object' && !Array.isArray(d.photos)) S.photos=d.photos;
      if(d.confChecked && typeof d.confChecked==='object' && !Array.isArray(d.confChecked)) S.confChecked=d.confChecked;
      save(); renderDashboard(); updateBanners();"""
assert old in s
s=s.replace(old,new,1)
s=s.replace("} catch{ toast('Arquivo JSON inválido','err'); }\n  };\n  reader.readAsText(file);", "} catch{ toast('Arquivo JSON inválido ou incompleto','err'); }\n    finally { e.target.value=''; }\n  };\n  reader.readAsText(file);",1)
p.write_text(s,encoding='utf-8')

p=Path('sw.js'); s=p.read_text(encoding='utf-8')
assert "const CACHE_NAME = 'stoq-pro-v2-2-cache';" in s
assert "keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))" in s
s=s.replace("const CACHE_NAME = 'stoq-pro-v2-2-cache';", "const CACHE_PREFIX = 'stoq-';\nconst CACHE_NAME = 'stoq-pro-v2-3-audit-safety';",1)
s=s.replace("keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))", "keys.filter(key => key.startsWith(CACHE_PREFIX) && key !== CACHE_NAME).map(key => caches.delete(key))",1)
p.write_text(s,encoding='utf-8')
