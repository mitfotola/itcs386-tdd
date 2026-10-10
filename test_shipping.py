import pytest

from shipping import shipping_fee


# Bug: breaks Rule 1. A weight of exactly 0 kg is not more than 0 kg,
# but the code only rejects negative weights.
@pytest.mark.parametrize("weight", [0, -1, -0.5])
def test_weight_of_zero_or_less_is_rejected(weight):
    with pytest.raises(ValueError, match="more than 0 kg"):
        shipping_fee(weight)


# Bug: breaks Rule 2. A parcel of exactly 1 kg is "up to 1 kg"
# and must cost 40, but the code charges 60.
@pytest.mark.parametrize("weight", [0.1, 0.5, 1])
def test_up_to_1_kg_costs_40(weight):
    assert shipping_fee(weight) == 40


@pytest.mark.parametrize("weight", [1.01, 3, 5])
def test_more_than_1_kg_up_to_5_kg_costs_60(weight):
    assert shipping_fee(weight) == 60


# Bug: breaks Rule 4. Every *started* kilogram above 5 kg costs 10 baht,
# but the code rounds the extra weight down, so 5.2 kg costs 60, not 70.
@pytest.mark.parametrize("weight, expected", [
    (5.2, 70),   # docstring example, first started kilogram
    (6, 70),     # exactly one full kilogram above 5
    (6.5, 80),   # second kilogram started
    (10, 110),   # five full kilograms above 5
])
def test_more_than_5_kg_adds_10_per_started_kg(weight, expected):
    assert shipping_fee(weight) == expected
