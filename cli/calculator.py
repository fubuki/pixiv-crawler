# -*- coding: utf-8 -*-

import cv2
import fire
import anime
import os
import imagehash
from PIL import Image

class Search(object):
    def double(self, number):
        return 2 * number

    def image_face(self, source):
        cascade_file = "lbpcascade_animeface.xml"
        if not os.path.isfile(cascade_file):
            raise RuntimeError("%s: not found" % cascade_file)

        source_img = cv2.imread(source)
        faces = anime.face(source_img, cascade_file)

        if len(faces) > 0:
            img = cv2.imread(source)
            for index, (x, y, w, h) in enumerate(faces):
                ##cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                dst = img[y:y + h, x:x + w]
                cv2.imwrite("fate-" + str(index) + ".jpg" , dst)

    def anime_face(self, filename):

        cap = cv2.VideoCapture(filename)

        framenum = 0
        faceframenum = 0
        color = (0, 0, 255)

        while (cap.isOpened()):
            framenum += 1

            ret, image = cap.read()
            if not ret:
                break

            if framenum % 50 == 0:
                faces = anime.face(image)
                if len(faces) == 0:
                    continue

                for rect in faces:
                    x = rect[0]
                    y = rect[1]
                    width = rect[2]
                    height = rect[3]
                    dst = image[y:y + height, x:x + width]
                    resized_dst = cv2.resize(dst, (64, 64))
                    faceframenum += 1

        cap.release()


    def search_object(self, object, image):
        object_kp, object_des = anime.img_sift(object)
        image_kp, image_des = anime.img_sift(image)

        object_img = cv2.imread(object, 0)
        image_img = cv2.imread(image, 0)

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(object_des, image_des, k=2)
        matches_mask = [[0, 0] for i in xrange(len(matches))]

        for i, (m, n) in enumerate(matches):
            if m.distance < 0.7 * n.distance:
                matches_mask[i] = [1, 0]

        draw_params = dict(matchColor=(0, 255, 0),
                           singlePointColor=(255, 0, 0),
                           matchesMask=matches_mask,
                           flags=0)

        img3 = cv2.drawMatchesKnn(object_img, object_kp, image_img, image_kp, matches, None, **draw_params)

        cv2.imwrite("search_object.png", img3)

    def imagehash(self, source, dest):
        source_hash = imagehash.phash(Image.open(source))
        dest_hash = imagehash.phash(Image.open(dest))
        print 1 - (source_hash - dest_hash) * 1.0/len(source_hash.hash)**2



if __name__ == '__main__':
    fire.Fire(Search)
