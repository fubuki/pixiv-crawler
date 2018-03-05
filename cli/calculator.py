# -*- coding: utf-8 -*-

import fire


class Search(object):
    def double(self, number):
        return 2 * number


if __name__ == '__main__':
    fire.Fire(Search)