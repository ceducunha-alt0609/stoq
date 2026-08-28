from pathlib import Path
p=Path('index.html'); s=p.read_text(encoding='utf-8')
old="""    ['ec2_items','ec2_movs','ec2_set','ec2_conf','ec2_lists','ec2_clist','ec2_photos'].forEach(k=>localStorage.removeItem(k));
    location.reload();"""
new="""    // Keep an explicit empty inventory marker so demo seed does not resurrect after an intentional reset.
    localStorage.setItem('ec2_items','[]');
    localStorage.setItem('ec2_movs','[]');
    ['ec2_set','ec2_conf','ec2_lists','ec2_clist','ec2_photos'].forEach(k=>localStorage.removeItem(k));
    location.reload();"""
assert old in s
s=s.replace(old,new,1)
old="function clearJBConfig(){ document.getElementById('jbKey').value=''; document.getElementById('jbBinId').value=''; jbSetStatus('off'); jbLog('Configuração removida'); }"
new="function clearJBConfig(){ document.getElementById('jbKey').value=''; document.getElementById('jbBinId').value=''; jbSetStatus('off'); jbLog('Configuração removida'); SP.set('jbKey',''); SP.set('jbBinId',''); }"
assert old in s
s=s.replace(old,new,1)
old="function clearSBConfig(){ document.getElementById('sbUrl').value=''; document.getElementById('sbKey').value=''; sbSetStatus('off'); sbLog('Configuração removida'); }"
new="function clearSBConfig(){ document.getElementById('sbUrl').value=''; document.getElementById('sbKey').value=''; sbSetStatus('off'); sbLog('Configuração removida'); SP.set('sbUrl',''); SP.set('sbKey',''); }"
assert old in s
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
p=Path('sw.js'); w=p.read_text(encoding='utf-8')
assert 'stoq-pro-v2-4-integrity' in w
p.write_text(w.replace('stoq-pro-v2-4-integrity','stoq-pro-v2-5-reset-cleanup',1),encoding='utf-8')
