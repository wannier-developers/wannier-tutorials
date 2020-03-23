#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-
import argparse
from aiida import orm

def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser(
        description=
        "A script to plot the projectabilities distribution"
    )
    parser.add_argument(
        'pk',
        metavar='WORKCHAIN_PK',
        type=int,
        help="PK of Wannier90BandsWorkChain"
    )
    return parser.parse_args()
    
def erfc_scdm(x,mu,sigma):
    from scipy.special import erfc
    return 0.5*erfc((x-mu)/sigma)

def get_mu_and_sigma_from_projections(bands, projections, thresholds):
    import numpy as np

    def find_max(proj_list,max_value):
        f = lambda x : True if x<max_value else False
        bool_list = map(f,proj_list)
        for i,item in enumerate(bool_list):
            if item:
                break
        print(i, proj_list[i])

    def fit_erfc(f,xdata,ydata):
        from scipy.optimize import curve_fit
        return curve_fit(f, xdata, ydata,bounds=([-50,0],[50,50]))

    # List of specifications of atomic orbitals in dictionary form
    dict_list = [i.get_orbital_dict() for i in projections.get_orbitals()]
    # Sum of the projections on all atomic orbitals (shape kpoints x nbands)
    out_array = sum([sum([x[1] for x in projections.get_projections(
        **get_dict)]) for get_dict in dict_list])
    # Flattening (projection modulus squared according to QE, energies)
    projwfc_flat, bands_flat = out_array.flatten(), bands.get_bands().flatten()
    # Sorted by energy
    sorted_bands, sorted_projwfc = zip(*sorted(zip(bands_flat, projwfc_flat)))
    popt,pcov = fit_erfc(erfc_scdm,sorted_bands,sorted_projwfc)
    mu = popt[0]
    sigma = popt[1]
    # Temporary, TODO add check on interpolation
    success = True
    return mu, sigma, sorted_bands, sorted_projwfc

def isNode(NodeType):
    return lambda x: x.process_label == NodeType

def findNode(NodeType, NodeList):
    # return last one
    nodes = list(filter(isNode(NodeType), NodeList))
    nodes.sort(key=lambda x: x.pk)
    return nodes[-1]

if __name__ == "__main__":
    args = parse_arguments()
    wannier90bandsworkchain = orm.load_node(args.pk)
    formula = wannier90bandsworkchain.inputs.structure.get_formula()
    wannier90workchain = findNode('Wannier90WorkChain', wannier90bandsworkchain.called)

    wannier90calculation = findNode('Wannier90Calculation', wannier90workchain.called)
    fermi_energy = wannier90calculation.inputs.parameters['fermi_energy']

    pw2wannier90calculation = findNode('Pw2wannier90Calculation', wannier90workchain.called)
    sigma = pw2wannier90calculation.inputs.parameters['inputpp']['scdm_sigma']
    mu = pw2wannier90calculation.inputs.parameters['inputpp']['scdm_mu']

    projwfccalculation = findNode('ProjwfcCalculation', wannier90workchain.called)
    projections = projwfccalculation.outputs.projections

    print("{:6s}:".format(formula))
    print("        mu = {}, e_fermi = {}, sigma = {}".format(mu, fermi_energy, sigma))

    proj_bands = projwfccalculation.outputs.bands
    mu_fit, sigma_fit, sorted_bands, sorted_projwfc = get_mu_and_sigma_from_projections(proj_bands, projections, {'sigma_factor_shift': 0.})
    import pylab as pl
    pl.figure()
    pl.plot(sorted_bands, sorted_projwfc, 'o')
    pl.plot(sorted_bands, erfc_scdm(sorted_bands, mu_fit, sigma_fit))
    pl.axvline([mu_fit], color='red', label=r"$\mu$")
    pl.axvline([mu_fit - 3. * sigma_fit], color='orange', label=r"$\mu-3\sigma$")
    pl.axvline([fermi_energy], color='green', label=r"$E_f$")
    pl.title(formula)
    pl.xlabel('Energy [eV]')
    pl.ylabel('Projectability')
    pl.legend(loc='best')
    pl.savefig('{}_proj.png'.format(formula))

