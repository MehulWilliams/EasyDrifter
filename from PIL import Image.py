from PIL import Image
import PIL.ImageGrab

img = PIL.ImageGrab.grab()
#img = img.resize((1440,900))
#print(img.size) 
img.show()