import sys, time, subprocess, os
from playwright.sync_api import sync_playwright
times=[float(x) for x in sys.argv[2].split(',')]
tag=sys.argv[1]
guides = len(sys.argv)>3 and sys.argv[3]=='g'
srv=subprocess.Popen(['python3','-m','http.server','8765','--bind','127.0.0.1'],cwd='/home/claude/reel',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(0.8)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--force-device-scale-factor=1','--hide-scrollbars','--disable-lcd-text','--font-render-hinting=none'])
    pg=b.new_page(viewport={'width':1080,'height':1920})
    msgs=[]
    pg.on('console',lambda m: msgs.append(m.text)); pg.on('response',lambda r: msgs.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None); pg.on('pageerror',lambda e: msgs.append('ERR '+str(e)))
    pg.goto('http://127.0.0.1:8765/src/reel.html'+('?guides' if guides else ''))
    pg.wait_for_function('window.READY===true',timeout=60000)
    for t in times:
        t0=time.time(); pg.evaluate(f'renderAt({t})'); pg.screenshot(path=f'/home/claude/reel/frames/{tag}_{t:05.2f}.jpg',type='jpeg',quality=90)
        print(t, round(time.time()-t0,3),'s')
    print('console:',msgs[:8])
    b.close()
srv.terminate()
