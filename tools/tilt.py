import cv2,numpy as np,glob,sys,math
def measure(path):
    im=cv2.imread(path); g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    e=cv2.Canny(g,50,150)
    h,w=g.shape
    lines=cv2.HoughLinesP(e,1,np.pi/1800,threshold=200,minLineLength=int(min(w,h)*0.35),maxLineGap=8)
    hs,vs=[],[]
    if lines is not None:
        for x1,y1,x2,y2 in lines.reshape(-1,4):
            a=math.degrees(math.atan2(y2-y1,x2-x1))
            L=math.hypot(x2-x1,y2-y1)
            if abs(a)<5: hs.append((a,L))
            elif abs(abs(a)-90)<5: vs.append(((a-90) if a>0 else (a+90),L))
    def wm(v): return (sum(a*L for a,L in v)/sum(L for a,L in v)) if v else None
    return wm(hs),wm(vs),len(hs),len(vs)
if __name__=="__main__":
  for p in sorted(glob.glob(sys.argv[1])):
    print(p.split('/')[-1],[round(x,3) if isinstance(x,float) else x for x in measure(p)])
