# WordErrorRate.py
Alignment and word error rate calculations

Python version of [WordErrorrate.jl](https://github.com/davidavdav/WordErrorRate.jl), which, because of Julia, is much faster. 

## Installation

```
pip install git+https://github.com/davidavdav/WordErrorRate.py.git
```

## Synopsys

Usage:
```python
import worderrorrate

w = worderrorrate.WER(["this", "is", "a", "test"], "this is another".split()])
print("Full alignment:\n", w)
print("The word error rate is", w.wer())
align = w.align()
print("Alignment indices:", align.refali, align.hypali, align.evalali)
```
