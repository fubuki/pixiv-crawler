# -*- coding: utf-8 -*-

import cv2
import os.path

cascade_file = "lbpcascade_animeface.xml"

def detect(image):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    cascade = cv2.CascadeClassifier(cascade_file)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.equalizeHist(gray)

    faces = cascade.detectMultiScale(gray,
            # 認識用オプション
            scaleFactor = 1.1,
            minNeighbors = 1,
            minSize = (24,24))

    return faces


filename = "/home/zero/exp/[SFEO-Raws] God Eater - 02 (BD 720P x264 10bit AAC)[6FF39F92].mp4"
cap = cv2.VideoCapture(filename)

# 顔だけを切り出して保存する
framenum = 0
faceframenum = 0
color = (0,0,255)

# 保存先のディレクトリ作成
path = os.path.splitext(filename)
dir_path = path[0] + '_face'
if os.path.isdir(dir_path) == False:
    os.mkdir(dir_path)

while(cap.isOpened()):
    framenum += 1

    ret, image = cap.read()
    if not ret:
        break

    if framenum%50 == 0:
        faces = detect(image)
        if len(faces) == 0:
            continue # 認識結果がnullなら次のフレームへ

        for rect in faces:
            x = rect[0]
            y = rect[1]
            width = rect[2]
            height = rect[3]
            dst = image[y:y + height, x:x + width]
            resized_dst = cv2.resize(dst,(64,64)) # サイズを64*64に調整
            if str(faceframenum) < 10:
                cv2.imwrite(dir_path  + '/' + "00" + str(faceframenum) + ".jpg", resized_dst)
            elif 10 < str(faceframenum) < 100:
                cv2.imwrite(dir_path + '/' + "0" + str(faceframenum) + ".jpg", resized_dst)
            else:
                cv2.imwrite(dir_path + '/' + str(faceframenum) + ".jpg", resized_dst)
            faceframenum += 1

cap.release()