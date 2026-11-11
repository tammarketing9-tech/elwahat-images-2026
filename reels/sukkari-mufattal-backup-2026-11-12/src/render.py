import sys, time, subprocess, os
from playwright.sync_api import sync_playwright
FPS=30
SCENES={1:(0,90),2:(90,240),3:(240,390),4:(390,600),5:(600,750),6:(750,900)}
ids=[int(x) for x in sys.argv[1].split(',')]
port=sys.argv[2]
outdir=sys.argv[3] if len(sys.argv)>3 else '/home/claude/reel/out'
limit=int(sys.argv[4]) if len(sys.argv)>4 else None   # frames per scene (tests only)
VF='scale=in_range=full:in_color_matrix=bt601:out_range=tv:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int,format=yuv420p'
ENC=['-c:v','libx264','-preset','medium','-crf','17','-profile:v','high','-pix_fmt','yuv420p','-g','30','-bf','2',
     '-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-r',str(FPS)]
os.makedirs(outdir,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--force-device-scale-factor=1','--hide-scrollbars','--disable-lcd-text','--font-render-hinting=none'])
    pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto(f'http://127.0.0.1:{port}/src/reel.html')
    pg.wait_for_function('window.READY===true',timeout=60000)
    for sid in ids:
        a,z=SCENES[sid]
        if limit: z=min(z,a+limit)
        tmp=f'{outdir}/tmp_sc{sid}.mp4'; fin=f'{outdir}/sc{sid}.mp4'
        ff=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-','-vf',VF]+ENC+[tmp],stdin=subprocess.PIPE)
        t0=time.time()
        for i in range(a,z):
            pg.evaluate(f'renderAt({i}/{FPS})')
            ff.stdin.write(pg.screenshot(type='jpeg',quality=92))
        ff.stdin.close(); rc=ff.wait()
        if rc==0:
            os.replace(tmp,fin); print(f'scene {sid}: {z-a} frames in {time.time()-t0:.1f}s -> {fin}',flush=True)
        else:
            print(f'scene {sid}: ffmpeg failed rc={rc}',flush=True); sys.exit(1)
    b.close()
print('WORKER DONE',ids,flush=True)
