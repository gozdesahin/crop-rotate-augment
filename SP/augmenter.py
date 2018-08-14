# encoding: utf-8

"""
Created by Gözde Gül Şahin
20.05.2018
Flipper (Rotatation) and Cropper classes

"""
__author__ = 'Gözde Gül Şahin'

from chunker import *
import numpy

class rotator:
    def __init__(self, asent, aloi = [u"nsubj", u"dobj", u"iobj", u"obj", u"obl"],
                                pl = u"root",
                         multilabs = [u"case", u"fixed", u"flat", u"cop", u"compound"],
                              prob = 0.3):

        self.sent = asent
        self.cnkr = chunker(asent, aloi, pl, multilabs)
        self.flex_chunks = self.cnkr.get_all_chunks()
        self.threshold = int(prob*10)

    def _reorder(self, chunk_order):
        """
        Only insert interesting chunks - get rid of adverbial stuff
        :param chunk_order: order of the chunks (0,2,1)...
        :return: new index list
        """
        chnks = self.flex_chunks
        # the new order
        nlst = [0]
        for chunk_id in chunk_order:
            chnk = chnks[chunk_id]
            # add nodes in order
            for j in range(chnk.min, chnk.max+1):
                nlst.append(j)
        return nlst

    def rotate(self, maxshuffle):
        """
        Shuffle the sentence by moving the flexible chunks around
        :param maxshuffle: Maximum number of shuffles per sentence
        :return: shuffled sentences + original sentences
        """
        shufledSents = []

        # add the original sentence - in all cases
        shufledSents.append(self.sent.rows)

        # if there are enough flexible chunks
        if len(self.flex_chunks) > 1:
            # Get all possible permutations
            num_shuffles = min(maxshuffle, perm(len(self.flex_chunks)))
            permlst = list(itertools.permutations(range(len(self.flex_chunks))))
            poss_perms = random.sample(permlst, num_shuffles)

            for chunk_order in poss_perms:
                # if above threshold
                num = numpy.random.choice(numpy.arange(1, 11))

                # augment data if we are above the probability threshold
                if num <= self.threshold:
                    neworder = self._reorder(chunk_order)
                    newrows = self.sent.reorder(neworder)
                    shufledSents.append(newrows)
        return shufledSents


class cropper:
    def __init__(self, asent, aloi = [u"nsubj", u"dobj", u"iobj", u"obj", u"obl"],
                                pl = u"root",
                         multilabs = [u"case", u"fixed", u"flat", u"cop", u"compound"],
                              prob = 0.3):

        self.sent = asent
        self.cnkr = chunker(asent, aloi, pl, multilabs)
        self.flex_chunks = self.cnkr.get_all_chunks()
        self.threshold = int(prob*10)

    def _reorder(self, chunk_order):
        """
        Only insert interesting chunks - get rid of adverbial stuff
        :param chunk_order: order of the chunks (0,2,1)...
        :return: new index list
        """
        chnks = self.flex_chunks
        # the new order
        nlst = [0]
        for chunk_id in chunk_order:
            chnk = chnks[chunk_id]
            # add nodes in order
            for j in range(chnk.min, chnk.max+1):
                nlst.append(j)
        return nlst

    def _get_root_chunk_ix(self):
        """
        Get the index of the root chunk
        :return: index of root chunk
        """
        for i, cnk in enumerate(self.flex_chunks):
            if cnk.type==u"root":
               return i


    def crop(self):
        """
        Crop the sentence into meaningful small sentences
        :return: cropped sentences + original sentences
        """
        croppedSents = []

        # add the original sentence - in all cases
        croppedSents.append(self.sent.rows)

        # if there are enough flexible chunks
        if len(self.flex_chunks) > 1:
            # get the root chunk
            root_ix = self._get_root_chunk_ix()
            for i in range(len(self.flex_chunks)):
                if i==root_ix:
                    continue
                elif i < root_ix:
                    chunk_order = [i, root_ix]
                elif i > root_ix:
                    chunk_order = [root_ix, i]
                # if above threshold
                num = numpy.random.choice(numpy.arange(1, 11))
                # augment data if we are above the probability threshold
                if num <= self.threshold:
                    neworder = self._reorder(chunk_order)
                    newrows = self.sent.reorder(neworder)
                    croppedSents.append(newrows)
        return croppedSents