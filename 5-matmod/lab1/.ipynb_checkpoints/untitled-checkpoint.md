and weights / coefs $a = \begin{pmatrix} a_0 \\ a_1 \end{pmatrix}$ or $a = \begin{pmatrix} a_0 \\ a_1 \\ a_2 \end{pmatrix}$

Then we want to minimize an scalar error $E = $ ``(r*r).sum()`` where $r_i = y_i - f(x_i, \vec a)$

This can be done by finding where 
$\vec\nabla E = 0$. That is, 
$$
\frac{\partial E}{\partial a_j} = 2 \sum_i E_i \frac{\partial E_i}{\partial a_j} = 0 $$