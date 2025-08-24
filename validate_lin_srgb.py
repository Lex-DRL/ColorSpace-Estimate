#!/usr/bin/env python
# encoding: utf-8

import json

def linear_to_srgb(linear: float) -> float:
	if linear <= 0.0031308:
		return 12.92 * linear
	else:
		return 1.055 * (linear ** (1/2.4)) - 0.055


def srgb_encode_scalar_icc(x: float) -> float:
	"""
	This is the form used in ICC’s sRGB profile.
	If your expanded dataset was generated from the ICC tables, this should give bit-for-bit agreement down to ~1e-7 or tighter.
	"""
	if x <= 0.003130668442500634:   # exact cutoff
		return (323/25) * x        # 12.92 exactly
	else:
		return (211/200) * (x ** (1/2.4)) - (11/200)


def f(a) -> list[float]:
	return [srgb_encode_scalar_icc(x) for x in a]

# Load data from JSON file
with open('conversion.json', 'r') as file:
	data = json.load(file)

# Verify each entry with tolerance
tolerance_rel = 0.755 / (10**6)
for entry in data:
	a: list[float] = entry['a']
	f_a_expected: list[float] = entry['f_a']
	f_a_computed: list[float] = f(a)
	intensity = min(max(f_a_expected), max(f_a_computed))
	tolerance = tolerance_rel * intensity if intensity > tolerance_rel * 10 else tolerance_rel
	for i in range(3):
		assert abs(f_a_computed[i] - f_a_expected[i]) < tolerance, f"Mismatch at {a}: expected {f_a_expected[i]}, computed {f_a_computed[i]}"
	print(f"Input: {a} -> Output: {f_a_computed}")

print("All tests passed with relative tolerance", tolerance_rel)
