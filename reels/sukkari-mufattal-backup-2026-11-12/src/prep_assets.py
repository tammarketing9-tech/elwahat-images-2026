import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import shutil
W,H=1080,1920
HZ=640   # horizon (wall/table edge)

# --- hook photo crop (9:16) ---
im=Image.open('assets/BW-SKR-MFR-1KG-v2-2.jpg').convert('RGB')
im.crop((400,0,1487,1932)).save('assets/hook.jpg',quality=93)

# --- cut-outs ---
for src,dst in [('f_cartons','cartons'),('f_dallah','dallah'),('f_flowers','flowers'),('f_p3kg','p3kg'),('f_p1kg_raw','p1kg'),('f_p500_raw','p500')]:
    shutil.copy(f'cut/{src}.png',f'assets/{dst}.png')
    print(dst, Image.open(f'assets/{dst}.png').size)

# --- background: warm wall + white table ---
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
def col(h): return np.array([int(h[i:i+2],16) for i in (1,3,5)],np.float32)
wall_top,wall_bot=col('#F6F2EA'),col('#ECE6DA')
tab_top,tab_bot=col('#F4F1EA'),col('#FAF8F4')
img=np.zeros((H,W,3),np.float32)
tw=np.clip(yy/HZ,0,1)[...,None]
img[:]=wall_top*(1-tw)+wall_bot*tw
tt=np.clip((yy-HZ)/(H-HZ),0,1)[...,None]
table=tab_top*(1-tt**0.6)+tab_bot*(tt**0.6)
mask=(yy>=HZ)[...,None]
img=np.where(mask,table,img)
# soft light pool on the wall (upper right)
d=np.exp(-(((xx-720)/540)**2+((yy-260)/340)**2))[...,None]
img+=d*np.array([7,7,6],np.float32)*(~mask)
# contact shade just above/below the table edge
band=np.exp(-((yy-HZ)/9.0)**2)[...,None]
img-=band*np.array([20,21,24],np.float32)
below=np.clip(1-(yy-HZ)/160,0,1)[...,None]*(yy>=HZ)[...,None]
img-=below*np.array([6,6,7],np.float32)
# vignette
v=((xx-W/2)/(W/2))**2*0.55+((yy-H/2)/(H/2))**2*0.35
img-=np.clip(v-0.45,0,1)[...,None]*26
img=np.clip(img,0,255).astype(np.uint8)
Image.fromarray(img).save('assets/bg.jpg',quality=95)

# --- white board (frosted serving mat) with soft shadow ---
SS=3
def rounded_quad(pts, r, size):
    # pts: TL,TR,BR,BL ; round only top corners
    m=Image.new('L',(size[0]*SS,size[1]*SS),0)
    d=ImageDraw.Draw(m)
    P=[(x*SS,y*SS) for x,y in pts]
    d.polygon(P,fill=255)
    # carve top corners and re-add circles (approximation good for small radius)
    return m
TL,TR,BR,BL=(170,900),(910,900),(1052,1990),(28,1990)
def board_mask(grow=0):
    m=Image.new('L',(W*SS,(H+80)*SS),0)
    d=ImageDraw.Draw(m)
    pts=[(TL[0]-grow,TL[1]-grow),(TR[0]+grow,TR[1]-grow),(BR[0]+grow,BR[1]),(BL[0]-grow,BL[1])]
    d.polygon([(x*SS,y*SS) for x,y in pts],fill=255)
    m=m.filter(ImageFilter.GaussianBlur(14*SS)).point(lambda p:255 if p>127 else 0)  # rounds corners (~r 30)
    return m.resize((W,H+80),Image.LANCZOS).crop((0,0,W,H))
bm=np.asarray(board_mask()).astype(np.float32)/255
sh=np.asarray(board_mask(6).filter(ImageFilter.GaussianBlur(20))).astype(np.float32)/255
sh=np.roll(sh,10,axis=0)
out=np.zeros((H,W,4),np.float32)
# shadow layer
out[...,0:3]=np.array([70,58,40],np.float32); out[...,3]=sh*0.30*255*(1-bm)
# board colour: white, a touch cooler/greyer toward the far edge like frosted plastic
t=np.clip((yy-900)/(H-900),0,1)
bc=(col('#F2F1EE')[None,None,:]*(1-t[...,None])+col('#FFFFFF')[None,None,:]*t[...,None])
a=bm[...,None]
rgb=out[...,0:3]*(1-a)+bc*a
alpha=np.maximum(out[...,3],bm*255)
# thin highlight on the far (top) edge
edge=np.clip(bm-np.roll(bm,3,axis=0),0,1)
rgb=np.clip(rgb+edge[...,None]*18,0,255)
res=np.dstack([rgb,alpha]).astype(np.uint8)
Image.fromarray(res,'RGBA').save('assets/board.png')
print('bg/board ok')
