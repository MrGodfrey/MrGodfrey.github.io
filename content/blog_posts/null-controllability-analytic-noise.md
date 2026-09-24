---
title: "Why One Control Can Be Enough for a Stochastic Heat Equation"
slug: "null-controllability-analytic-noise"
template: "paper_post"
date: 2026-09-24
lang: en
math: true
listed: true
cover:
  image: "/img/blog/null-controllability-analytic-noise.png"
  alt: "A noisy blue wave settles to zero while local control acts on the highlighted region G."
  width: 1672
  height: 941
---

Can we bring a temperature profile exactly to zero when its evolution is subject to noise—and our control acts only on a small part of the domain?

For a deterministic heat equation, this is a familiar control problem. With space-dependent multiplicative noise, an extra unknown appears in the equation used to design the control. The usual arguments struggle to get rid of it.

Our paper finds a way through when the noise coefficient is spatially analytic. The mechanism involves two exponentials: one in space, to handle frequency mixing, and one in time, to close an energy estimate.[^paper]

## A small example with the real difficulty

Consider the stochastic heat equation on a circle,

$$
dy=(y_{xx}+\mathbf 1_Gu)\,dt+\cos x\,y\,dW_t,
\qquad x\in\mathbb T=\mathbb R/(2\pi\mathbb Z).
$$

Here $G$ is a nonempty arc, and $u$ can use only the information available up to the current time. Can this one drift control drive every square-integrable initial profile to $y(T)=0$ at a prescribed time $T>0$—almost surely, not merely on average?

The answer is yes. The choice $b(x)=\cos x$ is simple, but it already contains the obstacle created by spatial dependence.

## Where the familiar arguments get stuck

Duality turns the control problem into an observation problem for the backward equation

$$
dz=-(z_{xx}+\cos x\,Z)\,dt+Z\,dW_t.
$$

There are two unknowns: the state $z$ and the martingale integrand $Z$. A single drift control requires an estimate using only observations of $z$ on $G$.

The usual stochastic Carleman estimates leave a term involving $Z$ on the observation side. A second control acting in the diffusion can account for it, but that changes the problem.

Spectral arguments face a different obstruction. A spatially constant coefficient preserves each Fourier mode. Multiplication by $\cos x$ does not:

$$
\cos x\,e^{ikx}
=\tfrac12e^{i(k+1)x}+\tfrac12e^{i(k-1)x}.
$$

A mode just outside a spectral cutoff can therefore feed into the retained modes through $Z$. The low-frequency equation no longer closes as it did for spatially constant noise.

So the difficulty is not simply that noise produces oscillations. It is that **spatial mixing brings an unobserved unknown into the frequencies we are trying to estimate.**

## The first exponential: look at mixing in a different norm

Analyticity does not stop modes from moving. It makes their movement manageable under exponential Fourier weights.

Write $D=-i\partial_x$. The operator $e^{\sigma D}$ multiplies the $k$th Fourier mode by $e^{\sigma k}$, which is exactly what happens under the complex translation $x\mapsto x-i\sigma$.

To see the mechanism, work with finite Fourier approximations and leave the projections implicit. Set $X=e^{\sigma D}z$ and $Y=e^{\sigma D}Z$. Then the coupling transforms as

$$
e^{\sigma D}(bZ)=b_\sigma Y,
\qquad
b_\sigma(x)=\cos(x-i\sigma),
\qquad
|b_\sigma(x)|\le\cosh\rho
\quad (|\sigma|\le\rho).
$$

The weighted $Y$ may be enormous. What matters is that the coupling is still **a bounded coefficient times that same $Y$**.

For a general periodic analytic coefficient, the Fourier picture is equally suggestive: the transfer from frequency $k$ to frequency $m$ has coefficient $\widehat b(m-k)$, with an exponentially decaying bound in $|m-k|$. The cosine example only transfers between neighboring modes.

There is one more choice that makes the argument work. On a time interval $[t,s]$, let

$$
\sigma(r)=\rho\frac{s-r}{s-t}.
$$

At the earlier time $t$, we measure an exponentially weighted spatial norm. At $s$, the translation has vanished. Thus the estimate can start from ordinary $L^2$ terminal data: no terminal analyticity is needed.

## The second exponential: what to do with the negative remainder

Apply Itô's formula to $\|X\|^2$. Its quadratic-variation term supplies $+\|Y\|^2$, which pairs with the coupling in an exact identity:

$$
\|Y\|^2-2\operatorname{Re}\langle X,b_\sigma Y\rangle
=
\|Y-\overline{b_\sigma}X\|^2-\|b_\sigma X\|^2.
$$

All norms here are spatial $L^2$ norms. The unknown $Y$ now sits inside a nonnegative square. But there is a negative remainder. Have we merely exchanged one problem for another?

The crucial difference is that the remainder contains **only the state**:

$$
-\|b_\sigma X\|^2\ge-\cosh^2\rho\,\|X\|^2.
$$

The moving translation also creates a first-order term. Pairing it with the Laplacian's energy leaves another state-only loss, $-\tfrac12|\sigma'|^2\|X\|^2$. Altogether,

$$
d\|X\|^2\ge-a\|X\|^2\,dr+dM_r,
\qquad
a=\cosh^2\rho+\frac{\rho^2}{2(s-t)^2},
$$

where the martingale term disappears after taking expectations.

Now multiply by the time weight $\Gamma(r)=e^{a(r-t)}$. Its derivative supplies exactly the term needed to compensate for the negative remainder. Integrating and taking expectations gives

$$
\mathbb E\|e^{\rho D}z(t)\|^2
\le e^{a(s-t)}\mathbb E\|z(s)\|^2.
$$

Repeating the calculation with the opposite translation controls both signs of the Fourier frequencies. Passing from the finite approximations to the limit gives quantitative spatial analyticity of $z(t)$, without assuming spatial analyticity of $Z$.

The two exponentials have distinct jobs: **the spatial one preserves a usable coupling structure; the temporal one compensates for the losses left by completing the squares.**

## From analytic smoothing to one control

At a fixed time, view $x\mapsto z(t,x)$ as an analytic function taking values in $L^2(\Omega)$. Propagation of smallness converts its local observation on $G$, together with its global analytic bound, into control of the whole spatial norm. The Hilbert-valued estimate follows by applying the scalar estimate to inner products with unit vectors.

A geometric time subdivision and a telescoping sum then remove the intermediate global norms, leaving

$$
\|z(0)\|_{L^2(\mathbb T)}
\le C\int_0^T
\left(\mathbb E\|z(t)\|_{L^2(G)}^2\right)^{1/2}\,dt.
$$

Only $z$ appears on the right. This is precisely the dual estimate needed for a single adapted drift control.

The full result allows higher-dimensional tori, any measurable spatial control set of positive measure, and coefficients depending jointly on time, space, and the sample point. Their holomorphic extensions must share a positive strip width, and the squared analytic norms must have a pathwise uniform time-integral bound. That last condition keeps the corresponding time exponential under control.

Beyond this setting, two obstacles remain for the method: general smooth coefficients need not admit complex translations, and translations need not preserve boundary conditions. These are limits of the argument, not proofs that one control must fail.

The central idea is to make the unobserved term disappear from the estimate—not by assuming it is small, but by putting it into a form that the equation's own quadratic variation can handle, and then paying for the remaining state terms with a time weight.

---

[^paper]: Qi Lü and Yu Wang, *Null Controllability of a Stochastic Parabolic Equation with a Space-Dependent Analytic Noise Coefficient*, manuscript. This post presents a one-dimensional example of the proof mechanism. See Section 2 for the analytic energy estimate, Sections 3–4 for propagation of smallness, telescoping, and duality, and Section 6 for the scope of the method.
