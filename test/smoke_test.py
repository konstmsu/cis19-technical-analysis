import requests


def test_challenge_registered():
    for coordinator in [
        "https://sg-codeit-backend.herokuapp.com",
        "https://hk-codeit-backend.herokuapp.com",
        "https://dryrun2-coordinator.herokuapp.com",
    ]:
        response = requests.get(f"{coordinator}/api/challenges")
        assert response.status_code == 200
        [challenge] = [c for c in response.json() if c["name"] == "Technical Analysis"]
        print(challenge.keys())
        assert challenge["isActive"]
        assert challenge["weight"] == 10
