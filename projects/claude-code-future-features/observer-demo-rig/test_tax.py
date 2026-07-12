from tax import calculate_tax


def test_calculate_tax():
    assert calculate_tax(100) == 8.25
    assert calculate_tax(150) == 17.10
    assert calculate_tax(200) == 14.50


if __name__ == "__main__":
    test_calculate_tax()
    print("ALL TESTS PASS")
