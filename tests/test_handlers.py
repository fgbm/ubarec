from ubarec.handlers import get_7zip, get_now_timestamp


def test_get_7zip():
    result = get_7zip()
    assert result[-2:] == '7z' or result[-6:] == '7z.exe'


def test_get_now_timestamp():
    result = get_now_timestamp()
    assert len(result) == 16
