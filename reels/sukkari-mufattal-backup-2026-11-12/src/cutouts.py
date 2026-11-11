import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import cv2

def load_mask(path):
    return np.asarray(Image.open(path).convert('RGBA'))[...,3].astype(np.float32)/255.0

def poly_mask(size, pts, feather=1.2, ss=4):
    w,h=size
    m=Image.new('L',(w*ss,h*ss),0)
    ImageDraw.Draw(m).polygon([(x*ss,y*ss) for x,y in pts],fill=255)
    m=m.resize((w,h),Image.LANCZOS)
    if feather: m=m.filter(ImageFilter.GaussianBlur(feather))
    return np.asarray(m).astype(np.float32)/255.0

def refine(mask, erode=1, feather=1.0):
    m=(mask*255).astype(np.uint8)
    if erode>0:
        k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*erode+1,2*erode+1)); m=cv2.erode(m,k)
    if feather>0: m=cv2.GaussianBlur(m,(0,0),feather)
    return m.astype(np.float32)/255.0

def keep_big(mask, thr=0.5, min_frac=0.01):
    b=(mask>thr).astype(np.uint8)
    n,lab,stats,_=cv2.connectedComponentsWithStats(b,8)
    keep=np.zeros_like(b)
    tot=b.sum()
    for i in range(1,n):
        if stats[i,cv2.CC_STAT_AREA]>=min_frac*tot: keep[lab==i]=1
    return mask*keep

def save_rgba(rgb, mask, out, pad=6):
    a=(np.clip(mask,0,1)*255).astype(np.uint8)
    ys,xs=np.where(a>8)
    x0,x1,y0,y1=max(xs.min()-pad,0),min(xs.max()+pad,a.shape[1]-1),max(ys.min()-pad,0),min(ys.max()+pad,a.shape[0]-1)
    im=np.dstack([rgb,a])[y0:y1+1,x0:x1+1]
    Image.fromarray(im,'RGBA').save(out)
    print(out, im.shape[1], im.shape[0], 'bbox',(x0,y0,x1,y1))
    return (x0,y0,x1,y1)

P1=np.asarray(Image.open('assets/plate1.jpg').convert('RGB'))
P2=np.asarray(Image.open('assets/plate2.jpg').convert('RGB'))

# 1) dallah from plate2 crop (840,0,1830,1250)
box=(840,0,1830,1250)
m=load_mask('cut/dallah_isnet-general-use.png'); m=keep_big(m); m=refine(m,1,0.9)
save_rgba(P2[box[1]:box[3],box[0]:box[2]], m, 'cut/f_dallah.png')

# 2) flowers from plate1 crop (1230,230,1932,1090)
box=(1230,230,1932,1090)
mu=load_mask('cut/flowers_u2net.png'); mi=load_mask('cut/flowers_isnet-general-use.png')
m=np.maximum(mu,mi); m=keep_big(m,0.5,0.02); m=refine(m,1,0.9)
save_rgba(P1[box[1]:box[3],box[0]:box[2]], m, 'cut/f_flowers.png')

# 3) cartons from plate2 by polygon
pts=[(0,0),(818,0),(826,268),(771,281),(782,601),(861,659),(864,916),(528,1051),(0,1288)]
m=poly_mask((1932,1932),pts,feather=1.0)
save_rgba(P2, m, 'cut/f_cartons.png', pad=0)
