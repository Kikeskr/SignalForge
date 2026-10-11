import pytest

from signalforge.cli import main


def test_help_returns_success(capsys):
    with pytest.raises(SystemExit) as exit_info:
        main(["--help"])
    assert exit_info.value.code == 0
    assert "research" in capsys.readouterr().out.lower()


def test_run_reports_provider_failure(monkeypatch, capsys, tmp_path):
    def fail(*args, **kwargs):
        raise RuntimeError("provider failure")

    monkeypatch.setattr("signalforge.cli.run_research", fail)
    assert main(["run", "test question", "--output", str(tmp_path)]) == 1
    assert "Research run failed" in capsys.readouterr().err


def test_source_limit_is_bounded(capsys):
    assert main(["run", "question", "--max-sources", "99"]) == 2
    assert "between 1 and 12" in capsys.readouterr().err
