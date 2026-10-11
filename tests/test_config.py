from signalforge.config import load_settings


def test_settings_read_names_without_exposing_values(monkeypatch):
    monkeypatch.setenv("LITELLM_API_KEY", "do-not-print")
    settings = load_settings()
    assert settings.model_api_key == "do-not-print"
