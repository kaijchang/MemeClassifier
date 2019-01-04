# MemeClassifier

## Installation

Install dependencies: `pip3 install -r requirements.txt`.

Scrape meme templates from [https://knowyourmeme.com](https://knowyourmeme.com): `python3 gatherer.py`

Build Cython extension: `python3 setup.py build_ext --inplace`

## Example
<img src="https://github.com/kajchang/MemeClassifier/raw/master/example.png" width="250">

```python
from classifier import classify_meme
import cv2

res = classify_meme(cv2.imread('example.png'))

print(max(res, key=lambda name: res[name])) # 'Hackerman'
```
