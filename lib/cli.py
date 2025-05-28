import click
from lib.db.database import engine, SessionLocal
from lib.models import Base, Car, Customer, Rental

# Initialize database schema
@click.group()
def cli():
    """Car Rental CLI"""
    pass

@cli.command()
def init_db():
    """Create database tables"""
    Base.metadata.create_all(bind=engine)
    click.echo("🔧 Database initialized.")

@cli.command()
@click.argument('make')
@click.argument('model')
@click.argument('year', type=int)
def add_car(make, model, year):
    """Add a new car to the fleet"""
    session = SessionLocal()
    car = Car(make=make, model=model, year=year)
    session.add(car)
    session.commit()
    click.echo(f"🚗 Added car {car.id}: {make} {model} ({year})")
    session.close()

@cli.command()
def list_cars():
    """List all cars in the fleet"""
    session = SessionLocal()
    cars = session.query(Car).all()
    for c in cars:
        status = 'Available' if c.available else 'Rented'
        click.echo(f"{c.id}: {c.make} {c.model} ({c.year}) — {status}")
    session.close()

@cli.command()
@click.argument('name')
def add_customer(name):
    """Register a new customer"""
    session = SessionLocal()
    cust = Customer(name=name)
    session.add(cust)
    session.commit()
    click.echo(f"🙋‍♂️ Added customer {cust.id}: {name}")
    session.close()

@cli.command()
def list_customers():
    """List all registered customers"""
    session = SessionLocal()
    for cust in session.query(Customer).all():
        click.echo(f"{cust.id}: {cust.name}")
    session.close()

@cli.command()
@click.argument('car_id', type=int)
@click.argument('customer_id', type=int)
@click.argument('start_date', type=click.DateTime(formats=["%Y-%m-%d"]))
def rent_car(car_id, customer_id, start_date):
    """Rent out a car to a customer"""
    session = SessionLocal()
    car = session.get(Car, car_id)
    cust = session.get(Customer, customer_id)
    if not car or not car.available:
        click.secho("Error: Car unavailable.", fg='red')
        return
    if not cust:
        click.secho("Error: Customer not found.", fg='red')
        return
    rental = Rental(
        car_id=car_id,
        customer_id=customer_id,
        start_date=start_date.date()
    )
    car.available = False
    session.add(rental)
    session.commit()
    click.echo(f"🔑 Car {car_id} rented to customer {customer_id} from {start_date.date()}")
    session.close()

@cli.command()
@click.argument('rental_id', type=int)
@click.argument('end_date', type=click.DateTime(formats=["%Y-%m-%d"]))
def return_car(rental_id, end_date):
    """Return a car and close a rental"""
    session = SessionLocal()
    rent = session.get(Rental, rental_id)
    if not rent or rent.end_date:
        click.secho("Error: Invalid rental ID or already returned.", fg='red')
        return
    rent.end_date = end_date.date()
    rent.car.available = True
    session.commit()
    click.echo(f"🔄 Rental {rental_id} closed on {end_date.date()}")
    session.close()

@cli.command()
def list_rentals():
    """Show all rentals"""
    session = SessionLocal()
    for r in session.query(Rental).all():
        status = 'Returned' if r.end_date else 'Active'
        click.echo(f"{r.id}: Car {r.car_id} → Cust {r.customer_id}, {r.start_date} to {r.end_date or '...'} [{status}]")
    session.close()

if __name__ == '__main__':
    cli()