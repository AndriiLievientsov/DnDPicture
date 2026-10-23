import json
R='/home/claude/dndpicture/'; S='/tmp/claude-0/-home-claude/1369d8ae-6a17-50fe-b23b-c9ba09d6c8a9/scratchpad/img/all/'; O='/home/claude/mapout/'
def I(lst):
    out=[]
    for box,t,st in lst:
        it=dict(box=box,text=t,style=st)
        if 'scale' in st: it['maxw']=(box[2]-box[0])*1.05
        out.append(it)
    return out
beacon=I([([1239,85,2351,201],'Маяк Таливара','gm_title_dark'),([1557,212,2033,286],'1 клетка = 5 футов','gm_scale_dark'),
 ([773,1048,1133,1123],'2-й этаж','gm_label_dark'),([1514,1048,1864,1123],'3-й этаж','gm_label_dark'),([635,1906,953,1980],'1-й этаж','gm_label_dark'),
 ([1684,1906,2029,1980],'4-й этаж','gm_label_dark'),([1161,2065,1487,2213],'Эфирная\nигла','gm_label_dark')])
gulch=I([([840,95,2175,228],'Ущелье Думатойна','gm_title'),([1071,252,1917,351],'1 клетка = 5 футов','gm_scale')])
maus=I([([868,85,2732,222],'Склеп Угольной Смерти','gm_title'),([1366,244,2150,339],'1 клетка = 10 футов','gm_scale'),([237,1790,483,1896],'Лестница\nнаверх','gm_label')])
icing=I([([1112,85,2489,191],'Ледяная Смерть и Мерцающий','gm_title'),([1436,201,2156,297],'1 клетка = 5 футов','gm_scale'),
 ([127,805,381,900],'Трюм','gm_label'),([3219,805,3484,900],'Трюм','gm_label'),([116,1483,434,1578],'Каюты','gm_label'),([3156,1483,3484,1578],'Каюты','gm_label'),
 ([127,2086,371,2182],'Палуба','gm_label'),([3230,2086,3484,2182],'Палуба','gm_label')])
cfg=[
 dict(src=S+'en3_p36_1223.png',dst=O+'158.jpg',items=beacon),
 dict(src=S+'en3_p12_372.png',dst=O+'161.jpg',items=gulch),
 dict(src=S+'en3_p16_512.png',dst=O+'169.jpg',items=maus),
 dict(src=R+'dc/153_map_en3-p19.jpg',dst=O+'153.jpg',items=icing),
 dict(src=R+'shared/138_pmap_en3-p57.jpg',dst=O+'138.jpg',items=I([([280,1940,930,2150],'Лейлон','gm_title_dark')])),
 dict(src=R+'sdw/139_pmap_ru-p201.jpg',dst=O+'139.jpg',items=I([([2030,120,3190,255],'Бронзовое святилище','gm_title'),([2256,294,2992,376],'1 клетка = 5 футов','gm_scale')])),
 dict(src=R+'sdw/140_pmap_ru-p202.jpg',dst=O+'140.jpg',items=I([([1046,65,2338,164],'Логово Клаугайлиаматар','gm_title'),([1292,180,2076,262],'1 клетка = 10 футов','gm_scale')])),
 dict(src=R+'shared/141_pmap_en3-p61.jpg',dst=O+'141.jpg',items=I([([1406,82,3270,203],'Дредноут рыцаря смерти','gm_title'),([2050,212,2773,310],'1 клетка = 5 футов','gm_scale'),
   ([70,1995,345,2175],'Верхние\nпалубы','gm_label'),([770,1995,1060,2170],'Каюты\nпалубы','gm_label'),([1505,2010,1730,2170],'Гребная\nпалуба','gm_label'),
   ([2190,2010,2450,2190],'Палуба\nэкипажа','gm_label'),([2878,2044,3090,2110],'Трюм','gm_label')])),
 dict(src=R+'sdw/142_pmap_ru-p204.jpg',dst=O+'142.jpg',items=I([([1373,65,2207,164],'Башни Иниарва','gm_title_red'),([1553,170,2027,235],'1 клетка = 5 футов','gm_scale_dark')])),
 dict(src=R+'sdw/143_pmap_ru-p205.jpg',dst=O+'143.jpg',items=[dict(box=[82,82,1046,203],text='Мыс Лейлон',style='gm_title',align='left'),dict(box=[82,212,850,310],text='1 клетка = 10 футов',style='gm_scale',align='left',maxw=800)]),
]
json.dump(cfg,open('rest.json','w'),ensure_ascii=False)
