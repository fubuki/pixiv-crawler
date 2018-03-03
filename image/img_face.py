# -*- coding: utf-8 -*-

import cv2
import os.path

def detect(filename, cascade_file="lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    # カスケード分類器の特徴量を取得
    cascade = cv2.CascadeClassifier(cascade_file)

    # ファイル読み込み
    img = cv2.imread(filename)

    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ヒストグラム表示用のイメージ作成
    gray = cv2.equalizeHist(gray)

    # キャラクター認識の実行
    # scaleFactorは画像スケールにおける縮小量
    # minNeighborsは値が大きくなれば検出の信頼性が上がるが見逃してしまう場合も増える
    # 認識する最小サイズ
    faces = cascade.detectMultiScale(gray,
            # 認識用オプション
            scaleFactor = 1.1,
            minNeighbors = 1,
            minSize = (24,24))

    # 保存先のディレクトリ作成
    if len(faces) > 0 :
        path = os.path.splitext(filename)
        dir_path = path[0] + '_face'
        if os.path.isdir(dir_path) == False:
            os.mkdir(dir_path)

    for rect in faces:
        x = rect[0]
        y = rect[1]
        width = rect[2]
        height = rect[3]
        dst = img[y:y + height, x:x + width]
        return dst

    return None


for path, subdirs, files in os.walk('/home/zero/pixiv_image/full/'):
    for name in files:
        print name[:-4]
        filename = os.path.join(path, name)
        dst = detect(filename)
        if dst is not  None:
            cv2.imwrite('/home/zero/detect/' + name[:-4] + "_face.png", dst)
