# encoding: utf-8

"""
Created by Gözde Gül Şahin
20.05.2018
Code to play with augmentation options and test on a single file
"""

__author__ = 'Gözde Gül Şahin'
from IO import conllud
from SP import augmenter
import codecs
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-infile', type=str, default='./data/ud-treebanks-v2.1/UD_Turkish/tr-ud-test.conllu', help='UD file to augment')
    parser.add_argument('-outfile', type=str, default='./data/ud-treebanks-v2.1/UD_Turkish/augmented.conllu', help='Output file')
    parser.add_argument('-maxrot', type=int, default=3, help='Maximum number of rotation operations per sentence')
    parser.add_argument('-prob', type=float, default=0.7, help='Probability of the augmentation operation')
    parser.add_argument('-operation', type=str, default='rotate', help='rotate|crop')
    args = parser.parse_args()
    # Rotates and crops with given probabilities and saves the results
    augment(args)

def augment(args):

    inFile = args.infile
    outfile = args.outfile
    operation = args.operation
    max_rotate = args.maxrot

    ud_reader = conllud.conllUD(inFile)
    ud_sents = ud_reader.sents
    loi = [u"nsubj", u"dobj", u"iobj", u"obj", u"obl"]
    pl = u"root"
    # for predicate
    multilabs = [u"case", u"fixed", u"flat", u"cop", u"compound"]
    fout = codecs.open(outfile,'w','utf-8')

    if operation=="rotate":
        for s in ud_sents:
            rotator = augmenter.rotator(s, aloi=loi, pl=pl, multilabs=multilabs, prob=1.0)
            augSents = rotator.rotate(maxshuffle=max_rotate)
            for augsent in augSents:
                for row in augsent:
                    line = u"\t".join(row)
                    fout.write(line)
                    fout.write(u"\n")
                fout.write(u"\n")

    elif operation=="crop":
        for s in ud_sents:
            cropper = augmenter.cropper(s, aloi=loi, pl=pl, multilabs=multilabs, prob=1.0)
            augSents = cropper.crop()
            for augsent in augSents:
                for row in augsent:
                    line = u"\t".join(row)
                    fout.write(line)
                    fout.write(u"\n")
                fout.write(u"\n")
    fout.close()

if __name__ == "__main__":
    main()