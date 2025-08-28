from lib.db import init_db
from lib.db.models import Trip, Destination, Activity, Category, Tag
from datetime import datetime

session = init_db()

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
    except ValueError:
        print("⚠ Invalid date format, should be YYYY-MM-DD. Skipping.")
        return None

def main_menu():
    while True:
        print("\n--- Travel Journal ---")
        print("1. Manage Trips")
        print("2. Manage Destinations")
        print("3. Manage Activities")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            trip_menu()
        elif choice == "2":
            destination_menu()
        elif choice == "3":
            activity_menu()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

def trip_menu():
    while True:
        print("\n--- Trip Menu ---")
        print("1. Create Trip")
        print("2. List Trips")
        print("3. Delete Trip")
        print("4. Search Trips")
        print("5. Trip Summary & Stats")
        print("6. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Trip name: ").strip()
            start = parse_date(input("Start date (YYYY-MM-DD, optional): ").strip())
            end = parse_date(input("End date (YYYY-MM-DD, optional): ").strip())
            notes = input("Notes (optional): ").strip()

            category_name = input("Category (optional): ").strip()
            category = None
            if category_name:
                category = Category.get_or_create(session, category_name)

            tags_input = input("Tags (comma separated, optional): ").strip()
            tags = []
            if tags_input:
                tags = [Tag.get_or_create(session, t.strip()) for t in tags_input.split(",")]

            Trip.create(session, name, start, end, notes, category, tags)
            print(f"✅ Trip '{name}' created!")

        elif choice == "2": 
            trips = Trip.get_all(session)
            if not trips:
                print("⚠ No trips found.")
            for trip in trips:
                cat = trip.category.name if trip.category else "None"
                tags = ", ".join([t.name for t in trip.tags]) or "None"
                print(f"{trip.id}. {trip.name} ({trip.start_date} → {trip.end_date}) | Category: {cat} | Tags: {tags}")

        elif choice == "3":
            trip_id = input("Enter trip ID to delete: ").strip()
            if trip_id.isdigit():
                trip = Trip.find_by_id(session, int(trip_id))
                if trip:
                    trip.delete(session)
                    print("🗑 Trip deleted.")
                else:
                    print("⚠ Trip not found.")
            else:
                print("⚠ Invalid ID.")

        elif choice == "4": 
            keyword = input("Enter keyword to search in trip name/notes: ").strip().lower()
            trips = Trip.get_all(session)
            results = [t for t in trips if keyword in t.name.lower() or keyword in (t.notes or "").lower()]
            if results:
                for t in results:
                    cat = t.category.name if t.category else "None"
                    tags = ", ".join([tg.name for tg in t.tags]) or "None"
                    print(f"{t.id}. {t.name} ({t.start_date} → {t.end_date}) | Category: {cat} | Tags: {tags}")
            else:
                print("⚠ No matching trips found.")

        elif choice == "5":  
            trip_id = input("Enter Trip ID for summary: ").strip()
            if trip_id.isdigit():
                trip = Trip.find_by_id(session, int(trip_id))
                if not trip:
                    print("⚠ Trip not found.")
                    continue

                destinations = trip.destinations
                activities = [a for d in destinations for a in d.activities]
                total_cost = sum(a.cost or 0 for a in activities)
                duration = (trip.end_date - trip.start_date).days if trip.start_date and trip.end_date else "N/A"

                print(f"\n📊 Summary for Trip: {trip.name}")
                print(f"Dates: {trip.start_date} → {trip.end_date}")
                print(f"Category: {trip.category.name if trip.category else 'None'}")
                print(f"Tags: {', '.join([t.name for t in trip.tags]) or 'None'}")
                print(f"Destinations: {len(destinations)}")
                print(f"Activities: {len(activities)}")
                print(f"Total Cost: ${total_cost:.2f}")
                print(f"Duration: {duration} days")
            else:
                print("⚠ Invalid ID.")

        elif choice == "6":
            break
        else:
            print("Invalid choice.")

def destination_menu():
    while True:
        print("\n--- Destination Menu ---")
        print("1. Add Destination to a Trip")
        print("2. List Destinations")
        print("3. Delete Destination")
        print("4. Search Destinations")
        print("5. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            trip_id = input("Trip ID for this destination: ").strip()
            trip = Trip.find_by_id(session, int(trip_id)) if trip_id.isdigit() else None
            if not trip:
                print("⚠ Trip not found.")
                continue
            name = input("City/Place name: ").strip()
            country = input("Country: ").strip()
            arrival = parse_date(input("Arrival date (YYYY-MM-DD, optional): ").strip())
            departure = parse_date(input("Departure date (YYYY-MM-DD, optional): ").strip())
            Destination.create(session, name, country, trip, arrival, departure)
            print(f"✅ Destination '{name}, {country}' added!")

        elif choice == "2":
            destinations = Destination.get_all(session)
            if not destinations:
                print("⚠ No destinations found.")
            for d in destinations:
                print(f"{d.id}. {d.name}, {d.country} (Trip: {d.trip.name})")

        elif choice == "3":
            dest_id = input("Enter destination ID to delete: ").strip()
            if dest_id.isdigit():
                dest = Destination.find_by_id(session, int(dest_id))
                if dest:
                    dest.delete(session)
                    print("🗑 Destination deleted.")
                else:
                    print("⚠ Destination not found.")
            else:
                print("⚠ Invalid ID.")

        elif choice == "4":  
            keyword = input("Enter city or country to search: ").strip().lower()
            results = [d for d in Destination.get_all(session)
                       if keyword in d.name.lower() or keyword in d.country.lower()]
            if results:
                for d in results:
                    print(f"{d.id}. {d.name}, {d.country} (Trip: {d.trip.name})")
            else:
                print("⚠ No matching destinations found.")

        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def activity_menu():
    while True:
        print("\n--- Activity Menu ---")
        print("1. Add Activity to a Destination")
        print("2. List Activities")
        print("3. Delete Activity")
        print("4. Search/Filter Activities")
        print("5. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            dest_id = input("Destination ID for this activity: ").strip()
            destination = Destination.find_by_id(session, int(dest_id)) if dest_id.isdigit() else None
            if not destination:
                print("⚠ Destination not found.")
                continue
            name = input("Activity name: ").strip()
            description = input("Description (optional): ").strip()
            date = parse_date(input("Activity date (YYYY-MM-DD, optional): ").strip())
            cost = input("Cost (optional, default 0): ").strip() or 0.0
            Activity.create(session, name, destination, description, date, float(cost))
            print(f"✅ Activity '{name}' added to {destination.name}!")

        elif choice == "2":
            activities = Activity.get_all(session)
            if not activities:
                print("⚠ No activities found.")
            for a in activities:
                print(f"{a.id}. {a.name} ({a.activity_date}) - {a.destination.name}, {a.destination.country}")

        elif choice == "3":
            act_id = input("Enter activity ID to delete: ").strip()
            if act_id.isdigit():
                act = Activity.find_by_id(session, int(act_id))
                if act:
                    act.delete(session)
                    print("🗑 Activity deleted.")
                else:
                    print("⚠ Activity not found.")
            else:
                print("⚠ Invalid ID.")

        elif choice == "4":  
            keyword = input("Enter keyword (name/description): ").strip().lower()
            min_cost = input("Min cost (optional): ").strip()
            max_cost = input("Max cost (optional): ").strip()

            activities = Activity.get_all(session)
            results = []
            for a in activities:
                if keyword not in a.name.lower() and keyword not in (a.description or "").lower():
                    continue
                if min_cost and a.cost < float(min_cost):
                    continue
                if max_cost and a.cost > float(max_cost):
                    continue
                results.append(a)

            if results:
                for a in results:
                    print(f"{a.id}. {a.name} (${a.cost}) ({a.activity_date}) - {a.destination.name}, {a.destination.country}")
            else:
                print("⚠ No matching activities found.")

        elif choice == "5":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()
