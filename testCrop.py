from croppaSfondo import croppaSfondo
import cv2

a = cv2.imread("imm/dog000.jpg",0)
cropper = croppaSfondo()
a = cropper.croppa(a)
cv2.imwrite("imm/risutato.jpg",a)
