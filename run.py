import cv2
import numpy as np


def extractGraph(input):
    kernel = np.ones((3, 3), np.uint8)
    img = imgFile.copy()
    erosion = cv2.erode(img, kernel, iterations=2)

    GRAY_img = cv2.cvtColor(erosion, cv2.COLOR_BGR2GRAY)

    (thresh, BW_img) = cv2.threshold(GRAY_img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    return BW_img


def BFS(graph,start,end):
    start = start[1],start[0]
    end=end[1],end[0]

    height,width = graph.shape
    levels = (np.zeros(shape=(height, width))) - 1
    parentPointerX = np.ones(shape=(height, width)) * -1
    parentPointerY = np.ones(shape=(height, width)) * -1

    def isWall(graph, point):
        if (graph[point[0], point[1]]) < 50:
            return True
        return False

    def setParent(Target,point):
        parentPointerX[Target[0]][Target[1]] = point[0]
        parentPointerY[Target[0]][Target[1]] = point[1]

    def getParent(point):
        # print("getting Parent of " , point)
        x,y = (parentPointerX[point[0]][point[1]]),(parentPointerY[point[0]][point[1]])
        return x,y

    Frontier = []
    # Add the Starting Point in the Frontier List
    Frontier.append(start)
    levels[start[0]][start[1]] = 0
    setParent(start,(-10,-10))      #Set Start Parent to Unique Number

    TotalNodes = 0
    FOUND_DESTINATION = False
    while True:
        # Ready Up List for nextFrontier
        nextFrontier = []

#         Visit All the Nodes in Current Frontier
        for x,y in Frontier:        #Loop Through Each Node
#           Check the Neighbours
#             neighbours = [ (x+1,y),(x,y+1) , (x,y-1) , (x-1,y)]
            neighbours = [(x,y-1) , (x-1,y) , (x,y+1) , (x+1,y),(x-1,y-1),(x+1,y+1),(x-1,y+1),(x+1,y-1)]  # With Diagonal Elements

            currentLevel = levels[x][y]


            for neighbour in neighbours:                            #Check North ,SOuth ,East,West,Diagonals(if-Required)
                tx, ty = neighbour
                if(tx<5 or ty<5 or tx>(height-5) or ty>(width-5)):  #Check for Graph Constrains
                    # print("OOB")
                    pass
                else:
                    # print("Checking Node At :",neighbour)
                    TotalNodes+=1
                    if(isWall(graph,neighbour)):                        #Wall Found , Just Skip it
                        # print("WAll Encountered ,Skipping")
                        pass
                    elif(levels[tx][ty] == -1):        # Add the Point to the Next-Frontier List & Set Parent
                        # print("Found New Node")
                        levels[tx][ty] = currentLevel + 1
                        nextFrontier.append(neighbour)
                        setParent((tx,ty),(x,y))
                    elif (levels[tx][ty] > currentLevel + 1):        #Found a new Shortest Path from Current Position and Change Parent
                        # print("Found Old Node With Optimal Path ")
                        levels[tx][ty] = currentLevel + 1
                        nextFrontier.append(neighbour)
                        setParent((tx, ty), (x, y))
                    else:                                            #Found A Repeated Node,Just Skip it
                        # print("Node Already Discovered,currentLevel=",levels[tx][ty]," ,FinderLevel=",currentLevel)
                        pass

                if (x == end[0] and y == end[1]):
                    FOUND_DESTINATION = True
                    break
        del Frontier

        if (len(nextFrontier) > 0 and not FOUND_DESTINATION):
            Frontier = nextFrontier.copy()
            del nextFrontier
        else:
            del nextFrontier
            break


    print("Computation Finished")
    parent = end
    path = []
    while True:
        # print(parent)
        newParent = getParent(parent)
        x, y = (newParent)
        y = int(y)
        x = int(x)


        if (parent[0] == -10):
            print("Path Found")
            break
        elif ( (parent[0]==x and parent[1]==y)):
            print("Path Not Possible")
            break

        del parent

        parent=(x,y)
        path.append((x,y))


    print("Total Nodes Checked = ",TotalNodes)
    return path


if __name__=="__main__":
    imgFile = cv2.imread("maze2.png")
    
    starting_point = (154,8)
    ending_point = (169,312)

    backupImg = imgFile.copy()
    graph =extractGraph(imgFile)

    path = BFS(graph,starting_point,ending_point)

    for point in path:
        point = point[1],point[0]
        cv2.circle(imgFile,point,1,(128,255,255),-1)


    cv2.circle(imgFile,ending_point,3,(255,255,0),-1)
    cv2.circle(imgFile,starting_point,3,(255,0,255),-1)
    
    cv2.imshow("Path",imgFile)
    cv2.imshow("Raw-Image",backupImg)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


