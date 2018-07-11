import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

with open ('zips.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader, None)
    for row in reader:
        db.execute("INSERT INTO zip (zipcode, city, state, lat, long, population) VALUES (:zipcode, :city, :state, :lat, :long, :population)",
            {"zipcode": row[0], "city": row[1], "state": row[2], "lat": row[3], "long": row[4], "population": row[5]})
        db.commit()