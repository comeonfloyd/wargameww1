import json
Q=100
def enc(ring,closed=False):
    out=[];px=py=None
    for p in ring:
        x=round(p[0]*Q);y=round(p[1]*Q)
        if (x,y)==(px,py): continue
        if px is None: out+= [x,y]
        else: out+=[x-px,y-py]
        px,py=x,y
    return out if len(out)>=(6 if closed else 4) else None
def rings(fn,minpts=0):
    res=[]
    for f in json.load(open('ne/'+fn))['features']:
        g=f['geometry']
        if not g: continue
        ps=[g['coordinates']] if g['type']=='Polygon' else g['coordinates']
        for p in ps:
            e=enc(p[0],True)
            if e: res.append(e)
    return res
def lines(fn,keep=lambda p:True,tag=None):
    res=[]
    for f in json.load(open('ne/'+fn))['features']:
        g=f['geometry'];pr=f['properties']
        if not g or not keep(pr): continue
        ls=[g['coordinates']] if g['type']=='LineString' else g['coordinates']
        for l in ls:
            e=enc(l)
            if e: res.append([tag(pr),e] if tag else e)
    return res
d={}
d['land']=rings('ne_10m_land.geojson')
d['land50']=rings('ne_50m_land.geojson')
d['urban']=rings('ne_10m_urban_areas.geojson')
d['lakes']=rings('ne_10m_lakes.geojson')+rings('ne_10m_lakes_europe.geojson')
rn=lambda p:[p.get('name') or '',int(p.get('scalerank') or 9)]
d['rivers']=lines('ne_10m_rivers_lake_centerlines.geojson',tag=rn)+lines('ne_10m_rivers_europe.geojson',tag=rn)
d['borders']=lines('ne_10m_admin_0_boundary_lines_land.geojson')
d['roads']=lines('ne_10m_roads.geojson',keep=lambda p:'Ferry' not in (p.get('type') or ''),tag=lambda p:1 if p.get('type') in ('Major Highway','Beltway','Bypass') else 2)
c=json.load(open('cities.json'))
d['cities']=[[n,round(x*Q),round(y*Q),p] for n,x,y,p in c]
for k,v in d.items(): print(k,len(v),len(json.dumps(v,separators=(',',':'),ensure_ascii=False)))
s=json.dumps(d,separators=(',',':'),ensure_ascii=False)
open('world.json','w').write(s);print('total',len(s))
