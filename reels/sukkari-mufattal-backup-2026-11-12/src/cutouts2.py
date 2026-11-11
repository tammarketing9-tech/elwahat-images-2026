import numpy as np, cv2
from PIL import Image
import sys
sys.path.insert(0,'src')
from cutouts import load_mask, poly_mask, refine, keep_big, save_rgba

A3=np.asarray(Image.open('assets/BW-SKR-MFR-3KG-2.jpg').convert('RGB'))
A1=np.asarray(Image.open('assets/BW-SKR-MFR-1KG-v2-1.jpg').convert('RGB'))
A5=np.asarray(Image.open('assets/BW-SKR-MFR-500G-1.jpg').convert('RGB'))

# 3kg carton
m=np.maximum(load_mask('cut/p3kg2_isnet-general-use.png'),load_mask('cut/p3kg2_u2net.png'))
reg=poly_mask((1932,1932),[(500,508),(1395,508),(1620,1932),(190,1932)],feather=0)
m=m*reg; m=keep_big(m,0.5,0.05); m=refine(m,1,0.9)
save_rgba(A3,m,'cut/f_p3kg.png',pad=4)
Image.fromarray((m*255).astype(np.uint8)).save('cut/m_p3kg.png')

# 1kg box (masks only first)
m=np.maximum(load_mask('cut/p1kg1_isnet-general-use.png'),load_mask('cut/p1kg1_u2net.png'))
reg=poly_mask((1932,1932),[(560,598),(1420,598),(1650,1932),(470,1932)],feather=0)
m=m*reg; m=keep_big(m,0.5,0.05); m=refine(m,1,0.9)
save_rgba(A1,m,'cut/f_p1kg_raw.png',pad=4)
Image.fromarray((m*255).astype(np.uint8)).save('cut/m_p1kg_raw.png')

# 500g bowl: crop (150,560,1700,1932)
box=(150,560,1700,1932)
m=np.maximum(load_mask('cut/bowl_isnet-general-use.png'),load_mask('cut/bowl_u2net.png'))
m=keep_big(m,0.5,0.05); m=refine(m,1,0.9)
save_rgba(A5[box[1]:box[3],box[0]:box[2]],m,'cut/f_p500_raw.png',pad=4)
