from snapshottest.pytest import SnapshotTest

from app.generation import ScenarioBuilder, get_standard_scenarios


def test_generate_price(snapshot: SnapshotTest):
    scenario = ScenarioBuilder(0, 20, 50).set_base().set_trend().add_waves(3).build()
    snapshot.assert_match(scenario.train_signal.tolist(), "train_signal")
    snapshot.assert_match(scenario.test_signal.tolist(), "test_signal")


def test_generator_is_stable(snapshot):
    for i, scenario in enumerate(get_standard_scenarios(42)):
        snapshot.assert_match(scenario.train_signal.tolist(), f"train_signal {i}")
        snapshot.assert_match(scenario.test_signal.tolist(), f"test_signal {i}")
