import io
import gzip
import tarfile

import pytest


STATES_SHAPEFILE = (
    "https://www2.census.gov/geo/tiger/TIGER2020/STATE/tl_2020_us_state.zip"
)
IANA_TIMEZONES = "https://data.iana.org/time-zones/releases/tzdata2022c.tar.gz"


def timezones():
    import iso6709
    import requests

    timezone_gz = io.BytesIO()
    for chunk in requests.get(IANA_TIMEZONES).iter_content():
        timezone_gz.write(chunk)
    timezone_gz.seek(0)

    gz_fd = gzip.open(timezone_gz)
    tar_fd = tarfile.open(fileobj=gz_fd, format=tarfile.GNU_FORMAT)

    for line in tar_fd.extractfile("zone.tab"):
        if not line.startswith(b"US"):
            continue
        _, coords, tz_name, _ = line.split(b"\t")
        coords = iso6709.Location(coords.decode("ASCII"))
        tz_name = tz_name.decode("ASCII")

        yield (tz_name, coords.lat.decimal, coords.lng.decimal)


@pytest.mark.skipif("not config.getoption('timezone')")
def test_timezone():
    import us.states

    import geopandas as gpd

    state_df = gpd.read_file(STATES_SHAPEFILE)

    timezone_df = gpd.GeoDataFrame().from_records(
        timezones(), columns=["timezone", "lat", "lng"], coerce_float=True
    )
    timezone_df.geometry = gpd.points_from_xy(timezone_df.lng, timezone_df.lat)
    timezone_df: gpd.GeoDataFrame = timezone_df.drop(columns=["lat", "lng"])
    timezone_df = timezone_df.set_crs(crs="EPSG:4326")  # probably?
    timezone_df = timezone_df.to_crs(state_df.crs)

    joined_df = gpd.sjoin(timezone_df, state_df, how="inner", op="within")

    for row in joined_df[["timezone", "STATEFP"]].itertuples(index=False, name=None):
        timezone_name, state_fips = row
        state_obj = us.states.lookup(state_fips, field="fips")
        assert timezone_name in state_obj.time_zones
