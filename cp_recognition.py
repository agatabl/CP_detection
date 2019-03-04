import cv2
import numpy as np

file_path = input('Direct path to georeferenced map (jpg or png): ')
output_path = input('Direct path for output. Remember about jpg or png extension: ')
output_path_csv = input('Direct path for output csv. Remember about csv extension: ')
md = input("""Minimum distance between circles. Too big number will cause skipping many circles,
while to small will cause random circles to appear all over the image sadly: """)
minR = input("Min radius of circles to be detected: ")
maxR = input("Max radius of circles to be detected: ")
N = float(input("North border of map: "))
E = float(input("East border of map: "))
S = float(input("South border of map: "))
W = float(input("West border of map: "))

img = cv2.imread(file_path)
img = cv2.medianBlur(img, 5)
imgCopy = img.copy()
cimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
height = cimg.shape[0]
width = cimg.shape[1]
rectangle = cv2.rectangle(imgCopy, (0, 0), (width, height), (255, 255, 255), cv2.FILLED)

try:
    # circle detection
    circles = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT, 1, int(md),
                               param1=50, param2=30, minRadius=int(minR), maxRadius=int(maxR))
except cv2.error as e:
    print('Error occured', e)

circles = np.uint16(np.around(circles))
for i in circles[0, :]:
    # draw the center of the circle on image( for reference)
    # cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 0), 3)
    # draw the center of the circle on plain background (for future usage)
    cv2.circle(rectangle, (i[0], i[1]), 2, (0, 0, 0), 3)

imgray = cv2.cvtColor(rectangle, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

outline_coords = []
for row in contours[0]:
    outline_coords.append(row[0, :])


list_of_coords = []
for array in contours:
    list_of_coords.append(array[0, :][0])


lat_dif = N - S
lon_dif = E - W
image_width = outline_coords[2][0]
image_height = outline_coords[1][1]
ar_list_of_coords = np.array(list_of_coords)

# calculation of gographocal coordinates based on image coordinates( transformation)
longitudes = []
for lon in ar_list_of_coords[:, 0]:
    lon_real = W + (lon * lon_dif)/(outline_coords[2][0]+1)
    longitudes.append(lon_real)

latitudes = []
for lat in ar_list_of_coords[:, 1]:
    lat_real = N - (lat * lat_dif)/(outline_coords[2][1]+1)
    latitudes.append(lat_real)

coords_tuple = tuple(zip(tuple(latitudes), tuple(longitudes)))
for e, c in zip(range(len(ar_list_of_coords)), coords_tuple):

    textt = str(coords_tuple.index(c))
    cv2.putText(cimg, textt, (ar_list_of_coords[e][0], ar_list_of_coords[e][1]),
                cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 5)

# drawing contours only of middles od circels
cv2.drawContours(cimg, contours, -1, (0, 255, 0))
cv2.imwrite(output_path, cimg)

f = open(output_path_csv, 'w')
for i, c in zip(range(len(longitudes)), range(len(coords_tuple))):
    f.write("{},{},{}\n".format(c, latitudes[i], longitudes[i]))
f.close()
