r"""
Modular Forms for `\Gamma_1(N)` and `\Gamma_H(N)` over `\QQ`.

EXAMPLES::

    sage: M = ModularForms(Gamma1(13),2); M
    Modular Forms space of dimension 13 for Congruence Subgroup Gamma1(13) of weight 2 over Rational Field
    sage: S = M.cuspidal_submodule(); S
    Cuspidal subspace of dimension 2 of Modular Forms space of dimension 13 for Congruence Subgroup Gamma1(13) of weight 2 over Rational Field
    sage: S.basis()
    [
    q - 4*q^3 - q^4 + 3*q^5 + O(q^6),
    q^2 - 2*q^3 - q^4 + 2*q^5 + O(q^6)
    ]

    sage: M = ModularForms(GammaH(50, [27])); M
    Modular Forms space of dimension 13 for Congruence Subgroup Gamma_H(50) with H generated by [27] of weight 2 over Rational Field
    sage: M.q_expansion_basis(25)
    [
    q + q^4 - q^6 - 2*q^9 - 3*q^11 - 2*q^14 + q^16 + 5*q^19 + 2*q^21 - q^24 + O(q^25),
    q^2 - q^3 - 2*q^7 + q^8 - q^12 + 4*q^13 + 3*q^17 - 2*q^18 - 3*q^22 - 6*q^23 + O(q^25),
    1 + O(q^25),
    q + 12*q^11 + 8*q^14 + q^16 - 6*q^19 + 19*q^21 + 5*q^24 + O(q^25),
    q^2 + 5*q^12 - q^18 + 12*q^22 + O(q^25),
    q^3 - 3/2*q^12 + 9/2*q^13 - 1/2*q^17 + q^18 + 8*q^23 + O(q^25),
    q^4 + 4*q^14 + q^16 + 8*q^24 + O(q^25),
    q^5 + 4*q^15 - 2*q^20 + O(q^25),
    q^6 - q^14 + 3*q^16 + q^24 + O(q^25),
    q^7 + 1/2*q^12 - 1/2*q^13 + 5/2*q^17 + q^18 - q^23 + O(q^25),
    q^8 + q^12 + 2*q^18 + O(q^25),
    q^9 - q^16 + 2*q^19 + q^21 - q^24 + O(q^25),
    q^10 + 3*q^20 + O(q^25)
    ]
    sage: M.q_integral_basis(25)
    [
    1 + O(q^25),
    q - 4*q^14 + q^16 + 6*q^19 + 7*q^21 - 7*q^24 + O(q^25),
    q^2 + 5*q^13 + 5*q^17 - q^18 + 2*q^22 + O(q^25),
    q^3 + 3*q^13 - 2*q^17 + q^18 + 3*q^22 + 8*q^23 + O(q^25),
    q^4 + 4*q^14 + q^16 + 8*q^24 + O(q^25),
    q^5 + 4*q^15 - 2*q^20 + O(q^25),
    q^6 - q^14 + 3*q^16 + q^24 + O(q^25),
    q^7 + 3*q^17 + q^18 - q^22 - q^23 + O(q^25),
    q^8 + q^13 + q^17 + 2*q^18 - 2*q^22 + O(q^25),
    q^9 - q^16 + 2*q^19 + q^21 - q^24 + O(q^25),
    q^10 + 3*q^20 + O(q^25),
    q^11 + q^14 - q^19 + q^21 + q^24 + O(q^25),
    q^12 - q^13 - q^17 + 2*q^22 + O(q^25)
    ]

TESTS::

    sage: m = ModularForms(Gamma1(20),2)
    sage: loads(dumps(m)) == m
    True

    sage: m = ModularForms(GammaH(15, [4]), 2)
    sage: loads(dumps(m)) == m
    True
"""

#########################################################################
#       Copyright (C) 2006 William Stein <wstein@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#                  http://www.gnu.org/licenses/
#########################################################################

import sage.rings.all as rings

import sage.modular.arithgroup.all as arithgroup

import ambient
import cuspidal_submodule
import eisenstein_submodule
import submodule

class ModularFormsAmbient_gH_Q(ambient.ModularFormsAmbient):
    """
    A space of modular forms for the group `\Gamma_H(N)` over the rational numbers.
    """
    def __init__(self, group, weight):
        r"""
        Create a space of modular forms for `\Gamma_H(N)` of integral weight over the
        rational numbers.

        EXAMPLES::

            sage: m = ModularForms(GammaH(100, [41]),5); m
            Modular Forms space of dimension 270 for Congruence Subgroup Gamma_H(100) with H generated by [41] of weight 5 over Rational Field
            sage: type(m)
            <class 'sage.modular.modform.ambient_g1.ModularFormsAmbient_gH_Q_with_category'>
        """
        ambient.ModularFormsAmbient.__init__(self, group, weight, rings.QQ)

    ####################################################################
    # Computation of Special Submodules
    ####################################################################
    def cuspidal_submodule(self):
        """
        Return the cuspidal submodule of this modular forms space.

        EXAMPLES::

            sage: m = ModularForms(GammaH(100, [29]),2); m
            Modular Forms space of dimension 48 for Congruence Subgroup Gamma_H(100) with H generated by [29] of weight 2 over Rational Field
            sage: m.cuspidal_submodule()
            Cuspidal subspace of dimension 13 of Modular Forms space of dimension 48 for Congruence Subgroup Gamma_H(100) with H generated by [29] of weight 2 over Rational Field
        """
        try:
            return self.__cuspidal_submodule
        except AttributeError:
            if self.level() == 1:
                self.__cuspidal_submodule = cuspidal_submodule.CuspidalSubmodule_level1_Q(self)
            else:
                self.__cuspidal_submodule = cuspidal_submodule.CuspidalSubmodule_gH_Q(self)
        return self.__cuspidal_submodule

    def eisenstein_submodule(self):
        """
        Return the Eisenstein submodule of this modular forms space.

        EXAMPLES::

            sage: E = ModularForms(GammaH(100, [29]),3).eisenstein_submodule(); E
            Eisenstein subspace of dimension 24 of Modular Forms space of dimension 72 for Congruence Subgroup Gamma_H(100) with H generated by [29] of weight 3 over Rational Field
            sage: type(E)
            <class 'sage.modular.modform.eisenstein_submodule.EisensteinSubmodule_gH_Q_with_category'>
        """
        try:
            return self.__eisenstein_submodule
        except AttributeError:
            self.__eisenstein_submodule = eisenstein_submodule.EisensteinSubmodule_gH_Q(self)
        return self.__eisenstein_submodule

    def _compute_diamond_matrix(self, d):
        r"""
        Compute the matrix of the diamond operator <d> on this space.

        EXAMPLE::

            sage: ModularForms(GammaH(9, [4]), 7)._compute_diamond_matrix(2)
            [-1  0  0  0  0  0  0  0]
            [ 0 -1  0  0  0  0  0  0]
            [ 0  0 -1  0  0  0  0  0]
            [ 0  0  0 -1  0  0  0  0]
            [ 0  0  0  0 -1  0  0  0]
            [ 0  0  0  0  0 -1  0  0]
            [ 0  0  0  0  0  0 -1  0]
            [ 0  0  0  0  0  0  0 -1]
        """
        return self.cuspidal_submodule().diamond_bracket_matrix(d).block_sum(self.eisenstein_submodule().diamond_bracket_matrix(d))

    def _compute_hecke_matrix(self, n):
        r"""
        Compute the matrix of the Hecke operator T_n acting on this space.

        EXAMPLE::

            sage: ModularForms(Gamma1(7), 4).hecke_matrix(3) # indirect doctest
            [           0          -42          133            0            0            0            0            0            0]
            [           0          -28           91            0            0            0            0            0            0]
            [           1           -8           19            0            0            0            0            0            0]
            [           0            0            0           28            0            0            0            0            0]
            [           0            0            0   -10152/259            0      5222/37    -13230/37    -22295/37     92504/37]
            [           0            0            0    -6087/259            0  312067/4329 1370420/4329   252805/333 3441466/4329]
            [           0            0            0     -729/259            1       485/37      3402/37      5733/37      7973/37]
            [           0            0            0      729/259            0      -189/37     -1404/37     -2366/37     -3348/37]
            [           0            0            0      255/259            0  -18280/4329  -51947/4329   -10192/333 -190855/4329]
        """
        return self.cuspidal_submodule().hecke_matrix(n).block_sum(self.eisenstein_submodule().hecke_matrix(n))


class ModularFormsAmbient_g1_Q(ModularFormsAmbient_gH_Q):
    """
    A space of modular forms for the group `\Gamma_1(N)` over the rational numbers.
    """
    def __init__(self, level, weight):
        r"""
        Create a space of modular forms for `\Gamma_1(N)` of integral weight over the
        rational numbers.

        EXAMPLES::

            sage: m = ModularForms(Gamma1(100),5); m
            Modular Forms space of dimension 1270 for Congruence Subgroup Gamma1(100) of weight 5 over Rational Field
            sage: type(m)
            <class 'sage.modular.modform.ambient_g1.ModularFormsAmbient_g1_Q_with_category'>
        """
        ambient.ModularFormsAmbient.__init__(self, arithgroup.Gamma1(level), weight, rings.QQ)

    ####################################################################
    # Computation of Special Submodules
    ####################################################################
    def cuspidal_submodule(self):
        """
        Return the cuspidal submodule of this modular forms space.

        EXAMPLES::

            sage: m = ModularForms(Gamma1(17),2); m
            Modular Forms space of dimension 20 for Congruence Subgroup Gamma1(17) of weight 2 over Rational Field
            sage: m.cuspidal_submodule()
            Cuspidal subspace of dimension 5 of Modular Forms space of dimension 20 for Congruence Subgroup Gamma1(17) of weight 2 over Rational Field
        """
        try:
            return self.__cuspidal_submodule
        except AttributeError:
            if self.level() == 1:
                self.__cuspidal_submodule = cuspidal_submodule.CuspidalSubmodule_level1_Q(self)
            else:
                self.__cuspidal_submodule = cuspidal_submodule.CuspidalSubmodule_g1_Q(self)
        return self.__cuspidal_submodule

    def eisenstein_submodule(self):
        """
        Return the Eisenstein submodule of this modular forms space.

        EXAMPLES::

            sage: ModularForms(Gamma1(13),2).eisenstein_submodule()
            Eisenstein subspace of dimension 11 of Modular Forms space of dimension 13 for Congruence Subgroup Gamma1(13) of weight 2 over Rational Field
            sage: ModularForms(Gamma1(13),10).eisenstein_submodule()
            Eisenstein subspace of dimension 12 of Modular Forms space of dimension 69 for Congruence Subgroup Gamma1(13) of weight 10 over Rational Field
        """
        try:
            return self.__eisenstein_submodule
        except AttributeError:
            self.__eisenstein_submodule = eisenstein_submodule.EisensteinSubmodule_g1_Q(self)
        return self.__eisenstein_submodule

