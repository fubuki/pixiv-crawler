# -*- coding: utf-8 -*-

import cv2
import fire
import anime

class Search(object):
    def double(self, number):
        return 2 * number

    def face(self, source, dest):
        cascade_file = "lbpcascade_animeface.xml"
        if not os.path.isfile(cascade_file):
            raise RuntimeError("%s: not found" % cascade_file)

        faces = anime.face(source, cascade_file)

        if len(faces) > 0:
            img = cv2.imread(source)
            for rect in faces:
                x = rect[0]
                y = rect[1]
                width = rect[2]
                height = rect[3]
                dst = img[y:y + height, x:x + width]
                if dst is not None:
                    cv2.imwrite(dest, dst)



if __name__ == '__main__':
    fire.Fire(Search)