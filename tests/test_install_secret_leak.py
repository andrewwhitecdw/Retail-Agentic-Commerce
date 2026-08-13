import pathlib


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_install_script_does_not_use_agent_env_prefix():
    install_sh = REPO_ROOT / "install.sh"
    assert install_sh.exists(), "install.sh not found at repo root"
    text = install_sh.read_text()
    assert "AGENT_ENV" not in text, (
        "install.sh still references AGENT_ENV; secrets can leak via command line"
    )
    assert "env $AGENT_ENV" not in text, (
