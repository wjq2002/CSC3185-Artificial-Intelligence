import cv2
import numpy as np

f = open('coordination.txt', 'w')
#定义形状检测函数
def ShapeDetection(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)  #寻找轮廓点
    for obj in contours:
        area = cv2.contourArea(obj)  #计算轮廓内区域的面积
        cv2.drawContours(imgContour, obj, -1, (255, 0, 0), 4)  #绘制轮廓线
        perimeter = cv2.arcLength(obj,True)  #计算轮廓周长
        approx = cv2.approxPolyDP(obj,0.02*perimeter,True)  #获取轮廓角点坐标
        CornerNum = len(approx)   #轮廓角点的数量
        x, y, w, h = cv2.boundingRect(approx)  #获取坐标值和宽度、高度
        f.write(str(x)+" "+str(y)+" "+str(w)+" "+str(h)+" ")
        #轮廓对象分类
        if CornerNum ==3: 
            objType ="triangle"
            f.write("triangle\n")
        elif CornerNum == 4:
            if w==h: 
                objType= "Square"
                f.write("Square\n")
            else:
                objType="Rectangle"
                f.write("Rectangle\n")
        elif CornerNum>4: 
            objType= "Circle"
            f.write("Circle\n")
        else:objType="N"

        cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,0,255),2)  #绘制边界框
        cv2.putText(imgContour,objType,(x+(w//2),y+(h//2)),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,0,0),1)  #绘制文字

path = 'Photos/shapes.png'
img = cv2.imread(path)
imgContour = img.copy()
W = img.shape[0]
H = img.shape[1]
f.write(str(W)+" "+str(H)+"\n")

imgGray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)  #转灰度图
imgBlur = cv2.GaussianBlur(imgGray,(5,5),0.5)  #高斯模糊
imgCanny = cv2.Canny(imgBlur,60,60)  #Canny算子边缘检测
ShapeDetection(imgCanny)  #形状检测

# cv2.imshow("Original img", img)
# cv2.imshow("imgGray", imgGray)
# cv2.imshow("imgBlur", imgBlur)
# cv2.imshow("imgCanny", imgCanny)
# cv2.imshow("shape Detection", imgContour)

# cv2.waitKey(0)

