""" Minimum working example of an SME script 
"""

from os.path import dirname, realpath, join
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import readsav

from pysme import sme as SME
from pysme import util
from pysme.solve import solve
from pysme.synthesize import synthesize_spectrum

from pysme.abund import Abund
from pysme.linelist.vald import ValdFile
from pysme.persistence import save_as_idl

if __name__ == "__main__":
    # Define the location of all your files
    # this will put everything into the example dir
    target = "sun"
    examples_dir = join(dirname(realpath(__file__)), "..")
    in_file = join(examples_dir, "sun_6440_test.inp")
    out_file = join(examples_dir, f"{target}.sme")
    plot_file = join(examples_dir, f"{target}.html")
    log_file = join(examples_dir, f"{target}.log")

    # Start the logging to the file
    util.start_logging(log_file)

    # Load your existing SME structure or create your own
    sme = SME.SME_Structure.load(in_file)
    sme.nmu = 7
    sme.teff = 5770
    sme.logg = 4.4
    sme.abund = Abund(0, "asplund2009")
    sme.vmic = 1
    sme.vmac = 2
    sme.vsini = 2

    sme.atmo.source = "marcs2014.sav"
    sme.linelist = ValdFile(join(examples_dir, "sun.lin"))

    # Start SME solver
    sme.cscale = None
    sme.vrad_flag = "whole"

    continuum = {}
    x = sme.wave[0] - sme.wave[0][0]
    # Mask linear
    sme.cscale_type = "mask"
    sme.cscale_flag = "linear"
    sme.cscale = None
    sme.vrad = None
    sme = synthesize_spectrum(sme)
    continuum["mask+linear"] = np.polyval(sme.cscale[0], x)
    # Mask quadratic
    sme.cscale_type = "mask"
    sme.cscale_flag = "quadratic"
    sme.cscale = None
    sme.vrad = None
    sme = synthesize_spectrum(sme)
    continuum["mask+quadratic"] = np.polyval(sme.cscale[0], x)
    # Match linear
    sme.cscale_type = "match"
    sme.cscale_flag = "linear"
    sme.cscale = None
    sme.vrad = None
    sme = synthesize_spectrum(sme)
    continuum["match+linear"] = np.polyval(sme.cscale[0], x)
    # Match quadratic
    sme.cscale_type = "match"
    sme.cscale_flag = "quadratic"
    sme.cscale = None
    sme.vrad = None
    sme = synthesize_spectrum(sme)
    continuum["match+quadratic"] = np.polyval(sme.cscale[0], x)
    # Match+Mask linear
    sme.cscale_type = "match+mask"
    sme.cscale_flag = "linear"
    sme.cscale = None
    sme.vrad = None
    sme = synthesize_spectrum(sme)
    continuum["match+mask+linear"] = np.polyval(sme.cscale[0], x)
    # Match+Mask quadratic
    sme.cscale_type = "match+mask"
    sme.cscale_flag = "quadratic"
    sme.cscale = None
    sme.vrad = None
    sme = synthesize_spectrum(sme)
    continuum["match+mask+quadratic"] = np.polyval(sme.cscale[0], x)
    # Match+Mask quadratic
    sme.cscale_type = "match+mask"
    sme.cscale_flag = "quadratic"
    sme.cscale = None
    sme.vrad = None
    sme = synthesize_spectrum(sme)
    continuum["match+mask+quadratic"] = np.polyval(sme.cscale[0], x)
    # Spline
    sme.cscale_type = "spline"
    sme.cscale_flag = 2
    sme.cscale = None
    sme = synthesize_spectrum(sme)
    continuum["spline"] = sme.cscale[0]
    # Spline+Mask
    sme.cscale_type = "spline+mask"
    sme.cscale_flag = 2
    sme.cscale = None
    sme.vrad = None
    sme = synthesize_spectrum(sme)
    continuum["spline+mask"] = sme.cscale[0]
    # MCMC
    # sme.cscale_type = "mcmc"
    # sme.cscale_flag = "linear"
    # sme.cscale = None
    # sme.vrad = None
    # sme = synthesize_spectrum(sme)
    # continuum["mcmc+linear"] = np.polyval(sme.cscale[0], x)

    # Add last calculate the spectrum without continuum correction
    sme.cscale_type = "mask"
    sme.cscale_flag = "none"
    sme = synthesize_spectrum(sme)

    # Plot results
    for label, cont in continuum.items():

        plot_file = join(dirname(__file__), f"images/continuum_{label}.png")
        plt.plot(sme.wave[0], sme.spec[0], label="Observation")
        plt.plot(sme.wave[0], sme.synth[0], label="Synthetic")
        plt.fill_between(
            sme.wave[0],
            0,
            sme.spec[0],
            where=sme.mask[0] == 1,
            label="Mask Line",
            facecolor="#bcbd22",
            alpha=1,
        )

        m = sme.mask[0] == 2
        m[1:] = m[:-1] | m[1:]
        m[:-1] = m[:-1] | m[1:]
        plt.fill_between(
            sme.wave[0],
            0,
            sme.spec[0],
            where=m,
            label="Mask Continuum",
            facecolor="#d62728",
            alpha=1,
        )

        plt.plot(sme.wave[0], cont, label=f"{label} Continuum")
        plt.plot(sme.wave[0], sme.synth[0] * cont, label=f"{label} Corrected")

        plt.legend(loc="upper left", fontsize="small")
        plt.xlabel("Wavelength [Å]")
        plt.ylabel("Flux [A.U.]")
        # plt.ylim(0.9925, 1.01)
        plt.savefig(plot_file)
        # plt.show()
        plt.clf()

    # plot_file = join(dirname(__file__), "images/continuum_2.png")
    # plt.plot(sme.wave[0], sme.spec[0], label="Observation")
    # plt.plot(sme.wave[0], sme.synth[0], label="Synthetic")
    # plt.fill_between(
    #     sme.wave[0],
    #     0,
    #     sme.spec[0],
    #     where=sme.mask[0] == 1,
    #     label="Mask Line",
    #     facecolor="#bcbd22",
    #     alpha=1,
    # )

    # m = sme.mask[0] == 2
    # m[1:] = m[:-1] | m[1:]
    # m[:-1] = m[:-1] | m[1:]
    # plt.fill_between(
    #     sme.wave[0],
    #     0,
    #     sme.spec[0],
    #     where=m,
    #     label="Mask Continuum",
    #     facecolor="#d62728",
    #     alpha=1,
    # )

    # for label, cont in continuum.items():
    #     plt.plot(sme.wave[0], sme.synth[0] * cont, label=label)
    # plt.legend(loc="lower right", fontsize="small")
    # plt.xlabel("Wavelength [Å]")
    # plt.ylabel("Flux [A.U.]")
    # plt.ylim(0.9925, 1.004)
    # plt.savefig(plot_file)
    # plt.show()

    pass
