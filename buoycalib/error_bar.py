import numpy
import pdb
import datetime, sys

from . import (modtran, atmo, sat, radiance, settings)
from .atmo import merra


def error_bar(spec_ref, scene_id, buoy_id, skin_temp, skin_temp_std, overpass_date, buoy_lat, buoy_lon, rsrs, bands, shared_args):
    atmos = merra.error_bar_atmos(overpass_date, buoy_lat, buoy_lon, shared_args)

    modeled_ltoas = {b:[] for b in bands}
    for temp in [skin_temp+skin_temp_std, skin_temp-skin_temp_std]:
        for i, atmo in enumerate(atmos):

            modtran_directory = '{0}/{1}_{2}_{3}_{4}'.format(settings.MODTRAN_BASH_DIR, scene_id, buoy_id, temp, i)
            
#            wavelengths, upwell_rad, gnd_reflect, transmission = modtran.process(atmo, buoy_lat, buoy_lon, overpass_date, modtran_directory, temp)
            modtran_data = modtran.process(atmo, buoy_lat, buoy_lon, overpass_date, modtran_directory, temp)
            mod_ltoa_spectral = radiance.calc_ltoa_spectral(spec_ref, modtran_data['wavelengths'], modtran_data['upwell_rad'], modtran_data['gnd_reflect'], modtran_data['transmission'], temp)

            for b in bands:
                if scene_id[0:3] == 'MOD':
                    RSR_wavelengths, RSR = sat.modis.load_rsr(rsrs[b])
                elif scene_id[0:3] in ('LC8', 'LC0'):
                    RSR_wavelengths, RSR = numpy.loadtxt(rsrs[b], unpack=True)

                modeled_ltoas[b].append(radiance.calc_ltoa(modtran_data['wavelengths'], mod_ltoa_spectral, RSR_wavelengths, RSR))

    error = {b:numpy.asarray(modeled_ltoas[b]).std() for b in modeled_ltoas}
    return error
