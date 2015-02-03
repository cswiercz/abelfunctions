#from .test_abelfunctions import AbelfunctionsTestCase
import unittest
from abelfunctions.puiseux import (
    almost_monicize,
    newton_data,
    newton_iteration,
    newton_polygon,
    newton_polygon_exceptional,
    puiseux,
    puiseux_rational,
    transform_newton_polynomial,
)
from .test_abelfunctions import AbelfunctionsTestCase

import sympy
from sympy.abc import x,y,z
from sympy import Poly, Point, Segment, Polygon, RootOf, sqrt, S

class TestNewtonPolygon(unittest.TestCase):

    def test_segment(self):
        H = Poly(y + x, y, x)
        self.assertEqual(newton_polygon(H,x,y),
                         [[(0,1),(1,0)]])

        H = Poly(y**2 + x**2, y, x)
        self.assertEqual(newton_polygon(H,x,y),
                         [[(0,2),(2,0)]])

    def test_general_segment(self):
        H = Poly(y**2 + x**4, y, x)
        self.assertEqual(newton_polygon(H,x,y),
                         [[(0,2),(2,0)]])

    def test_colinear(self):
        H = Poly(x**4 + x**2*y**2 + y**4, y, x)
        self.assertEqual(newton_polygon(H,x,y),
                         [[(0,4),(2,2),(4,0)]])

        H = Poly(x**4 + x**2*y**2 + x*y**3 + y**4, y, x)
        self.assertEqual(newton_polygon(H,x,y),
                         [[(0,4),(2,2),(3,1),(4,0)]])

    def test_multiple(self):
        H = Poly(2*x**2 + 3*x*y + 5*y**3, y, x)
        self.assertEqual(newton_polygon(H,x,y),
                         [[(0,2),(1,1)], [(1,1),(3,0)]])

    def test_general_to_colinear(self):
        H = Poly(x**5 + x**2*y**2 + y**4, y, x)
        self.assertEqual(newton_polygon(H,x,y),
                         [[(0,4),(2,2),(4,0)]])

        H = Poly(x**5 + x**3*y + x**2*y**2 + y**4, y, x)
        self.assertEqual(newton_polygon(H,x,y),
                         [[(0,4),(1,3),(2,2),(4,0)]])

        H = Poly(x**5 + x**2*y**2 + x*y**3 + y**4, y, x)
        self.assertEqual(newton_polygon(H,x,y),
                         [[(0,4),(2,2),(3,1),(4,0)]])

    def test_exceptional(self):
        H = Poly(x**5 + x**2*y**2 + y**4, y, x)
        EN = newton_polygon_exceptional(H,x,y)
        self.assertEqual(EN, [[(0,0),(4,0)]])


class TestNewtonData(unittest.TestCase):

    def test_segment(self):
        H = Poly(2*x + 3*y, y, x)
        self.assertEqual(newton_data(H,x,y),
                         [(1, 1, 1, 3*z + 2)])

        H = Poly(2*x**2 + 3*y**2, y, x)
        self.assertEqual(newton_data(H,x,y),
                         [(1, 1, 2, 3*z**2 + 2)])

        H = Poly(2*x**2 + 3*y**3, y, x)
        self.assertEqual(newton_data(H,x,y),
                         [(3, 2, 6, 3*z + 2)])

        H = Poly(2*x**2 + 3*y**4, y, x)
        self.assertEqual(newton_data(H,x,y),
                         [(2, 1, 4, 3*z**2 + 2)])

    def test_general_segment(self):
        H = Poly(x**2 + y, y, x)
        self.assertEqual(newton_data(H,x,y),
                         [(1, 1, 1, z)])

        H = Poly(x**3 + y**2, y, x)
        self.assertEqual(newton_data(H,x,y),
                         [(1, 1, 2, z**2)])

        H = Poly(x**5 + y**3, y, x)
        self.assertEqual(newton_data(H,x,y),
                         [(1, 1, 3, z**3)])

    def test_colinear(self):
        H = Poly(2*x**4 + 3*x**2*y**2 + 5*y**4, y, x)
        self.assertEqual(newton_data(H,x,y),
                         [(1, 1, 4, 5*z**4 + 3*z**2 + 2)])

        H = Poly(2*x**4 + 3*x**3*y + 5*x**2*y**2 + 7*y**4, y, x)
        self.assertEqual(newton_data(H,x,y),
                         [(1, 1, 4, 7*z**4 + 5*z**2 + 3*z + 2)])

        H = Poly(2*x**4 + 3*x**2*y**2 + 5*x*y**3 + 7*y**4, y, x)
        self.assertEqual(newton_data(H,x,y),
                         [(1, 1, 4, 7*z**4 + 5*z**3 + 3*z**2 + 2)])

    def test_multiple(self):
        H = Poly(2*x**2 + 3*x*y + 5*y**3, y, x)
        self.assertEqual(newton_data(H,x,y),
                         [(1, 1, 2, 3*z + 2),
                          (2, 1, 3, 5*z + 3)])

    def test_general_to_colinear(self):
        H = Poly(2*x**5 + 3*x**2*y**2 + 5*y**4, y, x)
        self.assertEqual(newton_data(H,x,y),
                         [(1, 1, 4, 5*z**4 + 3*z**2)])

        H = Poly(2*x**5 + 3*x**3*y + 5*x**2*y**2 + 7*y**4, y, x)
        self.assertEqual(newton_data(H,x,y),
                         [(1, 1, 4, 7*z**4 + 5*z**2 + 3*z)])

        H = Poly(2*x**5 + 3*x**3*y + 5*x**2*y**2 + 7*y**6, y, x)
        self.assertEqual(newton_data(H,x,y),
                         [(1, 1, 4, 5*z**2 + 3*z),
                          (2, 1, 6, 7*z**2 + 5)])


class TestNewPolynomial(unittest.TestCase):

    def setUp(self):
        self.p = sympy.random_poly(x,5,-5,5,domain=sympy.QQ)
        self.q = sympy.random_poly(y,5,-5,5,domain=sympy.QQ)

    def test_null_transform(self):
        H = (self.p*self.q).expand().as_poly(x,y)
        q,m,l,xi = 1,0,0,0
        Hprime = transform_newton_polynomial(H,x,y,q,m,l,xi)
        Htest = H
        self.assertEqual(Hprime, Htest)

    def test_yshift(self):
        H = (self.p*self.q).expand().as_poly(x,y)
        q,m,l,xi = 1,0,0,1
        Hprime = transform_newton_polynomial(H,x,y,q,m,l,xi)
        Htest = H.as_poly(y).compose((1+y).as_poly(y)).as_poly(x,y)
        self.assertEqual(Hprime, Htest)

    def test_y(self):
        H = Poly(y**2,x,y)

        q,m,l,xi = 0,1,0,1
        Hprime = transform_newton_polynomial(H,x,y,q,m,l,xi)
        Htest = Poly(x**2*(1+y)**2,x,y)
        self.assertEqual(Hprime, Htest)

        q,m,l,xi = 0,1,2,1
        Hprime = transform_newton_polynomial(H,x,y,q,m,l,xi)
        Htest = Poly((1+y)**2,x,y)
        self.assertEqual(Hprime, Htest)


class TestNewtonIteration(unittest.TestCase):

    def test_trivial(self):
        G = Poly(y - x,x,y)
        S = newton_iteration(G,x,y,3)
        self.assertEqual(S,x)

        G = Poly(y - x**2,x,y)
        S = newton_iteration(G,x,y,3)
        self.assertEqual(S,x**2)

    def test_sqrt(self):
        G = Poly(y**2 - (x+1),x,y)
        S = newton_iteration(G,x,y,9) + sympy.O(x**9)
        series = sympy.series(sympy.sqrt(x),x,1,9)
        self.assertEqual(S,series)

    def test_cuberoot(self):
        G = Poly(y**3 - (x+1), x, y)
        S = newton_iteration(G,x,y,9) + sympy.O(x**9)
        series = sympy.series(x**sympy.Rational(1,3),x,1,9)
        self.assertEqual(S,series)

    def test_geometric(self):
        G = Poly((1-x)*y - 1,x,y)
        S = newton_iteration(G,x,y,9) + sympy.O(x**9)
        series = sympy.series(1/(1-x),x,0,9)
        self.assertEqual(S,series)

    def test_n(self):
        # test if the solution is indeed given to the desired terms
        G = Poly(y - x**2, x, y)
        S = newton_iteration(G,x,y,0)
        self.assertEqual(S,0)

        G = Poly(y - x**2, x, y)
        S = newton_iteration(G,x,y,2)
        self.assertEqual(S,x**2)



class TestPuiseuxRational(AbelfunctionsTestCase):
    def is_G_vanishing(self, fmonic):
        # each G should satisfy G(0,0) = 0 and G_y(0,0) = 0
        for G,P,Q in puiseux_rational(fmonic,x,y):
            self.assertEqual(G.eval({x:0,y:0}).simplify(),0)
    def test_G_vanishing2(self):
        self.is_G_vanishing(self.f2)
    def test_G_vanishing4(self):
        self.is_G_vanishing(self.f4)
    def test_G_vanishing5(self):
        self.is_G_vanishing(self.f5)
    def test_G_vanishing6(self):
        self.is_G_vanishing(self.f6)
    def test_G_vanishing7(self):
        self.is_G_vanishing(self.f7)
    def test_G_vanishing9(self):
        self.is_G_vanishing(self.f9)


class TestAlmostMonicize(AbelfunctionsTestCase):
    def test_monic(self):
        f = y**2 + x
        g,transform = almost_monicize(f,x,y)
        self.assertEqual(f,g)

    def test_partially_monic(self):
        g,transform = almost_monicize(self.f1,x,y)
        self.assertEqual(self.f1.expand(),g)

        f = (x**2 + 1)*y
        g,transform = almost_monicize(f,x,y)
        self.assertEqual(f.expand(),g)

    def test_not_monic_simple(self):
        f = x**2*y
        g,transform = almost_monicize(f,x,y)
        self.assertEqual(g,y)
        self.assertEqual(transform,x**2)

        f = x**2*y + 1
        g,transform = almost_monicize(f,x,y)
        self.assertEqual(g,y + 1)
        self.assertEqual(transform,x**2)

        f = x**2*y + x
        g,transform = almost_monicize(f,x,y)
        self.assertEqual(g,y + x)
        self.assertEqual(transform,x**2)

        f = x*y**2 + y + x
        g,transform = almost_monicize(f,x,y)
        self.assertEqual(g,y**2 + y + x**2)
        self.assertEqual(transform,x)

        f = x**3*y**2 + y + x
        g,transform = almost_monicize(f,x,y)
        self.assertEqual(g,y**2 + y + x**4)
        self.assertEqual(transform,x**3)

    def test_not_monic(self):
        f = x**7*y**3 + 2*y - x**7
        g,transform = almost_monicize(f,x,y)

        self.assertEqual(g,y**3 + 2*x*y - x**12)
        self.assertEqual(transform,x**4)

        g,transform = almost_monicize(self.f8,x,y)
        self.assertEqual(g,y**3 + 2*x*y - 1)
        self.assertEqual(transform,x**2)


class TestPuiseux(AbelfunctionsTestCase):
    def setUp(self):
        self.f22 = y**3 - x**5
        self.f23 = (y - 1 - 2*x - x**2)*(y - 1 - 2*x - x**7)
        self.f27 = (y**2 - 2*x**3)*(y**2-2*x**2)*(y**3-2*x)
        super(TestPuiseux,self).setUp()

    def get_PQ(self,f):
        p = puiseux(f,x,y,0)
        if p:
            G,P,Q = zip(*puiseux(f,x,y,0))
            series = zip(P,(Qi.subs(y,0).expand() for Qi in Q))
        else:
            series = []
        return series
    def test_PQ_f1(self):
        series = self.get_PQ(self.f1)
        self.assertItemsEqual(
            series,
            [(x**2,x**4+x**5)])
    def test_PQ_f2(self):
        series = self.get_PQ(self.f2)
        self.assertItemsEqual(
            series,
            [(x,sympy.S(0)), (-x**2/2,-x**3/2)])
    def test_PQ_f3(self):
        # awaiting RootOf simplification issues
        pass
    def test_PQ_f4(self):
        series = self.get_PQ(self.f4)
        self.assertItemsEqual(
            series,
            [(x,x),(x,-x)])
    def test_PQ_f7(self):
        series = self.get_PQ(self.f7)
        self.assertItemsEqual(
            series,
            [])
    def test_PQ_f22(self):
        series = self.get_PQ(self.f22)
        self.assertItemsEqual(
            series,
            [(x**3,x**5)])
    def test_PQ_f23(self):
        series = self.get_PQ(self.f23)
        self.assertItemsEqual(
            series,
            [(x,1+2*x), (x,1+2*x+x**2)])
    def test_PQ_f27(self):
        series = self.get_PQ(self.f27)
        sqrt2 = RootOf(x**2-2,0,radicals=False)
        self.assertItemsEqual(
            series,
            [(x,sqrt2*x), (x**2/2,x**3/2), (x**3/2,x)])
