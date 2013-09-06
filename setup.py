from distutils.core import setup
import os
os.environ['EPICS_BASE']='/usr/lib/epics'
os.system('echo $EPICS_BASE')
os.system('ipython --version ')
os.system('cp -rf ~/pyBL/profile_arman $HOME/.config/ipython/')
#os.system('ipython --version ')
os.system('cp -rf ~/pyBL/pyOlog.conf $HOME/')
os.system('cp -rf $HOME/pyBL/pyBL.conf $HOME/')

setup(name='pyBL',
      version='0.1.0',
      description='Python scripting environment for XRD Beamlines',
      author='Arman Arkilic',
      author_email='arkilic@bnl.gov',
      packages=['pyBL']
     )

setup(name='pyOlog',
      version='0.1.0',
      description='Python Olog Client Lib',
      author='Kunal Shroff',
      author_email='shroffk@bnl.gov',
      packages=['pyOlog']
     )

setup(name='diffcalc',
      version=' ',
      description='Reciprocal space calculation library',
      author='Arman Arkilic',
      author_email='arkilic@bnl.gov',
      packages=['diffcalc']
     )

                                                                                      
                                                                                              
                                                                                              
            
