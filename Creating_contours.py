import cv2

CELL_SIZE = 20
# Cell border's thickness is 2


img = cv2.imread('Images/maze00.jpg')
h, w, c = img.shape

cv2.imshow('Original', img)

grid = []


def get_code(contours):
    WALL_AT_START_POSITION = 2 # IF below 2, no wall
    WALL_AT_END_POSITION = 17 # If above 17 , no wall

    code = {}
    for vertex in contours[0][0:4:2]: # Check ONLY first and third vertex among the 4 should be enough.
        x, y = vertex[0][0], vertex[0][1]
        if x < WALL_AT_START_POSITION: # No wall on left
            code['left'] = False
        elif x == WALL_AT_START_POSITION: # Wall on left
            code['left'] = True
        elif x == WALL_AT_END_POSITION: # Wall on right
            code['right'] = True
        elif x > WALL_AT_END_POSITION: # No wall on right
            code['right'] = False
        else:
            code['error'] = "Contour beyond start and end position of wall x"

        if y < WALL_AT_START_POSITION: # No wall on left
            code['up'] = False
        elif y == WALL_AT_START_POSITION: # Wall on left
            code['up'] = True
        elif y == WALL_AT_END_POSITION: # Wall on right
            code['down'] = True
        elif y > WALL_AT_END_POSITION: # No wall on right
            code['down'] = False
        else:
            code['error'] = "Contour beyond start and end position of wall y"

    return code



for x in range(0, h, CELL_SIZE):
    row = []
    grid.append(row)

    for y in range(0, w, CELL_SIZE):
        cell = img[x:x+CELL_SIZE, y:y+CELL_SIZE, :]

        gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        print('Number of coutours: ', len(contours))
        print(contours[0])
        
        code = get_code(contours)
        row.append(code)
        print(code)
            
        # Contour corners.
##        for a in contours[0]:
##            cv2.circle(cell, (a[0][0], a[0][1]), 2, (0,0,255), -1)
##            print(a[0][0], a[0][1])
##            cv2.imshow("tmp", cell)
##            cv2.waitKey(0)

        # Draw on same part of image from which cell was derived
        cv2.drawContours(cell, contours, 0, (0,255, 0), 1)
        cv2.putText(img, '>', (x+CELL_SIZE//2, y+CELL_SIZE//2), cv2.FONT_HERSHEY_SIMPLEX, 0, (0, 0, 255),0, cv2.LINE_AA)
        cv2.imshow("tmp", cell)
        cv2.imshow("Original", img)

        
        if cv2.waitKey(0) == 27:
            break
        # import pdb; pdb.set_trace()



cv2.waitKey(0)
cv2.destroyAllWindows()

