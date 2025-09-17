# Python for Programmers — Extra Exercises Worksheet

Use this worksheet to run a hands-on training session aligned with the presentation and this repository. Each exercise includes a short goal, repo references, estimated time, and a solution sketch so instructors can guide or participants can self-check.

Prerequisites
- Python 3.9+ recommended (3.11+ ideal)
- From repo root: optional `conda env create -f environment.yml` or your own venv
- Run scripts from the paths shown (use `python -m` or `chmod +x` where applicable)

Session Plan (suggested)
- Block 1 (Fundamentals) — 45–60 min
- Block 2 (Iterators) — 45–60 min
- Break — 10 min
- Block 3 (OOP + Functional Tools) — 45–60 min
- Block 4 (Data Formats) — 45–60 min
- Capstone (optional) — 30–45 min

Notes
- Files referenced live under `source_code/presentation/...` unless stated.
- “Solution sketch” shows core ideas; exact outputs may vary.

---

## Block 1 — Fundamentals

1) Hello with CLI args
- Goal: extend a hello script to accept a name and print Python version.
- Start from: `presentation/fundamentals/hello_world.py`
- Tasks: add `argparse` with `--name`; print `sys.version.split()[0]`.
- Estimated time: 8 min
- Solution sketch:
  ```python
  #!/usr/bin/env python3
  import argparse, sys
  def main():
      p = argparse.ArgumentParser()
      p.add_argument('--name', default='World')
      args = p.parse_args()
      print(f"Hello, {args.name}!")
      print(f"Python {sys.version.split()[0]}")
  if __name__ == '__main__': main()
  ```

2) Counting character classes
- Goal: count upper, lower, digits, other in text or a file.
- Start from: `presentation/fundamentals/counting_cases.py`
- Tasks: add `--file` (mutually exclusive with `--text`), robust decoding.
- Estimated time: 12 min
- Solution sketch:
  ```python
  import argparse
  def counts(s):
      up=sum(c.isupper() for c in s); lo=sum(c.islower() for c in s)
      di=sum(c.isdigit() for c in s); ot=len(s)-up-lo-di
      return up,lo,di,ot
  # argparse with mutually exclusive group; open(file, errors='replace')
  ```

3) Basic data parsing with stats
- Goal: compute min, max, mean, and invalid-line count from measurements.
- Data: `presentation/fundamentals/data/measurement.txt`
- Tasks: ignore empty/comment lines; two versions: (a) straightforward list processing, (b) generator pipeline.
- Estimated time: 15 min
- Solution sketch:
  ```python
  def parse_lines(lines):
      for ln in lines:
          ln=ln.strip()
          if not ln or ln.startswith('#'): continue
          try: yield float(ln)
          except ValueError: yield None
  vals = list(parse_lines(open(path)))
  good=[v for v in vals if v is not None]; bad=len(vals)-len(good)
  mmin=min(good); mmax=max(good); mean=sum(good)/len(good)
  ```

4) Safe normalization
- Goal: normalize a sequence to [0, 1] with edge cases handled.
- Start from: `presentation/fundamentals/modifying_data.py`
- Tasks: handle empty list; if all equal, return zeros; avoid division-by-zero.
- Estimated time: 8 min
- Solution sketch: `lo=min(xs); hi=max(xs); rng=hi-lo or 1; [ (x-lo)/rng for x in xs ]`.

5) String table formatting
- Goal: print n, n^2, n^3 aligned with f-strings and with `str.format`.
- Tasks: add width specifiers and alignment, e.g., `f"{n:>4} {n*n:>6} {n*n*n:>8}"`.
- Estimated time: 8 min
- Solution sketch: demonstrate both styles and fixed widths.

---

## Block 2 — Iterators and itertools

6) Prime generator in range
- Goal: yield primes in `[lo, hi)`; support `--count` to produce N primes.
- Start from: `presentation/iterators/primes.py`
- Tasks: add CLI args; break on upper bound or count.
- Estimated time: 12 min
- Solution sketch:
  ```python
  def primes():
      yield 2; n=3
      import math
      def is_prime(k):
          return all(k%d for d in range(2, int(math.sqrt(k))+1))
      while True:
          if is_prime(n): yield n
          n += 1
  ```

7) Reusable iterable vs single-use iterator
- Goal: show why a generator object is exhausted after one pass and how to fix.
- Start from: small script or `primes.py` behavior.
- Tasks: write a class with `__iter__` returning a fresh generator.
- Estimated time: 10 min
- Solution sketch:
  ```python
  class Odds:
      def __init__(self, n): self.n=n
      def __iter__(self):
          return (2*i+1 for i in range(self.n))
  # two loops over Odds(n) both work
  ```

8) Accumulate variants
- Goal: extend `accumulator.py` with cumulative min/max and concatenation.
- Start from: `presentation/iterators/accumulator.py`
- Tasks: show `accumulate(seq, min)` and `max`; use `operator.concat` on strings/lists.
- Estimated time: 8 min
- Solution sketch: add loops with `accumulate(data, min)` and `accumulate(data, max)`.

9) Grouping with `groupby`
- Goal: group objects by computed key; count per group.
- Start from: new script; refer to `presentation/iterators/people.py` pattern.
- Tasks: define `Person(name, age)`; sort by `age//10`, then `groupby` by decade.
- Estimated time: 12 min
- Solution sketch:
  ```python
  from itertools import groupby
  from operator import attrgetter
  people = [Person('A', 23), Person('B', 35), ...]
  people.sort(key=lambda p: p.age//10)
  for dec, grp in groupby(people, key=lambda p: p.age//10):
      grp=list(grp); print(dec, len(grp))
  ```

10) Minimal Dataset tests
- Goal: test append, type conversion failure, and compute.
- Start from: `presentation/iterators/dataset.py`
- Tasks: write 3 small tests (no framework needed) or `pytest` if available.
- Estimated time: 12–15 min
- Solution sketch:
  ```python
  from dataset import Dataset, ColumnDef, ConversionError
  ds=Dataset([ColumnDef('x', int), ColumnDef('y', int)])
  ds.append((1,2)); assert len(ds)==1
  try: ds.append(('a', 'b')); assert False
  except ConversionError: pass
  ds.compute([ColumnDef('s', int)], ['x','y'], lambda x,y:(x+y,))
  ```

---

## Block 3 — OOP and Functional Tools

11) Extend Point dataclass
- Goal: add validation and utilities to `Point`.
- Start from: `presentation/oop/point_01.py`
- Tasks: add `__post_init__` to ensure numeric; add `translate(dx,dy)` returning new `Point`; add `midpoint(other)`.
- Estimated time: 12 min
- Solution sketch:
  ```python
  import dataclasses, math
  @dataclasses.dataclass
  class Point:
      x: float; y: float
      def __post_init__(self):
          for v in (self.x, self.y):
              if not isinstance(v, (int,float)): raise TypeError
      def translate(self, dx, dy): return Point(self.x+dx, self.y+dy)
      def midpoint(self, other): return Point((self.x+other.x)/2, (self.y+other.y)/2)
  ```

12) Ordering Points
- Goal: make points orderable by distance to origin.
- Start from: `point_01.py`
- Tasks: set `order=True` and add `sort_index` field or define `__lt__`.
- Estimated time: 8 min
- Solution sketch:
  ```python
  @dataclasses.dataclass(order=True)
  class Point:
      sort_index: float = dataclasses.field(init=False, repr=False)
      x: float; y: float
      def __post_init__(self): self.sort_index = (self.x**2 + self.y**2)**0.5
  ```

13) Polyline length
- Goal: compose points into a polyline with total length.
- Tasks: class `Polyline(points: list[Point])` with `length()` summing consecutive distances; make it iterable.
- Estimated time: 10–12 min
- Solution sketch:
  ```python
  class Polyline:
      def __init__(self, pts): self._pts=list(pts)
      def __iter__(self): return iter(self._pts)
      def length(self):
          return sum(a.distance(b) for a,b in zip(self._pts, self._pts[1:]))
  ```

14) Sorting with `operator.itemgetter`
- Goal: sort nested tuples by multiple keys using `itemgetter` vs `lambda`.
- Start from: `presentation/operators-functools/sort.py`
- Tasks: add sorting by `(department, -score, name)`; discuss readability.
- Estimated time: 8 min
- Solution sketch:
  ```python
  from operator import itemgetter
  data=[('Sales', 90, 'A'), ('IT', 90, 'B'), ('Sales', 88, 'C')]
  data.sort(key=lambda t: (t[0], -t[1], t[2]))
  # or use a helper since negative with itemgetter needs transform
  ```

15) `reduce`, gcd and lcm
- Goal: practice `functools.reduce` with associative ops.
- Start from: `presentation/operators-functools/reduce.py`
- Tasks: implement gcd/lcm over a list; compare to `math.gcd`.
- Estimated time: 10 min
- Solution sketch:
  ```python
  from functools import reduce
  from math import gcd
  def lcm(a,b):
      from math import prod
      return abs(a*b)//gcd(a,b) if a and b else 0
  def gcd_list(xs): return reduce(gcd, xs)
  def lcm_list(xs): return reduce(lcm, xs)
  ```

16) `partial` and `cmp_to_key`
- Goal: use `partial` to preset arguments; sort with a custom comparator.
- Tasks: `partial(math.log, x, base=10)` alternative; implement case-insensitive comparator with case as tiebreaker using `functools.cmp_to_key`.
- Estimated time: 10 min
- Solution sketch:
  ```python
  from functools import partial, cmp_to_key
  import math
  log10 = partial(math.log, base=10)
  def cmp(a,b):
      ai, bi = a.lower(), b.lower()
      if ai!=bi: return -1 if ai<bi else 1
      return -1 if a<b else (1 if a>b else 0)
  words.sort(key=cmp_to_key(cmp))
  ```

---

## Block 4 — Data Formats (CSV, JSON, XML, Binary)

17) JSON averaging with robustness
- Goal: compute mean and median age; handle missing/null ages; optional `--min-age`.
- Start from: `presentation/data-formats/average_age.py`
- Estimated time: 12–15 min
- Solution sketch:
  ```python
  import json, statistics, argparse
  ages=[p.get('age') for p in json.load(open('people.json'))]
  ages=[a for a in ages if isinstance(a,(int,float))]
  if args.min_age is not None: ages=[a for a in ages if a>=args.min_age]
  print({'mean': statistics.fmean(ages), 'median': statistics.median(ages)})
  ```

18) CSV with comments and dialects
- Goal: detect delimiter and ignore comment headers.
- Start from: `presentation/data-formats/read_commented_csv.py`
- Estimated time: 12 min
- Solution sketch: use `csv.Sniffer().sniff` on non-comment sample, then iterate rows skipping lines starting with `#` or `;`.

19) Binary doubles — endianness
- Goal: extend `read_doubles.py` to support big-endian via a flag.
- Files: `presentation/data-formats/doubles.bin`, `read_doubles.py`
- Estimated time: 10 min
- Solution sketch:
  ```python
  import struct
  fmt = ('>' if args.big else '<') + 'd'
  while (chunk := f.read(8)):
      print(struct.unpack(fmt, chunk)[0])
  ```

20) Variable-length arrays summary
- Goal: compute per-array min/max/mean and write a CSV summary.
- Start from: `presentation/data-formats/read_variable_length_array.py`
- Estimated time: 12–15 min
- Solution sketch: iterate arrays, compute stats, use `csv.writer` to save `(idx, n, min, max, mean)`.

21) XML round-trip
- Goal: generate XML with `write_xml.py`, then parse with `read_xml.py`, verifying counts (including nested blocks).
- Files: `presentation/data-formats/write_xml.py`, `read_xml.py`
- Estimated time: 12 min
- Solution sketch: run writer with a few blocks/items; ensure reader lists all items; extend writer to support nested blocks if not present.

22) AGT parser aggregates
- Goal: compute per-file aggregates across `agt_data/*.CSV` and output a combined CSV.
- Files: `presentation/data-formats/agt_parser.py`, `presentation/data-formats/agt_data/*.CSV`
- Estimated time: 15–20 min
- Solution sketch: parse each file, accumulate min/max/avg per numeric column, write one row per file.

23) Text as binary — line index
- Goal: reproduce `line_indexer.py` on a new text file and verify with `read_line_index.py`.
- Files: `presentation/data-formats/line_indexer.py`, `read_line_index.py`
- Estimated time: 10 min
- Solution sketch: index `index.txt`; then for a few lines, read back with recorded offset/length and compare to original.

---

## Capstone (optional)

24) Streaming stats with Welford
- Goal: compute mean, variance, stdev, min, max in a single pass over measurements using an online algorithm.
- References: `source_code/welford_algorithm.ipynb`, `hands-on/data/measurement.txt`
- Tasks: build a generator pipeline that yields floats; update a `Stats` object per line; output JSON summary.
- Estimated time: 20–30 min
- Solution sketch:
  ```python
  import math, json
  class Stats:
      def __init__(self): self.n=0; self.mean=0.0; self.M2=0.0; self.lo=float('inf'); self.hi=float('-inf')
      def add(self, x):
          self.n+=1; delta=x-self.mean; self.mean += delta/self.n; self.M2 += delta*(x-self.mean)
          self.lo=min(self.lo,x); self.hi=max(self.hi,x)
      def result(self):
          var = self.M2/(self.n-1) if self.n>1 else 0.0
          return {'count': self.n, 'min': self.lo, 'max': self.hi, 'mean': self.mean, 'stdev': math.sqrt(var)}
  ```

25) Iterator-powered data pipeline
- Goal: generate synthetic CSV with `data_generator.py`, then build an iterator pipeline to group by a categorical column and compute per-group stats written to JSON.
- References: `presentation/data-formats/data_generator.py`, `itertools.groupby`
- Estimated time: 20–30 min
- Solution sketch: run generator; stream rows, sort by key, then `groupby(key)` computing mean per group; `json.dump` the summary.

---

Tips for Instructors
- Encourage small, runnable iterations and frequent prints.
- When time is short, prioritize exercises 1, 3, 6, 9, 11, 15, 17, 19, and 24.
- Pair participants on the capstone; one drives, one reviews.

