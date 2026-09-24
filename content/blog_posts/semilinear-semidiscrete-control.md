---
title: Making Nonlinear Control an Iteration
slug: semilinear-semidiscrete-control
template: paper_post
date: '2026-09-24'
lang: en
math: true
listed: true
excerpt: The right estimates make successive controlled trajectories move toward each other—even on a stochastic
  grid.
kicker: Paper Notes
cover:
  image: /img/blog/semilinear-semidiscrete-control.webp
  alt: Three fine blue and teal curves on discrete nodes move progressively toward a common flat profile, with a
    small amber control patch.
  width: 1600
  height: 900
---

Suppose a row of temperatures is evolving on a grid. You can act on a few of the grid points, but the dynamics also contain a nonlinear reaction and random forcing.

For a linear equation, one can design a control from an observability estimate. For a nonlinear equation, the trajectory we want to control also appears inside the coefficients of the problem we need to solve.

This circular dependence suggests an iteration. Whether that iteration converges is the real issue.[^paper]

## Start with a friendly nonlinearity

A useful model is

$$
dy_h=\bigl(D_h^2y_h+\sin y_h+\mathbf1_Gu_h\bigr)dt
     +\bigl(\sigma y_h+v_h\bigr)dW_t.
$$

Here $D_h^2$ is the discrete Laplacian. The drift control acts on the selected grid region; the diffusion control is a separate channel. The choice $\sin y$ keeps the example genuinely nonlinear while retaining a global Lipschitz bound.

Given a trial trajectory $w_h$, freeze the nonlinear reaction at $\sin w_h$ and solve the resulting controlled linear problem. Call the new trajectory $\mathcal T(w_h)$.

A fixed point of $\mathcal T$ is a trajectory whose frozen reaction was already the correct one. It solves the nonlinear controlled equation.

## The missing ingredient is a contraction

A fixed-point diagram is not a proof. We need two nearby trials to produce even closer outputs.

The paper obtains this through a discrete stochastic Carleman estimate with carefully tracked parameters. The resulting weighted control and solution estimates give the small factor needed to dominate the Lipschitz difference

$$
|\sin a-\sin b|\le |a-b|.
$$

The weight parameter cannot be chosen without regard to the mesh: a rapidly changing weight must still be resolved by the grid. Keeping those constraints compatible is what allows the linear estimate and the nonlinear iteration to work together.

Randomness matters here even though the spatial grid is finite. A process on finitely many nodes can still depend on an infinite collection of random outcomes; the usual spatial compactness intuition does not settle the stochastic fixed-point problem.

## What the iteration delivers

For sufficiently fine meshes, the theorem produces controls with a mesh-uniform energy bound and an exponentially small terminal residual, of the form $e^{-c/h}$ in the squared-state estimate.

This is $\phi$-null controllability: the allowed terminal error shrinks as the mesh is refined. It should not be confused with exact zero at a fixed mesh, nor with approximate controllability to an arbitrary random target.

The useful idea is that **nonlinear controllability can be organized as an iteration of controlled linear problems—provided the estimates make that iteration contract**. The estimates are not an afterthought to the algorithm; they are what makes the algorithm possible.

Locally Lipschitz reactions with stronger growth, or exact terminal cancellation with uniform mesh cost, require additional arguments beyond this result.

[^paper]: Yu Wang and Qingmei Zhao, *The ϕ-null controllability for semi-discrete stochastic semilinear parabolic equations*, ESAIM: COCV 31 (2025), 98. [Paper](https://doi.org/10.1051/cocv/2025082) · [Author version](https://arxiv.org/abs/2503.06440). See the controlled semilinear system, assumptions (A1)–(A5), Theorem 1.1 and the contraction construction.
