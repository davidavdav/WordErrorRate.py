#!/usr/bin/env python3

## perform alignment for word error rate and similar DTW problems.
## Inspired by https://martin-thoma.com/word-error-rate-calculation/

from builtins import zip
from builtins import str
from builtins import range
from builtins import object

import numpy
import random

# initialisation
class WER(object):
    def __init__(self, ref, hyp, subcost=4, inscost=3, delcost=3):
        cost = numpy.zeros((len(ref) + 1, len(hyp) + 1), dtype=numpy.uint16)
        dec = numpy.zeros((len(ref) + 1, len(hyp) + 1), dtype=numpy.uint8) ## 0123: csid, decision
        for i in range(1, len(ref)+1):
            cost[i, 0] = delcost * i
            dec[i, 0] = 3 ## del
        for j in range(1, len(hyp)+1):
            cost[0, j] = inscost * j
            dec[0, j] = 2 ## ins

        # computation
        for i in range(1, len(ref)+1):
            for j in range(1, len(hyp)+1):
                if ref[i-1] == hyp[j-1]:
                    cost[i, j] = cost[i-1, j-1]
                else:
                    sid = [cost[i-1, j-1] + subcost, cost[i, j-1] + inscost, cost[i-1, j] + delcost]
                    mini = numpy.argmin(sid)
                    cost[i, j] = sid[mini]
                    dec[i, j] = mini + 1

        ## backtrack
        self.refeval = []
        self.hypeval = []
        i, j = len(ref), len(hyp)
        self.nsub = self.nins = self.ndel = 0
        while i > 0 or j > 0:
            if dec[i, j] < 2: ## correct or subsitution
                d = "cs"[dec[i, j]]
                self.nsub += dec[i, j]
                i -= 1
                j -= 1
                self.refeval.insert(0, d)
                self.hypeval.insert(0, d)
            elif dec[i, j] == 2: ## insertion
                j -= 1
                self.hypeval.insert(0, "i")
                self.nins += 1
            else: ## deletion
                i -= 1
                self.refeval.insert(0, "d")
                self.ndel += 1
        self.nerr = self.nsub + self.nins + self.ndel

        self.ref = ref[:]
        self.hyp = hyp[:]

    def wer(self):
        return float(self.nerr) / len(self.ref)

    def align(self):
        refali = []
        hypali = []
        evalali = []
        ri = hi = 0
        while ri < len(self.refeval) or hi < len(self.hypeval):
            if ri < len(self.refeval) and self.refeval[ri] == 'd':
                hypali.append(None)
                refali.append(ri)
                evalali.append('d')
                ri += 1
            elif hi < len(self.hypeval) and self.hypeval[hi] == 'i':
                refali.append(None)
                hypali.append(hi)
                evalali.append('i')
                hi += 1
            else:
                refali.append(ri)
                hypali.append(hi)
                evalali.append(self.refeval[ri])
                ri += 1
                hi += 1
        return refali, hypali, evalali

    def pralign(self, inssym="*", delsym="*"):
        refali, hypali, evalali = self.align()
        prref = [str(self.ref[i]) if i is not None else delsym * len(str(self.hyp[j])) for i, j in zip(refali, hypali)]
        prhyp = [str(self.hyp[j]) if j is not None else inssym * len(str(self.ref[i])) for i, j in zip(refali, hypali)]
        return prref, prhyp, evalali

    def __repr__(self):
        ref, hyp, eva = self.pralign()
        lengths = [max(len(str(r)), len(str(h)), len(str(e))) for r, h, e in zip(ref, hyp, eva)]
        out = f"REF: {' '.join(('%%%ds' % l) % str(s) for l, s in zip(lengths, ref))}\n" + \
            f"HYP: {' '.join(('%%%ds' % l) % str(s) for l, s in zip(lengths, hyp))}\n" + \
            f"Eval {' '.join(('%%%ds' % l) % str(s) for l, s in zip(lengths, eva))}\n"
        return out
    
    @property
    def nref(self):
        return len(self.ref)
    
    @property
    def nhyp(self):
        return len(self.hyp)

class WERs:
    def __init__(self, subcost=4, inscost=3, delcost=3):
        self.subcost = subcost
        self.inscost = inscost
        self.delcost = delcost
        self.wers = list()
        for attr in ['nref', 'nhyp', 'ndel', 'nins', 'nsub', 'nerr']:
            setattr(self, attr, 0)
        
    def append(self, ref, hyp):
        wer = WER(ref, hyp, self.subcost, self.inscost, self.delcost)
        self.wers.append(wer)
        for attr in ['nref', 'nhyp', 'ndel', 'nins', 'nsub', 'nerr']:
            setattr(self, attr, getattr(self, attr) + getattr(wer, attr))

    def wer(self):
        return self.nerr / self.nref
    
    def align(self):
        return [wer.align() for wer in self.wers]
    
    @property
    def nutt(self):
        return len(self.wers)
        

def gentest(n=1000, v=100, p=0.25):
    ref = [random.randrange(v) for i in range(n)]
    hyp = ref[:]
    for i in range(int(p*n)):
        hyp[random.randrange(len(hyp))] = random.randrange(v) ## sub
        hyp.insert(random.randrange(len(hyp)), random.randrange(v)) ## insd
        hyp.pop(random.randrange(len(hyp))) ## del
    return ref, hyp
