def calc_line_total(item):
    """Atgriež daudzums x cena par vienību (qty * price)"""
    return item.get('qty', 1) * item.get('price', 0.0)

def calc_grand_total(items):
    """Summē visus rindiņu kopsummas"""
    return sum(calc_line_total(item) for item in items)

def count_units(items):
    """Saskaita kopējo vienību skaitu (qty summu)"""
    return sum(item.get('qty', 1) for item in items)