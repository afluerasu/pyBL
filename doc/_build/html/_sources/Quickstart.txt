Quickstart
============

Step 1:Modify pyBL.conf
-------------------------------------

Inside ~/pyBL/ locate pyBL.conf that looks like:

[diffractometer_config]

name=X11

geometry=SixCircle

engine=you

tag=default_tag

author=pyBL

pv1=test:m1

pv2=test:m2

pv3=test:m3

pv4=test:m4

pv5=test:m5

pv6=test:m6

Replace the process variable names with corresponding EPICS motor record PVs.If you do not have these PVs and would like to run a simulated version, please refer to **Installation** section of this documentation.

Step 2:Start the Command Line Interface
----------------------------------------

**$./runPyBL**

An IPython command-line will appear as you execute the above command. If there are no warnings or errors, you can go ahead and start a reciprocal space calculation and move some motors. This tutorial also shows how to write a sample scan. Unlike mainstream XRay diffraction experiment control softwares, this API provides powerful python scripting capability and simulatenous motor motion allowing users to write more complex applications that users were not able to perform before. 

Step 3:Perform a New Reciprocal Space Calculation
-----------------------------------------------

**Define new UB calculation and set lattice parameters**

.. highlights::

In [1]: position()

mu: 0.0

delta: 0.0

nu: 0.0

eta: 0.0

chi: 0.0

phi: 0.0

In [3]: setAngles(['mu','delta','gam','eta','chi','phi'])

In [4]: hardware()

Dummy:

  energy : 12.39842 keV

  wavelength : 1.0 Angstrom

  mu : 0.0 deg

  delta : 0.0 deg

  gam : 0.0 deg

  eta : 0.0 deg

  chi : 0.0 deg

  phi : 0.0 deg


In [5]:wavelength()

1.0

In [7]: energy()

12.39842

Out[7]: 12.39842

In [8]: hardware()

Dummy:

  energy : 12.39842 keV

  wavelength : 1.0 Angstrom

  mu : 0.0 deg

  delta : 0.0 deg

  gam : 0.0 deg

  eta : 0.0 deg

  chi : 0.0 deg

  phi : 0.0 deg


In [9]: help(ub)


In [10]: newub('test')

In [11]: setlat('cubic',1,1,1,90,90,90)

In [12]: ub()

UBCALC

   name:          test

CRYSTAL

   name:         cubic

   a, b, c:    1.00000   1.00000   1.00000

              90.00000  90.00000  90.00000

   B matrix:   6.28319  -0.00000  -0.00000

               0.00000   6.28319  -0.00000

               0.00000   0.00000   6.28319

UB MATRIX

   <<< none calculated >>>

REFLECTIONS

   <<< none specified >>>

In [13]: c2th([1, 0, 0])  

60.0

In [14]: position(delta=60,eta=30)

{'eta': 30, 'delta': 60}

[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

Dummy:

  energy : 12.39842 keV

  wavelength : 1.0 Angstrom

  mu : 0.0 deg

  delta : 0.0 deg

  gam : 0.0 deg

  eta : 0.0 deg

  chi : 0.0 deg

  phi : 0.0 deg


In [15]: hardware()

Dummy:

  energy : 12.39842 keV

  wavelength : 1.0 Angstrom


  mu : 0.0 deg

  delta : 3.5 deg

  gam : 0.0 deg

  eta : 3.5 deg

  chi : 0.0 deg

  phi : 0.0 deg


In [16]: hardware()

Dummy:

  energy : 12.39842 keV

  wavelength : 1.0 Angstrom

  mu : 0.0 deg

  delta : 9.23 deg

  gam : 0.0 deg

  eta : 9.23 deg

  chi : 0.0 deg

  phi : 0.0 deg


In [17]: hardware()

Dummy:

  energy : 12.39842 keV

  wavelength : 1.0 Angstrom

  mu : 0.0 deg

  delta : 40.550000000000004 deg

  gam : 0.0 deg

  eta : 30.0 deg

  chi : 0.0 deg

  phi : 0.0 deg


In [18]: hardware()

Dummy:

  energy : 12.39842 keV

  wavelength : 1.0 Angstrom

  mu : 0.0 deg

  delta : 42.26 deg

  gam : 0.0 deg

  eta : 30.0 deg

  chi : 0.0 deg

  phi : 0.0 deg


In [19]: hardware()

Dummy:

  energy : 12.39842 keV

  wavelength : 1.0 Angstrom

  mu : 0.0 deg

  delta : 44.07 deg

  gam : 0.0 deg

  eta : 30.0 deg

  chi : 0.0 deg

  phi : 0.0 deg


In [20]: hardware()

Dummy:

  energy : 12.39842 keV

  wavelength : 1.0 Angstrom

  mu : 0.0 deg

  delta : 46.18 deg

  gam : 0.0 deg

  eta : 30.0 deg

  chi : 0.0 deg

  phi : 0.0 deg


In [21]: hardware()

Dummy:

  energy : 12.39842 keV

  wavelength : 1.0 Angstrom

  mu : 0.0 deg

  delta : 46.89 deg

  gam : 0.0 deg

  eta : 30.0 deg

  chi : 0.0 deg

  phi : 0.0 deg


In [22]: hardware()

Dummy:

  energy : 12.39842 keV

  wavelength : 1.0 Angstrom

  mu : 0.0 deg

  delta : 47.59 deg

  gam : 0.0 deg

  eta : 30.0 deg

  chi : 0.0 deg

  phi : 0.0 deg


In [23]: hardware()

Dummy:

  energy : 12.39842 keV

  wavelength : 1.0 Angstrom

  mu : 0.0 deg

  delta : 48.19 deg

  gam : 0.0 deg

  eta : 30.0 deg

  chi : 0.0 deg

  phi : 0.0 deg


In [24]: hardware()

Dummy:

  energy : 12.39842 keV

  wavelength : 1.0 Angstrom

  mu : 0.0 deg

  delta : 48.89 deg

  gam : 0.0 deg

  eta : 30.0 deg

  chi : 0.0 deg

  phi : 0.0 deg


In [25]: hardware()

Dummy:

  energy : 12.39842 keV

  wavelength : 1.0 Angstrom

  mu : 0.0 deg

  delta : 49.4 deg

  gam : 0.0 deg

  eta : 30.0 deg

  chi : 0.0 deg

  phi : 0.0 deg


In [26]: hardware()

Dummy:

  energy : 12.39842 keV

  wavelength : 1.0 Angstrom

  mu : 0.0 deg

  delta : 50.0 deg

  gam : 0.0 deg

  eta : 30.0 deg

  chi : 0.0 deg

  phi : 0.0 deg


In [27]: hardware()

Dummy:

  energy : 12.39842 keV

  wavelength : 1.0 Angstrom

  mu : 0.0 deg

  delta : 50.800000000000004 deg

  gam : 0.0 deg

  eta : 30.0 deg

  chi : 0.0 deg

  phi : 0.0 deg


In [35]: ub()
UBCALC

   name:          test

CRYSTAL

   name:         cubic

   a, b, c:    1.00000   1.00000   1.00000
              90.00000  90.00000  90.00000

   B matrix:   6.28319  -0.00000  -0.00000
               0.00000   6.28319  -0.00000
               0.00000   0.00000   6.28319

UB MATRIX

   <<< none calculated >>>

REFLECTIONS

   <<< none specified >>>

In [36]: c2th([1, 0, 0])  
60.0

In [37]: addref([1, 0, 0])

In [38]: c2th([0, 1, 0])
60.0

In [40]: addref([0, 1, 0], [0, 60, 0, 30, 0, 90], energy())

12.39842

Calculating UB matrix.

In [41]: ub()

UBCALC

   name:          test

CRYSTAL

   name:         cubic

   a, b, c:    1.00000   1.00000   1.00000

              90.00000  90.00000  90.00000

   B matrix:   6.28319  -0.00000  -0.00000

               0.00000   6.28319  -0.00000

               0.00000   0.00000   6.28319

UB MATRIX

   U matrix:   1.00000   0.00000   0.00000

              -0.00000   1.00000   0.00000

               0.00000   0.00000   1.00000

   UB matrix:  6.28319  -0.00000  -0.00000

              -0.00000   6.28319  -0.00000

               0.00000   0.00000   6.28319

REFLECTIONS

     ENERGY     H     K     L        MU    DELTA      GAM      ETA      CHI      PHI  TAG

   1 12.398  1.00  0.00  0.00    0.0000  60.0000   0.0000  30.0000   0.0000   0.0000  

   2 12.398  0.00  1.00  0.00    0.0000  60.0000   0.0000  30.0000   0.0000  90.0000  






In [43]: angles_to_hkl((0., 60., 0., 30., 0., 0.))

((0.99999999999999978, 2.2714035513571318e-17, 0.0), {'tau': 90.0, 'psi': 90.0, 'qaz': 90.0, 'beta': 3.5082387819463295e-15, 'alpha': -0.0, 'naz': 0.0, 'theta': 29.999999999999996})

In [44]: angles_to_hkl((0.0, 90.0, 0.0, 45.0, 0.0, 45.0), energy())

12.39842

((1.0000000000000002, 0.99999999999999989, 0.0), {'tau': 90.0, 'psi': 90.0, 'qaz': 90.0, 'beta': 4.961398865471767e-15, 'alpha': -0.0, 'naz': 0.0, 'theta': 45.0})

In [45]: con('qaz', 90)
!   2 more constraints required
    qaz: 90.0000

In [46]: con('a_eq_b')
!   1 more constraint required
    qaz: 90.0000
    a_eq_b

In [47]: con('mu', 0)
    qaz: 90.0000
    a_eq_b
    mu: 0.0000

In [48]: con()
    DET        REF        SAMP
    ======     ======     ======
    delta  --> a_eq_b --> mu
    gam        alpha      eta
--> qaz        beta       chi
    naz        psi        phi
                          mu_is_gam

    qaz: 90.0000
    a_eq_b
    mu: 0.0000

    Type 'help con' for instructions

In [50]: set_low_limit('delta', 0)

In [53]: hkl_to_angles(1, 0, 0,energy())
12.39842

((0.0, 60.00000000000001, 0.0, 30.000000000000004, 0.0, 0.0), {'tau': 90.0, 'psi': 90.0, 'qaz': 90.0, 'beta': 3.5082387819463303e-15, 'alpha': -0.0, 'naz': 0.0, 'theta': 30.000000000000004})

In [54]: hkl_to_angles(1, 0, 0,energy())

12.39842                                                                                                                                               

((0.0, 60.00000000000001, 0.0, 30.000000000000004, 0.0, 0.0), {'tau': 90.0, 'psi': 90.0, 'qaz': 90.0, 'beta': 3.5082387819463303e-15, 'alpha': -0.0, 'naz': 0.0, 'theta': 30.000000000000004})                                                                                                                
                                                                                                                                                       
In [55]: hkl_to_angles(1.4, 0, 0,energy())                                                                                                             

12.39842                                                                                                                                               

((0.0, 88.8540080016114, 0.0, 44.4270040008057, 0.0, 0.0), {'tau': 90.0, 'psi': 90.0, 'qaz': 90.0, 'beta': 4.911534294724862e-15, 'alpha': -0.0, 'naz': 0.0, 'theta': 44.4270040008057})              





