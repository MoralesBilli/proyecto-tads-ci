import os
import pytest

# Esto permite modificar temporalmente variables de entorno para evitar fallos
@pytest.fixture(autouse=True)
def set_test_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setenv("SECRET_KEY", "testsecret")
    monkeypatch.setenv("CORS_ORIGINS", "*")

def test_app_imports():
    from Backend.app import app
    assert app is not None
