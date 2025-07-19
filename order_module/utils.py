def apply_discount(cart_total, discount_code):
    if discount_code.is_valid():
        discount_amount = (cart_total * discount_code.discount_percent) / 100
        new_total = cart_total - discount_amount
        discount_code.use_code()
        return new_total
    return cart_total
