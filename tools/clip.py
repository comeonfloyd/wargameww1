import json,sys
W,E,S,N=14.6,20.2,50.3,52.75
M=0.15
def inside(p): return W-M<=p[0]<=E+M and S-M<=p[1]<=N+M
def q(p): return [round(p[0],3),round(p[1],3)]
def lines(geom):
    t=geom['type'];c=geom['coordinates']
    return [c] if t=='LineString' else c if t=='MultiLineString' else []
def cliplines(fn,keyf=None):
    out=[]
    for f in json.load(open('ne/'+fn+'.geojson'))['features']:
        if not f['geometry']: continue
        k=keyf(f['properties']) if keyf else None
        if keyf and k is None: continue
        for l in lines(f['geometry']):
            run=[]
            for i,p in enumerate(l):
                if inside(p) or (i>0 and inside(l[i-1])) or (i+1<len(l) and inside(l[i+1])):
                    pp=q(p)
                    if not run or run[-1]!=pp: run.append(pp)
                else:
                    if len(run)>1: out.append([k,run] if keyf else run)
                    run=[]
            if len(run)>1: out.append([k,run] if keyf else run)
    return out
def polys(fn):
    out=[]
    for f in json.load(open('ne/'+fn+'.geojson'))['features']:
        g=f['geometry']
        if not g: continue
        ps=[g['coordinates']] if g['type']=='Polygon' else g['coordinates']
        for p in ps:
            ring=p[0]
            if any(inside(x) for x in ring):
                out.append([q(x) for x in ring])
    return out
def rivname(p):
    return [p.get('name') or '', p.get('scalerank',9)]
rivers=cliplines('ne_10m_rivers_lake_centerlines',rivname)+cliplines('ne_10m_rivers_europe',rivname)
def roadk(p):
    t=p.get('type','')
    if p.get('continent')!='Europe': return None
    return 1 if t=='Major Highway' else 2 if t in('Secondary Highway','Road') else None
roads=cliplines('ne_10m_roads',roadk)
lakes=polys('ne_10m_lakes')+polys('ne_10m_lakes_europe')
urban=polys('ne_10m_urban_areas')
prov=cliplines('ne_10m_admin_1_states_provinces_lines',lambda p: 1 if p.get('adm0_name')=='Poland' or p.get('ADM0_NAME')=='Poland' else None)
borders=cliplines('ne_10m_admin_0_boundary_lines_land')
places=[]
for f in json.load(open('ne/ne_10m_populated_places_simple.geojson'))['features']:
    p=f['properties'];c=f['geometry']['coordinates']
    if W<=c[0]<=E and S<=c[1]<=N:
        places.append([p['name'],round(c[0],3),round(c[1],3),p.get('pop_max',0),p.get('scalerank',9)])
places.sort(key=lambda x:-x[3])
d=dict(rivers=rivers,roads=roads,lakes=lakes,urban=urban,prov=[x[1] for x in prov],borders=borders,places=places,bbox=[W,S,E,N])
s=json.dumps(d,separators=(',',':'),ensure_ascii=False)
open('geo.json','w').write(s)
print(len(s),{k:len(v) for k,v in d.items()})
for p in places: print(p)
