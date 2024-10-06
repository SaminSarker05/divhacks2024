# Simulation to add to MongoDB

from faker import Faker
import random
import math
from pymongo import MongoClient
import re

fake = Faker()

client = MongoClient("mongodb+srv://saminsarker05:MrutdMWZtMlwi5JU@cluster0.oyvge.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.flask_db
users = db.users

def validate_government_id(government_id):
    if re.match(r"^[A-Z0-9]{6,10}$", government_id) and 'X' not in government_id:
        return True
    return False

def calculate_fair_score(monthly_income, monthly_debt_payments, current_savings, current_debt, savings_goal, max_dti_threshold=50, max_sir_threshold=200):
    weight_dti = 0.4
    weight_sir = 0.4
    weight_din = 0.2

    dti = (monthly_debt_payments / monthly_income) * 100 if monthly_income > 0 else 0
    sir = (current_savings / monthly_income) * 100 if monthly_income > 0 else 0
    din = math.log(1 + (current_debt / monthly_income)) if monthly_income > 0 else 0

    score = max(0, 100 - (dti * weight_dti) + (sir * weight_sir) - (din * weight_din))
    return score

def generate_person(high_score=False, mediocre_score=False, low_score=False):
    person = {
        'full_name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'address': fake.address(),
        'marital_status': random.choice(['Single', 'Divorced', 'Married']),
        'occupation': fake.job(),
        'employer': fake.company(),
        'monthly_income': random.randint(1000, 15000) if high_score else random.randint(1000, 6000) if mediocre_score else random.randint(500, 3000),
        'total_debt': random.randint(0, 3000) if high_score else random.randint(1000, 5000) if mediocre_score else random.randint(4000, 10000),
        'monthly_debt_payments': random.randint(100, 1000),
        'current_savings': random.randint(5000, 100000) if high_score else random.randint(1000, 5000) if mediocre_score else random.randint(0, 2000),
        'savings_goal': random.randint(5000, 20000),
        'dependents': random.randint(0, 3),
        'government_id': fake.bothify(text="??#####"),
        'ssn': None,
        'banking_info': fake.bban(),
    }
    return person

people = []
for _ in range(2):
    person = generate_person(high_score=True)
    person['score'] = calculate_fair_score(person['monthly_income'], person['monthly_debt_payments'], person['current_savings'], person['total_debt'], person['savings_goal'])
    people.append(person)

for _ in range(2):
    person = generate_person(mediocre_score=True)
    person['score'] = calculate_fair_score(person['monthly_income'], person['monthly_debt_payments'], person['current_savings'], person['total_debt'], person['savings_goal'])
    people.append(person)

for _ in range(2):
    person = generate_person(low_score=True)
    person['score'] = calculate_fair_score(person['monthly_income'], person['monthly_debt_payments'], person['current_savings'], person['total_debt'], person['savings_goal'])
    people.append(person)

person_no_occupation = {
    'full_name': fake.name(),
    'email': fake.email(),
    'phone': fake.phone_number(),
    'address': fake.address(),
    'marital_status': random.choice(['Single', 'Divorced', 'Married']),
    'occupation': None,
    'employer': None,
    'monthly_income': None,
    'total_debt': None,
    'monthly_debt_payments': None,
    'current_savings': None,
    'savings_goal': None,
    'dependents': None,
    'government_id': fake.bothify(text="??#####"),
    'ssn': None,
    'banking_info': None,
}

person_with_misdemeanor = generate_person()
person_with_misdemeanor['government_id'] = fake.bothify(text="??XX###")

for person in people:
    print(f"Adding {person['full_name']} with score {person['score']:.2f} to MongoDB")
    users.insert_one(person)

if not person_no_occupation['occupation']:
    print(f"Cannot add {person_no_occupation['full_name']} - No occupation provided.")

if not validate_government_id(person_with_misdemeanor['government_id']):
    print(f"Cannot add {person_with_misdemeanor['full_name']} - Misdemeanor detected.")

print("Simulation complete.")
