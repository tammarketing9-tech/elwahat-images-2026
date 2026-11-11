import sys, json, numpy as np, cv2
from PIL import Image
def run(src,dst,gamma=0.90,sat=1.04):
    a=np.array(Image.open(src).convert('RGB')).astype(np.float32); H,W=a.shape[:2]
    hsv=cv2.cvtColor(a.astype(np.uint8),cv2.COLOR_RGB2HSV).astype(np.float32); h,s,v=hsv[...,0],hsv[...,1]/255,hsv[...,2]/255
    # protected sticker: bright low-sat regions NOT touching the image border (background touches the border)
    paper=((s<0.28)&(v>0.6)).astype(np.uint8); paper=cv2.morphologyEx(paper,cv2.MORPH_CLOSE,np.ones((15,15),np.uint8))
    n,lab,st,_=cv2.connectedComponentsWithStats(paper); prot=np.zeros((H,W),np.uint8)
    for k in range(1,n):
        x,y,w,hh,ar=st[k]
        if x>2 and y>2 and x+w<W-2 and y+hh<H-2 and ar>0.03*H*W:
            cnt,_=cv2.findContours((lab==k).astype(np.uint8),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cv2.fillPoly(prot,[cv2.convexHull(np.vstack(cnt))],1)
    prot=cv2.dilate(prot,np.ones((25,25),np.uint8))
    # dates only: red-orange, saturated
    w=(((h<16)|(h>168)).astype(np.float32))*np.clip((s-0.40)/0.15,0,1)*(1-prot)
    w=cv2.GaussianBlur(w,(0,0),2.5)[...,None]
    x=a/255; lift=np.power(x,gamma)*255
    hs=cv2.cvtColor(lift.astype(np.uint8),cv2.COLOR_RGB2HSV).astype(np.float32); hs[...,1]=np.clip(hs[...,1]*sat,0,255)
    lift=cv2.cvtColor(hs.astype(np.uint8),cv2.COLOR_HSV2RGB).astype(np.float32)
    out=a*(1-w)+lift*w; out[prot>0]=a[prot>0]; out=np.clip(out,0,255).astype(np.uint8)
    Image.fromarray(out).save(dst,quality=94,subsampling=0)
    qa={'sticker_px':int(prot.sum()),'sticker_max_change':int(np.abs(out.astype(int)-a.astype(int))[prot>0].max()) if prot.sum() else None,
        'dates_V_before':round(float(v[w[...,0]>0.5].mean()),3),'dates_V_after':round(float(cv2.cvtColor(out,cv2.COLOR_RGB2HSV)[...,2][w[...,0]>0.5].mean()/255),3)}
    Image.fromarray((prot*255).astype(np.uint8)).resize((W//4,H//4)).save(dst+'.prot.png'); print(dst,qa)
run(sys.argv[1],sys.argv[2])
