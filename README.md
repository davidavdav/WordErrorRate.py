# WordErrorRate.py
Alignment and word error rate calculations

Python version of [WordErrorrate.jl](https://github.com/davidavdav/WordErrorRate.jl), which, because of Julia, is much faster. 

## Installation

```
pip install worderrorrate
```

## Synopsis

Usage:
```python
>>> import worderrorrate
>>> ## A single comparison / alignment between reference and hypothesis
>>> w = worderrorrate.WER(["this", "is", "a", "test"], "this is another".split())
>>> print(f"Full alignment:\n{w}")
Full alignment:
REF: this is a    test
HYP: this is * another
Eval    c  c d       s
>>> print("The word error rate is", w.wer())
The word error rate is 0.5
>>> refali, hypali, evalali = w.align()
>>> print("Alignment indices:", refali, hypali, evalali)
Alignment indices: [0, 1, 2, 3] [0, 1, None, 2] ['c', 'c', 'd', 's']
>>> w.nref ## number of words in the reference
4
>>> w.nhyp ## in hypothesis
3
>>> w.nsub ## substitutions
1
>>> w.nins ## insertions
0
>>> w.ndel ## deletions
1
>>> ## Aggregate over multiple pairs of reference and hypothesis
>>> ws = worderrorrate.WERs() ## multiple utterances
>>> ws.append(["this", "is", "a", "test"], "this is another".split())
>>> ws.append("a b c d".split(), "a c e".split())
>>> ws.wer()
0.5
>>> ws.nref
8
>>> ws.nhyp
6
>>> ws.nsub
2
>>> ws.nins
0
>>> ws.ndel
2
```
