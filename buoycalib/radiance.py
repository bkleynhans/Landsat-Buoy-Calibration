import numpy
import pdb
from . import settings


def calc_ltoa_spectral(spec_ref, wavelengths, upwell_rad, gnd_reflect, transmission, skin_temp, water_file=settings.WATER_TXT):
    """
    Calculate modeled radiance for band 10 and 11.

    Args:
        modtran_data: modtran output, Units: [W cm-2 sr-1 um-1]
            upwell_rad, downwell_rad, wavelengths, transmission, gnd_reflect
        wavelengths: [microns]
        skin_temp: ground truth surface temperature

    Returns:
        spectral top of atmosphere radiance: Ltoa(lambda) [W m-2 sr-1 um-1]
    """
    # calculate temperature array (input units: [meters, Kelvin], output units: [W m-2 sr-1 um-1])
    # input wavelength units [microns -> meters]
    # output units [W m-2 sr-1 m-1] -> [W cm-2 sr-1 um-1]
    bb_rad = bb_radiance(wavelengths / 1e6, skin_temp) / (1e4 * 1e6)

    # Load Emissivity / Reflectivity
    spec_r_wvlens, spec_r = numpy.loadtxt(water_file, unpack=True, skiprows=3)
    
    # If emmissivity is supplied, use the supplied value, alternatively use the data file
    if spec_ref == None:
        spec_ref = numpy.interp(wavelengths, spec_r_wvlens, spec_r)
        
    spec_emis = 1 - spec_ref   # calculate emissivity
    
    # calculate spectral top of atmosphere radiance
    # Ltoa = (Lbb(T) * tau * emis) + (gnd_ref * reflect) + pth_thermal
    # units: [W cm-2 sr-1 um-1] --> [W m-2 sr-1 um-1]
    ltoa_spectral = 1e4 * ((upwell_rad) + (bb_rad * spec_emis * transmission) + (spec_ref * gnd_reflect))

    return ltoa_spectral


def calc_ltoa(wavelengths, ltoa, RSR_wavelengths, RSR):
    """
    Calculate radiance from spectral radiance and response curve of a sensor.

    Args:
        wavelengths: for LToa [um]
        ltoa: spectral top of atmosphere radiance [W m-2 sr-1 um-1]
        rsr_file: relative spectral response data to use

    Returns:
        radiance: L [W m-2 sr-1 um-1]
    """

    w = (wavelengths > RSR_wavelengths.min()) & (wavelengths < RSR_wavelengths.max())

    wvlens = wavelengths[w]
    ltoa_trimmed = ltoa[w]

    # upsample RSR to wavelength range
    RSR = numpy.interp(wvlens, RSR_wavelengths, RSR)

    # calculate observed radiance [ W m-2 sr-1 um-1 ]
    # trapz is a trapezoidal sum
    radiance = numpy.trapz(ltoa_trimmed * RSR, wvlens) / numpy.trapz(RSR, wvlens)

    return radiance


def bb_radiance(wvlen, temp):
    """
    Calculate spectral blackbody radiance.

    Args:
        wvlen: wavelengths to calculate blackbody at [meters]
        temp: temperature to calculate blackbody at [Kelvin]

    Returns:
        rad: [W m-2 sr-1 m-1]
    """
    # define constants
    c = 3e8   # speed of light, [m s-1]
    h = 6.626e-34   # [J*s = kg m2 s-1], planck's constant
    k = 1.38064852e-23   # [m2 kg s-2 K-1], boltzmann's constant

    rad = (2 * h * c**2) / ((wvlen**5) * (numpy.exp((h * c) / (k * temp * wvlen)) - 1))
    # units = [W sr−1 m−3], reference: https://en.wikipedia.org/wiki/Planck%27s_law

    return rad
