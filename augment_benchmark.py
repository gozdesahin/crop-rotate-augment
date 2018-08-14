#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 06.04.2018
 Gözde Gül Şahin
 Copyright 2018

 Uses *-train.conllu files under UD-treebank folder and augments each via cropping and rotating.
 Saves augmented files as train.conllu.crop|rotate.(probabilty*10)

"""
__author__ = 'Periphery'

import os
import time
import argparse
from IO import conllud
from SP import augmenter
import codecs

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-input', type=str, default='./data/ud-treebanks-v2.1', help='Root directory for ud-treebanks')
    parser.add_argument('-maxrot', type=int, default=3, help='Maximum number of rotate operations per sentence')
    parser.add_argument('-prob', type=float, default=0.7, help='Probability of an operation')
    args = parser.parse_args()
    # Rotates and crops with given probabilities and saves the results
    augment(args)

def rotate_file(trainFile, outFile, args):
    """
    Rotates all sentences in the file
    :param trainFile: file that contains ud training sentences
    :param outFile: flipped sentences will be saved here
    :param args: command line arguments (maxflip and prob)
    :return: nothing
    """
    max_rot = args.maxrot
    prob = args.prob
    loi = [u"nsubj", u"dobj", u"iobj", u"obj", u"obl"]
    pl = u"root"
    multilabs = [u"case", u"fixed", u"flat", u"cop", u"compound"]

    ud_reader = conllud.conllUD(trainFile)
    ud_sents = ud_reader.sents

    fout = codecs.open(outFile,'w','utf-8')
    for s in ud_sents:
        rotator = augmenter.rotator(s, aloi=loi, pl=pl, multilabs=multilabs, prob=prob)
        augSents = rotator.rotate(maxshuffle=max_rot)
        for augsent in augSents:
            for row in augsent:
                line = u"\t".join(row)
                fout.write(line)
                fout.write(u"\n")
            fout.write(u"\n")

def crop_file(trainFile, outFile, args):
    """
    Crops all sentences in the file
    :param trainFile: file that contains ud training sentences
    :param outFile: cropped sentences will be saved here
    :param args: command line arguments (maxflip and prob)
    :return: nothing
    """
    prob = args.prob
    loi = [u"nsubj", u"dobj", u"iobj", u"obj", u"obl"]
    pl = u"root"
    multilabs = [u"case", u"fixed", u"flat", u"cop", u"compound"]

    ud_reader = conllud.conllUD(trainFile)
    ud_sents = ud_reader.sents

    fout = codecs.open(outFile,'w','utf-8')
    for s in ud_sents:
        cropper = augmenter.cropper(s, aloi=loi, pl=pl, multilabs=multilabs, prob=prob)
        augSents = cropper.crop()
        for augsent in augSents:
            for row in augsent:
                line = u"\t".join(row)
                fout.write(line)
                fout.write(u"\n")
            fout.write(u"\n")

def augment(args):
    """
    :param args from main file
    :return:
    """

    localTest = False
    start = time.time()
    if localTest:
        args.input = './data/ud-treebanks-v2.1'
        args.maxflip = 3
        args.prob = 1.0

    # Save language encoding - training file path
    for dirName, subdirList, fileList in os.walk(args.input):
        for fname in fileList:
            if ('train.conllu' in fname) and not (('crop' in fname) or ('rotate' in fname)):
                trainFile = os.path.join(dirName, fname)
                print("Processing file: %s " % (trainFile))
                save_lang_to = dirName

                ####  rotate and save ####
                settings = ".rotate" + str(int(args.prob*10))
                rotatedFile = os.path.join(save_lang_to, fname+settings)
                rotate_file(trainFile,rotatedFile,args)

                ####  crop and save ####
                settings = ".crop" + str(int(args.prob*10))
                croppedFile = os.path.join(save_lang_to, fname+settings)
                crop_file(trainFile,croppedFile,args)
    end = time.time()

    print("Time elapsed %.2f secs" %((end-start)))

if __name__ == '__main__':
    main()