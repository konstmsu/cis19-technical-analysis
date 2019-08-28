from app.maths import local_extrema


def do_test(values, expected_optimal_trades):
    assert list(local_extrema(values)) == expected_optimal_trades


# def test_increasing():
#     do_test([1, 2], [0, 1])
#     do_test([3, 7, 8, 9], [0, 3])


# def test_decreasing():
#     do_test([5, 3], [])
#     do_test([7, 5, 3], [])


def test_peak():
    do_test([5, 3, 4], [1])
    do_test([2, 7, 9, 4], [0, 2])
