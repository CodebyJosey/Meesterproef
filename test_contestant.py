import datetime
from contestant import Contestant


def test_get_age() -> None | AssertionError:
    dt: datetime.date = datetime.date(year=2007, month=7, day=27)
    contestant: Contestant = Contestant('abcdef-ghijkl-mnopqr-stuvwx', 'Josey', 'van Aarsen', 'Pro', dt)

    assert contestant.get_age() == 17, 'Josey van Aarsen should be 17 on 14-01-2025'


def test_get_age_before_birthday() -> None | AssertionError:
    dt: datetime.date = datetime.date(year=2007, month=7, day=27)
    contestant: Contestant = Contestant('abcdef-ghijkl-mnopqr-stuvwx', 'Josey', 'van Aarsen', 'Pro', dt)

    before_birthday: datetime.date = datetime.date(year=2025, month=7, day=26)
    assert contestant.get_age(before_birthday) == 17, 'Josey van Aarsen should be 17 on 26-07-2025'


def test_get_age_on_birthday() -> None | AssertionError:
    dt: datetime.date = datetime.date(year=2007, month=7, day=27)
    contestant: Contestant = Contestant('abcdef-ghijkl-mnopqr-stuvwx', 'Josey', 'van Aarsen', 'Pro', dt)

    before_birthday: datetime.date = datetime.date(year=2025, month=7, day=27)
    assert contestant.get_age(before_birthday) == 18, 'Josey van Aarsen should be 18 on 27-07-2025'


def test_get_age_after_birthday() -> None | AssertionError:
    dt: datetime.date = datetime.date(year=2007, month=7, day=27)
    contestant: Contestant = Contestant('abcdef-ghijkl-mnopqr-stuvwx', 'Josey', 'van Aarsen', 'Pro', dt)

    before_birthday: datetime.date = datetime.date(year=2025, month=7, day=28)
    assert contestant.get_age(before_birthday) == 18, 'Josey van Aarsen should be 18 on 28-07-2025'
