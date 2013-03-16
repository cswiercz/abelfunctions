"""
Riemann Surfaces
"""
import numpy
import scipy
import scipy.integrate
import sympy


from abelfunctions.monodromy import monodromy, show_paths
from abelfunctions.homology import homology
from abelfunctions.riemannsurface_path import (
    path_around_branch_point,
    RiemannSurfacePath,
    )
from abelfunctions.riemannsurface_point import RiemannSurfacePoint
from abelfunctions.singularities import genus
from abelfunctions.utilities import cached_function


import pdb
        

class RiemannSurface(object):
    """
    Class for defining a Riemann surface corresponding to a plane
    algebraic curve.
    """
    def __init__(self, f, x, y):
        self.f = f
        self.x = x
        self.y = y

#         self._monodromy = monodromy()
#         self._homology  = homology(f,x,y)

    def __repr__(self):
        return "Riemann surface defined by the algebraic curve %s." %(self.f)

    def __call__(self, x, y):
        return RiemannSurfacePoint(self, x, y)


    def point(self, x0, y0):
        """
        Returns the point on the Riemann surface closest to
        `(x0,y0)`. (In the event that floating point precision is used
        to calculate the coordinates `(x0,y0)`.
        """
        return RiemannSurfacePoint(self,x0,y0)
    

    def monodromy(self):
        """
        """
        return monodromy(self.f, self.x, self.y)


    def monodromy_graph(self):
        """
        """
        #base_point, base_sheets, branch_points, mon, G = self.monodromy()
        return self.monodromy()[4]


    def base_point(self):
        return self.monodromy()[0]


    def base_sheets(self):
        return self.monodromy()[1]


    def base_lift(self):
        return self.base_sheets()


    def branch_points(self):
        return self.monodromy()[2]


    def monodromy_group(self):
        return self.monodromy()[3]


    def homology(self):
        return homology(self.f, self.x, self.y)


    def holomorphic_differentials(self):
        """ 
        Returns the basis of holomorphic differentials defined on the
        Riemann surface.

        NOTE: NOT IMPLEMENTED
        """
#        return differentials(f,x,y)
        f,x,y = self.f,self.x,self.y
        dfdy = sympy.diff(f,y)

#        return [x*y/dfdy, x**3/dfdy]
        
        return [1/(2*y)]

    def genus(self):
        """
        Return the genus of the Riemann surface.
        """
        return genus(self.f, self.x, self.y)


    def a_cycle(self, i):
        """
        Returns the ith a_cycle as an array of interpolating points
        starting from and ending at the basepoint of the Riemann
        surface.
        """
        pass

    
    def b_cycle(self, i):
        """
        Returns the ith b_cycle as an array of interpolating points
        starting from and ending at the basepoint of the Riemann
        surface.
        """
        pass


    @cached_function
    def c_cycle(self, i):
        """
        Returns a path in the complex x-plane of the x-points in the
        monodromy path.
        
        Input:

        - i: the index of the c-cycle
        
        Output:

        - a RiemannSurfacePath parameterizing the c-cycle
        """
        # get the cycle data from homology: each c-cycle is a list of
        # alternating sheet numbers s_k and branch point / number of
        # rotations tuples (b_{i_k}, n_k)
        cycles  = self.homology()['cycles']
        
        G = self.monodromy_graph()
        root = G.node[0]['root']
        path_segments = []

        # For each (branch point, rotation number) pair appearing in
        # the cycle compute the path segments the complex x-plane
        # going around the given branch points a number of times equal
        # to the rotation number. Add these segments to the list of
        # path segemnts.
        for (bpt, rot) in cycles[i][1::2]:
            bpt_path_segments = path_around_branch_point(G, bpt, rot)
            path_segments.extend(bpt_path_segments)

        # Construct the RiemannSurfacePath
        x0 = self.base_point()
        y0 = self.base_lift()[0]  # c-cycles always start on sheet 0
        gamma = RiemannSurfacePath(self, (x0,y0), path_segments=path_segments)

        return gamma


    def integrate(self, omega, x, y, path):
        """
        Integrates the differential `omega`, defined on the
        Riemann surface, on the RiemannSurfacePath `path`.
        
        Input:

        - `omega,x,y`: a Sympy funciton in the variables `x` and `y`

        - `path`: a RiemannSurfacePath defined on the Riemann surface
        """
        x0,y0 = path(0)
        omega = sympy.lambdify((x,y), omega, "numpy")
        
        # Numerically integrate over each path segment. This is most
        # probably a good idea since it allows for good checkpointing.
        def integrand(t,omega,path):
            (xi,yi),dxdt = path(t, dxdt=True)
            return omega(xi,yi) * dxdt

        val = numpy.double(0)
        n   = numpy.int(path._num_path_segments)
        for k in xrange(n):
#             val += sympy.mpmath.quadgl(lambda t: integrand(t,omega,path), 
#                                        [k/n,(k+1)/n])
#             val_real += scipy.integrate.quad(
#                 lambda t: scipy.real(integrand(t,omega,path)),
#                 k/n,(k+1)/n
#                 )

#             val_imag += scipy.integrate.quad(
#                 lambda t: scipy.imag(integrand(t,omega,path)),
#                 k/n,(k+1)/n
#                 )
        
#         return val_real + 1.0j*val_imag
            k = numpy.double(k)
            tpts = numpy.linspace(k/n,(k+1)/n,512)
            fpts = [integrand(tpt,omega,path) for tpt in tpts]
            val += scipy.integrate.trapz(tpts,fpts)

        return val


    def period_matrix(self):
        """
        Returns the period matrix `\tau = (A \; B)` where `A_{ij}` is
        the integral of the `j`th holomorphic differential basis element
        about the cycle `a_i`. (`B` is defined in the same way about the 
        `b`-cycles.)

        Note: this function computes the integrals of the
        differentials over each of the c-cycles and then uses the
        homology data to determine which linear combination of
        c-cycles integrals gives the a- and b-cycles integrals.
        """
        lincombs = self.homology()['linearcombination']
        n_cycles = len(self.homology()['cycles'])
        c_cycles = [self.c_cycle(i) for i in range(n_cycles)]
        differentials = self.holomorphic_differentials()
        g = self.genus()
        x = self.x
        y = self.y

        # XXX temporary...still need to figure out good way to do
        # this...
        A = []
        B = []
        for i in xrange(g):
            omega = differentials[i]
            Ai = []
            Bi = []
            for j in xrange(g):
                lincomb  = lincombs[j]
                # XXX check that len(lincomb) == n_cycles
                integral = sum(
                    lincomb[k]*self.integrate(omega,x,y,c_cycles[k]) 
                    for k in xrange(n_cycles) if lincomb[k] != 0
                    )
                Ai.append(integral)

                lincomb  = lincombs[j+g]
                integral = sum(
                    lincomb[k]*self.integrate(omega,x,y,c_cycles[k]) 
                    for k in xrange(n_cycles) if lincomb[k] != 0
                    )
                Bi.append(integral)

            A.append(Ai)
            B.append(Bi)

        # need to transpose...?
        return (A,B)


    def show_paths(self):
        """
        """
        G = self.monodromy_graph()
        show_paths(G)



if __name__ == '__main__':
    from sympy.abc import x,y

    f0 = y**3 - 2*x**3*y - x**8  # Klein curve

    f1 = (x**2 - x + 1)*y**2 - 2*x**2*y + x**4
    f2 = -x**7 + 2*x**3*y + y**3
    f3 = (y**2-x**2)*(x-1)*(2*x-3) - 4*(x**2+y**2-2*x)**2
    f4 = y**2 + x**3 - x**2
    f5 = (x**2 + y**2)**3 + 3*x**2*y - y**3
    f6 = y**4 - y**2*x + x**2   # case with only one finite disc pt
    f7 = y**3 - (x**3 + y)**2 + 1
    f8 = (x**6)*y**3 + 2*x**3*y - 1
    f9 = 2*x**7*y + 2*x**7 + y**3 + 3*y**2 + 3*y
    f10= (x**3)*y**4 + 4*x**2*y**2 + 2*x**3*y - 1  # genus 3

    f11= y**2 - x*(x-1)*(x-2)*(x-3)  # simple genus one hyperelliptic


    f = f2
    X = RiemannSurface(f,x,y)


