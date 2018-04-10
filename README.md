## Description

Interface for reading atomic and molecular line lists. Right now just APOGEE, 15000-17000 angstroms.

## Databases

**NIST** ([download](https://physics.nist.gov/PhysRefData/ASD/lines_form.html)): atomic lines

**HITEMP** ([download](ftp://cfa-ftp.harvard.edu/pub/HITEMP-2010/), [paper](https://www.cfa.harvard.edu/atmosphere/publications/2010-HITEMP-JQSRT-111.pdf)): molecular lines H2O, CO2, CO, NO, and OH

**APOGEE** ([download](https://zenodo.org/record/32629#.Vi0XBBCrSfS), [paper](https://arxiv.org/abs/1502.04080)): atomic and molecular lines

## Usage


	import interface
	from interface import searchLines

	interface.listLibraries()
	
	interface.listSpecies('APOGEE_ATOMS')

Search a wavelegth region for certain species of atoms/molecules (returns a dictionary):

	lines = searchLines(species=['OH', 'Fe I'], libraries=['NIST', 'APOGEE_ATOMS', 'APOGEE_MOLEC'], range=[15200,15300])
