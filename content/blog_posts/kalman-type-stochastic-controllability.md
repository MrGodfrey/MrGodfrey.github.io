---
title: Bringing a Noisy System to Rest Is Different from Reaching Every Random Target
slug: kalman-type-stochastic-controllability
template: paper_post
date: '2026-10-10'
lang: en
math: true
listed: true
excerpt: A finite sequence of subspaces classifies four controllability properties, while the joint diffusion rank separates exact steering from exact return to zero.
kicker: Paper Notes
---

Suppose a controller must bring a system to rest at a prescribed time. Now ask it to meet a target that depends on the entire noise history up to that time. Both are terminal control problems, but randomness makes the second requirement stronger.

Our paper with Qi Lü gives a common algebraic description of these problems for linear stochastic systems with constant coefficients.[^paper] It also shows that, within this class, being able to approach zero arbitrarily closely already guarantees an exact return to zero with finite control energy.

## The same input can affect motion and noise

We consider

$$
dy=(Ay+Bu)\,dt+\sum_{j=1}^{m}(C_jy+D_ju)\,dW^j.
$$

Here $y\in\mathbb R^n$ is the state and $u\in\mathbb R^r$ is the control. The matrices $B$ and $D_j$ describe how the same input enters the drift and the different diffusion channels. The controller uses only information already available from the Brownian motion, and its energy must satisfy

$$
\mathbb E\int_0^T |u(t)|^2\,dt<\infty.
$$

The target may be any square-integrable random vector measurable at time $T$. Although the state has only $n$ coordinates, the space of such targets is infinite-dimensional. This is why approximate reachability does not automatically give exact reachability.

For deterministic constant-coefficient systems, the Kalman rank test settles the familiar terminal steering questions together. In the stochastic setting we distinguish four requirements: approach any random target in mean square, approach zero in mean square, reach zero exactly, and reach every random target exactly. All statements concern every deterministic initial state and a prescribed positive terminal time.

## A scalar example that separates the requirements

Take two independent Brownian motions and three control components:

$$
dy=u_1\,dt+u_2\,dW^1+(u_2+\varepsilon u_3)\,dW^2.
$$

Returning to zero is easy for every value of $\varepsilon$: choose $u_1=-y_0/T$ and $u_2=u_3=0$.

Reaching every random target depends on $\varepsilon$. The joint diffusion-control matrix is the **vertical stack**

$$
\mathcal D=
\begin{pmatrix}
0&1&0\\
0&1&\varepsilon
\end{pmatrix}.
$$

When $\varepsilon\ne0$, its two rows are independent. Given a target $\xi$, write its Brownian martingale representation as

$$
\xi=\mathbb E\xi+\int_0^T Z_1\,dW^1+\int_0^T Z_2\,dW^2.
$$

The choices $u_1=(\mathbb E\xi-y_0)/T$, $u_2=Z_1$, and $u_3=(Z_2-Z_1)/\varepsilon$ reach it exactly with finite energy.

At $\varepsilon=0$, the same input drives both noise channels. Our criterion shows that exact controllability to arbitrary random targets fails, although approximate controllability and exact null controllability still hold. Checking each $D_j$ separately would miss this distinction: both individual rows have full row rank even at $\varepsilon=0$. It is the rank of their vertical stack that matters.

## Find the directions that remain invisible to control

The second ingredient is a subspace $\mathcal V_*$ that records a geometric obstruction. It comes from the adjoint equation: the quantity observed by the control is

$$
B^\top z+\sum_{j=1}^{m}D_j^\top Z_j.
$$

An adjoint motion for which this expression vanishes is invisible to every admissible control. To find directions that can sustain such a motion, start with $\mathcal V_0=\mathbb R^n$. Keep $v\in\mathcal V_k$ at the next step precisely when there are $w_1,\ldots,w_m\in\mathcal V_k$ such that

$$
\begin{cases}
B^\top v+\displaystyle\sum_{j=1}^{m}D_j^\top w_j=0,\\[4pt]
A^\top v+\displaystyle\sum_{j=1}^{m}C_j^\top w_j\in\mathcal V_k.
\end{cases}
$$

The first condition makes the observation vanish. The second keeps the adjoint drift inside the surviving subspace; the requirement $w_j\in\mathcal V_k$ does the same for its noise directions.

These subspaces decrease. Every strict change removes at least one dimension, so the sequence stabilizes after at most $n$ steps. Its final value is $\mathcal V_*$.

The classification has only three possible outcomes:

| Geometric obstruction | Joint diffusion rank | What the controls can achieve |
| --- | --- | --- |
| $\mathcal V_*\ne\{0\}$ | Any rank | None of the four properties holds |
| $\mathcal V_*=\{0\}$ | $\operatorname{rank}\mathcal D<mn$ | Approximate control to any random target, approximate null control, and exact null control |
| $\mathcal V_*=\{0\}$ | $\operatorname{rank}\mathcal D=mn$ | All four properties, including exact control to any random target |

The conditions depend only on the coefficient matrices. Once a property holds, it holds at every positive terminal time.

## Why the finite-energy conclusion matters

A sequence of controls can make the terminal error tend to zero while its energy tends to infinity. Thus the equivalence between approximate and exact null controllability needs more than a density argument.

When $\mathcal V_*=\{0\}$, we construct a deterministic time-dependent matrix gain $K_T(t)$ such that the adapted feedback $u(t)=K_T(t)y(t)$ reaches zero at time $T$. For constants $c>0$ and an integer $N\ge1$ depending on the coefficient matrices,

$$
\mathbb E\int_0^T |u(t)|^2\,dt\le cT^{-N}|y_0|^2,
\qquad 0<T\le1.
$$

The gain may grow near the terminal time. The estimate controls the energy of the actual input $K_Ty$, as the state itself contracts. It also quantifies how demanding a shorter steering time can become.

## From a criterion to an input-design test

The paper expresses the codimension of $\mathcal V_*$ as a rank difference of explicit polynomial block matrices in the original coefficients. This gives a finite algebraic test without first changing the control variables.

Those explicit matrices can be large. An equivalent orthogonal elimination algorithm computes the same obstruction using QR and singular value decompositions, with polynomial storage and arithmetic cost. Numerical rank decisions still depend on the scale and tolerance; the scalar example already shows how a small coefficient can change exact controllability.

The complete manuscript includes a two-state, two-noise example with three input configurations. One has a nonzero obstruction. Adding a drift-only input removes that obstruction and permits exact null control. Adding further diffusion inputs makes $\mathcal D$ surjective and permits exact steering to every square-integrable random target. Penalized linear-quadratic computations then show the terminal-error and control-energy behavior of these configurations.

This makes the classification useful before solving a steering problem: first identify which terminal requirements the available inputs can meet, then design a control for the requirement that is actually feasible.

[^paper]: Qi Lü and Yu Wang, *A Unified Kalman-Type Classification of Controllability for Linear Stochastic Systems*, 2026. [Complete manuscript (PDF)](/files/kalman-type-stochastic-controllability.pdf). The paper contains the geometric classification, the finite-energy feedback construction, rank criteria, and the orthogonal elimination algorithm with numerical comparisons.
