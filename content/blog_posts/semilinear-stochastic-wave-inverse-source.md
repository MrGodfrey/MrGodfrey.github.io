---
title: Reconstructing the Pluck from a Noisy Wave
slug: semilinear-stochastic-wave-inverse-source
template: paper_post
date: '2026-09-24'
lang: en
math: true
listed: true
excerpt: A weighted iteration turns an unknown initial disturbance into a sequence of simpler reconstruction problems.
kicker: Paper Notes
cover:
  image: /img/blog/semilinear-stochastic-wave-inverse-source.webp
  alt: An elegant blue vibrating string carries faint ghost profiles of an earlier pluck toward small amber boundary
    sensors.
  width: 1600
  height: 900
---

A string is plucked, released from rest, and watched at its boundary. Can we work backward to the shape of the original pluck?

Now add a nonlinear restoring effect and random forcing proportional to the displacement. The boundary trace is no longer a simple replay of the initial profile. Yet the initial disturbance still leaves a recoverable signature.

This is the inverse source problem studied in our paper: the unknown is the **initial displacement**, with initial velocity prescribed to be zero.[^paper] It is not an arbitrary unknown force acting throughout the experiment.

## Why the obvious iteration can fail

Think of a globally Lipschitz nonlinearity such as $F(u)=\sin u$. If a trial wave $w$ were already known, then replacing $\sin u$ by $\sin w$ would leave a linear reconstruction problem.

That suggests an iteration: guess a wave, freeze its nonlinear term, reconstruct a new wave, and repeat.

But simply repeating a linear solver does not ensure that the guesses move closer to the truth. Inverse problems can magnify errors. A small mistake in the frozen nonlinearity may cause a larger mistake in the next reconstructed state.

The key question is not whether the subproblem is linear. It is whether the entire update is a contraction in a useful norm.

## Choose the norm so that the equation helps

The paper builds the reconstruction around a Carleman weight. Instead of treating all space–time errors equally, the weighted objective is arranged so that the wave equation gives a coercive estimate.

Each update solves a regularized quadratic minimization problem with the nonlinearity frozen at the previous iterate. The Carleman estimate controls the new error by a reduced portion of the previous error, plus contributions from measurement noise and regularization.

The stochastic equation is handled in an integrated form. There is no need to pretend that a Brownian path has an ordinary time derivative.

The result is a globally convergent reconstruction iteration under the paper's hypotheses: the argument does not require an initial guess already close to the unknown solution. “Globally” describes this convergence property, not access to arbitrary sources from arbitrary sensors.

## Convergence does not mean ignoring the noise

The data include boundary displacement and the specified normal-derivative observations. With imperfect data and a nonzero regularization parameter, the error estimate has an accuracy floor. Iterating longer contracts the initial-guess error; it does not make those other errors vanish by magic.

This distinction is useful in practice. An algorithm should stop because it has extracted the available information, not because it has learned to fit every fluctuation.

The mechanism to remember is **freeze, solve, contract**. The nonlinear problem becomes approachable not by assuming that the nonlinearity is negligible, but by choosing a weighted reconstruction in which its effect can be controlled from one iteration to the next.

Extending the same strategy beyond the stated Lipschitz and observation assumptions remains a separate problem.

[^paper]: Qi Lü and Yu Wang, *An Inverse Source Problem for Semilinear Stochastic Hyperbolic Equations*, Inverse Problems 41 (2025), 115014. [Paper](https://doi.org/10.1088/1361-6420/ae1da0) · [Author version](https://arxiv.org/abs/2504.17398). See problem (1.2), Problem 1 and Theorem 3.2 for the reconstruction and its error estimate.
