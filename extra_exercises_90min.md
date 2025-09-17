# Python for Programmers — 90‑Minute Worksheet

A trimmed plan for a 90‑minute hands‑on session using this repository. Each item includes a short goal, file reference, estimated time, and a minimal solution sketch.

Suggested flow (target ~80–90 min including brief discussion):
1) Hello CLI (6m)
2) Parse + stats (12m)
3) Primes in range (10m)
4) Groupby decades (12m)
5) Dataclass Point (12m)
6) JSON averaging (12m)
Stretch) Reduce gcd/lcm or Welford mini (10–15m)

Prereqs
- Python 3.9+ (3.11+ ideal). Optional: create env from `environment.yml`.
- Run from repo root; paths are relative to `source_code/presentation/...`.

---

## 1) Hello with CLI args (6m)
- Goal: greet a name and print Python version.
- Start from: `presentation/fundamentals/hello_world.py`
- Steps: add `argparse --name`; print `sys.version.split()[0]`.
- Sketch:
  ```python
  #!/usr/bin/env python3
  import argparse, sys
  p = argparse.ArgumentParser()
  p.add_argument('--name', default='World')
  a = p.parse_args()
  print(f"Hello, {a.name}!")
  print(f"Python {sys.version.split()[0]}")
  ```

## 2) Parse measurements + stats (12m)
- Goal: min/max/mean and invalid count from text file.
- Data: `presentation/fundamentals/data/measurement.txt`
- Steps: strip, skip empty/#, parse float; count failures.
- Sketch:
  ```python
  good = []; bad = 0
  for ln in open(path):
      s = ln.strip()
      if not s or s.startswith('#'): continue
      try: good.append(float(s))
      except ValueError: bad += 1
  mmin, mmax = min(good), max(good)
  mean = sum(good)/len(good)
  ```

## 3) Prime generator in range (10m)
- Goal: emit primes in `[lo, hi)` or first `N` primes.
- Start from: `presentation/iterators/primes.py`
- Steps: add `--lo --hi --count` (mutually exclusive hi/count); stop accordingly.
- Sketch:
  ```python
  import math
  def is_prime(n):
      return n>1 and all(n%d for d in range(2, int(math.sqrt(n))+1))
  def primes():
      yield 2; k = 3
      while True:
          if is_prime(k): yield k
          k += 1
  ```

## 4) Group people by decade (12m)
- Goal: group objects by computed key with `groupby`.
- Pattern: like `presentation/iterators/people.py`.
- Steps: define `Person(name, age)`; sort by `age//10`; `groupby` by decade and count.
- Sketch:
  ```python
  from itertools import groupby
  class Person: 
      def __init__(s,n,a): s.name=n; s.age=a
  people = [Person('A',23), Person('B',35), Person('C',31)]
  people.sort(key=lambda p: p.age//10)
  for dec, grp in groupby(people, key=lambda p: p.age//10):
      grp = list(grp); print(dec, len(grp))
  ```

## 5) Dataclass Point utilities (12m)
- Goal: add validation and helpers to `Point`.
- Start from: `presentation/oop/point_01.py`
- Steps: `__post_init__` numeric check; `translate(dx,dy)`; `midpoint(other)`.
- Sketch:
  ```python
  @dataclasses.dataclass
  class Point:
      x: float; y: float
      def __post_init__(self):
          for v in (self.x, self.y):
              if not isinstance(v, (int,float)): raise TypeError
      def translate(self, dx, dy): return Point(self.x+dx, self.y+dy)
      def midpoint(self, o): return Point((self.x+o.x)/2, (self.y+o.y)/2)
  ```

## 6) JSON averaging with robustness (12m)
- Goal: mean and median age; handle nulls; optional `--min-age`.
- Start from: `presentation/data-formats/average_age.py` and `people.json`.
- Sketch:
  ```python
  import json, statistics, argparse
  p = argparse.ArgumentParser(); p.add_argument('--min-age', type=float)
  a = p.parse_args()
  ages = [r.get('age') for r in json.load(open('people.json'))]
  ages = [x for x in ages if isinstance(x,(int,float))]
  if a.min_age is not None: ages = [x for x in ages if x >= a.min_age]
  print({'mean': statistics.fmean(ages), 'median': statistics.median(ages)})
  ```

---

### Stretch (choose one if time remains)

S1) Reduce gcd/lcm (8–10m)
- Start: `presentation/operators-functools/reduce.py`
- Sketch:
  ```python
  from functools import reduce
  from math import gcd
  def lcm(a,b): return abs(a*b)//gcd(a,b) if a and b else 0
  def gcd_list(xs): return reduce(gcd, xs)
  def lcm_list(xs): return reduce(lcm, xs)
  ```

S2) Welford streaming stats (12–15m)
- Refs: `source_code/welford_algorithm.ipynb`, `hands-on/data/measurement.txt`
- Sketch:
  ```python
  import math
  class Stats:
      def __init__(s): s.n=0; s.mean=0.0; s.M2=0.0
      def add(s,x): s.n+=1; d=x-s.mean; s.mean+=d/s.n; s.M2+=d*(x-s.mean)
      def stdev(s): return math.sqrt(s.M2/(s.n-1)) if s.n>1 else 0.0
  ```

