# CP_detection
Detection of geographic coordinates of CPs based on georeferenced image. Final result is csv file with point number and coordinates and image with orresponding data located respectively.

The key arguments are in HoughCircles() function. Although the input forces determinig min and max radius of 
circle and distnace between circles, it is also crucial to consider changing:

- dp – Inverse ratio of the accumulator resolution to the image resolution. For example, if dp=1 , the accumulator has the same resolution as the input image. If dp=2 , the accumulator has half as big width and height
- param1 – First method-specific parameter. In case of CV_HOUGH_GRADIENT , it is the higher threshold of the two passed to the Canny() edge detector (the lower one is twice smaller).
- param2 – Second method-specific parameter. In case of CV_HOUGH_GRADIENT , it is the accumulator threshold for the circle centers at the detection stage. The smaller it is, the more false circles may be detected. Circles, corresponding to the larger accumulator values, will be returned first.

in

`cv2.HoughCircles(image, method, dp, minDist[, circles[, param1[, param2[, minRadius[, maxRadius]]]]])`

Depending of type of imge one's working on the values may vary significantly.

Values of N,S,E,W inputs must be in decimal degrees.
