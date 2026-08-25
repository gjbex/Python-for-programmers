import Lean.Elab.Tactic.Omega

/-!
# The hopping puzzle

This file formalizes the parity proof for `hopping.ipynb`.

A configuration contains three points on the integer grid.  A hop reflects one
point through another point.  There are six possible directed hops.  The order
of the three points is only used to state those six moves; the invariant below
is the parity of the *sum* of their coordinates, so it is independent of that
order.
-/

namespace Hopping

abbrev Point := Int × Int

structure Configuration where
  first : Point
  second : Point
  third : Point
deriving Repr, DecidableEq

/- Reflect `moving` through `fixed`. -/
def hop (moving fixed : Point) : Point :=
  (2 * fixed.1 - moving.1, 2 * fixed.2 - moving.2)

/- The six directed hops possible in a three-point configuration. -/
inductive OneHop : Configuration → Configuration → Prop where
  | firstOverSecond (c) :
      OneHop c { c with first := hop c.first c.second }
  | firstOverThird (c) :
      OneHop c { c with first := hop c.first c.third }
  | secondOverFirst (c) :
      OneHop c { c with second := hop c.second c.first }
  | secondOverThird (c) :
      OneHop c { c with second := hop c.second c.third }
  | thirdOverFirst (c) :
      OneHop c { c with third := hop c.third c.first }
  | thirdOverSecond (c) :
      OneHop c { c with third := hop c.third c.second }

/- Reflexive, transitive reachability by zero or more hops. -/
inductive Reachable : Configuration → Configuration → Prop where
  | refl (c) : Reachable c c
  | tail {start before after} :
      Reachable start before → OneHop before after → Reachable start after

def totalX (c : Configuration) : Int :=
  c.first.1 + c.second.1 + c.third.1

def totalY (c : Configuration) : Int :=
  c.first.2 + c.second.2 + c.third.2

/-
The signature records whether the total x-coordinate and total y-coordinate
are even or odd.  Summing makes this invariant insensitive to any permutation
of the three points.
-/
def paritySignature (c : Configuration) : Int × Int :=
  (totalX c % 2, totalY c % 2)

/- A single hop changes each coordinate total by an even integer. -/
theorem oneHop_preserves_paritySignature
    {before after : Configuration} (h : OneHop before after) :
    paritySignature before = paritySignature after := by
  cases h <;>
    simp [paritySignature, totalX, totalY, hop] <;>
    omega

/- Hence any finite sequence of hops preserves the same signature. -/
theorem reachable_preserves_paritySignature
    {start finish : Configuration} (h : Reachable start finish) :
    paritySignature start = paritySignature finish := by
  induction h with
  | refl => rfl
  | tail _ oneHop inductionHypothesis =>
      exact inductionHypothesis.trans
        (oneHop_preserves_paritySignature oneHop)

def start : Configuration where
  first := (0, 0)
  second := (1, 0)
  third := (0, 1)

def target : Configuration where
  first := (1, 0)
  second := (0, 1)
  third := (1, 1)

/-
The start signature is `(1, 1)`, whereas the target signature is `(0, 0)`.
They therefore cannot be connected by any finite sequence of hops.
-/
theorem target_not_reachable : ¬ Reachable start target := by
  intro reachable
  have invariant := reachable_preserves_paritySignature reachable
  simp [paritySignature, totalX, totalY, start, target] at invariant

end Hopping
