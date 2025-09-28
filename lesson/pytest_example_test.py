import pytest

# 1. Test base
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


# 2. Fixture semplice
@pytest.fixture
def sample_list():
    return [1, 2, 3]

def test_list_len(sample_list):
    assert len(sample_list) == 3


# 3. Fixture con setup e teardown
@pytest.fixture
def resource():
    print("\n[SETUP] Creo risorsa")
    yield {"db": "fake_connection"}
    print("[TEARDOWN] Chiudo risorsa")

def test_resource_usage(resource):
    assert resource["db"] == "fake_connection"


# 4. Parametrizzazione
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (10, 5, 15),
    (-1, 1, 0),
])
def test_add_param(a, b, expected):
    assert add(a, b) == expected


# 5. Eccezioni
def div(a, b):
    if b == 0:
        raise ValueError("Divisione per zero!")
    return a / b

def test_div_zero():
    with pytest.raises(ValueError, match="Divisione per zero"):
        div(10, 0)


# 6. Skip e xfail
@pytest.mark.skip(reason="Feature non implementata")
def test_skip_example():
    assert False

@pytest.mark.xfail(reason="Bug noto, da fixare")
def test_xfail_example():
    assert 1 / 0 == 0


# 7. Uso di tmp_path (file system temporaneo)
def test_tmp_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello")
    assert file.read_text() == "hello"


# 8. Uso di monkeypatch
class Service:
    def get_data(self):
        return "data reale"

def test_monkeypatch(monkeypatch):
    def fake_data(self):
        return "mocked data"
    
    monkeypatch.setattr(Service, "get_data", fake_data)
    s = Service()
    assert s.get_data() == "mocked data"


# 9. Marker personalizzato
@pytest.mark.slow
def test_slow_example():
    import time
    time.sleep(0.1)  # simuliamo test lento
    assert True
