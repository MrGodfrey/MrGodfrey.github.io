---
title: Two Hidden Shapes, Two Kinds of Signal
slug: geometric-stochastic-inverse-sources
template: paper_post
date: '2026-09-24'
lang: en
math: true
listed: true
excerpt: Recovering where a source lives is different from recovering a single coefficient.
kicker: Paper Notes
cover:
  image: /img/blog/geometric-stochastic-inverse-sources.webp
  alt: A pale translucent domain contains two smooth warm and teal source shapes, with a faint trial outline and
    a small highlighted boundary sensor.
  width: 1600
  height: 900
---

Inside a material, one hidden region emits a steady source. Another produces random fluctuations. We can measure only part of the boundary. Can those measurements reveal the shapes of both regions?

This is a geometric inverse problem. The unknowns are not two numbers or two point locations, but two subsets of space.[^paper]

## A disk is already more than its center

Imagine that both regions are small disks. Moving a center changes where the signal originates. Changing a radius changes how much material contributes. Allow a general boundary, and there are infinitely many possible deformations.

A simplified model is

$$
du=\bigl(\Delta u+\mathbf1_{D_0}\bigr)dt
   +\mathbf1_{D_1}\,dW_t.
$$

The indicator $\mathbf1_{D_0}$ marks the drift-source region; $\mathbf1_{D_1}$ marks the diffusion-source region. The full paper also includes lower-order terms.

In this toy model, taking expectation removes the direct contribution of the diffusion source. The mean may help identify $D_0$, but it cannot by itself tell the whole story about $D_1$. Random observations contain another channel of information.

The two regions are not assumed to be disjoint. Two different kinds of emission can occupy the same part of the material.

## First prove that the shapes can be distinguished

Before optimizing a boundary, we need to know whether different pairs of regions can produce identical observations.

The paper establishes uniqueness under its assumptions from the prescribed boundary-flux observations on an accessible boundary portion. The equation's unique-continuation structure is what connects a local measurement to hidden interior supports.

This is a statement about that observation framework. It is not a promise that one isolated sensor reading or the mean temperature alone determines two arbitrary shapes.

## Then move the boundary, not every pixel independently

To reconstruct the sources, compare the predicted boundary data with the measured data and add a perimeter penalty. The penalty discourages complicated boundaries introduced solely to fit noise.

A small deformation changes an indicator source in a thin layer near its boundary. Shape differentiation tells us how that deformation changes the objective. An adjoint calculation avoids solving a separate sensitivity equation for every possible boundary movement.

Here the stochastic structure matters again. Changes in the drift source pair with the adjoint state; changes in the diffusion source involve its martingale component. Treating both regions as if they were deterministic sources would miss this distinction.

The paper establishes existence for the regularized shape problem, derives shape sensitivities under the corresponding smoothness assumptions, and studies a reconstruction method numerically. A descent algorithm's successful examples are not a proof that every initial guess finds the global minimizer.

The idea to retain is **to let the two ways a source enters the equation determine the two ways we reconstruct its geometry**. Extending stability and algorithms to weaker measurements or more difficult shape configurations remains an important direction.

[^paper]: Y. Li, Q. Lü, M. Qian and Y. Wang, *A Geometric Inverse Source Problem for Stochastic Parabolic Equations*. [Preprint](https://arxiv.org/abs/2608.01351). See the inverse problem and uniqueness result, the perimeter-regularized formulation, and the shape-derivative and reconstruction sections. The displayed equation is the zero-lower-order-coefficient model.
