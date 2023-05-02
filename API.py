import os
import csv
from dotenv import load_dotenv
from flask import Flask, jsonify

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# create a base class for our models
Base = declarative_base()

# define a Leaderboard model
class Leaderboard(Base):
    __tablename__ = 'leaderboard'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    first_name = Column(String(120))
    last_name = Column(String(120))
    number_of_messages = Column(Integer) 

json_payload = {
    "data_path": os.getenv("PIPELINE_CSV_PATH")
                           # Path to your pipeline_result.csv file
}

db_uri = os.getenv('db_uri') # Your DB_URI path

# Get the data_path field from the JSON payload
data_path = json_payload['data_path']

# create a database engine
engine = create_engine(db_uri, pool_pre_ping=True)

# create the table
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

app = Flask(__name__)

@app.post('/feed')
def feed_data():
    session = Session()
    
    # Open the CSV file and read the data
    with open(data_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # skip the header row
        
        # Store the data in the database
        for row in csv_reader:
            new_leaderboard = Leaderboard(user_id=row[0], first_name=row[1], last_name=row[2], number_of_messages=row[3])
            session.add(new_leaderboard)
            session.commit()
        
    session.close()
    
    return jsonify({'message': 'Data successfully fed into the database'}), 200


@app.get("/leaderboard")
def get_leaderboard():
    session = Session()
    
    response = session.query(Leaderboard).all()
    
    data = {
        "leaderboard": []
    }
    
    for result in response:
        data['leaderboard'].append({
            'user_id': result.user_id,
            'first_name': result.first_name,
            'last_name': result.last_name,
            'number_of_messages': result.number_of_messages
            })
        
    session.close()
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3000)