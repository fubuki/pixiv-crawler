# -*- coding: utf-8 -*-

import imagehash
from PIL import Image

origin_hash = imagehash.average_hash(Image.open('../cli/source.jpg'))

for r in range(1, 30, 5):
    rothash = imagehash.average_hash(Image.open('../cli/source.jpg').rotate(r))
    print('Rotation by %d: %d Hamming difference' % (r, origin_hash - rothash))
