import json
import sys
import os

CONTACTS_FILE = "contacts.json"

def load_contacts():
    if not os.path.exists(CONTACTS_FILE):
        return []
    with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)

def add_contact(name, phone):
    contacts = load_contacts()
    contacts.append({"name": name, "phone": phone})
    save_contacts(contacts)
    print(f"✓ Pievienots: {name} ({phone})")

def list_contacts():
    contacts = load_contacts()
    if not contacts:
        print("Kontaktu saraksts ir tukšs.")
        return
    print("Kontakti:")
    for idx, contact in enumerate(contacts, 1):
        print(f"  {idx}. {contact['name']} — {contact['phone']}")

def search_contacts(query):
    contacts = load_contacts()
    found = [c for c in contacts if query.lower() in c['name'].lower()]
    if not found:
        print(f"Netika atrasts neviens kontakts ar vaicājumu '{query}'.")
        return
    print(f"Atrasti {len(found)} kontakti:")
    for idx, contact in enumerate(found, 1):
        print(f"  {idx}. {contact['name']} — {contact['phone']}")

def main():
    if len(sys.argv) < 2:
        print("Lietošana: python contacts.py [add|list|search] [argumenti]")
        return

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) < 4:
            print("Kļūda: Jānorāda vārds un tālruņa numurs!")
            return
        add_contact(sys.argv[2], sys.argv[3])
    elif command == "list":
        list_contacts()
    elif command == "search":
        if len(sys.argv) < 3:
            print("Kļūda: Jānorāda meklējamais vārds!")
            return
        search_contacts(sys.argv[2])
    else:
        print(f"Nezināma komanda: {command}")

if __name__ == "__main__":
    main()