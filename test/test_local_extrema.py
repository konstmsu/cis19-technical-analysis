from app.maths import local_extrema


def do_test(values, expected_local_extrema):
    assert list(local_extrema(values)) == expected_local_extrema


# def test_increasing():
#     do_test([1, 2], [0, 1])
#     do_test([3, 7, 8, 9], [0, 3])


# def test_decreasing():
#     do_test([5, 3], [0, 1])
#     do_test([7, 5, 3], [0, 2])


def test_peak():
    do_test([5, 3, 4], [1])
    do_test([2, 7, 9, 4], [2])
