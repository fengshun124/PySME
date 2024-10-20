# Changelog

This page storages the change log for pysme since May 2024.

## In-development

- New readthedocs theme (alabaster -> sphinx_book_theme).
- New NLTE grids

## In github-repo

- (synthesize) fix the vstep issue when synthesizing sparce spectrum.
- (nlte) add ResetDepartureCoefficients function to ensure correct NLTE calculation
- (solve) use 'vrad' instead of 'v_rad' for the radial velocity fitting.
- (solve) add dynamic parameter function; sme parameter can changes according to other parameters while not being included in the fitting.

## v0.4.180

- fix mask bug. The continuum fitting function is now available.

## v0.4.179

- Add line depth result to sme_structure.
- Add line range result to sme_structure.
- Support python 3.12.
- Support new VALD3 line format.