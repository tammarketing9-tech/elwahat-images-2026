import re
tpl=open('src/reel.tpl.html',encoding='utf-8').read()
icon=open('assets/logo-icon.svg',encoding='utf-8').read()
crown=re.search(r'<path id="crown"[^>]*\sd="([^"]+)"',icon).group(1)
full=open('assets/logo-full.svg',encoding='utf-8').read()
full=re.sub(r'<\?xml[^>]*\?>\s*','',full)
full=re.sub(r'width="1204\.60" height="656\.17"','width="820" height="446.7"',full)
full=full.replace('<path id="tagline"','<path id="taglinePath"')
out=tpl.replace('{{CROWN_D}}',crown).replace('{{LOGO_FULL}}',full)
assert '{{' not in out
open('src/reel.html','w',encoding='utf-8').write(out)
print('built', len(out))
