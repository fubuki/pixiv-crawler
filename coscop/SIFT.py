import cv2
import cPickle

file_img = "/home/zero/Desktop/dataset/66065214_p0.jpg"
img = cv2.imread(file_img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

sift = cv2.xfeatures2d.SIFT_create()
kp = sift.detect(gray)
sift_img = cv2.drawKeypoints(gray, kp, img)
cv2.imwrite('/home/zero/Desktop/dataset/sift_keypoints.jpg', sift_img)

surf = cv2.xfeatures2d.SURF_create()
kp = sift.detect(gray)
surf_img = cv2.drawKeypoints(gray, kp, img)
cv2.imwrite('/home/zero/Desktop/dataset/surf_keypoints.jpg', surf_img)


index = []
for point in kp:
    temp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id)
    index.append(temp)

# Dump the keypoints
f = open("/home/zero/Desktop/dataset/keypoints.txt", "w")
f.write(cPickle.dumps(index))
f.close()




