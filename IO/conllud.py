# encoding: utf-8

"""
Created by Gözde Gül Şahin
20.05.2018
Read UD treebanks into a data structure suitable to cropping and flipping
"""

__author__ = 'Gözde Gül Şahin'

import codecs
import copy

class conllUD:

    def __init__(self, fpath=None):
        """
        init: read sentences into conllUDsent structure
        """
        self.sents = []
        if fpath is not None:
            self.sents= self._read_file(fpath)
        else:
            print("File can not be opened, check path")

    def _read_file(self, file_path):
        """
        read_file: read tokens and create a dependency tree for all UD sentences
        """
        fin = codecs.open(file_path, encoding='utf-8')
        strIn = fin.read()
        fin.close()
        conllsentences = []
        sent_no = 0

        sentences = strIn.split("\n\n")
        for sent in sentences:
            if(len(sent)>0):
                lines = sent.split("\n")
                # create new conllud sentence
                csent = conllUDsent()
                rows = []
                tok_index = 1
                for line in lines:
                    # create UD token (if it is not a comment line or an IG token)
                    if not line.startswith(u"#") and not (u"-" in line.split("\t")[0]):
                        ctoken = conllUDtoken(line.split("\t"),tok_index)
                        csent.add_token(ctoken)
                        rows.append(line.split())
                        tok_index+=1

                csent.rows = rows

                # add token words
                csent.tokenWords = [row[1] for row in rows]
                csent.tokenLemmas = [row[2] for row in rows]
                conllsentences.append(csent)

                # build the dependency tree
                # head -> all children tokens
                for tok in csent.tokens:
                    if tok.head in csent.deptree:
                        csent.deptree[tok.head].append(tok)
                    else:
                        csent.deptree[tok.head] = [tok]
            sent_no+=1
        return conllsentences

class conllUDsent:
    def __init__(self):
        self.tokens = []
        # token words and lemmas
        self.tokenWords = []
        self.tokenLemmas = []
        # for reordering purposes
        self.deptree = {}
        self.rows = []

    def add_token(self, token):
        self.tokens.append(token)

    def print_sent_ord(self,ord):
        """
        print_sent_ord: print sentence as text with the given order
        """
        strsent = ""
        for i in ord:
            if i==0:
                continue
            tok = self.tokens[i-1]
            strsent+=(tok.word+' ')
        print strsent

    def reorder(self, neword):
        """
        reorder: Reorder the tokens of the sentence with the given new order (neword)
        """
        newrows = []

        # mapping[oldorder]=neworder
        mapping = {}
        mapping[u"0"]=u"0"

        # first put them together
        for i, j in zip(neword,range(len(neword))):
            if i==0:
                continue
            newrows.append(copy.deepcopy(self.rows[i-1]))
            mapping[self.tokens[i-1].depid] = self.tokens[j-1].depid

        # replace old ids with new ids
        for r in newrows:
            # change id
            r[0] = unicode(mapping[r[0]])
            if r[6] in mapping:
                r[6] = unicode(mapping[r[6]])
            else:
                r[6] = u"_"
        return newrows

class conllUDtoken:
    def __init__(self, fields, tok_index):
        # index in the sentence (the order)
        self.index = tok_index
        # dependency id for the dependency tree
        self.depid = fields[0]
        self.word = fields[1]
        self.lemma = fields[2]
        self.pos = fields[3]
        self.ppos = fields[4]
        self.feat = fields[5]
        self.head = fields[6]
        self.deprel = fields[7]
        self.pdeprel = fields[8]

