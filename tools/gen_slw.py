import json
R='/home/claude/dndpicture/slw/'; O='/home/claude/mapout/'
TD='gm_title_dark'; SD='gm_scale_dark'; LD='gm_label_dark'; RM='gm_room'; TW='gm_title'; SW='gm_scale'
way=[([338,14,512,42],'Придорожный',TD),([362,40,488,58],'1 клетка = 5 футов',SD)]
way_rooms=[([112,236,188,268],'Общий\nзал',RM),([272,250,333,270],'Конюшня',RM),([120,396,182,416],'Кухня',RM),([226,390,282,412],'Кузница',RM),
 ([168,448,232,480],'Вниз\nв подвал',RM),([468,153,537,173],'Общая A',RM),([498,201,567,221],'Общая B',RM),([498,264,557,284],'Комната A',RM),
 ([498,325,559,345],'Комната B',RM),([486,386,550,408],'Комната C',RM),([743,403,792,424],'Погреб',RM)]
thal=[([400,22,800,72],'Дом Таливара',TD),([512,70,684,98],'1 клетка = 5 футов',SD),([252,348,382,378],'2-й этаж',LD),([498,348,628,378],'3-й этаж',LD),
 ([206,633,324,665],'1-й этаж',LD),([552,631,684,663],'4-й этаж',LD)]
def items(lst,extra=None):
    out=[]
    for box,t,st in lst:
        it=dict(box=box,text=t,style=st)
        if st in (SD,SW): it['maxw']=(box[2]-box[0])*1.05
        if st==RM: it.update(wfac=1.3,size=17)
        out.append(it)
    return out
cfg=[
 dict(src=R+'072_map_en1-p11.jpg',dst=O+'072.jpg',items=items(way+way_rooms)),
 dict(src=R+'096_pmap_en1-p53.jpg',dst=O+'096.jpg',scale=1562/849,items=items(way)),
 dict(src=R+'076_map_en1-p23.jpg',dst=O+'076.jpg',items=items(thal)),
 dict(src=R+'098_pmap_en1-p56.jpg',dst=O+'098.jpg',scale=1562/1200,items=items(thal)),
 dict(src=R+'097_pmap_en1-p55.jpg',dst=O+'097.jpg',items=items([([352,66,895,128],'Городские задворки',TW),([470,132,780,182],'1 клетка = 5 футов',SW)])),
 dict(src=R+'099_pmap_en1-p57.jpg',dst=O+'099.jpg',items=items([([552,32,1012,98],'Пропавший патруль',TW),([612,103,945,152],'1 клетка = 5 футов',SW)])),
]
json.dump(cfg,open('slw.json','w'),ensure_ascii=False)
