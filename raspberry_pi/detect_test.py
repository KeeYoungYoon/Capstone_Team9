import cv2
import numpy as np


def findNonZero(rgb_image):
  rows, cols, _ = rgb_image.shape
  counter = 0
  for row in range(rows):
    for col in range(cols):
      pixel = rgb_image[row, col]
      if sum(pixel) != 0:
        counter = counter + 1
  return counter

  def red_green(rgb_image):

    hsv = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)
    sum_saturation = np.sum(hsv[:,:,1])
    area = 48*48
    avg_saturation = sum_saturation / area

    sat_low = int(avg_saturation * 1.3)
    val_low = 140

    # Green
    lower_green = np.array([70,sat_low,val_low])
    upper_green = np.array([100,255,255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    green_result = cv2.bitwise_and(rgb_image, rgb_image, mask = green_mask)

  # Red
    lower_red = np.array([150,sat_low,val_low])
    upper_red = np.array([180,255,255])
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    red_result = cv2.bitwise_and(rgb_image, rgb_image, mask = red_mask)

    sum_green = findNonZero(green_result)
    sum_red = findNonZero(red_result)

    if sum_red >= sum_green:
        return 'red' # Red
    return 'green' # Green


 in_img=cv2.imread('1.PNG', cv2.IMREAD_COLOR) #detect 1.PNG photo 
 st_img = cv2.resize(in_img, (48,48))
 print(red_green(st_img))

 cv2.waitKey(0)
 cv2.destroyAllWindows()
