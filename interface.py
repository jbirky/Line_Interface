import numpy as np
import pandas as pd
import os
import h5py
from itertools import chain

PATH = os.path.realpath(__file__)
PARENT = os.path.split(PATH)[0]


def listLibraries():

	lib_list = [x.strip('.hdf5') for x in os.listdir(PARENT + '/compressed')]
	lib_list.append('NIST')

	return lib_list


def listSpecies(lib):

	hf = h5py.File(PARENT + '/compressed/' + lib + '.hdf5', 'r')
	species = list(hf.keys())
	hf.close()

	return species


def searchLines(**kwargs):

    species = kwargs.get('species')
    rng = kwargs.get('range') #units assumed angstroms
    libraries = kwargs.get('lib', 'APOGEE_ATOMS')

    line_dict = dict([(key, []) for key in species])

    for lib in libraries:
        
        if lib != 'NIST':

            fname = PARENT + '/compressed/' + lib + '.hdf5'
            print('Searching library', fname)

            hf = h5py.File(fname, 'r')
            hf_keys = [k.upper() for k in hf.keys()]

            for spec in line_dict.keys():

                spec = spec.upper()
                if spec in hf_keys:
                    spec_lines = np.array(hf[spec])
                    range_indx = np.where((spec_lines > rng[0]) & (spec_lines < rng[1]))[0]

                    if len(range_indx) != 0:
                        line_dict[spec].append(spec_lines[range_indx])

            hf.close()

    if 'NIST' in libraries:
        
        from astroquery.nist import Nist
        import astropy.units as u
        
        print('Searching NIST library.')
        
        for spec in species:
            try:
                search = Nist.query(rng[0] * u.AA, rng[1] * u.AA, linename=spec)

                spec_lines = np.array(search['Ritz'])
                if len(spec_lines) != 0:
                    line_dict[spec].append(spec_lines)
                
            except:
                print(spec, 'not found in NIST.')
       
    # Flatten lists in line dictionary
    for key in line_dict.keys():
        line_dict[key] = np.array(list(chain(*line_dict[key])))

    return line_dict