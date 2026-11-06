import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import base64, json
def f4(rows):
    rows=[r.replace('.','0') for r in rows]; w=len(rows[0]); h=len(rows)
    out=bytearray([0x87,4,w&255,w>>8,h&255,h>>8,0,0])
    for c in range(w):
        for r in range(0,h,2):
            lo=int(rows[r][c],16); hi=int(rows[r+1][c],16) if r+1<h else 0
            out.append(lo|(hi<<4))
    return base64.b64encode(bytes(out)).decode()
T={}
T['sol']=[
"7777777777777777",
"7767777677776777",
"6666666666666666",
"eeeeeeeeeeeeeeee",
"eeeeeceeeeeeeeee",
"eeeeeeeeeeeceeee",
"eeceeeeeeeeeeeee",
"eeeeeeeeceeeeeee",
"eeeeeeeeeeeeeece",
"eeeeceeeeeeeeeee",
"eeeeeeeeeeeceeee",
"eceeeeeeeeeeeeee",
"eeeeeeeceeeeeeee",
"eeeeeeeeeeeeceee",
"eeeceeeeeeeeeeee",
"eeeeeeeeeeeeeeee"]
T['terre']=[
"eeeeeeeeeeeeeeee",
"eeeeceeeeeeeeeee",
"eeeeeeeeeeeceeee",
"eceeeeeeeeeeeeee",
"eeeeeeeeceeeeeee",
"eeeeeeeeeeeeeece",
"eeeceeeeeeeeeeee",
"eeeeeeeeeeeceeee",
"eeeeeeeeeeeeeeee",
"eeeeeeceeeeeeeee",
"eceeeeeeeeeeceee",
"eeeeeeeeeeeeeeee",
"eeeeeeeeceeeeeee",
"eeeceeeeeeeeeeee",
"eeeeeeeeeeeeeece",
"eeeeeeeeeeeeeeee"]
T['brique']=[
"cccccccccccccccc",
"bbbbbbbcbbbbbbbc",
"bbbbbbbcbbbbbbbc",
"bbbbbbbcbbbbbbbc",
"cccccccccccccccc",
"bbbcbbbbbbbcbbbb",
"bbbcbbbbbbbcbbbb",
"bbbcbbbbbbbcbbbb",
"cccccccccccccccc",
"bbbbbbbcbbbbbbbc",
"bbbbbbbcbbbbbbbc",
"bbbbbbbcbbbbbbbc",
"cccccccccccccccc",
"bbbcbbbbbbbcbbbb",
"bbbcbbbbbbbcbbbb",
"cccccccccccccccc"]
T['piece']=[
"................",
"................",
"................",
"......4444......",
".....455554.....",
"....45511554....",
"....45155554....",
"....45155554....",
"....45155554....",
"....45155554....",
"....45555554....",
".....455554.....",
"......4444......",
"................",
"................",
"................"]
T['lave']=[
"................",
"................",
"................",
"................",
"................",
"..4......4......",
".424....424.....",
"42224..4222444..",
"2222244222222244",
"2222222222222222",
"2224222222242222",
"2222222422222222",
"2222222222222222",
"2422222222224222",
"2222222222222222",
"2222222222222222"]
T['drapeau']=[
"...f............",
"...f222222......",
"...f2222222.....",
"...f22222222....",
"...f2222222.....",
"...f222222......",
"...f............",
"...f............",
"...f............",
"...f............",
"...f............",
"...f............",
"...f............",
"...f............",
"..fff...........",
".fffff.........."]
empty=["0"*16]*16
jres={"transparency16":{"data":f4(empty),"mimeType":"image/x-mkcd-f4","tilemapTile":True}}
for k,v in T.items(): jres[k]={"data":f4(v),"mimeType":"image/x-mkcd-f4","tilemapTile":True,"displayName":k}
# niveau : . vide, S sol, B brique, P piece, L lave, D drapeau
import sys
N=[
"B.......................................",
"B.......................................",
"B..................P.P..................",
"B.........PPP.....BBBBB.......P.P....D..",
"B.......BBBBB..........P....BBBBB....S..",
"B...P...............BBB..............S..",
"SSSSSSSSS...SSSSSSLLLLLLSSSS..SSSLLLLSSS",
"TTTTTTTTTLLLTTTTTTTTTTTTTTTTLLTTTTTTTTTT"]
TOUS_MURS = "--tous-murs" in sys.argv
def mur(r, c):
    ch = N[r][c]
    if ch in "ST": return True
    if ch == "B": return c == 0 or TOUS_MURS
    return False
w=len(N[0]); h=len(N); assert all(len(r)==w for r in N) and w%2==0
code={'.':0,'S':1,'B':2,'P':3,'L':4,'D':5,'T':6}
tileset=["myTiles.transparency16","myTiles.sol","myTiles.brique","myTiles.piece","myTiles.lave","myTiles.drapeau","myTiles.terre"]
s="10%02x%02x%02x%02x"%(w&255,w>>8,h&255,h>>8)
s+=''.join("%02x"%code[ch] for r in N for ch in r)
for ri,r in enumerate(N):
    row=''.join('2' if mur(ri,ci) else '0' for ci,ch in enumerate(r))
    s+=''.join(row[i+1]+row[i] for i in range(0,w,2))
jres["niveau1"]={"id":"niveau1","mimeType":"application/mkcd-tilemap","data":base64.b64encode(s.encode()).decode(),"tileset":tileset,"displayName":"niveau1"}
jres["*"]={"mimeType":"image/x-mkcd-f4","dataEncoding":"base64","namespace":"myTiles"}
open('niveau-murs.jres' if TOUS_MURS else 'niveau.jres','w').write(json.dumps(jres,indent=4))
print("ok",w,h)
# tilemap.g.ts
tl="%02x%02x%02x%02x"%(w&255,w>>8,h&255,h>>8)+''.join("%02x"%code[ch] for r in N for ch in r)
walls='\n'.join(' '.join('2' if mur(ri,ci) else '.' for ci,ch in enumerate(r)) for ri,r in enumerate(N))
names=["transparency16"]+list(T)
ts="// Auto-generated code. Do not edit.\nnamespace myTiles {\n"
for n in names: ts+="    //% fixedInstance jres blockIdentity=images._tile\n    export const "+n+" = image.ofBuffer(hex``);\n"
ts+='''
    helpers._registerFactory("tilemap", function(name: string) {
        switch(helpers.stringTrim(name)) {
            case "niveau1":return tiles.createTilemap(hex`%s`, img`
%s
`, [%s], TileScale.Sixteen);
        }
        return null;
    })

    helpers._registerFactory("tile", function(name: string) {
        switch(helpers.stringTrim(name)) {
%s
        }
        return null;
    })

}
// Auto-generated code. Do not edit.
'''%(tl,walls,','.join(tileset),'\n'.join('            case "%s":return %s;'%(n,n) for n in names))
open('tilemap-murs.g.ts.txt' if TOUS_MURS else 'tilemap.g.ts.txt','w').write(ts)
