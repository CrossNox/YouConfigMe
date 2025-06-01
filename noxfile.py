"""Entrypoint for nox."""
import nox


@nox.session(reuse_venv=True, python="3.8")
def cop(session):
    """Run all pre-commit hooks."""
    session.install(".")
    session.install(".[dev,test]")

    session.run("pre-commit", "install")
    session.run("pre-commit", "run", "--show-diff-on-failure", "--all-files")


@nox.session(reuse_venv=True, python="3.8")
def tests(session):
    """Run all tests."""
    session.install(".")
    session.install(".[test]")

    cmd = ["pytest"]
    if session.posargs:
        cmd.extend(session.posargs)
    session.run(*cmd)
