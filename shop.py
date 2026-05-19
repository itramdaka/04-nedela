import os
import sys
import importlib.util

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

def _load_local_module(module_name):
    module_path = os.path.join(script_dir, f"{module_name}.py")
    if not os.path.isfile(module_path):
        raise ModuleNotFoundError(f"No module named '{module_name}'")
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[module_name] = module
    return module

try:
    import storage  # type: ignore[import]
    import utils  # type: ignore[import]
except ImportError:
    storage = _load_local_module("storage")
    utils = _load_local_module("utils")

def parse_positive_int(val_str, name="Daudzums"):
    """Validē un konvertē pozitīvu veselu skaitli."""
    try:
        val = int(val_str)
        if val <= 0:
            raise ValueError()
        return val
    except ValueError:
        print(f"Kļūda: '{val_str}' nav derīgs pozitīvs {name.lower()} skaitlis!")
        sys.exit(1)

def parse_positive_float(val_str, name="Cena"):
    """Validē un konvertē pozitīvu decimālskaitli."""
    try:
        val = float(val_str)
        if val <= 0:
            raise ValueError()
        return val
    except ValueError:
        print(f"Kļūda: '{val_str}' nav derīga pozitīva {name.lower()} vērtība!")
        sys.exit(1)

def handle_add():
    # Pārbaudām pamata argumentu skaitu (mazākais: python shop.py add Nosaukums Daudzums)
    if len(sys.argv) < 4:
        print("Kļūda: Trūkst argumentu!")
        print("Lietošana: python shop.py add [nosaukums] [daudzums] (cena_nav_obligāta)")
        return

    name = sys.argv[2]
    qty = parse_positive_int(sys.argv[3], "Daudzums")
    
    price = None

    # Ja cena ir norādīta komandrindā (tāpat kā 2. solī)
    if len(sys.argv) >= 5:
        price = parse_positive_float(sys.argv[4], "Cena")
        # Ja lietotājs tieši norāda cenu, mēs to uzreiz saglabājam/atjauninām cenu DB
        db_price = storage.get_price(name)
        if db_price != price:
            storage.set_price(name, price)
            if db_price is not None:
                print(f"✓ Cena atjaunināta datubāzē: {name} ({price:.2f} EUR)")          
            else:
                print(f"✓ Cena saglabāta datubāzē: {name} ({price:.2f} EUR)")
    else:
        # 3. Solis: Interaktīvā cenu meklēšana un vaicāšana, ja cena nav norādīta komandrindā
        known_price = storage.get_price(name)
        if known_price is not None:
            print(f"Atrasta cena: {known_price:.2f} EUR/gab.")
            choice = input("[A]kceptēt / [M]ainīt? > ").strip().upper()
            
            if choice == 'M':
                price_input = input("Jaunā cena: > ").strip()
                price = parse_positive_float(price_input, "Cena")
                storage.set_price(name, price)
                print(f"✓ Cena atjaunināta: {name} → {price:.2f} EUR")
            else:
                # Pēc noklusējuma vai ja nospiež 'A'
                price = known_price
        else:
            print("Cena nav zināma.")
            price_input = input("Ievadi cenu: > ").strip()
            price = parse_positive_float(price_input, "Cena")
            storage.set_price(name, price)
            print(f"✓ Cena saglabāta: {name} ({price:.2f} EUR)")

    # Pievienojam preci iepirkumu sarakstam
    items = storage.load_list()
    items.append({"name": name, "qty": qty, "price": price})
    storage.save_list(items)
    
    line_total = qty * price
    print(f"✓ Pievienots: {name} × {qty} ({price:.2f} EUR/gab.) = {line_total:.2f} EUR")

def handle_list():
    items = storage.load_list()
    if not items:
        print("Iepirkumu saraksts ir tukšs.")
        return
    print("Iepirkumu saraksts:")
    for idx, item in enumerate(items, 1):
        line_total = utils.calc_line_total(item)
        print(f"  {idx}. {item['name']} × {item['qty']} — {item['price']:.2f} EUR/gab. — {line_total:.2f} EUR")

def handle_total():
    items = storage.load_list()
    grand_total = utils.calc_grand_total(items)
    total_units = utils.count_units(items)
    total_products = len(items)
    print(f"Kopā: {grand_total:.2f} EUR ({total_units} vienības, {total_products} produkti)")

def handle_clear():
    storage.save_list([])
    print("✓ Iepirkumu saraksts notīrīts!")

def main():
    if len(sys.argv) < 2:
        print("Lietošana: python shop.py [add|list|total|clear] [argumenti]")
        return

    command = sys.argv[1].lower()

    if command == "add":
        handle_add()
    elif command == "list":
        handle_list()
    elif command == "total":
        handle_total()
    elif command == "clear":
        handle_clear()
    else:
        print(f"Nezināma komanda: {command}")

if __name__ == "__main__":
    main()