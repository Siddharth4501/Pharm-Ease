from django import template

register = template.Library()

@register.filter
def calculate_discounted_price(original_price, discount_percentage):
    discount_amount = float(original_price) * (discount_percentage / 100)
    discounted_price = float(original_price) - discount_amount
    return discounted_price

