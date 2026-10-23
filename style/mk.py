import sys
t=open('style_template.css').read()
def make(base,head,rng):
    HF={'alegreyasc':('ru-head-alegreyasc.woff2','Alegreya SC'),'cormorantsc':('ru-head-cormorantsc.woff2','Cormorant SC'),'spectralsc':('ru-head-spectralsc.woff2','Spectral SC')}[head]
    R={'full':'','cyr':'unicode-range: U+0400-045F, U+0490-0491, U+00AB, U+00BB, U+2116;'}[rng]
    return t.replace('{BASE}',base).replace('{HEADFILE}',HF[0]).replace('{HEADFONT}',HF[1]).replace('{RANGE}',R)
if __name__=='__main__':
    open(sys.argv[1],'w').write(make(sys.argv[2],sys.argv[3],sys.argv[4]))
