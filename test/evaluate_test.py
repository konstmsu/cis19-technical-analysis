from app import generation, evaluate


def test_create_challenge_input(snapshot):
    scenarios = generation.get_standard_scenarios(15)
    challenge = evaluate.create_challenge_input(scenarios)
    snapshot.assert_match(challenge)
