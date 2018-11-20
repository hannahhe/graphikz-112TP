import sys
import cv2 as cv
import numpy as np
import math

#class ScatterPlot(object):
    
def laTexPoints(laTex, circles, height, width, origin): 
    pointLaTex = ""
    defaultColor = "black"
    size = 5
    #scaling section
    #actual LaTex
    # \node[circle,fill=black,inner sep=0pt,minimum size=5pt] at (1,2) {};
    xLen = width - origin[0]
    yLen = origin[1]
    for i in range(0, len(circles[0])):
        oldX = circles[0][i][0]
        oldY = circles[0][i][1] 
        r = circles[0][i][2] //2 #might need to scale this later, at the moment, just halve it
        newX = (5*(oldX))/xLen
    # print("newX",newX)
        newY = 5 - (5*(oldY))/yLen
        pointLaTex += "\\node[circle,fill="+defaultColor+",inner sep=0pt,minimum size="+str(r)+"pt] at ("+str(newX)+","+str(newY)+") {};" + "\n"
    return pointLaTex


def laTexAxes(laTex, axes, height, width, origin): #need to expand beyond just quadrants
    print(axes)
    axesLatex = ""
    defaultLength = 5
    if(len(axes) == 2 and origin[0] < width/2 and origin[1] > height/2): #first quad
        axesLatex += "\draw[->] (0,0) -- ("+str(defaultLength)+",0);" + "\n" + "\draw[->] (0,0) -- (0,"+str(defaultLength)+");" + "\n"
    elif(len(axes) == 2 and origin[0] > width/2 and origin[1] > height/2): #second quad
        print("SECOND QUAD FAM")
        axesLatex += "\draw[->] (0,0) -- (-"+str(defaultLength)+",0);" + "\n" + "\draw[->] (0,0) -- (0,"+str(defaultLength)+");" + "\n"
    elif(len(axes) == 2 and origin[0] > width/2 and origin[1] < height/2): #third quad
        axesLatex += "\draw[->] (0,0) -- (-"+str(defaultLength)+",0);" + "\n" + "\draw[->] (0,0) -- (0,-"+str(defaultLength)+");" + "\n"
    elif(len(axes) == 2 and origin[0] < width/2 and origin[1] < height/2): #fourth quad
        axesLatex += "\draw[->] (0,0) -- ("+str(defaultLength)+",0);" + "\n" + "\draw[->] (0,0) -- (0,-"+str(defaultLength)+");" + "\n"
    return axesLatex


def detectPointsAndAxes(argv):
    
    #what file/picture will it look at?
    default_file =  "C:/Users/hanna/Desktop/TPTechDemo/HoughTest1.png"
    filename = argv[0] if len(argv) > 0 else default_file
    # Loads an image
    src = cv.imread(filename, cv.IMREAD_COLOR)
    
    height,width, channels = src.shape
    
    # Check if image is loaded fine
    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_circle.py [image_name -- default ' + default_file + '] \n')
        return -1
    
    
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY) #change the color scale to grayscale
    
    
    gray = cv.medianBlur(gray, 5) #reduce noise and false positives
    
    
    rows = gray.shape[0]
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 12, #change this value to detect circles with different distances to each other
                               param1=100, param2=20,
                               minRadius=0, maxRadius=0)
                                # change the last two parameters
                                # (min_radius & max_radius) to detect larger circles
    
    #To draw the detected circlesSE
    #= x, y, radius
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv.circle(src, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv.circle(src, center, radius, (255, 0, 255), 3)

    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray,50,150,apertureSize = 3)
    
    lines = cv.HoughLines(edges,1,np.pi/180, 200)
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv.line(src, pt1, pt2, (0,0,255), 3, cv.LINE_AA)
    
    cartCoord = []
    for i in range(0, len(lines)):
        theta = lines[i][0][1]
        r = lines[i][0][0]
        x = r * np.cos(theta)
        x = round(x, 3)
        y = r * np.sin(theta)
        y = round(y, 3)
        cartCoord.append((x,y))
    origin = (cartCoord[1][0], cartCoord[0][1])
    
    laTexCode = "\\begin{figure}"+"\n"+"\centering" + "\n" + "\\begin{tikzpicture}"+"\n"
    laTexCode += laTexAxes(laTexCode, lines, height, width, origin) #add axes
    print(laTexCode)
    #laTexCode += laTexPoints(laTexCode, circles, height, width, origin) #add points
    #when you're all done:
    laTexCode += "\end{tikzpicture}" + "\n" +"\end{figure}" + "\n"
    #print(laTexCode)  
    cv.imshow('linesAndPoints.jpg',src)
    cv.waitKey(0)
    
    return 0
    
if __name__ == "__main__":
    detectPointsAndAxes(sys.argv[1:])
    