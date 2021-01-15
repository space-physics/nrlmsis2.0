from pathlib import Path
import shutil
import subprocess
import importlib.resources
import os
from datetime import datetime
import typing as T
import xarray
import numpy as np

from .timeutils import todatetime
import geomagindices as gi

species = ["He", "O", "N2", "O2", "Ar", "Total", "H", "N", "AnomalousO"]
ttypes = ["Texo", "Tn"]
first = True


def run(
    time: datetime, altkm: float, glat: float, glon: float, indices: T.Dict[str, T.Any] = None
) -> xarray.Dataset:
    """
    This is the "atomic" function looped by other functions
    """
    time = todatetime(time)
    # %% get solar parameters for date
    if not indices:
        indices = gi.getApF107(time, smoothdays=81).squeeze()
    # %% dimensions
    altkm = np.atleast_1d(altkm)
    if altkm.ndim != 1:
        raise ValueError("altitude read incorrectly")
    if not isinstance(glon, (int, float, np.int32, np.int64)):
        raise TypeError("single longitude only")
    if not isinstance(glat, (int, float, np.int32, np.int64)):
        raise TypeError("single latitude only")

    # %%
    iyd = time.strftime("%y%j")
    altkm = np.atleast_1d(altkm)
    # %%
    dens = np.empty((altkm.size, len(species)))
    temp = np.empty((altkm.size, len(ttypes)))
    # %% build on run
    exe_name = "msis2driver"
    if os.name == "nt":
        exe_name += ".exe"
    if not importlib.resources.is_resource(__package__, exe_name):
        with importlib.resources.path(__package__, "CMakeLists.txt") as setup_file:
            cmake(setup_file.parent)
    if not importlib.resources.is_resource(__package__, exe_name):
        raise RuntimeError("could not build MSIS 2.0 Fortran driver")

    if not importlib.resources.is_resource(__package__, "msis20.parm"):
        raise FileNotFoundError("could not find msis20.parm")

    with importlib.resources.path(__package__, exe_name) as exe:
        for i, a in enumerate(altkm):
            cmd = [
                str(exe),
                iyd,
                str(time.hour),
                str(time.minute),
                str(time.second),
                str(glat),
                str(glon),
                str(indices["f107s"]),
                str(indices["f107"]),
                str(indices["Ap"]),
                str(a),
            ]

            ret = subprocess.run(
                cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=exe.parent
            )

            if ret.returncode != 0:
                raise RuntimeError(f"MSIS 2.0 error code {ret.returncode}\n{ret.stderr}")
            # different compilers throw in extra \n
            raw = list(map(float, ret.stdout.split()))
            if not len(raw) == 9 + 2:
                raise ValueError(ret)
            dens[i, :] = raw[:9]
            temp[i, :] = raw[9:]

    dsf = {
        k: (("time", "alt_km", "lat", "lon"), v[None, :, None, None])
        for (k, v) in zip(species, dens.T)
    }
    dsf.update(
        {
            "Tn": (("time", "alt_km", "lat", "lon"), temp[:, 1][None, :, None, None]),
            "Texo": (("time", "alt_km", "lat", "lon"), temp[:, 0][None, :, None, None]),
        }
    )

    atmos = xarray.Dataset(
        dsf,
        coords={"time": [time], "alt_km": altkm, "lat": [glat], "lon": [glon]},
        attrs={
            "species": species,
            "f107s": indices["f107s"],
            "f107": indices["f107"],
            "Ap": indices["Ap"],
        },
    )

    return atmos


def cmake(src: Path):
    """
    attempt to build using CMake
    """

    exe = shutil.which("cmake")
    if not exe:
        raise FileNotFoundError("CMake not available")

    build = src / "build"

    subprocess.check_call([exe, f"-S{src}", f"-B{build}", "-DBUILD_TESTING:BOOL=off"])
    subprocess.check_call([exe, "--build", str(build)])

    exe_name = "msis2driver"
    if os.name == "nt":
        exe_name += ".exe"
    if not importlib.resources.is_resource(__package__, exe_name):
        raise RuntimeError("could not build MSIS 2.0 Fortran driver")
