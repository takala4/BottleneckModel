# Departure time choice problem

The modeling and analysis of rush-hour traffic congestion has a rich history, 
dating back tothe seminal work of Vickrey (1969). In the basic model proposed by Vickrey, 
it is assumed that afixed number of commuters with homogeneous preferences wish to arrive at a single destination(workplace) at the same preferred time, traveling through a single route that has a bottleneckof a fixed capacity. 
Each commuter chooses the departure time of his/her trip from home tominimize his/her generalized trip cost, 
including trip time, queuing delay at the bottleneck andschedule delay (i.e., costs of arriving early or late at their destination). The problem is to deter-mine a dynamic equilibrium distribution of departure times for which no commuter can reducehis/her generalized cost by changing his/her departure time unilaterally.

## References

* Vickrey
* New look

## Model and Framework

### Parameters

* 総需要：$Q$
* 希望到着時刻：$t^{\ast}$
* 目的地到着時刻：$t$
* スケジュールコスト：$s(t;t^{\ast}) = s(t)$
* 自由流走行時間：$d$
* ボトルネック容量：$\mu$


### Variables

* 到着流出フロー：$q(t)$
* ボトルネック流入フロー：$\lambda(t)$
* 累積流出曲線：$D(\sigma(t))$
* 累積流入曲線：$A(\tau(t))$
* 待ち行列遅れ時間：$w(t)$
* 均衡コスト：$\rho$


$$
t = \tau(t) + w(t) + d
\\
\sigma = \tau(t) + w(t)
$$


## Dynamic system optimal : DSO

### Objective function

$$
\sum_{k \in \ClK} \int_{\ClT} q^{k}(t) s^{k}(t) \mathrm{d} t
$$


### OD cnsv


$$
\int_{\mathcal{T}} q(t) \mathrm{d} t = Q
$$


### Capacity constraint


$$
&\sum_{k \in \ClK} q^{k}(t) = \mu \quad \Rightarrow \quad p(t) > 0
\\\\
&\sum_{k \in \ClK} q^{k}(t) < \mu \quad \Rightarrow \quad p(t) = 0
$$



## Dynamic user equilibrium : DUE


### Departure time choice condition

誰もが出発時刻変更のインセンティブを持たない状態である．

$$
 \mu(t) > 0 \quad \Rightarrow \quad d + w(t) + s(t) = \rho 
  \\
 \mu(t) = 0 \quad \Rightarrow \quad d + w(t) + s(t) \geq \rho
$$



### OD cnsv

配分対象時間帯においてOD需要は保存される：

$$
\int_{\mathcal{T}} q(t) \mathrm{d} t = Q
$$

均衡コスト変数$\rho$と併せて，
相補性条件の形で記述する：

$$
\int_{\mathcal{T}} q(t) \mathrm{d} t = Q
\quad \Rightarrow \quad
\rho > 0
\\
\int_{\mathcal{T}} q(t) \mathrm{d} t < Q
\quad \Rightarrow \quad
\rho = 0
$$


### Bottleneck


$$
q(t) = \mu \quad \Rightarrow \quad w(t) > 0
\\
q(t) < \mu \quad \Rightarrow \quad w(t) = 0
$$


### LCP

find $q(t), w(t), \rho$

such that.

\begin{align}
&0 \leq - \rho  + d + w(t) + s(t) \perp q(t) \geq 0 \quad \forall t
\\\\
&0 \leq - \int q(t) \mathrm{d} t  + Q \perp \rho \geq 0 
\\\\
&0 \leq - q(t-d) + \mu \perp w(t) \geq 0 \quad \forall t
\end{align}



## Solving method and algorithm

This package solves DSO and DUE as LP and QP, respectively.