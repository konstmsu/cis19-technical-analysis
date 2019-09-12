from snapshottest.pytest import SnapshotTest
from app.generation import ScenarioBuilder, get_standard_scenarios


def test_generate_price(snapshot: SnapshotTest):
    builder = (
        ScenarioBuilder(0, 1000, 0)
        .add_base()
        .add_trend()
        .add_waves(10)
        .add_noise()
    )
    snapshot.assert_match(builder.signal.tolist(), "signal")
    snapshot.assert_match(builder.train_noise.tolist(), "noise")


def test_generator_is_stable(snapshot):
    for i, builder in enumerate(get_standard_scenarios(42)):
        snapshot.assert_match(builder.signal.tolist(), f"Signal {i}")
        snapshot.assert_match(builder.train_noise.tolist(), f"Noise {i}")
