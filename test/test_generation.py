from app.generation import PriceGenerator


def test_generate_price():
    price = PriceGenerator().generate_price(100)
    assert price.shape == (2, 100)
    assert abs(price[1].mean()) < 0.01


def test_generator_is_stable(snapshot):
    price = PriceGenerator(42).generate_price(100).tolist()
    snapshot.assert_match(price)
