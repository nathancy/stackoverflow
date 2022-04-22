from PIL import ImageFont, ImageDraw, Image
import cv2
import numpy as np

# Create black mask using Numpy and convert from BGR (OpenCV) to RGB (PIL)
# image = cv2.imread('1.png') # If you were using an actual image
image = np.zeros((100, 950, 3), dtype=np.uint8)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
pil_image = Image.fromarray(image)

# Draw non-ascii text onto image
font = ImageFont.truetype("C:\Windows\Fonts\\arial.ttf", 35)
draw = ImageDraw.Draw(pil_image)
draw.text((30, 30), "ԱԲԳԴԵԶԷԸԹԺԻԼԽԾԿՀՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՓՔՖ", font=font)

# Convert back to Numpy array and switch back from RGB to BGR
image = np.asarray(pil_image)
image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
cv2.imshow('image', image)
cv2.waitKey()
