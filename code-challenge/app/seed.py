from datetime import datetime
from faker import Faker
from models import db, Power, Hero, HeroPower
from app import app

fake = Faker()

def seed_powers():
    powers_data = [
        {"name": fake.word(), "description": fake.text()[:20]} for _ in range(10)
    ]

    for power_info in powers_data:
        power = Power(**power_info, created_at=datetime.now(), updated_at=datetime.now())
        db.session.add(power)

def seed_heroes():
    heroes_data = [
        {"name": fake.name(), "super_name": fake.word()} for _ in range(10)
    ]

    for hero_info in heroes_data:
        hero = Hero(**hero_info, created_at=datetime.now(), updated_at=datetime.now())
        db.session.add(hero)

def seed_hero_powers():
    strengths = ["Strong", "Weak", "Average"]

    heroes = Hero.query.all()

    for hero in heroes:
        for _ in range(1, 4):
            power = Power.query.order_by(db.func.random()).first()
            hero_power = HeroPower(
                hero_id=hero.id,
                power_id=power.id,
                strength=fake.random_element(elements=strengths),
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            db.session.add(hero_power)
            db.session.commit()

def seed_data():
    seed_powers()
    seed_heroes()
    seed_hero_powers()

if __name__ == '__main__':
    with app.app_context():
        print("Seeding started -----")
        seed_data()
        print("Seeded successfully")
