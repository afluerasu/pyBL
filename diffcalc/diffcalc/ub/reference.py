from math import pi

try:
    from numpy import matrix, hstack
    from numpy.linalg import norm
except ImportError:
    from numjy import matrix, hstack
    from numjy.linalg import norm

SMALL = 1e-7
TODEG = 180 / pi



class YouReference(object):
    
    def __init__(self, ubcalc):
        self._ubcalc = ubcalc
        self._n_phi_configured = None
        self._n_hkl_configured = None
        self._set_n_phi_configured(matrix('0; 0; 1'))
    
    def _set_n_phi_configured(self, n_phi):
        self._n_phi_configured = n_phi
        self._n_hkl_configured = None
    
    def _get_n_phi_configured(self):
        return self._n_phi_configured
    
    n_phi_configured = property(_get_n_phi_configured, _set_n_phi_configured)
                    
    def _set_n_hkl_configured(self, n_hkl):
        self._n_phi_configured = None
        self._n_hkl_configured = n_hkl
        
    def _get_n_hkl_configured(self):
        return self._n_hkl_configured
    
    n_hkl_configured = property(_get_n_hkl_configured, _set_n_hkl_configured)
    
    @property
    def n_phi(self):
        n_phi = (self._ubcalc.UB * self._n_hkl_configured if self._n_phi_configured is None 
                 else self._n_phi_configured)
        return n_phi / norm(n_phi)
        
    @property
    def n_hkl(self):
        n_hkl = (self._ubcalc.UB.I * self._n_phi_configured if self._n_hkl_configured is None
                  else self._n_hkl_configured) 
        return n_hkl / norm(n_hkl)
    
    def _pretty_vector(self, m):
        return ', '.join(['%.5f' % e for e in m.T.tolist()[0]])
        
    def __str__(self):
        lines = []
        if self._n_phi_configured is not None:
            lines.append("configured n_phi: " + self._pretty_vector(self._n_phi_configured))
        elif self._n_hkl_configured is not None:
            lines.append("configured n_hkl: " + self._pretty_vector(self._n_hkl_configured))
        else:
            raise AssertionError("Neither a manual n_phi nor n_hkl is configured")
        lines.append("           n_phi: " + self._pretty_vector(self.n_phi))
        lines.append("           n_hkl: " + self._pretty_vector(self.n_hkl))
        lines.append("")
        lines.append("To change: set n_hkl_configured or n_phi_configured property.")
        return '\n'.join(lines)
    
    def __repr__(self):
        return self.__str__()
