"""Seed database with realistic mock data."""
import random
from datetime import datetime, timedelta
from decimal import Decimal
from faker import Faker
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models import (
    Customer,
    Vehicle,
    Mechanic,
    WorkOrder,
    Part,
    LaborItem,
    CertificationLevel,
    WorkOrderStatus,
    WorkOrderPriority,
    PaymentStatus,
    PaymentMethod,
    APIKey
)

fake = Faker()

# Car makes and models for realistic data
CAR_MAKES_MODELS = {
    "Toyota": ["Camry", "Corolla", "RAV4", "Highlander", "Tacoma", "Tundra", "Prius"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot", "Odyssey", "Ridgeline"],
    "Ford": ["F-150", "Escape", "Explorer", "Mustang", "Edge", "Ranger"],
    "Chevrolet": ["Silverado", "Equinox", "Malibu", "Traverse", "Colorado"],
    "Nissan": ["Altima", "Rogue", "Sentra", "Pathfinder", "Frontier"],
    "BMW": ["3 Series", "5 Series", "X3", "X5", "7 Series"],
    "Mercedes-Benz": ["C-Class", "E-Class", "GLC", "GLE", "S-Class"],
    "Volkswagen": ["Jetta", "Passat", "Tiguan", "Atlas", "Golf"],
    "Mazda": ["Mazda3", "Mazda6", "CX-5", "CX-9", "MX-5 Miata"],
    "Subaru": ["Outback", "Forester", "Crosstrek", "Impreza", "Ascent"],
}

COLORS = ["Black", "White", "Silver", "Gray", "Red", "Blue", "Green", "Brown", "Gold", "Beige"]

# Common repair parts
PARTS_CATALOG = [
    {"part_number": "OF-101", "description": "Oil Filter", "unit_cost": Decimal("12.99"), "supplier": "AutoZone", "warranty": 6},
    {"part_number": "BP-201", "description": "Brake Pads (Front)", "unit_cost": Decimal("45.99"), "supplier": "NAPA", "warranty": 12},
    {"part_number": "BP-202", "description": "Brake Pads (Rear)", "unit_cost": Decimal("38.99"), "supplier": "NAPA", "warranty": 12},
    {"part_number": "BR-301", "description": "Brake Rotors (Front)", "unit_cost": Decimal("89.99"), "supplier": "NAPA", "warranty": 24},
    {"part_number": "BR-302", "description": "Brake Rotors (Rear)", "unit_cost": Decimal("79.99"), "supplier": "NAPA", "warranty": 24},
    {"part_number": "AF-401", "description": "Air Filter", "unit_cost": Decimal("18.99"), "supplier": "AutoZone", "warranty": 12},
    {"part_number": "CF-501", "description": "Cabin Filter", "unit_cost": Decimal("22.99"), "supplier": "AutoZone", "warranty": 12},
    {"part_number": "SP-601", "description": "Spark Plugs (Set of 4)", "unit_cost": Decimal("34.99"), "supplier": "O'Reilly", "warranty": 12},
    {"part_number": "BAT-701", "description": "Car Battery", "unit_cost": Decimal("129.99"), "supplier": "Interstate", "warranty": 36},
    {"part_number": "ALT-801", "description": "Alternator", "unit_cost": Decimal("189.99"), "supplier": "Advance Auto", "warranty": 24},
    {"part_number": "ST-901", "description": "Starter Motor", "unit_cost": Decimal("169.99"), "supplier": "Advance Auto", "warranty": 24},
    {"part_number": "WP-1001", "description": "Water Pump", "unit_cost": Decimal("89.99"), "supplier": "NAPA", "warranty": 12},
    {"part_number": "TB-1101", "description": "Timing Belt", "unit_cost": Decimal("79.99"), "supplier": "Gates", "warranty": 60},
    {"part_number": "SB-1201", "description": "Serpentine Belt", "unit_cost": Decimal("34.99"), "supplier": "Gates", "warranty": 24},
    {"part_number": "TR-1301", "description": "Tire (Single)", "unit_cost": Decimal("125.00"), "supplier": "Michelin", "warranty": 60},
    {"part_number": "WB-1401", "description": "Wiper Blades (Pair)", "unit_cost": Decimal("29.99"), "supplier": "Bosch", "warranty": 6},
    {"part_number": "RAD-1501", "description": "Radiator", "unit_cost": Decimal("249.99"), "supplier": "NAPA", "warranty": 24},
    {"part_number": "COOL-1601", "description": "Coolant (1 Gallon)", "unit_cost": Decimal("19.99"), "supplier": "Prestone", "warranty": None},
    {"part_number": "OIL-1701", "description": "Motor Oil (5 Quarts)", "unit_cost": Decimal("24.99"), "supplier": "Mobil 1", "warranty": None},
    {"part_number": "TF-1801", "description": "Transmission Fluid (1 Quart)", "unit_cost": Decimal("14.99"), "supplier": "Valvoline", "warranty": None},
]

# Common labor tasks
LABOR_TASKS = [
    {"description": "Oil Change Service", "hours": Decimal("0.5")},
    {"description": "Brake Pad Replacement", "hours": Decimal("1.5")},
    {"description": "Brake Rotor Replacement", "hours": Decimal("2.0")},
    {"description": "Tire Rotation", "hours": Decimal("0.5")},
    {"description": "Tire Replacement (4 tires)", "hours": Decimal("1.0")},
    {"description": "Battery Replacement", "hours": Decimal("0.5")},
    {"description": "Alternator Replacement", "hours": Decimal("2.5")},
    {"description": "Starter Motor Replacement", "hours": Decimal("2.0")},
    {"description": "Water Pump Replacement", "hours": Decimal("3.0")},
    {"description": "Timing Belt Replacement", "hours": Decimal("4.5")},
    {"description": "Diagnostic Service", "hours": Decimal("1.0")},
    {"description": "Air Filter Replacement", "hours": Decimal("0.25")},
    {"description": "Cabin Filter Replacement", "hours": Decimal("0.25")},
    {"description": "Spark Plug Replacement", "hours": Decimal("1.5")},
    {"description": "Wiper Blade Installation", "hours": Decimal("0.25")},
    {"description": "Coolant Flush", "hours": Decimal("1.0")},
    {"description": "Transmission Service", "hours": Decimal("2.5")},
    {"description": "Radiator Replacement", "hours": Decimal("3.5")},
]

# Mechanic specialties
SPECIALTIES = ["Engine", "Transmission", "Electrical", "Brakes", "AC", "Diagnostics"]


def generate_vin():
    """Generate a realistic-looking VIN."""
    chars = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
    return ''.join(random.choice(chars) for _ in range(17))


def generate_work_order_number(date: datetime, sequence: int):
    """Generate work order number in format WO-YYYYMMDD-XXXX."""
    return f"WO-{date.strftime('%Y%m%d')}-{sequence:04d}"


def create_customers(db: Session, count: int = 500):
    """Create customer records."""
    print(f"Creating {count} customers...")
    customers = []

    for _ in range(count):
        # Random date between 1-10 years ago
        days_ago = random.randint(365, 3650)
        customer_since = datetime.now().date() - timedelta(days=days_ago)

        customer = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            phone=fake.phone_number()[:20],
            address_line1=fake.street_address(),
            address_line2=fake.secondary_address() if random.random() > 0.7 else None,
            city=fake.city(),
            state=fake.state_abbr(),
            zip_code=fake.zipcode(),
            customer_since=customer_since,
            notes=fake.sentence() if random.random() > 0.8 else None
        )
        customers.append(customer)

    db.add_all(customers)
    db.commit()
    print(f"Created {count} customers")
    return customers


def create_mechanics(db: Session, count: int = 50):
    """Create mechanic records."""
    print(f"Creating {count} mechanics...")
    mechanics = []

    for _ in range(count):
        cert_level = random.choice(list(CertificationLevel))

        # Set hourly rate based on certification
        if cert_level == CertificationLevel.APPRENTICE:
            hourly_rate = Decimal(str(random.uniform(25, 40)))
        elif cert_level == CertificationLevel.JOURNEYMAN:
            hourly_rate = Decimal(str(random.uniform(40, 65)))
        else:  # Master
            hourly_rate = Decimal(str(random.uniform(65, 95)))

        # Random specialties (1-4)
        num_specialties = random.randint(1, 4)
        specialties = random.sample(SPECIALTIES, num_specialties)

        mechanic = Mechanic(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            certification_level=cert_level,
            specialties=specialties,
            hourly_rate=round(hourly_rate, 2),
            is_active=random.random() > 0.1  # 90% active
        )
        mechanics.append(mechanic)

    db.add_all(mechanics)
    db.commit()
    print(f"Created {count} mechanics")
    return mechanics


def create_vehicles(db: Session, customers: list, count: int = 750):
    """Create vehicle records."""
    print(f"Creating {count} vehicles...")
    vehicles = []

    # Some customers have multiple vehicles
    customer_vehicle_count = {}
    for _ in range(count):
        customer = random.choice(customers)
        customer_vehicle_count[customer.id] = customer_vehicle_count.get(customer.id, 0) + 1

        make = random.choice(list(CAR_MAKES_MODELS.keys()))
        model = random.choice(CAR_MAKES_MODELS[make])
        year = random.randint(2005, 2024)

        # Mileage based on age
        age = 2024 - year
        base_mileage = age * random.randint(8000, 15000)
        mileage = base_mileage + random.randint(0, 10000)

        vehicle = Vehicle(
            customer_id=customer.id,
            vin=generate_vin(),
            year=year,
            make=make,
            model=model,
            trim=fake.word().title() if random.random() > 0.5 else None,
            color=random.choice(COLORS),
            license_plate=fake.license_plate(),
            mileage=mileage
        )
        vehicles.append(vehicle)

    db.add_all(vehicles)
    db.commit()
    print(f"Created {count} vehicles")
    return vehicles


def create_work_orders_with_details(db: Session, vehicles: list, customers: list, mechanics: list, count: int = 2000):
    """Create work orders with parts and labor."""
    print(f"Creating {count} work orders with parts and labor...")

    work_orders = []
    all_parts = []
    all_labor = []

    # Track work order sequence by date
    wo_sequence = {}

    # Create work orders distributed over the past 2 years
    start_date = datetime.now() - timedelta(days=730)

    for i in range(count):
        vehicle = random.choice(vehicles)
        customer = next(c for c in customers if c.id == vehicle.customer_id)
        mechanic = random.choice([m for m in mechanics if m.is_active])

        # Random date in past 2 years
        days_offset = random.randint(0, 730)
        created_date = start_date + timedelta(days=days_offset)

        # Generate work order number
        date_key = created_date.strftime('%Y%m%d')
        wo_sequence[date_key] = wo_sequence.get(date_key, 0) + 1
        work_order_number = generate_work_order_number(created_date, wo_sequence[date_key])

        # Determine status based on age
        days_old = (datetime.now() - created_date).days
        if days_old > 14:
            # Old orders are likely completed or cancelled
            status = random.choices(
                [WorkOrderStatus.COMPLETED, WorkOrderStatus.CANCELLED],
                weights=[0.95, 0.05]
            )[0]
        elif days_old > 7:
            status = random.choices(
                [WorkOrderStatus.COMPLETED, WorkOrderStatus.IN_PROGRESS, WorkOrderStatus.WAITING_PARTS],
                weights=[0.7, 0.2, 0.1]
            )[0]
        else:
            # Recent orders
            status = random.choices(
                [WorkOrderStatus.PENDING, WorkOrderStatus.IN_PROGRESS, WorkOrderStatus.COMPLETED],
                weights=[0.3, 0.5, 0.2]
            )[0]

        priority = random.choices(
            list(WorkOrderPriority),
            weights=[0.2, 0.5, 0.2, 0.1]  # low, normal, high, urgent
        )[0]

        # Generate description and concern
        concerns = [
            "Vehicle making strange noise",
            "Check engine light is on",
            "Brakes feel soft",
            "Scheduled maintenance",
            "Oil change needed",
            "Tire replacement needed",
            "Battery issues",
            "AC not working properly",
            "Transmission slipping",
            "Engine overheating"
        ]

        customer_concern = random.choice(concerns)
        description = f"Service request: {customer_concern}"
        diagnosis = fake.paragraph() if status != WorkOrderStatus.PENDING else None

        # Completion dates
        if status == WorkOrderStatus.COMPLETED:
            actual_completion = created_date + timedelta(days=random.randint(1, 5))
            estimated_completion = actual_completion - timedelta(hours=random.randint(0, 12))
        elif status in [WorkOrderStatus.IN_PROGRESS, WorkOrderStatus.WAITING_PARTS]:
            estimated_completion = created_date + timedelta(days=random.randint(1, 7))
            actual_completion = None
        else:
            estimated_completion = None
            actual_completion = None

        # Odometer readings
        odometer_in = vehicle.mileage + random.randint(0, 5000)
        odometer_out = odometer_in + random.randint(5, 50) if actual_completion else None

        work_order = WorkOrder(
            work_order_number=work_order_number,
            vehicle_id=vehicle.id,
            customer_id=customer.id,
            assigned_mechanic_id=mechanic.id,
            status=status,
            priority=priority,
            description=description,
            customer_concern=customer_concern,
            diagnosis=diagnosis,
            estimated_completion=estimated_completion,
            actual_completion=actual_completion,
            odometer_in=odometer_in,
            odometer_out=odometer_out,
            created_at=created_date,
            updated_at=created_date
        )
        work_orders.append(work_order)

    # Commit work orders first to get IDs
    db.add_all(work_orders)
    db.commit()

    # Now add parts and labor for each work order
    print("Adding parts and labor to work orders...")
    for work_order in work_orders:
        # Determine number of parts and labor items based on type of work
        num_parts = random.randint(1, 5)
        num_labor = random.randint(1, 3)

        subtotal_parts = Decimal("0.00")
        subtotal_labor = Decimal("0.00")

        # Add parts
        for _ in range(num_parts):
            part_info = random.choice(PARTS_CATALOG)
            quantity = random.randint(1, 2) if part_info["part_number"].startswith("TR-") else 1

            unit_cost = part_info["unit_cost"]
            total_cost = unit_cost * quantity
            subtotal_parts += total_cost

            part = Part(
                work_order_id=work_order.id,
                part_number=part_info["part_number"],
                description=part_info["description"],
                quantity=quantity,
                unit_cost=unit_cost,
                total_cost=total_cost,
                supplier=part_info["supplier"],
                warranty_months=part_info["warranty"],
                created_at=work_order.created_at
            )
            all_parts.append(part)

        # Add labor
        mechanic = next(m for m in mechanics if m.id == work_order.assigned_mechanic_id)
        for _ in range(num_labor):
            labor_info = random.choice(LABOR_TASKS)
            hours = labor_info["hours"]
            hourly_rate = mechanic.hourly_rate
            total_cost = hours * hourly_rate
            subtotal_labor += total_cost

            labor = LaborItem(
                work_order_id=work_order.id,
                mechanic_id=mechanic.id,
                description=labor_info["description"],
                hours=hours,
                hourly_rate=hourly_rate,
                total_cost=total_cost,
                created_at=work_order.created_at
            )
            all_labor.append(labor)

        # Calculate totals
        tax_rate = Decimal("0.08")
        tax_amount = (subtotal_parts + subtotal_labor) * tax_rate
        total_amount = subtotal_parts + subtotal_labor + tax_amount

        # Update work order financials
        work_order.subtotal_parts = subtotal_parts
        work_order.subtotal_labor = subtotal_labor
        work_order.tax_amount = tax_amount
        work_order.total_amount = total_amount

        # Payment status and method
        if work_order.status == WorkOrderStatus.COMPLETED:
            payment_status = random.choices(
                [PaymentStatus.PAID, PaymentStatus.UNPAID, PaymentStatus.PARTIAL],
                weights=[0.85, 0.10, 0.05]
            )[0]
            if payment_status == PaymentStatus.PAID:
                payment_method = random.choice(list(PaymentMethod))
            else:
                payment_method = None
        else:
            payment_status = PaymentStatus.UNPAID
            payment_method = None

        work_order.payment_status = payment_status
        work_order.payment_method = payment_method

    # Commit all parts and labor
    db.add_all(all_parts)
    db.add_all(all_labor)
    db.commit()

    print(f"Created {count} work orders with {len(all_parts)} parts and {len(all_labor)} labor items")
    return work_orders


def create_initial_api_keys(db: Session):
    """Create some initial API keys for testing."""
    print("Creating initial API keys...")

    api_keys = [
        APIKey(
            key="test-key-1234567890",
            name="Test API Key",
            is_active=True
        ),
        APIKey(
            key="demo-key-abcdefghij",
            name="Demo API Key",
            is_active=True
        )
    ]

    db.add_all(api_keys)
    db.commit()
    print(f"Created {len(api_keys)} API keys")
    return api_keys


def seed_database():
    """Main function to seed the database."""
    print("Starting database seed...")
    print("=" * 50)

    # Initialize database tables
    print("Initializing database tables...")
    init_db()

    # Create session
    db = SessionLocal()

    try:
        # Check if data already exists
        existing_customers = db.query(Customer).count()
        if existing_customers > 0:
            print(f"Database already contains {existing_customers} customers.")
            response = input("Do you want to continue and add more data? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("Seeding cancelled.")
                return

        # Create data
        customers = create_customers(db, 500)
        mechanics = create_mechanics(db, 50)
        vehicles = create_vehicles(db, customers, 750)
        work_orders = create_work_orders_with_details(db, vehicles, customers, mechanics, 2000)
        api_keys = create_initial_api_keys(db)

        print("=" * 50)
        print("Database seeding completed successfully!")
        print(f"Summary:")
        print(f"  - Customers: {len(customers)}")
        print(f"  - Mechanics: {len(mechanics)}")
        print(f"  - Vehicles: {len(vehicles)}")
        print(f"  - Work Orders: {len(work_orders)}")
        print(f"  - API Keys: {len(api_keys)}")
        print("\nTest API Keys:")
        for key in api_keys:
            print(f"  - {key.name}: {key.key}")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
