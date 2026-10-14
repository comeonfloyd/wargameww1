from PIL import Image, ImageDraw, ImageFilter
import numpy as np, json, os
day=Image.open('tex/earth_day_4096.jpg').convert('RGB')
D=np.asarray(day).astype(np.float32)
bmp=Image.open('tex/earth_bump_roughness_clouds_4096.jpg').convert('RGB').split()[0].filter(ImageFilter.MedianFilter(5))
E=np.asarray(bmp).astype(np.int16)
relief=np.asarray(bmp.filter(ImageFilter.MaxFilter(7))).astype(np.int16)-np.asarray(bmp.filter(ImageFilter.MinFilter(7))).astype(np.int16)
r,g,b=D[...,0],D[...,1],D[...,2];br=(r+g+b)/3
L=Image.fromarray(br.astype(np.uint8)).filter(ImageFilter.BoxBlur(10));loc=np.asarray(L).astype(np.float32)
greenness=g-(r+b)/2
cls=np.zeros(E.shape,np.uint8)
bb=np.asarray(Image.fromarray(br.astype(np.uint8)).filter(ImageFilter.BoxBlur(2))).astype(np.float32)
gg=np.asarray(Image.fromarray(np.clip(greenness+64,0,255).astype(np.uint8)).filter(ImageFilter.BoxBlur(2))).astype(np.float32)-64
forest=((bb<loc-3)&(gg>9))|((bb<62)&(gg>11))
fm=Image.fromarray((forest*255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5));forest=np.asarray(fm)>127
cls[forest]=1
cls[(br>135)&(r>=g)&(E<70)]=4
cls[(relief>=20)&(E>=12)]=2
cls[(E>=60)&(relief>=28)]=3
mk=Image.new('L',(4096,2048),0);dr=ImageDraw.Draw(mk)
for f in json.load(open('ne/geo_regions.geojson'))['features']:
    if f['properties']['FEATURECLA'] not in('Wetlands','Delta'):continue
    gm=f['geometry'];ps=[gm['coordinates']] if gm['type']=='Polygon' else gm['coordinates']
    for p in ps: dr.polygon([((x+180)/360*4096,(90-y)/180*2048) for x,y in p[0]],fill=1)
cls[np.asarray(mk)>0]=5
Image.fromarray(cls,'L').save('terrain.png',optimize=True)
print(os.path.getsize('terrain.png'),np.bincount(cls.ravel(),minlength=6))
pal=np.array([[225,228,210],[40,120,40],[170,130,80],[90,60,40],[230,210,150],[80,160,170]],np.uint8)
W,H=4096,2048
def crop(b,out):
  x0=int((b[0]+180)/360*W);x1=int((b[2]+180)/360*W);y0=int((90-b[3])/180*H);y1=int((90-b[1])/180*H)
  a=Image.fromarray(pal[cls[y0:y1,x0:x1]]);c=day.crop((x0,y0,x1,y1))
  out_im=Image.new('RGB',((x1-x0)*2*3,(y1-y0)*3));out_im.paste(a.resize(((x1-x0)*3,(y1-y0)*3),Image.NEAREST),(0,0));out_im.paste(c.resize(((x1-x0)*3,(y1-y0)*3)),((x1-x0)*3,0));out_im.save(out)
crop([14.6,50.3,20.2,52.75],'tv_pl.png');crop([5,46,30,56],'tv_no.png');crop([4,44,16,49],'tv_alps.png')
