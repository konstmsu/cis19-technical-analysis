from app import generation, evaluate, my_solver


def test_create_challenge_input(snapshot):
    scenarios = generation.get_standard_scenarios(15)
    challenge = evaluate.create_challenge_input(scenarios)
    snapshot.assert_match(challenge)


def test_calculate_score(snapshot):
    scenarios = generation.get_standard_scenarios(1)
    results = [
        my_solver.solve(0, s.train_signal, s.test_size, max_wave_count=1)[0]
        for s in scenarios
    ]
    snapshot.assert_match(evaluate.calculate_score("test_run", scenarios, results))
