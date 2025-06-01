"""Config tests to .env"""
# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring


from youconfigme import Config


def test_to_env():
    cfg = Config(
        from_items={"s1": {"b": 1, "c": 2}, "s2": {"y": 1, "z": 2}},
        default_section="s2",
    )
    assert (
        cfg.to_dotenv()
        == """S1_B=1
S1_C=2
Y=1
Z=2"""
    )
