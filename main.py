import sys
import copy
import cv2 as cv
import numpy as np
import math
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import *
from PIL import ImageTk,Image
from tkinter import ttk
import tkinter as ttk

class GraphTheory(object):
    def laTeXnodes(self, circles):
        pointLaTex = ""
        defaultColor = "black"
        defaultSize = 5
        scaledPoints = copy.deepcopy(circles)
        scalingFactor = 0
        xCoord = []
        xAverage = 0
        xMax = 0
        xMin = 0
        xDist = 0
        yCoord = []
        yAverage = 0
        yMax = 0
        yMin = 0
        yDist = 0
        for i in circles[0, :].tolist():
            xCoord.append(i[0])
            yCoord.append(i[1])
        xMax = max(xCoord)
        xMin = min(xCoord)
        yMax = max(yCoord)
        yMin = min(yCoord)
        xAverage = np.mean(xCoord)
        yAverage = np.mean(yCoord)
        scaledPoints = scaledPoints[0, :].tolist()
        for i in scaledPoints:
            i[0] -= xAverage
            i[1] -= yAverage
        xDist = xMax-xMin
        yDist = yMax-yMin
        scalingFactor = max(xDist, yDist)
        for i in scaledPoints:
            i[0] /= scalingFactor
            i[0] *= 5
            i[1] /= scalingFactor
            i[1] *= 5
            i[1] = 5 - i[1]
            i[2] = defaultSize
            pointLaTex += "\\node[circle,fill="+defaultColor+",inner sep=0pt,minimum size="+str(i[2])+"pt] at ("+str(i[0])+","+str(i[1])+") {};" + "\n"
        return [pointLaTex, scaledPoints]

    def laTeXEdges(self, noCircles, lines, circles):
        circles = circles[0].tolist()
        actualLines = []
        sumArray = []
        img = cv.imread(noCircles)
        tempPlot = cv.imread(noCircles, cv.IMREAD_COLOR)
        taiPlot = cv.imread(noCircles, cv.IMREAD_COLOR)
        cutoff = 73000
        circlePoints = []
        for i in range(len(circles)):
            for j in range(i+1,len(circles)):
                circlePoints.append([circles[i], circles[j]])
        for pair in circlePoints:
            sum = 0
            pt1 = pair[0]
            pt2 = pair[1]
            x1 = pt1[0] #let p be x1,y1 and q be x2,y2
            y1 = pt1[1]
            x2 = pt2[0]
            y2 = pt2[1]
            p = [x1,y1]
            q = [x2,y2]
            offset = 10
            for k in range(-offset, offset):
                for l in range(-offset, offset):
                    for i in range(100):
                        t= i * 0.01
                        pPrime = [x1+k,y1+l]
                        qPrime = [x2+k,y2+l]
                        d = [pi+t*(qi-pi) for (qi,pi) in zip(qPrime,pPrime)] #q-p
                        d[0] = int(d[0])
                        d[1] = int(d[1])
                        d = tuple(d)
                        #cv.circle(tempPlot, d, 10, (255, 0, 255), 3)
                        sum += img[int(d[1]),int(d[0])][0] #r
                        sum += img[int(d[1]),int(d[0])][1] #g
                        sum += img[int(d[1]),int(d[0])][2] #b
            print(sum)
            sumArray.append((sum, [x1, y1, x2, y2]))
        sumArray.sort()
        # iterate through sum array
        for i in range (8):
            #actualLines.append([x1,y1,x2,y2]) #add the line end points
            x1, y1, x2, y2 = sumArray[i][1]
            cv.line(taiPlot,(x1,y1),(x2,y2),(0,0,255),2)

        print(actualLines)
        cv.imwrite('taiPlot.jpg', taiPlot)
        cv.imwrite('tempPlot.jpg', tempPlot)
        return 'hi'


    def detectPointsAndAxes(self, picFile): #This code is modified from: https://docs.opencv.org/3.4/d4/d70/tutorial_hough_circle.html
        #what file/picture will it look at?
        if(picFile != ""):
            default_file = picFile
            print(default_file)
            filename = default_file
        # Loads an image
            src = cv.imread(filename, cv.IMREAD_COLOR) #picFile
            noCircles =  cv.imread(filename, cv.IMREAD_COLOR)

            height,width, channels = src.shape #get the height and width of the picture

        # Check if image is loaded fine
            if src is None:
                print ('Error opening image!')
                print ('Usage: hough_circle.py [image_name -- default ' + default_file + '] \n')
                return -1


            gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY) #change the color scale to grayscale


            gray = cv.medianBlur(gray, 5) #reduce noise and false positives


            rows = gray.shape[0]
            #actual function to detect circles = HoughCircles
            circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 12, #change this value to detect circles with different distances to each other
                                param1=100, param2=20,
                                minRadius=0, maxRadius=0)
                                    # change the last two parameters
                                    # (min_radius & max_radius) to detect larger circles

            #To draw the detected circles
            #circles = array of [x, y, radius] per each circle detected
            circleTol = 7
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for i in circles[0, :]:
                    center = (i[0], i[1])
                    # circle center
                    cv.circle(src, center, 1, (0, 100, 100), 3)
                    # circle outline
                    radius = i[2]
                    cv.circle(src, center, radius, (255, 0, 255), 3)
                    cv.circle(noCircles, center, radius + circleTol, (255,255,255), -1)

            cv.imwrite('noCircles.jpg', noCircles)

            gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
            edges = cv.Canny(gray,50,150,apertureSize = 3) #edge detection

            kernel_size = 5
            blur_gray = cv.GaussianBlur(gray,(kernel_size, kernel_size),0)

            low_threshold = 50
            high_threshold = 150
            edges = cv.Canny(blur_gray, low_threshold, high_threshold)

            rho = 1  # distance resolution in pixels of the Hough grid
            theta = np.pi / 180  # angular resolution in radians of the Hough grid
            threshold = 15  # minimum number of votes (intersections in Hough grid cell)
            min_line_length = 100  # minimum number of pixels making up a line
            max_line_gap = 20  # maximum gap in pixels between connectable line segments
            line_image = np.copy(src) * 0  # creating a blank to draw lines on

            # Run Hough on edge detected image
            # Output "lines" is an array containing endpoints of detected line segments
            lines = cv.HoughLines(edges,1,np.pi/180,124) #120-125
            #lines = cv.HoughLines(edges, rho, theta, threshold)#, np.array([]),
                                #min_line_length, max_line_gap)
            lines = np.ndarray.tolist(lines)
            numOfCircles = len(circles)
            mappings = dict()
            thetaMappings = dict()
            theta = []
            for i in range(len(lines)):
                if(lines[i][0][1] not in mappings):
                    mappings[lines[i][0][1]] = lines[i][0][0]
            for key in mappings:
                theta.append(key)
            theta = sorted(theta)
            filteredTheta = [theta[0]]
            sum = filteredTheta[0] + 0.05
            diff = filteredTheta[0] - 0.05
            for i in range(len(theta)):
                if(theta[i] < sum and theta[i] > diff):
                    pass
                else:
                    filteredTheta.append(theta[i])
                    sum = filteredTheta[-1] + 0.05
                    diff = filteredTheta[-1] - 0.05
            filteredLines = []

            for i in range(len(filteredTheta)):
                filteredLines.append([mappings[filteredTheta[i]],filteredTheta[i]])

            #you can also filter by rho
            '''rho = []
            for i in range(len(lines)):
                if(lines[i][0][0] not in mappings):
                    mappings[lines[i][0][0]] = lines[i][0][1]
            for key in mappings:
                rho.append(key)
            rho = sorted(rho)
            #print(rho)
            filteredRho = [rho[0]]
            sum = filteredRho[0] + 7
            diff = filteredRho[0] - 7
            print("rho", rho)
            for i in range(len(rho)):
                if(rho[i] < sum and rho[i] > diff):
                    pass
                else:
                    filteredRho.append(rho[i])
                    sum = filteredRho[-1] + 7
                    diff = filteredRho[-1] - 7
            print("filter", filteredRho)
            filteredLines = []

            for i in range(len(filteredRho)):
                filteredLines.append([filteredRho[i], mappings[filteredRho[i]]])
            print(filteredLines)'''

            for i in range(0,len(filteredLines)):
                rho = filteredLines[i][0]
                theta = filteredLines[i][1]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b)) #1000 is the length of the line drawn
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))

                cv.line(src,(x1,y1),(x2,y2),(0,0,255),2)

            cv.imwrite('linesAndPoints.jpg', src)

            #Start building the LaTeX code:
            laTexCode = "\\begin{figure}"+"\n"+"\centering" + "\n" + "\\begin{tikzpicture}"+"\n"
            #laTexCode += self.laTexAxes(laTexCode, lines, height, width, origin)[0] #add axes
            #x_axis_length = self.laTexAxes(laTexCode, lines, height, width, origin)[1] #get the length of axes: important for scaling points
            #y_axis_length = self.laTexAxes(laTexCode, lines, height, width, origin)[2]
            laTexCode += self.laTeXnodes(circles)[0] #add points
            scaledPoints = self.laTeXnodes(circles)[1]
            laTexCode += self.laTeXEdges('noCircles.jpg', lines, circles)
            #when you're all done:
            laTexCode += "\end{tikzpicture}" + "\n" +"\end{figure}" + "\n"
            #Write the code to a .tex file so the user can download it
            with open('yourLatexFile.tex', 'w') as fp:
                fp.write(laTexCode)
            cv.waitKey(0)

        return laTexCode


class ScatterPlot(object):
    #take the detected points and scale them, as well as creating LaTeX code to plot said points
    def laTexPoints(self,laTex, circles, width, height, origin, xLength, yLength):
        pointLaTex = "" #code string to be added
        defaultColor = "black" #color of points
        size = 5 #size of points
        if(xLength > 0 and yLength > 0): #first quad
            xLen = width - origin[0]
            yLen = origin[1]
            for i in range(0, len(circles[0])):
                oldX = circles[0][i][0] - origin[0]
                oldY = circles[0][i][1]
                r = circles[0][i][2] //2 #might need to scale this later, at the moment, just halve it
                newX = (xLength*(oldX))/xLen #math for scaling
                newY = yLength - (yLength*(oldY))/yLen
                pointLaTex += "\\node[circle,fill="+defaultColor+",inner sep=0pt,minimum size="+str(r)+"pt] at ("+str(newX)+","+str(newY)+") {};" + "\n"
        elif(xLength < 0 and yLength > 0): #second quad
            xLen = origin[0]
            yLen = origin[1]
            for i in range(0, len(circles[0])):
                oldX = circles[0][i][0] - origin[0]
                oldY = circles[0][i][1]
                r = circles[0][i][2] //2 #might need to scale this later, at the moment, just halve it
                newX = -(xLength*(oldX))/xLen #math for scaling
                newY = yLength - (yLength*(oldY))/yLen
                pointLaTex += "\\node[circle,fill="+defaultColor+",inner sep=0pt,minimum size="+str(r)+"pt] at ("+str(newX)+","+str(newY)+") {};" + "\n"
        elif(xLength < 0 and yLength < 0): #third quad
            xLen = origin[0]
            yLen = height - origin[1]
            print(yLen)
            for i in range(0, len(circles[0])):
                oldX = circles[0][i][0] - origin[0]
                oldY = circles[0][i][1]
                r = circles[0][i][2] //2 #might need to scale this later, at the moment, just halve it
                newX = -(xLength*(oldX))/xLen #math for scaling
                newY = (yLength*(oldY))/yLen
                pointLaTex += "\\node[circle,fill="+defaultColor+",inner sep=0pt,minimum size="+str(r)+"pt] at ("+str(newX)+","+str(newY)+") {};" + "\n"
        elif(xLength > 0 and yLength < 0): #fourth quad
            xLen = width - origin[0]
            yLen = height - origin[1]
            print(yLen)
            for i in range(0, len(circles[0])):
                oldX = circles[0][i][0] - origin[0]
                oldY = circles[0][i][1]
                r = circles[0][i][2] //2 #might need to scale this later, at the moment, just halve it
                newX = (xLength*(oldX))/xLen #math for scaling
                newY = (yLength*(oldY))/yLen
                pointLaTex += "\\node[circle,fill="+defaultColor+",inner sep=0pt,minimum size="+str(r)+"pt] at ("+str(newX)+","+str(newY)+") {};" + "\n"
        return pointLaTex

    #take the detected lines as axes and scales them, as well as creating LaTeX code to draw said axes
    def laTexAxes(self,laTex, axes, height, width, origin):
        axesLatex = "" #LaTeX code string to be added
        defaultxLength = 5 #default axes lengths
        defaultyLength = 5
        #quadrants are determined based on where the origin is in relation to the rest of the picture/graph
        if(len(axes) == 2 and origin[0] < width/2 and origin[1] > height/2): #first quad
            axesLatex += "\draw[->] (0,0) -- ("+str(defaultxLength)+",0);" + "\n" + "\draw[->] (0,0) -- (0,"+str(defaultyLength)+");" + "\n"
            #if in the first quad, defaultxLength is positive and defaultyLength is positive
        elif(len(axes) == 2 and origin[0] > width/2 and origin[1] > height/2): #second quad
            defaultxLength *= -1
            axesLatex += "\draw[->] (0,0) -- ("+str(defaultxLength)+",0);" + "\n" + "\draw[->] (0,0) -- (0,"+str(defaultyLength)+");" + "\n"
            #if in the second quad, defaultxLength is negative and defaultyLength is positive
        elif(len(axes) == 2 and origin[0] > width/2 and origin[1] < height/2): #third quad
            defaultxLength *= -1
            defaultyLength *= -1
            axesLatex += "\draw[->] (0,0) -- ("+str(defaultxLength)+",0);" + "\n" + "\draw[->] (0,0) -- (0,"+str(defaultyLength)+");" + "\n"
            #if in the third quad, defaultxLength is negative and defaultyLength is negative
        elif(len(axes) == 2 and origin[0] < width/2 and origin[1] < height/2): #fourth quad
            defaultyLength *= -1
            axesLatex += "\draw[->] (0,0) -- ("+str(defaultxLength)+",0);" + "\n" + "\draw[->] (0,0) -- (0,"+str(defaultyLength)+");" + "\n"
            #if in the third quad, defaultxLength is positive and defaultyLength is negative
        return [axesLatex, defaultxLength, defaultyLength]


    def detectPointsAndAxes(self, picFile): #This code is modified from: https://docs.opencv.org/3.4/d4/d70/tutorial_hough_circle.html
        #what file/picture will it look at?
        if(picFile != ""):
            default_file = picFile
            print(default_file)
            filename = default_file
        # Loads an image
            src = cv.imread(filename, cv.IMREAD_COLOR) #picFile

            height,width, channels = src.shape #get the height and width of the picture

        # Check if image is loaded fine
            if src is None:
                print ('Error opening image!')
                print ('Usage: hough_circle.py [image_name -- default ' + default_file + '] \n')
                return -1


            gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY) #change the color scale to grayscale


            gray = cv.medianBlur(gray, 5) #reduce noise and false positives


            rows = gray.shape[0]
            #actual function to detect circles = HoughCircles
            circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 12, #change this value to detect circles with different distances to each other
                                param1=100, param2=20,
                                minRadius=0, maxRadius=0)
                                    # change the last two parameters
                                    # (min_radius & max_radius) to detect larger circles

            #To draw the detected circlesSE
            #circles = array of [x, y, radius] per each circle detected
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for i in circles[0, :]:
                    center = (i[0], i[1])
                    # circle center
                    cv.circle(src, center, 1, (0, 100, 100), 3)
                    # circle outline
                    radius = i[2]
                    cv.circle(src, center, radius, (255, 0, 255), 3)

            #After circle/point detection is line/axes detection via HoughLines
            gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
            edges = cv.Canny(gray,50,150,apertureSize = 3) #edge detection

            #actual function to detect lines = HoughLines
            lines = cv.HoughLines(edges,1,np.pi/180, 200)

            #draw the lines, but if there are more than 2 lines, we will take the first 2 lines to satisfy the theta criteria
            if lines is not None:
                x_axis, y_axis = None, None #finding the x and y axes
                for i in range(0, len(lines)): #HoughLines returns (p, theta), polar coordinates for each line detected
                    rho = lines[i][0][0]
                    theta = lines[i][0][1]
                    if(x_axis is None and abs(theta) < np.pi/4 or abs(np.pi-theta) < np.pi/4): #a line is horizontal if the theta is less than 45 degrees
                        x_axis = lines[i]
                    if(y_axis is None and theta > np.pi/4): #a line is vertical if the theta is greater than 45 degrees
                        y_axis = lines[i]
                lines = [y_axis, x_axis] #reduce the number of lines found to 2 lines
                assert(x_axis is not None)
                assert(y_axis is not None)

                #To find the origin of the 2 lines
                pts = []
                for i in range(0, len(lines)): #first convert to cartesion coordinates
                    rho = lines[i][0][0]
                    theta = lines[i][0][1]
                    a = math.cos(theta)
                    b = math.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a))) #find 2 x and 2 y for each line
                    pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                    pts.append([pt1, pt2])
                    cv.line(src, pt1, pt2, (0,0,255), 3, cv.LINE_AA)
                x_1, y_1 = pts[0][0]
                x_2,y_2 = pts[0][1]
                x_3,y_3 = pts[1][0]
                x_4,y_4 = pts[1][1]
                #Algorithm to calculate the intersection of 2 lines:
                x_intersection = ((x_1*y_2 - y_1*x_2)*(x_3-x_4)-(x_1-x_2)*(x_3*y_4-y_3*x_4))/((x_1-x_2)*(y_3-y_4)-(y_1-y_2)*(x_3-x_4))
                y_intersection = ((x_1*y_2 - y_1*x_2)*(y_3-y_4)-(y_1-y_2)*(x_3*y_4-y_3*x_4))/((x_1-x_2)*(y_3-y_4)-(y_1-y_2)*(x_3-x_4))
                origin = (x_intersection, y_intersection) #set the origin to the intersection points of the x and y axes

            #Start building the LaTeX code:
            laTexCode = "\\begin{figure}"+"\n"+"\centering" + "\n" + "\\begin{tikzpicture}"+"\n"
            laTexCode += self.laTexAxes(laTexCode, lines, height, width, origin)[0] #add axes
            x_axis_length = self.laTexAxes(laTexCode, lines, height, width, origin)[1] #get the length of axes: important for scaling points
            y_axis_length = self.laTexAxes(laTexCode, lines, height, width, origin)[2]
            laTexCode += self.laTexPoints(laTexCode, circles, width, height, origin, x_axis_length, y_axis_length) #add points
            #when you're all done:
            laTexCode += "\end{tikzpicture}" + "\n" +"\end{figure}" + "\n"
            #Write the code to a .tex file so the user can download it
            with open('yourLatexFile.tex', 'w') as fp:
                fp.write(laTexCode)
            cv.imwrite('linesAndPoints.jpg',src)
            cv.waitKey(0)

        return laTexCode


# Basic Animation Framework from 112 website: http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

def init(data):
    try: #check if there is an image of the detected lines and points
        data.image = Image.open("linesAndPoints.jpg")
    except FileNotFoundError:
        data.image = None
        print("Please upload your file") #instruct user to upload a file if there isn't one
    else:
        data.image = Image.open("linesAndPoints.jpg")
        # to scale the picture
        data.ratio = data.image.width/data.image.height
        data.picHeight = 300
        data.picWidth = int(data.picHeight / data.ratio)
        data.image = data.image.resize((data.picHeight,data.picWidth))
        data.image = ImageTk.PhotoImage(data.image)

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def redrawAll(canvas, data):
    # draw in canvas
    canvas.create_text(data.width/2, 0, anchor = N, text = "Graphikz", fill = "black", font =
    "Arial 26")
    canvas.create_text(data.width/2, data.height/12, anchor = N, text = "Step 1: Please select the type of graph you will upload (via Pick Graph Type).",fill = "black", font =
    "Arial 12")
    canvas.create_text(data.width/2, data.height/8, anchor = N, text = "Step 2: Please upload an image of your graph below (via Upload File).",fill = "black", font =
    "Arial 12")
    canvas.create_text(data.width/2, data.height/6, anchor = N, text = "Step 3: A picture of detected points(magenta) and axes(red) will appear:",fill = "black", font =
    "Arial 12")
    if(data.image != None): #make sure there is an image
        canvas.create_image(data.width/2, data.height/1.5, anchor=S, image=data.image)
    canvas.create_text(data.width/2, data.height/1.3, anchor = N, text = "Step 4: Please download your LaTeX File (via Download)",fill = "black", font =
    "Arial 12")

####################################
# use the run function as-is
####################################

def run(width, height):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)


    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)

    #Browse Button Setup
    file_browser = Browse(data, canvas, root, initialdir=r"C:\Users",
                                filetypes=(('Portable Network Graphics','*.png'), ("JPEG", "*.jpg"),
                                                            ("All files", "*.*")))
    file_browser.pack(fill='x', expand=True)

    #Choose Graph Type button set up, dropdown set up
    #Based and modified from: https://pythonspot.com/tk-dropdown-example/ and https://stackoverflow.com/questions/45441885/python-tkinter-creating-a-dropdown-select-bar-from-a-list/45442534
    OPTIONS = [
    "Scatter Plot", "Graph Theory"
    ] #will add more options as I add more supported graphs

    variable = StringVar(root)
    variable.set("Pick a graph type...") # default value

    w = OptionMenu(root, variable, *OPTIONS)
    print ("value is:" + variable.get()) #print selected option from the dropdown menu
    w.pack()

    # on change dropdown value
    def change_dropdown(*args):
        print(variable.get())
        if(variable.get() == "Scatter Plot"):
            data.graph1 = ScatterPlot() #create a Scatter Plot Object when selected from dropdown
        elif(variable.get() == "Graph Theory"):
            data.graph1 = GraphTheory()

    # link function to change dropdown
    variable.trace('w', change_dropdown)

    #Download Button Setup
    def downloadFile():
        exportFile = fd.asksaveasfile(mode='a') #gets filename, location user wants to save it in
        with open(exportFile.name, 'w') as fp: #write to a txt file, and then to tex file at the end
            fp.write(data.laTexCode)

    tk.Button(root, text = "Download File", command = downloadFile).pack() #create a Button

    root.mainloop()  # blocks until window is closed
    print("bye!")


class Browse(tk.Frame): # based from https://codereview.stackexchange.com/questions/184589/basic-file-browse
#Plus my additions
    """ Creates a frame that contains a button when clicked lets the user to select
    a file and put its filepath into an entry.
    """

    def __init__(self, data, canvas, root, initialdir='', filetypes=()):
        super().__init__(root)
        self.filepath = tk.StringVar()
        self._initaldir = initialdir
        self._filetypes = filetypes
        self._create_widgets()
        self._display_widgets()
        self.data = data
        self.canvas = canvas
        self.root = root
        self.filepath.trace('w', self.on_file_change) # detect filepath change, callbacks

    def on_file_change(self, *args):
        print('file changed to {}'.format(self.filepath.get())) #if the file has changed (user has uploaded a different file)
        self.data.laTexCode = self.data.graph1.detectPointsAndAxes(self.filepath.get()) #Call the main function
        # load data.xyz as appropriate
        data = self.data
        try: #check if there is a file of detected lines and points
            data.image = Image.open("linesAndPoints.jpg")
        except FileNotFoundError:
            data.image = None
            print("Please upload your file")
        else:
            data.image = Image.open("linesAndPoints.jpg")
            data.ratio = data.image.width/data.image.height
            data.picHeight = 300
            data.picWidth = int(data.picHeight / data.ratio)
            data.image = data.image.resize((data.picHeight,data.picWidth))
            data.image = ImageTk.PhotoImage(data.image)
            redrawAll(self.canvas, self.data) #manually call redrawAll to update properly
            self.canvas.update()

    def _create_widgets(self): #creates the entry text box and browse button
        self._entry = tk.Entry(self, textvariable=self.filepath)
        self._button = tk.Button(self, text="Upload File", command=self.browse)

    def _display_widgets(self):
        self._entry.pack(fill='x', expand=True)
        self._button.pack(anchor='se')

    def browse(self):
        """ Browses a .png file or all files and then puts it on the entry.
        """
        self.file = fd.askopenfilename(initialdir=self._initaldir,
                                             filetypes=self._filetypes)
                                             #file is the actual file the user has selected
        self.filepath.set(self.file) #puts the selected file in the entry textbox

    def getFilePath(self):
        return self.filepath.get() #retrieves the path of the selected file

if __name__ == "__main__":
    run(550, 550)
