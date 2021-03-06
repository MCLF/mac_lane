# -*- coding: utf-8 -*-
r"""
Augmented valuations on polynomial rings

Implements augmentations of valutions as defined in [ML1936].

Starting from a :class:`GaussValuation`, we can create augmented valuations on
polynomial rings::

    sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
    sage: R.<x> = QQ[]
    sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
    sage: w = v.augmentation(x, 1); w
    [ Gauss valuation induced by 2-adic valuation, v(x) = 1 ]
    sage: w(x)
    1

This also works for polynomial rings over base rings which are not fields.
However, much of the functionality is only available over fields::

    sage: R.<x> = ZZ[]
    sage: v = GaussValuation(R, pAdicValuation(ZZ, 2))
    sage: w = v.augmentation(x, 1); w
    [ Gauss valuation induced by 2-adic valuation, v(x) = 1 ]
    sage: w(x)
    1

TESTS::

    sage: R.<x> = QQ[]
    sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
    sage: w = v.augmentation(x, 1)
    sage: TestSuite(w).run() # long time

    sage: w = v.augmentation(x, 2)
    sage: TestSuite(w).run() # long time

Run the test suite for a valuation with a residual extension::

    sage: R.<x> = QQ[]
    sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
    sage: w = v.augmentation(x^2 + x + 1, 1)
    sage: TestSuite(w).run() # long time

Run the test suite for an iterated residual extension starting from a
non-prime residue field::

    sage: R.<u> = Qq(4, 40)
    sage: S.<x> = R[]
    sage: v = GaussValuation(S)
    sage: w = v.augmentation(x^2 + x + u, 1/2)
    sage: TestSuite(w).run() # long time

    sage: ww = w.augmentation(x^8 + 4*x^7 + 2*x^6 + 2*x^5 + x^4 + 2*x^3 + 4*(u + 1)*x^2 + 6*(u + 1)*x + 4 + 3*u, 10)
    sage: TestSuite(ww).run() # long time

Run the test suite for an augmentation of a ramified augmentation::

    sage: R.<u> = Qq(4, 5)
    sage: S.<x> = R[]
    sage: v = GaussValuation(S)
    sage: w = v.augmentation(x, 3/4)
    sage: TestSuite(w).run() # long time

    sage: ww = w.augmentation(x^4 + 8, 5)
    sage: TestSuite(ww).run() # long time

Run the test suite for a ramified augmentation of an unramified augmentation::

    sage: R.<x> = QQ[]
    sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
    sage: w = v.augmentation(x^2 + x + 1, 1)
    sage: TestSuite(w).run() # long time

    sage: ww = w.augmentation(x^4 + 2*x^3 + 5*x^2 + 8*x + 3, 16/3)
    sage: TestSuite(ww).run() # long time

Run the test suite for a ramified augmentation of a ramified augmentation::

    sage: R.<u> = Qq(4, 20)
    sage: S.<x> = R[]
    sage: v = GaussValuation(S)
    sage: w = v.augmentation(x^2 + x + u, 1/2)
    sage: TestSuite(w).run() # long time

    sage: ww = w.augmentation((x^2 + x + u)^2 + 2, 5/3)
    sage: TestSuite(ww).run() # long time

Run the test suite for another augmentation with iterated residue field extensions::

    sage: R.<u> = Qq(4, 10)
    sage: S.<x> = R[]
    sage: v = GaussValuation(S)
    sage: w = v.augmentation(x^2 + x + u, 1)
    sage: TestSuite(w).run() # long time

    sage: ww = w.augmentation((x^2 + x + u)^2 + 2*x*(x^2 + x + u) + 4*x, 3)
    sage: TestSuite(ww).run() # long time

Run the test suite for a rather trivial pseudo-valuation::

    sage: R.<u> = Qq(4, 5)
    sage: S.<x> = R[]
    sage: v = GaussValuation(S)
    sage: w = v.augmentation(x, infinity)
    sage: TestSuite(w).run() # long time

Run the test suite for an infinite valuation which extends the residue field::

    sage: R.<u> = Qq(4, 5)
    sage: S.<x> = R[]
    sage: v = GaussValuation(S)
    sage: w = v.augmentation(x^2 + x + u, infinity)
    sage: TestSuite(w).run() # long time

Run the test suite for an infinite valuation which extends a valuation which
extends the residue field::

    sage: R.<u> = Qq(4, 5)
    sage: S.<x> = R[]
    sage: v = GaussValuation(S)
    sage: w = v.augmentation(x^2 + x + u, 1/2)
    sage: TestSuite(w).run() # long time

    sage: ww = w.augmentation((x^2 + x + u)^2 + 2, infinity)
    sage: TestSuite(ww).run() # long time

Run the test suite if the polynomial ring is not over a field::

    sage: R.<x> = ZZ[]
    sage: v = GaussValuation(R, pAdicValuation(ZZ, 2))
    sage: w = v.augmentation(x, 1)
    sage: TestSuite(w).run() # long time

REFERENCES:

.. [ML1936] Mac Lane, S. (1936). A construction for prime ideals as absolute
values of an algebraic field. Duke Mathematical Journal, 2(3), 492-510.

.. [ML1936'] MacLane, S. (1936). A construction for absolute values in
polynomial rings. Transactions of the American Mathematical Society, 40(3),
363-395.

AUTHORS:

- Julian Rüth (2013-04-15): initial version

"""
#*****************************************************************************
#       Copyright (C) 2013-2016 Julian Rüth <julian.rueth@fsfe.org>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************
from inductive_valuation import _lift_to_maximal_precision
from inductive_valuation import FinalInductiveValuation, NonFinalInductiveValuation, FiniteInductiveValuation, InfiniteInductiveValuation, InductiveValuation
from valuation import InfiniteDiscretePseudoValuation, DiscreteValuation

from sage.misc.cachefunc import cached_method
from sage.rings.all import infinity, QQ, ZZ
from sage.structure.factory import UniqueFactory

class AugmentedValuationFactory(UniqueFactory):
    r"""
    Factory for augmented valuations.

    EXAMPLES:

    This factory is not meant to be called directly. Instead,
    :meth:`augmentation` of a valuation should be called::

        sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
        sage: R.<x> = QQ[]
        sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
        sage: w = v.augmentation(x, 1) # indirect doctest

    Note that trivial parts of the augmented valuation might be dropped, so you
    should not rely on ``_base_valuation`` to be the valuation you started
    with::

        sage: ww = w.augmentation(x, 2)
        sage: ww._base_valuation is v
        True

    """
    def create_key(self, base_valuation, phi, mu, check=True):
        r"""
        Create a key which uniquely identifies the valuation over
        ``base_valuation`` which sends ``phi`` to ``mu``.

        .. NOTE::

            The uniqueness that this factory provides is not why we chose to
            use a factory.  However, it makes pickling and equality checks much
            easier. At the same time, going through a factory makes it easier
            to enforce that all instances correctly inherit methods from the
            parent Hom space.

        TESTS::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
            sage: w = v.augmentation(x, 1) # indirect doctest
            sage: ww = v.augmentation(x, 1)
            sage: w is ww
            True

        """
        if check:
            is_key, reason = base_valuation.is_key(phi, explain=True)
            if not is_key:
                raise ValueError(reason)
            if mu <= base_valuation(phi):
                raise ValueError("the value of the key polynomial must strictly increase but `%s` does not exceed `%s`."%(mu, base_valuation(phi)))
            if not isinstance(base_valuation, InductiveValuation):
                raise TypeError("base_valuation must be inductive")

        phi = base_valuation.domain().coerce(phi)
        if mu is not infinity:
            mu = QQ(mu)

        if isinstance(base_valuation, AugmentedValuation_base):
            if phi.degree() == base_valuation.phi().degree():
                # drop base_valuation and extend base_valuation._base_valuation instead
                return self.create_key(base_valuation._base_valuation, phi, mu, check=check)

        return base_valuation, phi, mu

    def create_object(self, version, key):
        r"""
        Create the augmented valuation represented by ``key``.

        TESTS::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
            sage: w = v.augmentation(x^2 + x + 1, 1) # indirect doctest

        """
        base_valuation, phi, mu = key

        from valuation_space import DiscretePseudoValuationSpace
        parent = DiscretePseudoValuationSpace(base_valuation.domain())
        if mu is not infinity:
            if base_valuation.is_trivial():
                return parent.__make_element_class__(FinalFiniteAugmentedValuation)(parent, base_valuation, phi, mu)
            else:
                return parent.__make_element_class__(NonFinalFiniteAugmentedValuation)(parent, base_valuation, phi, mu)
        else:
            return parent.__make_element_class__(InfiniteAugmentedValuation)(parent, base_valuation, phi, mu)

AugmentedValuation = AugmentedValuationFactory("AugmentedValuation")

class AugmentedValuation_base(InductiveValuation):
    """
    An augmented valuation is a discrete valuation on a polynomial ring. It
    extends another discrete valuation `v` by setting the valuation of a
    polynomial `f` to the minumum of `v(f_i)i\mu` when writing `f=\sum_i
    f_i\phi^i`.

    INPUT:

    - ``v`` -- a :class:`InductiveValuation` on a polynomial ring

    - ``phi`` -- a key polynomial over ``v`` (see :meth:`is_key`)

    - ``mu`` -- a rational number such that ``mu > v(phi)`` or ``infinity``

    EXAMPLES::

        sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
        sage: K.<u> = CyclotomicField(5)
        sage: R.<x> = K[]
        sage: v = GaussValuation(R, pAdicValuation(K, 2))
        sage: w = v.augmentation(x, 1/2); w # indirect doctest
        [ Gauss valuation induced by 2-adic valuation, v(x) = 1/2 ]
        sage: ww = w.augmentation(x^4 + 2*x^2 + 4*u, 3); ww
        [ Gauss valuation induced by 2-adic valuation, v(x) = 1/2, v(x^4 + 2*x^2 + 4*u) = 3 ]

    TESTS::

        sage: TestSuite(w).run() # long time
        sage: TestSuite(ww).run() # long time

    """
    def __init__(self, parent, v, phi, mu):
        """
        TESTS::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: K.<u> = Qq(4, 5)
            sage: R.<x> = K[]
            sage: v = GaussValuation(R)
            sage: w = AugmentedValuation(v, x, 1/2)
            sage: isinstance(w, AugmentedValuation_base)
            True

            sage: TestSuite(w).run() # long time

        """
        InductiveValuation.__init__(self, parent, phi)

        self._base_valuation = v
        self._mu = mu

    @cached_method
    def equivalence_unit(self, s, reciprocal=False):
        """
        Return an equivalence unit of minimal degree and valuation ``s``.

        INPUT:

        - ``s`` -- a rational number

        - ``reciprocal`` -- a boolean (default: ``False``); whether or not to
          return the equivalence unit as the :meth:`equivalence_reciprocal` of
          the equivalence unit of valuation ``-s``.

        OUTPUT:

        A polynomial in the domain of this valuation which
        :meth:`is_equivalence_unit` for this valuation.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 5)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)
            sage: w = v.augmentation(x^2 + x + u, 1)

            sage: w.equivalence_unit(0)
            1 + O(2^5)
            sage: w.equivalence_unit(-4)
            2^-4 + O(2)

        Since an equivalence unit is of effective degree zero, `\phi` must not
        divide it. Therefore, its valuation is in the value group of the base
        valuation::

            sage: w = v.augmentation(x, 1/2)

            sage: w.equivalence_unit(3/2)
            Traceback (most recent call last):
            ...
            ValueError: 3/2 is not in the value semigroup of 2-adic valuation
            sage: w.equivalence_unit(1)
            2 + O(2^6)

        An equivalence unit might not be integral, even if ``s >= 0``::

            sage: w = v.augmentation(x, 3/4)
            sage: ww = w.augmentation(x^4 + 8, 5)

            sage: ww.equivalence_unit(1/2)
            (2^-1 + O(2^4))*x^2

        """
        if reciprocal:
            ret = self._base_valuation.element_with_valuation(s)
            residue = self.reduce(ret*self._base_valuation.element_with_valuation(-s), check=False)
            assert residue.is_constant()
            ret *= self.lift(~(residue[0]))
            #ret = self.equivalence_reciprocal(self.equivalence_unit(-s))
        else:
            ret = self._base_valuation.element_with_valuation(s)

        assert self.is_equivalence_unit(ret)
        assert self(ret) == s
        return ret

    @cached_method
    def element_with_valuation(self, s):
        """
        Create an element of minimal degree and of valuation ``s``.

        INPUT:

        - ``s`` -- a rational number in the value group of this valuation

        OUTPUT:

        An element in the domain of this valuation

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 5)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)
            sage: w = v.augmentation(x^2 + x + u, 1/2)
            sage: w.element_with_valuation(0)
            1 + O(2^5)
            sage: w.element_with_valuation(1/2)
            (1 + O(2^5))*x^2 + (1 + O(2^5))*x + u + O(2^5)
            sage: w.element_with_valuation(1)
            2 + O(2^6)
            sage: c = w.element_with_valuation(-1/2); c
            (2^-1 + O(2^4))*x^2 + (2^-1 + O(2^4))*x + u*2^-1 + O(2^4)
            sage: w(c)
            -1/2
            sage: w.element_with_valuation(1/3)
            Traceback (most recent call last):
            ...
            ValueError: s must be in the value group of the valuation but 1/3 is not in Additive Abelian Group generated by 1/2.

        """
        if s not in self.value_group():
            raise ValueError("s must be in the value group of the valuation but %r is not in %r."%(s, self.value_group()))
        error = s

        ret = self.domain().one()
        while s not in self._base_valuation.value_group():
            ret *= self._phi
            s -= self._mu
        ret = ret * self._base_valuation.element_with_valuation(s)
        return self.simplify(ret, error=error)

    def _repr_(self):
        """
        Return a printable representation of this valuation.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 5)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)
            sage: w = v.augmentation(x^2 + x + u, 1/2)
            sage: w # indirect doctest
            [ Gauss valuation induced by 2-adic valuation, v((1 + O(2^5))*x^2 + (1 + O(2^5))*x + u + O(2^5)) = 1/2 ]

        """
        vals = self.augmentation_chain()
        vals.reverse()
        vals = [ "v(%s) = %s"%(v._phi, v._mu) if isinstance(v, AugmentedValuation_base) else str(v) for v in vals ]
        return "[ %s ]"%", ".join(vals)

    def augmentation_chain(self):
        r"""
        Return a list with the chain of augmentations down to the underlying
        :class:`GaussValuation`.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
            sage: w = v.augmentation(x, 1)
            sage: w.augmentation_chain()
            [[ Gauss valuation induced by 2-adic valuation, v(x) = 1 ],
                 Gauss valuation induced by 2-adic valuation]

        For performance reasons, (and to simplify the underlying
        implementation,) trivial augmentations might get dropped. You should
        not rely on :meth:`augmentation_chain` to contain all the steps that
        you specified to create the current valuation::

            sage: ww = w.augmentation(x, 2)
            sage: ww.augmentation_chain()
            [[ Gauss valuation induced by 2-adic valuation, v(x) = 2 ],
                 Gauss valuation induced by 2-adic valuation]

        """
        return [self] + self._base_valuation.augmentation_chain()

    @cached_method
    def psi(self):
        """
        Return the minimal polynomial of the residue field extension of this valuation.

        OUTPUT:

        A polynomial in the residue ring of the base valuation

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 5)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)

            sage: w = v.augmentation(x^2 + x + u, 1/2)
            sage: w.psi()
            x^2 + x + u0

            sage: ww = w.augmentation((x^2 + x + u)^2 + 2, 5/3)
            sage: ww.psi()
            x + 1

        """
        R = self._base_valuation.equivalence_unit(-self._base_valuation(self._phi))
        F = self._base_valuation.reduce(self._phi*R, check=False).monic()
        assert F.is_irreducible()
        return F

    @cached_method
    def E(self):
        """
        Return the ramification index of this valuation over its underlying
        Gauss valuation.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 5)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)

            sage: w = v.augmentation(x^2 + x + u, 1)
            sage: w.E()
            1

            sage: w = v.augmentation(x, 1/2)
            sage: w.E()
            2

        """
        if self.augmentation_chain()[-1].is_trivial():
            raise NotImplementedError("ramification index is not defined over a trivial Gauss valuation")
        return self.value_group().index(self._base_valuation.value_group()) * self._base_valuation.E()

    @cached_method
    def F(self):
        """
        Return the degree of the residue field extension of this valuation
        over the underlying Gauss valuation.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 5)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)

            sage: w = v.augmentation(x^2 + x + u, 1)
            sage: w.F()
            2

            sage: w = v.augmentation(x, 1/2)
            sage: w.F()
            1

        """
        return self.phi().degree() // self._base_valuation.E()

    def extensions(self, ring):
        r"""
        Return the extensions of this valuation to ``ring``.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
            sage: w = v.augmentation(x^2 + x + 1, 1)

            sage: w.extensions(GaussianIntegers().fraction_field()['x'])
            [[ Gauss valuation induced by 2-adic valuation, v(x^2 + x + 1) = 1 ]]
            
        """
        if ring is self.domain():
            return [self]

        from sage.rings.polynomial.polynomial_ring import is_PolynomialRing
        if is_PolynomialRing(ring) and ring.ngens() == 1:
            base_valuations = self._base_valuation.extensions(ring)
            phi = self.phi().change_ring(ring.base_ring())

            ret = []
            for v in base_valuations:
                if v.is_key(phi):
                    ret.append(AugmentedValuation(v, phi, self._mu))
                else:
                    F = v.equivalence_decomposition(phi)
                    mu0 = v(phi)
                    for f,e in F:
                        # We construct a valuation with [v, w(phi) = mu] which should be such that
                        # self(phi) = self._mu, i.e., w(phi) = w(unit) + sum e_i * w(f_i) where
                        # the sum runs over all the factors in the equivalence decomposition of phi
                        # Solving for mu gives
                        mu = (self._mu - v(F.unit()) - sum([ee*v(ff) for ff,ee in F if ff != f])) / e
                        ret.append(AugmentedValuation(v, f, mu))
            return ret

        return super(AugmentedValuation_base, self).extensions(ring)

    def restriction(self, ring):
        r"""
        Return the restriction of this valuation to ``ring``.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: K = GaussianIntegers().fraction_field()
            sage: R.<x> = K[]
            sage: v = GaussValuation(R, pAdicValuation(K, 2))
            sage: w = v.augmentation(x^2 + x + 1, 1)

            sage: w.restriction(QQ['x'])
            [ Gauss valuation induced by 2-adic valuation, v(x^2 + x + 1) = 1 ]

        """
        if ring.is_subring(self.domain()):
            base = self._base_valuation.restriction(ring)
            if ring.is_subring(self.domain().base_ring()):
                return base
            from sage.rings.polynomial.polynomial_ring import is_PolynomialRing
            if is_PolynomialRing(ring) and ring.ngens() == 1:
                return base.augmentation(self.phi().change_ring(ring.base()), self._mu)
        return super(AugmentedValuation_base, self).restriction(ring)

    def uniformizer(self):
        r"""
        Return a uniformizing element for this valuation.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
            sage: w = v.augmentation(x^2 + x + 1, 1)

            sage: w.uniformizer()
            2

        """
        return self.element_with_valuation(self.value_group()._generator)

    def is_gauss_valuation(self):
        r"""
        Return whether this valuation is a Gauss valuation.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
            sage: w = v.augmentation(x^2 + x + 1, 1)

            sage: w.is_gauss_valuation()
            False

        """
        assert(self._mu > 0)
        return False

    def monic_integral_model(self, G):
        r"""
        Return a monic integral irreducible polynomial which defines the same
        extension of the base ring of the domain as the irreducible polynomial
        ``G`` together with maps between the old and the new polynomial.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
            sage: w = v.augmentation(x^2 + x + 1, 1)

            sage: w.monic_integral_model(5*x^2 + 1/2*x + 1/4)
            (Ring endomorphism of Univariate Polynomial Ring in x over Rational Field
               Defn: x |--> 1/2*x,
             Ring endomorphism of Univariate Polynomial Ring in x over Rational Field
               Defn: x |--> 2*x,
            x^2 + 1/5*x + 1/5)

        """
        return self._base_valuation.monic_integral_model(G)
            
    def _ge_(self, other):
        r"""
        Return whether this valuation is greater or equal than ``other``
        everywhere.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
            sage: w = v.augmentation(x^2 + x + 1, 1)
            sage: w >= v
            True
            sage: ww = v.augmentation(x^2 + x + 1, 2)
            sage: ww >= w
            True
            sage: www = w.augmentation(x^4 + 2*x^3 + 5*x^2 + 8*x + 3, 16/3)
            sage: www >= w
            True
            sage: www >= ww
            False

        """
        from gauss_valuation import GaussValuation_generic
        if other.is_trivial():
            return other.is_discrete_valuation()
        if isinstance(other, GaussValuation_generic):
            return self._base_valuation >= other
        if isinstance(other, AugmentedValuation_base):
            if self(other._phi) >= other._mu:
                return self >= other._base_valuation
            else:
                return False

        return super(AugmentedValuation_base, self)._ge_(other)

    def is_trivial(self):
        r"""
        Return whether this valuation is trivial, i.e., zero outside of zero.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
            sage: w = v.augmentation(x^2 + x + 1, 1)
            sage: w.is_trivial()
            False

        """
        # We need to override the default implementation from valuation_space
        # because that one uses uniformizer() which might not be implemented if
        # the base ring is not a field.
        return False

    def scale(self, scalar):
        r"""
        Return this valuation scaled by ``scalar``.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
            sage: w = v.augmentation(x^2 + x + 1, 1)
            sage: 3*w # indirect doctest
            [ Gauss valuation induced by 3 * 2-adic valuation, v(x^2 + x + 1) = 3 ]

        """
        if scalar in QQ and scalar > 0 and scalar != 1:
            return self._base_valuation.scale(scalar).augmentation(self.phi(), scalar*self._mu)
        return super(AugmentedValuation_base, self).scale(scalar)

    def _residue_ring_generator_name(self):
        r"""
        Return a name for a generator of the residue ring.

        This method is used by :meth:`residue_ring` to work around name clashes
        with names in subrings of the residue ring.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
            sage: w = v.augmentation(x^2 + x + 1, 1)
            sage: w._residue_ring_generator_name()
            'u1'
            
        """
        base = self._base_valuation.residue_ring().base()
        # we need a name for a generator that is not present already in base
        generator = 'u' + str(len(self.augmentation_chain()) - 1)
        while True:
            try:
                base(generator)
                generator = 'u' + generator
            except NameError:
                # use this name, it has no meaning in base
                return generator
            except TypeError:
                # use this name, base can not handle strings, so hopefully,
                # there are no variable names (such as in QQ or GF(p))
                return generator

    def _relative_size(self, f):
        r"""
        Return an estimate on the coefficient size of ``f``.

        The number returned is an estimate on the factor between the number of
        bits used by ``f`` and the minimal number of bits used by an element
        congruent to ``f``.

        This is used by :meth:`simplify` to decide whether simplification of
        coefficients is going to lead to a significant shrinking of the
        coefficients of ``f``.

        EXAMPLES:: 

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = QQ[]
            sage: K.<u> = QQ.extension(u^2 + u+ 1)
            sage: S.<x> = K[]
            sage: v = GaussValuation(S, pAdicValuation(K, 2))
            sage: w = v.augmentation(x^2 + x + u, 1/2)
            sage: w._relative_size(x^2 + x + 1)
            1
            sage: w._relative_size(1048576*x^2 + 1048576*x + 1048576)
            21

        """
        return self._base_valuation._relative_size(f)

    def is_negative_pseudo_valuation(self):
        r"""
        Return whether this valuation attains `-\infty`.

        EXAMPLES:

        No element in the domain of an augmented valuation can have valuation
        `-\infty`, so this method always returns ``False``::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, TrivialValuation(QQ))
            sage: w = v.augmentation(x, infinity)
            sage: w.is_negative_pseudo_valuation()
            False

        """
        return False

    def change_domain(self, ring):
        r"""
        Return this valuation over ``ring``.

        EXAMPLES:

        We can change the domain of an augmented valuation even if there is no coercion between rings::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = GaussianIntegers()[]
            sage: v = GaussValuation(R, pAdicValuation(GaussianIntegers(), 2))
            sage: v = v.augmentation(x, 1)
            sage: v.change_domain(QQ['x'])
            [ Gauss valuation induced by 2-adic valuation, v(x) = 1 ]

        """
        from sage.rings.polynomial.polynomial_ring import is_PolynomialRing
        if is_PolynomialRing(ring) and ring.ngens() == 1 and ring.variable_name() == self.domain().variable_name():
            return self._base_valuation.change_domain(ring).augmentation(self.phi().change_ring(ring.base_ring()), self._mu, check=False)
        return super(AugmentedValuation_base, self).change_domain(ring)


class FinalAugmentedValuation(AugmentedValuation_base, FinalInductiveValuation):
    r"""
    An augmented valuation which can not be augmented anymore, either because
    it augments a trivial valuation or because it is infinite.

    EXAMPLES::

        sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
        sage: R.<x> = QQ[]
        sage: v = GaussValuation(R, TrivialValuation(QQ))
        sage: w = v.augmentation(x, 1)

    """
    def __init__(self, parent, v, phi, mu):
        r"""
        TESTS::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, TrivialValuation(QQ))
            sage: w = v.augmentation(x, 1)
            sage: isinstance(w, FinalAugmentedValuation)
            True

        """
        AugmentedValuation_base.__init__(self, parent, v, phi, mu)
        FinalInductiveValuation.__init__(self, parent, phi)

    @cached_method
    def residue_ring(self):
        r"""
        Return the residue ring of this valuation, i.e., the elements of
        non-negative valuation modulo the elements of positive valuation.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, TrivialValuation(QQ))

            sage: w = v.augmentation(x, 1)
            sage: w.residue_ring()
            Rational Field

            sage: w = v.augmentation(x^2 + x + 1, infinity)
            sage: w.residue_ring()
            Number Field in u1 with defining polynomial x^2 + x + 1

        An example with a non-trivial base valuation::

            sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
            sage: w = v.augmentation(x^2 + x + 1, infinity)
            sage: w.residue_ring()
            Finite Field in u1 of size 2^2

        Since trivial extensions of finite fields are not implemented, the
        resulting ring might be identical to the residue ring of the underlying
        valuation::

            sage: w = v.augmentation(x, infinity)
            sage: w.residue_ring()
            Finite Field of size 2

        TESTS:

        We avoid clashes in generator names::

            sage: K.<x> = FunctionField(QQ)
            sage: v = FunctionFieldValuation(K, x^2 + 2)
            sage: R.<y> = K[]
            sage: L.<y> = K.extension(y^2 + x^2)
            sage: w = v.extension(L)
            sage: w.residue_field()
            Number Field in uu1 with defining polynomial y^2 - 2 over its base field
            sage: w.residue_field().base_field()
            Number Field in u1 with defining polynomial x^2 + 2

        """
        # the following is correct, even if the polynomial ring is not over a field

        base = self._base_valuation.residue_ring().base()
        if self.psi().degree() > 1:
            generator = self._residue_ring_generator_name()
            return base.extension(self.psi(), names=generator)
        else:
            # Do not call extension() if self.psi().degree() == 1:
            # In that case the resulting field appears to be the same as the original field,
            # however, it is not == to the original field (for finite fields at
            # least) but a distinct copy (this is a bug in finite field's
            # extension() implementation.)
            return base

    def reduce(self, f, check=True, degree_bound=None, coefficients=None, valuations=None):
        r"""
        Reduce ``f`` module this valuation.

        INPUT:

        - ``f`` -- an element in the domain of this valuation

        - ``check`` -- whether or not to check whether ``f`` has non-negative
          valuation (default: ``True``)

        - ``degree_bound`` -- an a-priori known bound on the degree of the
          result which can speed up the computation (default: not set)

        - ``coefficients`` -- the coefficients of ``f`` as produced by
          :meth:`coefficients` or ``None`` (default: ``None``); this can be
          used to speed up the computation when the expansion of ``f`` is
          already known from a previous computation.

        - ``valuations`` -- the valuations of ``coefficients`` or ``None``
          (default: ``None``); ignored

        OUTPUT:

        an element of the :meth:`residue_ring` of this valuation, the reduction
        modulo the ideal of elements of positive valuation

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, TrivialValuation(QQ))

            sage: w = v.augmentation(x, 1)
            sage: w.reduce(x^2 + x + 1)
            1

            sage: w = v.augmentation(x^2 + x + 1, infinity)
            sage: w.reduce(x)
            u1

        TESTS:

        Cases with non-trivial base valuation::

            sage: R.<u> = Qq(4, 10)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)
            sage: v.reduce(x)
            x
            sage: v.reduce(S(u))
            u0

            sage: w = v.augmentation(x^2 + x + u, 1/2)
            sage: w.reduce(S.one())
            1
            sage: w.reduce(S(2))
            0
            sage: w.reduce(S(u))
            u0
            sage: w.reduce(x) # this gives the generator of the residue field extension of w over v
            u1
            sage: f = (x^2 + x + u)^2 / 2
            sage: w.reduce(f)
            x
            sage: w.reduce(f + x + 1)
            x + u1 + 1

            sage: ww = w.augmentation((x^2 + x + u)^2 + 2, 5/3)
            sage: g = ((x^2 + x + u)^2 + 2)^3 / 2^5
            sage: ww.reduce(g)
            x
            sage: ww.reduce(f)
            1
            sage: ww.is_equivalent(f, 1)
            True
            sage: ww.reduce(f * g)
            x
            sage: ww.reduce(f + g)
            x + 1

        """
        f = self.domain().coerce(f)

        if check:
            v = self(f)
            if v < 0:
                raise ValueError("f must have non-negative valuation")
            elif v > 0:
                return self.residue_ring().zero()

        if coefficients is None:
            constant_term = self.coefficients(f).next()
        else:
            constant_term = coefficients[0]
        constant_term_reduced = self._base_valuation.reduce(constant_term)
        return constant_term_reduced(self._residue_field_generator())

    @cached_method
    def _residue_field_generator(self):
        r"""
        Return a root of :meth:`psi` in :meth:`residue_ring`.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, TrivialValuation(QQ))

            sage: w = v.augmentation(x, 1)
            sage: w._residue_field_generator()
            0

            sage: w = v.augmentation(x^2 + x + 1, infinity)
            sage: w._residue_field_generator()
            u1

        A case with non-trivial base valuation::
            
            sage: R.<u> = Qq(4, 10)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)
            sage: w = v.augmentation(x^2 + x + u, infinity)
            sage: w._residue_field_generator()
            u1

        """
        if self.psi().degree() == 1:
            ret = self.residue_ring()(-self.psi()[0])
        else:
            ret = self.residue_ring().gen()

        assert self.psi()(ret).is_zero()
        return ret

    def lift(self, F):
        """
        Return a polynomial which :meth:`reduce`s to ``F``.

        INPUT:

        - ``F`` -- an element of the :meth:`residue_ring`

        ALGORITHM:

        We simply undo the steps performed in :meth:`reduce`.

        OUTPUT:

        A polynomial in the domain of the valuation with reduction ``F``

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, TrivialValuation(QQ))

            sage: w = v.augmentation(x, 1)
            sage: w.lift(1/2)
            1/2

            sage: w = v.augmentation(x^2 + x + 1, infinity)
            sage: w.lift(w.residue_ring().gen())
            x

        A case with non-trivial base valuation::
            
            sage: R.<u> = Qq(4, 10)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)
            sage: w = v.augmentation(x^2 + x + u, infinity)
            sage: w.lift(w.residue_ring().gen())
            (1 + O(2^10))*x

        """
        F = self.residue_ring().coerce(F)

        if F.is_zero():
            return self.domain().zero()
        if F.is_one():
            return self.domain().one()

        # Write F as a polynomial in self._residue_field_generator()
        # We only have to do that if psi is non-trivial
        if self.psi().degree() > 1:
            from sage.rings.polynomial.polynomial_quotient_ring_element import PolynomialQuotientRingElement
            from sage.rings.function_field.function_field_element import FunctionFieldElement_polymod
            if isinstance(F, PolynomialQuotientRingElement):
                G = F.lift()
            elif isinstance(F, FunctionFieldElement_polymod):
                G = F.element()
            else:
                G = F.polynomial()
            assert(G(self._residue_field_generator()) == F)
            F = G.change_variable_name(self._base_valuation.residue_ring().variable_name())

        H = self._base_valuation.lift(F)
        return self.domain()(H)


class NonFinalAugmentedValuation(AugmentedValuation_base, NonFinalInductiveValuation):
    r"""
    An augmented valuation which can be augmented further.

    EXAMPLES::

        sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
        sage: R.<x> = QQ[]
        sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
        sage: w = v.augmentation(x^2 + x + 1, 1)

    """
    def __init__(self, parent, v, phi, mu):
        r"""
        TESTS::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
            sage: w = v.augmentation(x^2 + x + 1, 1)
            sage: isinstance(w, NonFinalAugmentedValuation)
            True

        """
        AugmentedValuation_base.__init__(self, parent, v, phi, mu)
        NonFinalInductiveValuation.__init__(self, parent, phi)

    @cached_method
    def residue_ring(self):
        r"""
        Return the residue ring of this valuation, i.e., the elements of
        non-negative valuation modulo the elements of positive valuation.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, pAdicValuation(QQ, 2))

            sage: w = v.augmentation(x^2 + x + 1, 1)
            sage: w.residue_ring()
            Univariate Polynomial Ring in x over Finite Field in u1 of size 2^2

        Since trivial valuations of finite fields are not implemented, the
        resulting ring might be identical to the residue ring of the underlying
        valuation::

            sage: w = v.augmentation(x, 1)
            sage: w.residue_ring()
            Univariate Polynomial Ring in x over Finite Field of size 2 (using NTL)

        """
        from sage.categories.fields import Fields
        if self.domain().base() not in Fields():
            raise NotImplementedError("only implemented for polynomial rings over fields")

        base = self._base_valuation.residue_ring().base()
        if self.psi().degree() > 1:
            generator = self._residue_ring_generator_name()
            base = base.extension(self.psi(), names=generator)
        else:
            # Do not call extension() if self.psi().degree() == 1:
            # In that case the resulting field appears to be the same as the original field,
            # however, it is not == to the original field (for finite fields at
            # least) but a distinct copy (this is a bug in finite field's
            # extension() implementation.)
            pass
        return base[self.domain().variable_name()]

    def reduce(self, f, check=True, degree_bound=None, coefficients=None, valuations=None):
        r"""
        Reduce ``f`` module this valuation.

        INPUT:

        - ``f`` -- an element in the domain of this valuation

        - ``check`` -- whether or not to check whether ``f`` has non-negative
          valuation (default: ``True``)

        - ``degree_bound`` -- an a-priori known bound on the degree of the
          result which can speed up the computation (default: not set)

        - ``coefficients`` -- the coefficients of ``f`` as produced by
          :meth:`coefficients` or ``None`` (default: ``None``); this can be
          used to speed up the computation when the expansion of ``f`` is
          already known from a previous computation.

        - ``valuations`` -- the valuations of ``coefficients`` or ``None``
          (default: ``None``)

        OUTPUT:

        an element of the :meth:`residue_ring` of this valuation, the reduction
        modulo the ideal of elements of positive valuation

        ALGORITHM:

        We follow the algorithm given in the proof of Theorem 12.1 of [ML1936]:
        If ``f`` has positive valuation, the reduction is simply zero.
        Otherwise, let `f=\sum f_i\phi^i` be the expansion of `f`, as computed
        by :meth:`coefficients`. Since the valuation is zero, the exponents `i`
        must all be multiples of `\tau`, the index the value group of the base
        valuation in the value group of this valuation.
        Hence, there is an :meth:`equivalence_unit` `Q` with the same valuation
        as `\phi^\tau`. Let `Q'` be its :meth:`reciprocal_inverse`.
        Now, rewrite each term `f_i\phi^{i\tau}=(f_iQ^i)(\phi^\tauQ^{-1})^i`;
        it turns out that the second factor in this expression is a lift of the
        generator of the :meth:`residue_field`. The reduction of the first
        factor can be computed recursively.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 10)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)
            sage: v.reduce(x)
            x
            sage: v.reduce(S(u))
            u0

            sage: w = v.augmentation(x^2 + x + u, 1/2)
            sage: w.reduce(S.one())
            1
            sage: w.reduce(S(2))
            0
            sage: w.reduce(S(u))
            u0
            sage: w.reduce(x) # this gives the generator of the residue field extension of w over v
            u1
            sage: f = (x^2 + x + u)^2 / 2
            sage: w.reduce(f)
            x
            sage: w.reduce(f + x + 1)
            x + u1 + 1

            sage: ww = w.augmentation((x^2 + x + u)^2 + 2, 5/3)
            sage: g = ((x^2 + x + u)^2 + 2)^3 / 2^5
            sage: ww.reduce(g)
            x
            sage: ww.reduce(f)
            1
            sage: ww.is_equivalent(f, 1)
            True
            sage: ww.reduce(f * g)
            x
            sage: ww.reduce(f + g)
            x + 1

        """
        f = self.domain().coerce(f)

        if self.lower_bound(f) > 0:
            return self.residue_ring().zero()

        tau = self.value_group().index(self._base_valuation.value_group())

        if coefficients is None:
            coefficients = self.coefficients(f)
            if degree_bound is not None:
                from itertools import islice
                coefficients = islice(coefficients, 0, tau*degree_bound + 1, 1)
        coefficients = list(coefficients)

        if valuations is None:
            valuations = []
        valuations = valuations[::tau]

        # rewrite as sum of f_i phi^{i tau}, i.e., drop the coefficients that
        # can have no influence on the reduction
        for i,c in enumerate(coefficients):
            if i % tau != 0:
                if check:
                    v = self._base_valuation(c) + i*self._mu
                    assert v != 0 # this can not happen for an augmented valuation
                    if v < 0:
                        raise ValueError("f must not have negative valuation")
            else:
                # the validity of the coefficients with i % tau == 0 is checked by
                # the recursive call to reduce below
                # replace f_i by f_i Q^{i tau}
                if i//tau >= len(valuations):
                    # we do not the correct valuation of the coefficient, but
                    # the computation is faster if we know that the coefficient
                    # has positive valuation
                    valuations.append(self._base_valuation.lower_bound(c) + i*self._mu)
                v = valuations[i//tau]
                if v is infinity or v > 0:
                    coefficients[i] = self.domain().zero()
                    valuations[i//tau] = infinity
                else:
                    coefficients[i] = c * self._Q(i//tau)
                    valuations[i//tau] -= i*self._mu

        coefficients = coefficients[::tau]

        # recursively reduce the f_i Q^{i tau}
        C = [self._base_valuation.reduce(c, check=False)(self._residue_field_generator()) if valuations[i] is not infinity else self._base_valuation.residue_ring().zero() for i,c in enumerate(coefficients)]

        # reduce the Q'^i phi^i
        return self.residue_ring()(C)

    @cached_method
    def _residue_field_generator(self):
        r"""
        Return a root of :meth:`psi` in :meth:`residue_ring`.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 10)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)
            sage: w = v.augmentation(x^2 + x + u, 1/2)
            sage: w._residue_field_generator()
            u1
            
        """
        if self.residue_ring() == self._base_valuation.residue_ring():
            assert self.psi().degree() == 1
            ret = self.residue_ring().base()(-self.psi()[0])
        else:
            ret = self.residue_ring().base().gen()

        assert ret.parent() is self.residue_ring().base()
        assert self.psi()(ret).is_zero()
        return ret

    def lift(self, F, report_coefficients=False):
        """
        Return a polynomial which :meth:`reduce`s to ``F``.

        INPUT:

        - ``F`` -- an element of the :meth:`residue_ring`

        - ``report_coefficients`` -- whether to return the coefficients of the
          :meth:`phi`-adic expansion or the actual polynomial (default:
          ``False``, i.e., return the polynomial)

        OUTPUT:

        A polynomial in the domain of the valuation with reduction ``F``, monic
        if ``F`` is monic.

        ALGORITHM:

        Since this is the inverse of :meth:`reduce`, we only have to go backwards
        through the algorithm described there.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 10)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)

            sage: w = v.augmentation(x^2 + x + u, 1/2)
            sage: y = w.residue_ring().gen()
            sage: u1 = w.residue_ring().base().gen()

            sage: w.lift(1)
            1 + O(2^10)
            sage: w.lift(0)
            0
            sage: w.lift(u1)
            (1 + O(2^10))*x
            sage: w.reduce(w.lift(y)) == y
            True
            sage: w.reduce(w.lift(y + u1 + 1)) == y + u1 + 1
            True

            sage: ww = w.augmentation((x^2 + x + u)^2 + 2, 5/3)
            sage: y = ww.residue_ring().gen()
            sage: u2 = ww.residue_ring().base().gen()

            sage: ww.reduce(ww.lift(y)) == y
            True
            sage: ww.reduce(ww.lift(1)) == 1
            True
            sage: ww.reduce(ww.lift(y + 1)) == y +  1
            True

        A more complicated example::

            sage: v = GaussValuation(S)
            sage: w = v.augmentation(x^2 + x + u, 1)
            sage: ww = w.augmentation((x^2 + x + u)^2 + 2*x*(x^2 + x + u) + 4*x, 3)
            sage: u = ww.residue_ring().base().gen()

            sage: F = ww.residue_ring()(u); F
            u2
            sage: f = ww.lift(F); f
            (2^-1 + O(2^9))*x^2 + (2^-1 + O(2^9))*x + u*2^-1 + O(2^9)
            sage: F == ww.reduce(f)
            True

        """
        F = self.residue_ring().coerce(F)

        from sage.categories.fields import Fields
        if not self.domain().base_ring() in Fields():
            raise NotImplementedError("only implemented for polynomial rings over fields")

        if F.is_constant():
            if F.is_zero():
                return self.domain().zero()
            if F.is_one():
                return self.domain().one()

        R0 = self._base_valuation.residue_ring()

        # in the last step of reduce, the f_iQ^i are reduced, and evaluated at
        # the generator of the residue field
        # here, we undo this:
        coeffs = [ R0(c if self.psi().degree()==1 else list(c._vector_() if hasattr(c, '_vector_') else c.list())) for c in F.coefficients(sparse=False) ]
        coeffs = [ self._base_valuation.lift(c) for c in coeffs ]
        # now the coefficients correspond to the expansion with (f_iQ^i)(Q^{-1} phi)^i

        # now we undo the factors of Q^i (the if else is necessary to handle the case when mu is infinity, i.e., when _Q_reciprocal() is undefined)
        coeffs = [ (c if i == 0 else c*self._Q_reciprocal(i)).map_coefficients(_lift_to_maximal_precision) for i,c in enumerate(coeffs) ]

        if report_coefficients:
            return coeffs

        RR = self.domain().change_ring(self.domain())

        tau = self.value_group().index(self._base_valuation.value_group())
        ret = RR(coeffs)(self.phi()**tau)
        ret = ret.map_coefficients(lambda c:_lift_to_maximal_precision(c))
        return ret

    def lift_to_key(self, F, check=True):
        """
        Lift the irreducible polynomial ``F`` to a key polynomial.

        INPUT:

        - ``F`` -- an irreducible non-constant polynomial in the
          :meth:`residue_ring` of this valuation

        - ``check`` -- whether or not to check correctness of ``F`` (default:
          ``True``)

        OUTPUT:

        A polynomial `f` in the domain of this valuation which is a key
        polynomial for this valuation and which, for a suitable equivalence
        unit `R`, satifies that the reduction of `Rf` is ``F``

        ALGORITHM:

        We follow the algorithm described in Theorem 13.1 [ML1936] which, after
        a :meth:`lift` of ``F``, essentially shifts the valuations of all terms
        in the `\phi`-adic expansion up and then kills the leading coefficient.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 10)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)

            sage: w = v.augmentation(x^2 + x + u, 1/2)
            sage: y = w.residue_ring().gen()
            sage: f = w.lift_to_key(y + 1); f
            (1 + O(2^10))*x^4 + (2 + O(2^11))*x^3 + (1 + u*2 + O(2^10))*x^2 + (u*2 + O(2^11))*x + (u + 1) + u*2 + O(2^10)
            sage: w.is_key(f)
            True

        A more complicated example::

            sage: v = GaussValuation(S)
            sage: w = v.augmentation(x^2 + x + u, 1)
            sage: ww = w.augmentation((x^2 + x + u)^2 + 2*x*(x^2 + x + u) + 4*x, 3)

            sage: u = ww.residue_ring().base().gen()
            sage: y = ww.residue_ring().gen()
            sage: f = ww.lift_to_key(y^3+y+u)
            sage: f.degree()
            12
            sage: ww.is_key(f)
            True

        """
        F = self.residue_ring().coerce(F)

        from sage.categories.fields import Fields
        if not self.domain().base_ring() in Fields():
            raise NotImplementedError("only implemented for polynomial rings over fields")

        if check:
            if self._base_valuation.is_gauss_valuation() and self._mu is infinity:
                raise TypeError("there are no keys over this valuation")
            if F.is_constant():
                raise ValueError("F must not be constant")
            if not F.is_monic():
                raise ValueError("F must be monic")
            if not F.is_irreducible():
                raise ValueError("F must be irreducible")

        if F == F.parent().gen():
            return self.phi()

        coefficients = self.lift(F, report_coefficients=True)[:-1]
        coefficients = [c*self._Q(F.degree()) for i,c in enumerate(coefficients)] + [self.domain().one()]
        if len(coefficients) >= 2:
            # The second-highest coefficient could %phi spill over into the
            # highest constant (which is a constant one) so we need to mod it
            # away.
            # This can not happen for other coefficients because self._Q() has
            # degree at most the degree of phi.
            coefficients[-2] %= self.phi()
        tau = self.value_group().index(self._base_valuation.value_group())
        vf = self._mu * tau * F.degree()
        ret = self.domain().change_ring(self.domain())([c for c in coefficients])(self.phi()**tau)
        ret = self.simplify(ret, error=vf, force=True)
        ret = ret.map_coefficients(lambda c:_lift_to_maximal_precision(c))
        assert (ret == self.phi()) == (F == F.parent().gen())
        assert self.is_key(ret)
        return ret

    @cached_method
    def _Q(self, e):
        r"""
        Return the polynomial `Q^e` used in the construction to :meth:`reduce` an
        element to the :meth:`residue_ring`.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
            sage: w = v.augmentation(x^2 + x + 1, 1)

            sage: w._Q(1)
            2

        """
        tau = self.value_group().index(self._base_valuation.value_group())
        v = self._mu * tau
        return self._pow(self.equivalence_unit(v), e, error=v*e, effective_degree=0)

    @cached_method
    def _Q_reciprocal(self, e=1):
        r"""
        Return the :meth:`equivalence_reciprocal` of the ``e``-th power of
        :meth:`_Q`.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
            sage: w = v.augmentation(x^2 + x + 1, 1)

            sage: w._Q_reciprocal()
            1/2

        """
        if e == 1:
            return self.equivalence_reciprocal(self._Q(1), check=False)
        
        tau = self.value_group().index(self._base_valuation.value_group())
        v = -self._mu * tau
        ret = self._pow(self._Q_reciprocal(1), e, error=v*e, effective_degree=0)

        assert self.is_equivalence_unit(ret)
        # esentially this checks that the reduction of Q'*phi^tau is the
        # generator of the residue field
        assert self._base_valuation.reduce(self._Q(e)*ret)(self._residue_field_generator()).is_one()

        return ret


class FiniteAugmentedValuation(AugmentedValuation_base, FiniteInductiveValuation):
    r"""
    A finite augmented valuation, i.e., an augmented valuation which is
    discrete, or equivalently an augmented valuation which assigns to its last
    key polynomial a finite valuation.

    EXAMPLES::

        sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
        sage: R.<u> = Qq(4, 5)
        sage: S.<x> = R[]
        sage: v = GaussValuation(S)
        sage: w = v.augmentation(x^2 + x + u, 1/2)

    """
    def __init__(self, parent, v, phi, mu):
        r"""
        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 5)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)
            sage: w = v.augmentation(x^2 + x + u, 1/2)
            sage: isinstance(w, FiniteAugmentedValuation)
            True

        """
        AugmentedValuation_base.__init__(self, parent, v, phi, mu)
        FiniteInductiveValuation.__init__(self, parent, phi)

    @cached_method
    def value_group(self):
        """
        Return the value group of this valuation.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 5)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)

            sage: w = v.augmentation(x^2 + x + u, 1/2)
            sage: w.value_group()
            Additive Abelian Group generated by 1/2

            sage: ww = w.augmentation((x^2 + x + u)^2 + 2, 5/3)
            sage: ww.value_group()
            Additive Abelian Group generated by 1/6

        """
        return self._base_valuation.value_group() + self._mu

    def value_semigroup(self):
        r"""
        Return the value semigroup of this valuation.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Zq(4, 5)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)

            sage: w = v.augmentation(x^2 + x + u, 1/2)
            sage: w.value_semigroup()
            Additive Abelian Semigroup generated by 1/2

            sage: ww = w.augmentation((x^2 + x + u)^2 + 2, 5/3)
            sage: ww.value_semigroup()
            Additive Abelian Semigroup generated by 1/2, 5/3

        """
        return self._base_valuation.value_semigroup() + self._mu

    def valuations(self, f, coefficients=None, call_error=False):
        """
        Return the valuations of the `f_i\phi^i` in the expansion `f=\sum_i
        f_i\phi^i`.

        INPUT:

        - ``f`` -- a polynomial in the domain of this valuation

        - ``coefficients`` -- the coefficients of ``f`` as produced by
          :meth:`coefficients` or ``None`` (default: ``None``); this can be
          used to speed up the computation when the expansion of ``f`` is
          already known from a previous computation.

        - ``call_error` -- whether or not to speed up the computation by
          assuming that the result is only used to compute the valuation of
          ``f`` (default: ``False``)

        OUTPUT:

        An iterator over rational numbers (or infinity) `[v(f_0), v(f_1\phi), \dots]`

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 5)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)

            sage: w = v.augmentation(x^2 + x + u, 1/2)
            sage: list(w.valuations( x^2 + 1 ))
            [0, 1/2]

            sage: ww = w.augmentation((x^2 + x + u)^2 + 2, 5/3)
            sage: list(ww.valuations( ((x^2 + x + u)^2 + 2)^3 ))
            [+Infinity, +Infinity, +Infinity, 5]

        """
        f = self.domain().coerce(f)

        if call_error:
            lowest_valuation = infinity
        for i,c in enumerate(coefficients or self.coefficients(f)):
            if call_error:
                if lowest_valuation is not infinity:
                    v = self._base_valuation.lower_bound(c)
                    if v is infinity or v >= lowest_valuation:
                        yield infinity
                        continue
            v = self._base_valuation(c)
            if v is infinity:
                yield v
            else:
                ret = v + i*self._mu
                if call_error:
                    if lowest_valuation is infinity or ret < lowest_valuation:
                        lowest_valuation = ret
                yield ret

    def simplify(self, f, error=None, force=False, effective_degree=None, size_heuristic_bound=32):
        r"""
        Return a simplified version of ``f``.

        Produce an element which differs from ``f`` by an element of valuation
        strictly greater than the valuation of ``f`` (or strictly greater than
        ``error`` if set.)

        INPUT:

        - ``f`` -- an element in the domain of this valuation

        - ``error`` -- a rational, infinity, or ``None`` (default: ``None``),
          the error allowed to introduce through the simplification

        - ``force`` -- whether or not to simplify ``f`` even if there is
          heuristically no change in the coefficient size of ``f`` expected
          (default: ``False``)

        - ``effective_degree`` -- when set, assume that coefficients beyond
          ``effective_degree`` in the :meth:`phi`-adic development can be
          safely dropped (default: ``None``)

        - ``size_heuristic_bound` -- when ``force`` is not set, the expected
          factor by which the coefficients need to shrink to perform an actual
          simplification (default: 32)

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 5)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)
            sage: w = v.augmentation(x^2 + x + u, 1/2)
            sage: w.simplify(x^10/2 + 1, force=True) # not tested - error is incorrect
            (u + 1)*2^-1 + O(2^4)

        """
        f = self.domain().coerce(f)

        if effective_degree is not None:
            if (QQ(f.degree())/self.phi().degree()).ceil() > effective_degree:
                from itertools import islice
                f = self.domain().change_ring(self.domain())(list(islice(self.coefficients(f), 0, effective_degree + 1, 1)))(self.phi())

        if not force and self._relative_size(f) < size_heuristic_bound:
            return f

        if error is None:
            error = self.upper_bound(f)

        return self._base_valuation.simplify(f, error=error, force=force)

    def lower_bound(self, f):
        r"""
        Return a lower bound of this valuation at ``f``.

        Use this method to get an approximation of the valuation of ``f``
        when speed is more important than accuracy.

        ALGORITHM:

        The main cost of evaluation is the computation of the
        :meth:`coefficients` of the :meth:`phi`-adic expansion of ``f`` (which
        often leads to coefficient bloat.) So unless :meth:`phi` is trivial, we
        fall back to valuation which this valuation augments since it is
        guaranteed to be smaller everywhere.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 5)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)
            sage: w = v.augmentation(x^2 + x + u, 1/2)
            sage: w.lower_bound(x^2 + x + u)
            0

        """
        f = self.domain().coerce(f)

        if self.phi() == self.domain().gen():
            constant_valuation = self.restriction(f.base_ring())
            ret = infinity
            for i,c in enumerate(f.coefficients(sparse=False)):
                v = constant_valuation.lower_bound(c)
                if v is infinity:
                    continue
                v += i*self._mu
                if ret is infinity or v < ret:
                    ret = v
            return ret
        else:
            return self._base_valuation.lower_bound(f)

    def upper_bound(self, f):
        r"""
        Return an upper bound of this valuation at ``f``.

        Use this method to get an approximation of the valuation of ``f``
        when speed is more important than accuracy.

        ALGORITHM:

        Any entry of :meth:`valuations` serves as an upper bound. However,
        computation of the :meth:`phi`-adic expansion of ``f`` is quite costly.
        Therefore, we produce an upper bound on the last entry of
        :meth:`valuations`, namely the valuation of the leading coefficient of
        ``f`` plus the valuation of the appropriate power of :meth:`phi`.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 5)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)
            sage: w = v.augmentation(x^2 + x + u, 1/2)
            sage: w.upper_bound(x^2 + x + u)
            1/2

        """
        f = self.domain().coerce(f)

        len_coefficients_bound = (QQ(f.degree()) / self.phi().degree()).ceil()
        return self.restriction(f.base_ring())(f.leading_coefficient()) + len_coefficients_bound * self._mu


class FinalFiniteAugmentedValuation(FiniteAugmentedValuation, FinalAugmentedValuation):
    r"""
    An augmented valuation which is discrete, i.e., which assigns a finite
    valuation to its last key polynomial, but which can not be further
    augmented.

    EXAMPLES::

        sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
        sage: R.<x> = QQ[]
        sage: v = GaussValuation(R, TrivialValuation(QQ))
        sage: w = v.augmentation(x, 1)

    """
    def __init__(self, parent, v, phi, mu):
        r"""
        TESTS::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, TrivialValuation(QQ))
            sage: w = v.augmentation(x, 1)
            sage: isinstance(w, FinalFiniteAugmentedValuation)
            True

        """
        FiniteAugmentedValuation.__init__(self, parent, v, phi, mu)
        FinalAugmentedValuation.__init__(self, parent, v, phi, mu)


class NonFinalFiniteAugmentedValuation(FiniteAugmentedValuation, NonFinalAugmentedValuation):
    r"""
    An augmented valuation which is discrete, i.e., which assigns a finite
    valuation to its last key polynomial, and which can be augmented furter.

    EXAMPLES::

        sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
        sage: R.<x> = QQ[]
        sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
        sage: w = v.augmentation(x, 1)

    """
    def __init__(self, parent, v, phi, mu):
        r"""
        TESTS::
    
            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
            sage: w = v.augmentation(x, 1)
            sage: isinstance(w, NonFinalFiniteAugmentedValuation)
            True
    
        """
        FiniteAugmentedValuation.__init__(self, parent, v, phi, mu)
        NonFinalAugmentedValuation.__init__(self, parent, v, phi, mu)


class InfiniteAugmentedValuation(FinalAugmentedValuation, InfiniteInductiveValuation):
    r"""
    An augmented valuation which is infinite, i.e., which assigns valuation
    infinity to its last key polynomial (and which can therefore not be
    augmented further.)

    EXAMPLES::

        sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
        sage: R.<x> = QQ[]
        sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
        sage: w = v.augmentation(x, infinity)

    """
    def __init__(self, parent, v, phi, mu):
        r"""
        TESTS::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<x> = QQ[]
            sage: v = GaussValuation(R, pAdicValuation(QQ, 2))
            sage: w = v.augmentation(x, infinity)
            sage: isinstance(w, InfiniteAugmentedValuation)
            True

        """
        FinalAugmentedValuation.__init__(self, parent, v, phi, mu)
        InfiniteInductiveValuation.__init__(self, parent, phi)

    @cached_method
    def value_group(self):
        """
        Return the value group of this valuation.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 5)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)
            sage: w = v.augmentation(x, infinity)
            sage: w.value_group()
            Additive Abelian Group generated by 1

        """
        return self._base_valuation.value_group()

    @cached_method
    def value_semigroup(self):
        """
        Return the value semigroup of this valuation.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Zq(4, 5)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)
            sage: w = v.augmentation(x, infinity)
            sage: w.value_semigroup()
            Additive Abelian Semigroup generated by 1

        """
        return self._base_valuation.value_semigroup()

    def valuations(self, f, coefficients=None, call_error=False):
        """
        Return the valuations of the `f_i\phi^i` in the expansion `f=\sum_i
        f_i\phi^i`.

        INPUT:

        - ``f`` -- a polynomial in the domain of this valuation

        - ``coefficients`` -- the coefficients of ``f`` as produced by
          :meth:`coefficients` or ``None`` (default: ``None``); this can be
          used to speed up the computation when the expansion of ``f`` is
          already known from a previous computation.

        - ``call_error` -- whether or not to speed up the computation by
          assuming that the result is only used to compute the valuation of
          ``f`` (default: ``False``)

        OUTPUT:

        An iterator over rational numbers (or infinity) `[v(f_0), v(f_1\phi), \dots]`

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 5)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)
            sage: w = v.augmentation(x, infinity)
            sage: list(w.valuations(x^2 + 1))
            [0, +Infinity, +Infinity]

        """
        f = self.domain().coerce(f)

        num_infty_coefficients = f.degree() // self.phi().degree()
        if coefficients is not None:
            constant_coefficient = coefficients[0]
        else:
            constant_coefficient = self.coefficients(f).next()
        yield self._base_valuation(constant_coefficient)
        for i in range(num_infty_coefficients):
            yield infinity

    def simplify(self, f, error=None, force=False, effective_degree=None):
        r"""
        Return a simplified version of ``f``.

        Produce an element which differs from ``f`` by an element of valuation
        strictly greater than the valuation of ``f`` (or strictly greater than
        ``error`` if set.)

        INPUT:

        - ``f`` -- an element in the domain of this valuation

        - ``error`` -- a rational, infinity, or ``None`` (default: ``None``),
          the error allowed to introduce through the simplification

        - ``force`` -- whether or not to simplify ``f`` even if there is
          heuristically no change in the coefficient size of ``f`` expected
          (default: ``False``)

        - ``effective_degree`` -- ignored; for compatibility with other
          ``simplify`` methods

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 5)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)
            sage: w = v.augmentation(x^2 + x + u, infinity)
            sage: w.simplify(x^10/2 + 1, force=True) # not tested - error incorrect
            (u + 1)*2^-1 + O(2^4)

        """
        f = self.domain().coerce(f)

        if error is None:
            error = self.upper_bound(f)

        if error is infinity:
            return f

        return self.domain()(self._base_valuation.simplify(self.coefficients(f).next(), error, force=force))

    def lower_bound(self, f):
        r"""
        Return a lower bound of this valuation at ``f``.

        Use this method to get an approximation of the valuation of ``f``
        when speed is more important than accuracy.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 5)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)
            sage: w = v.augmentation(x^2 + x + u, infinity)
            sage: w.lower_bound(x^2 + x + u)
            +Infinity

        """
        return self._base_valuation.lower_bound(self.coefficients(f).next())

    def upper_bound(self, f):
        r"""
        Return an upper bound of this valuation at ``f``.

        Use this method to get an approximation of the valuation of ``f``
        when speed is more important than accuracy.

        EXAMPLES::

            sage: sys.path.append(os.getcwd()); from mac_lane import * # optional: standalone
            sage: R.<u> = Qq(4, 5)
            sage: S.<x> = R[]
            sage: v = GaussValuation(S)
            sage: w = v.augmentation(x^2 + x + u, infinity)
            sage: w.upper_bound(x^2 + x + u)
            +Infinity

        """
        return self._base_valuation.upper_bound(self.coefficients(f).next())
