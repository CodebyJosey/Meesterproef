import datetime
from catch import Catch


def test_get_weight_in_local_units_mm() -> None | AssertionError:
    dt: datetime.datetime = datetime.datetime(2023, 5, 15, 18, 0)
    catch = Catch(id=1, fish=12345, contestant=67890, caught_at=dt, latitude=52.370216,
                  longitude=4.895168, country_code="MM", weight=10139, length=50)

    pound = f"{catch.weight / 453.592:.2f}"
    viss = f"{catch.weight / 1600:.2f}"
    assert catch.get_weight_in_local_units() == f"{pound} Pound, {viss} Viss"


def test_get_weight_in_local_units_gb() -> None | AssertionError:
    dt: datetime.datetime = datetime.datetime(2023, 5, 15, 18, 0)
    catch = Catch(id=1, fish=12345, contestant=67890, caught_at=dt, latitude=52.370216,
                  longitude=4.895168, country_code="GB", weight=2874383, length=50)

    pound = f"{catch.weight / 453.592:.2f}"
    stone = f"{catch.weight / 6350.29:.2f}"
    assert catch.get_weight_in_local_units() == f"{pound} Pound, {stone} Stone"


def test_get_weight_in_local_units_kh() -> None | AssertionError:
    dt: datetime.datetime = datetime.datetime(2023, 5, 15, 18, 0)
    catch = Catch(id=1, fish=12345, contestant=67890, caught_at=dt, latitude=52.370216,
                  longitude=4.895168, country_code="KH", weight=38473.323, length=50)

    pound = f"{catch.weight / 453.592:.2f}"
    kilogram = f"{catch.weight / 1000:.2f}"
    assert catch.get_weight_in_local_units() == f"{pound} Pound, {kilogram} Kilogram"


def test_get_weight_in_local_units_bs() -> None | AssertionError:
    dt: datetime.datetime = datetime.datetime(2023, 5, 15, 18, 0)
    catch = Catch(id=1, fish=12345, contestant=67890, caught_at=dt, latitude=52.370216,
                  longitude=4.895168, country_code="BS", weight=4985738.39, length=50)

    pound = f"{catch.weight / 453.592:.2f}"
    ounce = f"{catch.weight / 28.3495:.2f}"
    assert catch.get_weight_in_local_units() == f"{pound} Pound, {ounce} Ounce"


def test_get_weight_in_local_units_nl() -> None | AssertionError:
    dt: datetime.datetime = datetime.datetime(2023, 5, 15, 18, 0)
    catch = Catch(id=1, fish=12345, contestant=67890, caught_at=dt, latitude=52.370216,
                  longitude=4.895168, country_code="NL", weight=4985738.39, length=50)

    gram = f"{catch.weight:.2f}"
    kilogram = f"{catch.weight / 1000:.2f}"
    assert catch.get_weight_in_local_units() == f"{gram} Gram, {kilogram} Kilogram"


def test_get_day_part_night() -> None | AssertionError:
    night_dt: datetime.datetime = datetime.datetime(year=2025, month=1, day=14, hour=0, minute=0)
    night_dt_2: datetime.datetime = datetime.datetime(year=2025, month=1, day=14, hour=5, minute=59, second=59)

    night_catch: Catch = Catch(id=1, fish=12345, contestant=67890, caught_at=night_dt, latitude=52.370216,
                               longitude=4.895168, country_code="US", weight=1000.0, length=50.0)
    night_catch_2: Catch = Catch(id=1, fish=12345, contestant=67890, caught_at=night_dt_2, latitude=52.370216,
                                 longitude=4.895168, country_code="US", weight=1000.0, length=50.0)

    assert night_catch.get_day_part() == "Night", '00:00:00 should be night'
    assert night_catch_2.get_day_part() == "Night", '05:59:59 should be night'


def test_get_day_part_morning() -> None | AssertionError:
    morning_dt: datetime.datetime = datetime.datetime(year=2025, month=1, day=14, hour=6, minute=0)
    morning_dt_2: datetime.datetime = datetime.datetime(year=2025, month=1, day=14, hour=11, minute=59, second=59)

    morning_catch: Catch = Catch(id=1, fish=12345, contestant=67890, caught_at=morning_dt, latitude=52.370216,
                                 longitude=4.895168, country_code="US", weight=1000.0, length=50.0)
    morning_catch_2: Catch = Catch(id=1, fish=12345, contestant=67890, caught_at=morning_dt_2, latitude=52.370216,
                                   longitude=4.895168, country_code="US", weight=1000.0, length=50.0)

    assert morning_catch.get_day_part() == "Morning", '06:00:00 should be morning'
    assert morning_catch_2.get_day_part() == "Morning", '11:59:59 should be morning'


def test_get_day_part_afternoon() -> None | AssertionError:
    afternoon_dt: datetime.datetime = datetime.datetime(year=2025, month=1, day=14, hour=12, minute=0)
    afternoon_dt_2: datetime.datetime = datetime.datetime(year=2025, month=1, day=14, hour=17, minute=59, second=59)

    afternoon_catch: Catch = Catch(id=1, fish=12345, contestant=67890, caught_at=afternoon_dt, latitude=52.370216,
                                   longitude=4.895168, country_code="US", weight=1000.0, length=50.0)
    afternoon_catch_2: Catch = Catch(id=1, fish=12345, contestant=67890, caught_at=afternoon_dt_2, latitude=52.370216,
                                     longitude=4.895168, country_code="US", weight=1000.0, length=50.0)

    assert afternoon_catch.get_day_part() == "Afternoon", '12:00:00 should be afternoon'
    assert afternoon_catch_2.get_day_part() == "Afternoon", '17:59:59 should be afternoon'


def test_get_day_part_evening() -> None | AssertionError:
    evening_dt: datetime.datetime = datetime.datetime(year=2025, month=1, day=14, hour=18, minute=0)
    evening_dt_2: datetime.datetime = datetime.datetime(year=2025, month=1, day=14, hour=23, minute=59, second=59)

    evening_catch: Catch = Catch(id=1, fish=12345, contestant=67890, caught_at=evening_dt, latitude=52.370216,
                                 longitude=4.895168, country_code="US", weight=1000.0, length=50.0)
    evening_catch_2: Catch = Catch(id=1, fish=12345, contestant=67890, caught_at=evening_dt_2, latitude=52.370216,
                                   longitude=4.895168, country_code="US", weight=1000.0, length=50.0)

    assert evening_catch.get_day_part() == "Evening", '18:00:00 should be evening'
    assert evening_catch_2.get_day_part() == "Evening", '23:59:59 should be evening'


def test_get_season_winter() -> None | AssertionError:
    dt: datetime.datetime = datetime.datetime(2024, 12, 1, 0, 0)
    catch = Catch(id=1, fish=12345, contestant=67890, caught_at=dt, latitude=52.370216,
                  longitude=4.895168, country_code="US", weight=1000.0, length=50.0)
    assert catch.get_season() == 'Winter', 'December 1st should be in the Winter.'

    catch.caught_at = datetime.datetime(2025, 1, 1, 0, 0)
    assert catch.get_season() == 'Winter', 'January 1st should be in the Winter.'

    catch.caught_at = datetime.datetime(2025, 2, 28, 0, 0)
    assert catch.get_season() == 'Winter', 'February 28th should be in the Winter.'


def test_get_season_spring() -> None | AssertionError:
    dt: datetime.datetime = datetime.datetime(2025, 3, 1, 0, 0)
    catch = Catch(id=1, fish=12345, contestant=67890, caught_at=dt, latitude=52.370216,
                  longitude=4.895168, country_code="US", weight=1000.0, length=50.0)
    assert catch.get_season() == 'Spring', 'March 1st should be in the Spring.'

    catch.caught_at = datetime.datetime(2025, 4, 1, 0, 0)
    assert catch.get_season() == 'Spring', 'April 1st should be in the Spring.'

    catch.caught_at = datetime.datetime(2025, 5, 31, 0, 0)
    assert catch.get_season() == 'Spring', 'May 31th should be in the Spring.'


def test_get_season_summer() -> None | AssertionError:
    dt: datetime.datetime = datetime.datetime(2025, 6, 1, 0, 0)
    catch = Catch(id=1, fish=12345, contestant=67890, caught_at=dt, latitude=52.370216,
                  longitude=4.895168, country_code="US", weight=1000.0, length=50.0)
    assert catch.get_season() == 'Summer', 'June 1st should be in the Summer.'

    catch.caught_at = datetime.datetime(2025, 7, 1, 0, 0)
    assert catch.get_season() == 'Summer', 'July 1st should be in the Summer.'

    catch.caught_at = datetime.datetime(2025, 8, 31, 0, 0)
    assert catch.get_season() == 'Summer', 'August 31th should be in the Summer.'


def test_get_season_autumn() -> None | AssertionError:
    dt: datetime.datetime = datetime.datetime(2025, 9, 1, 0, 0)
    catch = Catch(id=1, fish=12345, contestant=67890, caught_at=dt, latitude=52.370216,
                  longitude=4.895168, country_code="US", weight=1000.0, length=50.0)
    assert catch.get_season() == 'Autumn', 'September 1st should be in the Autumn.'

    catch.caught_at = datetime.datetime(2025, 10, 1, 0, 0)
    assert catch.get_season() == 'Autumn', 'October 1st should be in the Autumn.'

    catch.caught_at = datetime.datetime(2025, 11, 30, 0, 0)
    assert catch.get_season() == 'Autumn', 'November 30th should be in the Autumn.'


def test_get_weight_category_light() -> None | AssertionError:
    dt: datetime.datetime = datetime.datetime(2025, 1, 14, 17, 30)
    catch = Catch(id=1, fish=12345, contestant=67890, caught_at=dt, latitude=52.370216,
                  longitude=4.895168, country_code="US", weight=1.76899, length=5)
    assert catch.get_weight_category() == 'light', '0.9795.. is more than ±2% less of the expected weight, so it should be light.'


def test_get_weight_category_average() -> None | AssertionError:
    dt: datetime.datetime = datetime.datetime(2025, 1, 14, 17, 30)
    catch = Catch(id=1, fish=12345, contestant=67890, caught_at=dt, latitude=52.370216,
                  longitude=4.895168, country_code="US", weight=1.770, length=5)
    assert catch.get_weight_category() == 'average', '0.98007.. is in ±2% of the expected weight, so it should be average.'


def test_get_weight_category_heavy() -> None | AssertionError:
    dt: datetime.datetime = datetime.datetime(2025, 1, 14, 17, 30)
    catch = Catch(id=1, fish=12345, contestant=67890, caught_at=dt, latitude=52.370216,
                  longitude=4.895168, country_code="US", weight=1.8422, length=5)
    assert catch.get_weight_category() == 'heavy', '1.02005.. is more than ±2% above the expected weight, so it should be heavy.'
