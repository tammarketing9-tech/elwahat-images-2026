import subprocess, json, sys, os
import numpy as np
from PIL import Image
F='/home/claude/reel/out/basateen-sukkari-mufattal-malaki-reel-30s.mp4'
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',F]))
fmt=info['format']; print('size MB',round(int(fmt['size'])/1e6,2),'duration',fmt['duration'],'bitrate kbps',int(fmt['bit_rate'])//1000)
for s in info['streams']:
    print(s['codec_type'],s.get('codec_name'),s.get('profile'),s.get('width'),s.get('height'),s.get('pix_fmt'),s.get('r_frame_rate'),'frames',s.get('nb_frames'),s.get('color_range'),s.get('color_space'),s.get('color_transfer'),s.get('color_primaries'))
print('audio streams:',sum(1 for s in info['streams'] if s['codec_type']=='audio'))
# decode everything at low res to check continuity
W,H=108,192
raw=subprocess.check_output(['ffmpeg','-v','error','-i',F,'-vf',f'scale={W}:{H}','-f','rawvideo','-pix_fmt','rgb24','-'])
n=len(raw)//(W*H*3); a=np.frombuffer(raw,np.uint8).reshape(n,H,W,3).astype(np.int16)
print('decoded frames',n)
d=np.abs(a[1:]-a[:-1]).mean(axis=(1,2,3))
print('frozen pairs (diff==0):',[int(i) for i in np.where(d==0)[0]][:40], 'count',int((d==0).sum()))
for b in (90,240,390,600,750):
    print('boundary',b,'diffs',[round(float(x),2) for x in d[b-3:b+2]])
print('max diff',round(float(d.max()),1),'at frame',int(d.argmax()))
dark=a.mean(axis=(1,2,3)); print('darkest frame mean',round(float(dark.min()),1),'at',int(dark.argmin()))
os.makedirs('/home/claude/reel/out/chk',exist_ok=True)
times=[0.5,1.6,2.9,4.0,6.6,8.3,11.8,14.6,16.6,19.0,20.8,22.6,24.95,26.2,28.0,29.9]
tiles=[]
for t in times:
    out=f'/home/claude/reel/out/chk/v_{t:05.2f}.jpg'
    subprocess.check_call(['ffmpeg','-v','error','-y','-ss',str(t),'-i',F,'-frames:v','1','-q:v','2',out])
    tiles.append(Image.open(out).resize((270,480),Image.LANCZOS))
sheet=Image.new('RGB',(270*8+6*7,480*2+6),'black')
for i,im in enumerate(tiles): sheet.paste(im,((i%8)*276,(i//8)*486))
sheet.save('/home/claude/reel/out/chk/sheet_final.jpg',quality=88)
subprocess.check_call(['ffmpeg','-v','error','-y','-ss','29.9','-i',F,'-frames:v','1','-vf','scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24','/home/claude/reel/out/chk/v_end.png'])
im=np.asarray(Image.open('/home/claude/reel/out/chk/v_end.png').convert('RGB')).astype(int)
print('CTA green sample (target 34,90,69):',tuple(im[1228,270]),' cream bg sample (target 245,241,232):',tuple(im[1750,540]))
