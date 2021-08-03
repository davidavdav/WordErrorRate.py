# WordErrorRate.py
Alignment and word error rate calculations

Python version of [WordErrorrate.jl](https://github.com/davidavdav/WordErrorRate.jl), which, because of Julia, is much faster. 

Usage:
```python
import wer

w = wer.WER(["this", "is", "a", "test"], "this is another".split()])
print("Full alignment:\n", w)
print("The word error rate is", w.wer)
align = w.align()
print("Indices:", align.refali, align.hypali, align.evalali)
```
