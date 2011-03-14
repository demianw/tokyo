#!/usr/bin/env python

# from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

from numpy.distutils.core import setup
from numpy.distutils.misc_util import Configuration
from numpy.distutils.system_info import get_info

blas_info = get_info('blas_opt', 0)

import numpy as np

ext_params = {}
'''
ext_params['include_dirs'] = [
    '/usr/include',
    '/System/Library/Frameworks/vecLib.framework/Versions/A/Headers',
    np.get_include()]
ext_params['extra_compile_args'] = ["-O2"]
ext_params['extra_link_args'] = ["-Wl,-O1", "-Wl,--as-needed"]  # TODO: as-needed
'''

ext_params['extra_compile_args'] = blas_info.get('extra_compile_args')
ext_params['extra_link_args'] = blas_info.get('extra_link_args')

# ignored due to parameter order bug in distutils (when calling linker)

tokyo_ext_params = ext_params.copy()
'''

tokyo_ext_params['libraries'] = ['blas']  # TODO: detect library name.
    # Candidates: blas, cblas, lapack, lapack_atlas, atlas
    # On OSX, blas points to the Accelerate framework's ATLAS library.
tokyo_ext_params['library_dirs'] = ['/usr/lib']  # needed by OSX, perhaps
'''

def configuration(parent_package='', top_path=None):
    config = Configuration(None, parent_package, top_path)

    ext_kwds = {'include_dirs' : [np.get_include()],
                'extra_info' : blas_info}

    config.add_extension('tokyo', sources=['tokyo.pyx'], **ext_kwds)
    config.add_extension('verify', sources=['verify.pyx'], **ext_kwds)
    config.add_extension('single_speed', sources=['single_speed.pyx'],
                         **ext_kwds)
    config.add_extension('double_speed', sources=['double_speed.pyx'],
                         **ext_kwds)
    config.add_extension('demo_outer', sources=['demo_outer.pyx'], **ext_kwds)

    return config

'''
ext_modules = [
    Extension("tokyo",        ["tokyo.pyx"],        **tokyo_ext_params),
    Extension("verify",       ["verify.pyx"],       **ext_params),
    Extension("single_speed", ["single_speed.pyx"], **ext_params),
    Extension("double_speed", ["double_speed.pyx"], **ext_params),
    Extension("demo_outer",   ["demo_outer.pyx"],   **ext_params)
]
'''

setup(
    #name='BLAS and LAPACK wrapper',
    name='BLAS wrapper',
    cmdclass={'build_ext': build_ext},
    configuration=configuration,
    # ext_modules=ext_modules,
)
