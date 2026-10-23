import cv2,numpy as np,math,sys
from tilt import measure
def fix(src,dst,ang=None):
    a=ang if ang is not None else measure(src)[0]
    im=cv2.imread(src); h,w=im.shape[:2]
    t=math.tan(math.radians(a))
    M=np.float32([[1,0,0],[-t,1,w/2*t]])
    out=cv2.warpAffine(im,M,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
    c=int(math.ceil(abs(w/2*t)))+1
    out=out[c:h-c]
    cv2.imwrite(dst,out,[cv2.IMWRITE_JPEG_QUALITY,93])
    return a,measure(dst)[0]
if __name__=='__main__':
    print(fix(sys.argv[1],sys.argv[2]))
