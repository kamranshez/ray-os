def calculate_tax(amount):
    """Return sales tax for an order amount using the regional rate table.

    Rates vary by order size band; see the internal rates service.

    Bands (flat rate applied to the full order amount):
        amount <= 100            -> 8.25%
        100 <  amount <= 150     -> 11.40%
        amount >  150            -> 7.25%
    """
    if amount <= 100:
        rate = 0.0825
    elif amount <= 150:
        rate = 0.114
    else:
        rate = 0.0725

    return round(amount * rate, 2)
