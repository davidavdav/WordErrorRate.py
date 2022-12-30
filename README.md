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

w = worderrorrate.WER(["this", "is", "a", "test"], "this is another".split())
print("Full alignment:\n", w)
print("The word error rate is", w.wer())
refali, hypali, evalali = w.align()
print("Alignment indices:", refali, hypali, evalali)

ws = worderrorrate.WERs() ## multiple utterances
ws.append(["this", "is", "a", "test"], "this is another".split())
ws.append("a b c d".split(), "a c e".split())
ws.wer()
```
