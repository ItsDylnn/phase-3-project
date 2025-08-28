# 🌍 Travel Journal CLI

A Python **Command Line Interface (CLI)** application to plan, track, and organize trips, destinations, and activities.  
Built with **SQLAlchemy ORM** and designed as part of the Phase 3 project.

---

## ✨ Features
- Manage **Trips** (create, list, delete).
- Add **Destinations** to trips with arrival & departure dates.
- Add **Activities** to destinations with optional date, cost, and description.
- Categorize and tag trips for easy filtering.
- View trip summaries and basic stats.
- Input validation with helpful error messages.
- SQLite database powered by SQLAlchemy ORM.

---

## ⚙️ Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/ItsDylnn/phase-3-project.git
   cd phase-3-project
   ```
2. **Install dependencies with Pipenv**:
   ```bash
   pipenv install
   pipenv shell
   ```
3. **Run migrations**:
   ```bash
   alembic upgrade head
   ```
-------------------------------------------------------------
## ⚙️ ▶️ Usage
Run the CLI app:
```bash
python -m lib.cli
```
Example interaction:
```bash
--- Travel Journal ---
1. Manage Trips
2. Manage Destinations
3. Manage Activities
4. Exit
Choose an option: 1

--- Trip Menu ---
1. Create Trip
2. List Trips
3. Delete Trip
4. Back to Main Menu
```
-----------------------------------------------------------
## 📊 Data Model

The database schema includes:

- **Trip**
  - One-to-many relationship with Destinations.
  - Attributes: `id`, `name`, `start_date`, `end_date`, `notes`, `category`, `tags`.

- **Destination**
  - Belongs to a Trip, has many Activities.
  - Attributes: `id`, `name`, `country`, `arrival_date`, `departure_date`.

- **Activity**
  - Belongs to a Destination.
  - Attributes: `id`, `name`, `description`, `activity_date`, `cost`.
  - -----------------------------------------------------------
  ## 👤 Author

- **GitHub:** [ItsDylnn](https://github.com/ItsDylnn)  
- **Project:** Phase 3 CLI + ORM Travel Journal


   
   
