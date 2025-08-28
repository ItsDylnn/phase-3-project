from lib.db import init_db
from lib.db.models import Trip, Destination, Activity, Category, Tag
from datetime import datetime



session = init_db()

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
    except ValueError:
        print("⚠ Oops! That date didn’t look right. Please use YYYY-MM-DD format.")
        return None


def main_menu():
    while True:
        print("\n🌍 Welcome to Your Travel Journal 🌍")
        print("What would you like to do today?")
        print("1. ✈ Manage Trips")
        print("2. 🏝 Manage Destinations")
        print("3. 🎟 Manage Activities")
        print("4. 🚪 Exit")


        choice = input("\n👉 Choose an option (1-4): ").strip()


        if choice == "1":
            trip_menu()
        elif choice == "2":
            destination_menu()
        elif choice == "3":
            activity_menu()
        elif choice == "4":
            print("\n👋 Thanks for using Travel Journal. Safe travels!")
            break
        else:
            print("⚠ Hmm, I didn’t get that. Please choose 1-4.")




def trip_menu():
    while True:
        print("\n--- 🧳 Trip Menu ---")
        print("1. ➕ Create a new Trip")
        print("2. 📋 View all Trips")
        print("3. ❌ Delete a Trip")
        print("4. 🔍 Search Trips")
        print("5. 📊 Trip Summary & Stats")
        print("6. 🔙 Back to Main Menu")

        choice = input("\n👉 Choose an option (1-6): ").strip()


        if choice == "1":
            name = input("Trip name: ").strip()
            start = parse_date(input("Start date (YYYY-MM-DD, leave blank if none): ").strip())
            end = parse_date(input("End date (YYYY-MM-DD, leave blank if none): ").strip())
            notes = input("Notes about this trip (optional): ").strip()

            category_name = input("Category (optional, e.g., Vacation, Work): ").strip()
            category = Category.get_or_create(session, category_name) if category_name else None

            tags_input = input("Tags (comma separated, e.g., family, adventure): ").strip()
            tags = [Tag.get_or_create(session, t.strip()) for t in tags_input.split(",")] if tags_input else []

            Trip.create(session, name, start, end, notes, category, tags)
            print(f"✅ Great! Trip '{name}' has been created.")



        elif choice == "2":
            trips = Trip.get_all(session)
            if not trips:
                print("⚠ No trips yet. Time to plan one? ✈️")
            else:
                for trip in trips:
                    cat = trip.category.name if trip.category else "None"
                    tags = ", ".join([t.name for t in trip.tags]) or "None"
                    print(f"{trip.id}. {trip.name} ({trip.start_date} → {trip.end_date}) | Category: {cat} | Tags: {tags}")

        elif choice == "3":
            trip_id = input("Enter the Trip ID to delete: ").strip()
            if trip_id.isdigit():
                trip = Trip.find_by_id(session, int(trip_id))
                if trip:
                    trip.delete(session)
                    print("🗑 Trip deleted successfully.")
                else:
                    print("⚠ That trip doesn’t exist.")
            else:
                print("⚠ Please enter a valid number.")

        elif choice == "4":
            keyword = input("Enter a keyword to search (name or notes): ").strip().lower()
            trips = Trip.get_all(session)
            results = [t for t in trips if keyword in t.name.lower() or keyword in (t.notes or "").lower()]
            if results:
                print("\n🔎 Search Results:")
                for t in results:
                    cat = t.category.name if t.category else "None"
                    tags = ", ".join([tg.name for tg in t.tags]) or "None"
                    print(f"{t.id}. {t.name} ({t.start_date} → {t.end_date}) | Category: {cat} | Tags: {tags}")
            else:
                print("⚠ No trips matched your search.")

        elif choice == "5":
            trip_id = input("Enter the Trip ID for a summary: ").strip()
            if trip_id.isdigit():
                trip = Trip.find_by_id(session, int(trip_id))
                if not trip:
                    print("⚠ Couldn’t find that trip.")
                    continue

                destinations = trip.destinations
                activities = [a for d in destinations for a in d.activities]
                total_cost = sum(a.cost or 0 for a in activities)
                duration = (trip.end_date - trip.start_date).days if trip.start_date and trip.end_date else "N/A"

                print(f"\n📊 Summary for Trip: {trip.name}")
                print(f"🗓 Dates: {trip.start_date} → {trip.end_date}")
                print(f"🏷 Category: {trip.category.name if trip.category else 'None'}")
                print(f"🔖 Tags: {', '.join([t.name for t in trip.tags]) or 'None'}")
                print(f"📍 Destinations: {len(destinations)}")
                print(f"🎟 Activities: {len(activities)}")
                print(f"💰 Total Cost: ${total_cost:.2f}")
                print(f"⏳ Duration: {duration} days")
            else:
                print("⚠ Please enter a valid Trip ID.")

        elif choice == "6":
            break
        else:
            print("⚠ Invalid choice. Please try again.")



if __name__ == "__main__":
    main_menu()

