# MazeSolver-OpenCV
A Python based Maze Solver Program That Extract Maze-Data From Image and Finds the Shortest Path Between 2 Desired Points.

Used Breadth First Search Algorithm (Flood-Fill)


### Installing Dependencies
```
python -m pip install opencv-python numpy
```


### Run 
```
python run.py
```


### Input File Structure  (run.py)
``` python
imgFile = cv2.imread("inputImage.png")
starting_point = (154,8)   # Source Cordinates
ending_point = (169,312)   # Destination Cordinates
```


### Sample Output

![alt text](https://github.com/SuyashMore/MazeSolver-OpenCV/blob/master/demo.png )


