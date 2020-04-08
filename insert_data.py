from create import Agent, Office, Sale, Listing, Commission, Summary, engine, AgentCom
import sqlalchemy, datetime
from datetime import datetime, date
from sqlalchemy import create_engine, Table, Column, Text, Integer, ForeignKey, Float, DateTime, MetaData, func, extract
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Make a session
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()

# Define commission calculation
def commission_cal(x):
    if x < 100000:
        return x*0.01
    elif x < 200000:
        return x*0.075
    elif x < 500000:
        return x*0.06
    elif x < 1000000:
        return x*0.05
    else:
        return x*0.04

# Transaction - insert initial value to the summary
try:
    session.add(Summary(id=1, num_sale=0,tot_price=0))
    session.commit()
except:
    session.rollback()
    raise
finally:
    session.close()

# Transaction - insert agent and office info
try:
    agent_data = [Agent(agent_id=1, name='Harvey Spector', email='s.harvey@gmail.com', phone='123-456-789'),\
                Agent(agent_id=2, name='Donna Paulsen', email='p.donna@gmail.com', phone='789-456-123'),\
                Agent(agent_id=3, name='Louis Litt', email='l.louis@gmail.com', phone='123-456-123'),\
                Agent(agent_id=4, name='Mike Ross', email='r.mike@gmail.com', phone='000-456-123'),\
                Agent(agent_id=6, name='Jessica Pearson', email='p.jessica@gmail.com', phone='000-416-993'),
                Agent(agent_id=7, name='Rachel Zane', email='z.rachel@gmail.com', phone='000-459-993'),
                Agent(agent_id=8, name='Norma', email='p.jessica@gmail.com', phone='000-456-983')]

    office_data = [Office(office_id=1, zip_code=555, agent=[agent_data[0], agent_data[1]]),\
    Office(office_id=2, zip_code=777, agent=[agent_data[1], agent_data[2]]),\
    Office(office_id=3, zip_code=999, agent=[agent_data[2], agent_data[3]]),\
    Office(office_id=4, zip_code=333, agent=[agent_data[0], agent_data[3], agent_data[4]]),
    Office(office_id=5, zip_code=111, agent=[agent_data[5], agent_data[6]]),
    Office(office_id=6, zip_code=222, agent=[agent_data[4], agent_data[6], agent_data[2]])]

    session.add_all(agent_data)
    session.add_all(office_data)
    session.commit()
except:
    session.rollback()
    raise
finally:
    session.close()

# Transaction - insert listing data
try:
    listing_data = [Listing(listing_id=1, seller_id=1,num_bed=2,num_bath=1,listing_price=90000.43,zip_code=555, listing_date=datetime.strptime('2018-03-03 20:59:29', '%Y-%m-%d %H:%M:%S'), agent_id=1,office_id=1,status='Available'),\
    Listing(listing_id=2, seller_id=2,num_bed=2,num_bath=2,listing_price=150000.43,zip_code=555, listing_date=datetime.strptime('2019-04-06 20:59:29', '%Y-%m-%d %H:%M:%S'), agent_id=2,office_id=1,status='Available'),\
    Listing(listing_id=3, seller_id=3,num_bed=3,num_bath=2,listing_price=400000.43,zip_code=777,listing_date=datetime.strptime('2019-04-07 20:59:29', '%Y-%m-%d %H:%M:%S'), agent_id=3,office_id=2,status='Available'),\
    Listing(listing_id=4, seller_id=4,num_bed=3,num_bath=3,listing_price=900000.43,zip_code=555, listing_date=datetime.strptime('2019-04-08 20:59:29', '%Y-%m-%d %H:%M:%S'), agent_id=1,office_id=1,status='Available'),\
    Listing(listing_id=5, seller_id=5,num_bed=4,num_bath=3,listing_price=1300000.43,zip_code=333, listing_date=datetime.strptime('2019-04-09 20:59:29', '%Y-%m-%d %H:%M:%S'),agent_id=5,office_id=4,status='Available'),\
    Listing(listing_id=6, seller_id=6,num_bed=2,num_bath=1,listing_price=130000.43,zip_code=999, listing_date=datetime.strptime('2019-05-01 20:59:29', '%Y-%m-%d %H:%M:%S'),agent_id=4,office_id=3,status='Available'),\
    Listing(listing_id=7, seller_id=7,num_bed=3,num_bath=3,listing_price=900000.43,zip_code=999, listing_date=datetime.strptime('2019-05-02 20:59:29', '%Y-%m-%d %H:%M:%S'),agent_id=4,office_id=3,status='Available'),\
    Listing(listing_id=8, seller_id=8,num_bed=3,num_bath=1,listing_price=1000000.43,zip_code=333, listing_date=datetime.strptime('2019-05-03 20:59:29', '%Y-%m-%d %H:%M:%S'),agent_id=5,office_id=4,status='Available'),\
    Listing(listing_id=9, seller_id=9,num_bed=2,num_bath=2,listing_price=800000.43,zip_code=555, listing_date=datetime.strptime('2019-05-04 20:59:29', '%Y-%m-%d %H:%M:%S'),agent_id=2,office_id=1,status='Available'),\
    Listing(listing_id=10, seller_id=10,num_bed=2,num_bath=3,listing_price=1500000.43,zip_code=777, listing_date=datetime.strptime('2019-05-05 20:59:29', '%Y-%m-%d %H:%M:%S'),agent_id=3,office_id=2,status='Available'),\
    Listing(listing_id=11, seller_id=11,num_bed=2,num_bath=2,listing_price=950000.43,zip_code=111, listing_date=datetime.strptime('2019-06-05 20:59:29', '%Y-%m-%d %H:%M:%S'),agent_id=6,office_id=5,status='Available'),\
    Listing(listing_id=12, seller_id=12,num_bed=4,num_bath=3,listing_price=1400000.43,zip_code=111, listing_date=datetime.strptime('2019-07-05 20:59:29', '%Y-%m-%d %H:%M:%S'),agent_id=7,office_id=5,status='Available'),\
    Listing(listing_id=13, seller_id=13,num_bed=4,num_bath=2,listing_price=1250000.43,zip_code=222, listing_date=datetime.strptime('2019-08-05 20:59:29', '%Y-%m-%d %H:%M:%S'),agent_id=3,office_id=6,status='Available'),\
    Listing(listing_id=14, seller_id=14,num_bed=2,num_bath=1,listing_price=400000.43,zip_code=222, listing_date=datetime.strptime('2019-09-05 20:59:29', '%Y-%m-%d %H:%M:%S'),agent_id=5,office_id=6,status='Available'),\
    Listing(listing_id=15, seller_id=15,num_bed=3,num_bath=1,listing_price=970000.43,zip_code=222, listing_date=datetime.strptime('2019-10-05 20:59:29', '%Y-%m-%d %H:%M:%S'),agent_id=7,office_id=6,status='Available'),\
    Listing(listing_id=16, seller_id=16,num_bed=1,num_bath=1,listing_price=200000.43,zip_code=333, listing_date=datetime.strptime('2019-11-05 20:59:29', '%Y-%m-%d %H:%M:%S'),agent_id=4,office_id=4,status='Available'),\
    Listing(listing_id=17, seller_id=17,num_bed=2,num_bath=3,listing_price=1200000.43,zip_code=999, listing_date=datetime.strptime('2019-12-05 20:59:29', '%Y-%m-%d %H:%M:%S'),agent_id=3,office_id=3,status='Available')]

    session.add_all(listing_data)
    session.commit()
except:
    session.rollback()
    raise
finally:
    session.close()

# Transaction - insert sale data
try:
    sale_data = [Sale(sale_id=1, listing_id=1,sale_price=85000, sale_date=datetime.strptime('2019-05-05 20:59:29', '%Y-%m-%d %H:%M:%S'), agent_id=2),\
    Sale(sale_id=2, listing_id=3,sale_price=390000, sale_date=datetime.strptime('2020-03-03 20:59:29', '%Y-%m-%d %H:%M:%S'), agent_id=2),\
    Sale(sale_id=3, listing_id=4,sale_price=850000, sale_date=datetime.strptime('2020-03-06 20:59:29', '%Y-%m-%d %H:%M:%S'), agent_id=1),\
    Sale(sale_id=4, listing_id=5,sale_price=1200000, sale_date=datetime.strptime('2020-03-07 20:59:29', '%Y-%m-%d %H:%M:%S'), agent_id=5),\
    Sale(sale_id=5, listing_id=6,sale_price=120000, sale_date=datetime.strptime('2020-03-08 20:59:29', '%Y-%m-%d %H:%M:%S'), agent_id=4),\
    Sale(sale_id=6, listing_id=7,sale_price=850000, sale_date=datetime.strptime('2020-03-09 20:59:29', '%Y-%m-%d %H:%M:%S'), agent_id=3),\
    Sale(sale_id=7, listing_id=8,sale_price=950000, sale_date=datetime.strptime('2020-03-10 20:59:29', '%Y-%m-%d %H:%M:%S'), agent_id=1),\
    Sale(sale_id=8, listing_id=9,sale_price=750000, sale_date=datetime.strptime('2020-03-11 20:59:29', '%Y-%m-%d %H:%M:%S'), agent_id=2),\
    Sale(sale_id=9, listing_id=10,sale_price=1400000, sale_date=datetime.strptime('2020-03-12 20:59:29', '%Y-%m-%d %H:%M:%S'), agent_id=3),\
    Sale(sale_id=10, listing_id=11,sale_price=900000, sale_date=datetime.strptime('2020-03-15 20:59:29', '%Y-%m-%d %H:%M:%S'), agent_id=6),\
    Sale(sale_id=11, listing_id=12,sale_price=1330000, sale_date=datetime.strptime('2020-03-17 20:59:29', '%Y-%m-%d %H:%M:%S'), agent_id=7),\
    Sale(sale_id=12, listing_id=13,sale_price=1200000, sale_date=datetime.strptime('2020-03-19 20:59:29', '%Y-%m-%d %H:%M:%S'), agent_id=3),\
    Sale(sale_id=13, listing_id=14,sale_price=390000, sale_date=datetime.strptime('2020-03-28 20:59:29', '%Y-%m-%d %H:%M:%S'), agent_id=7),\
    Sale(sale_id=14, listing_id=15,sale_price=950000, sale_date=datetime.strptime('2020-03-30 20:59:29', '%Y-%m-%d %H:%M:%S'), agent_id=5)]

    session.add_all(sale_data)

    # update the summary table
    total_sale = session.query(func.sum(Sale.sale_price)).scalar()
    summary = session.query(Summary).first()
    summary.num_sale += len(sale_data)
    summary.tot_price += total_sale

    # insert commission to the commission table for each sale
    for sale in session.query(Sale).all():
        session.add(Commission(sale_id=sale.sale_id, agent_id=sale.agent_id, commission=commission_cal(sale.sale_price)))
    # update listing status
    listing_sold = session.query(Listing).join(Sale).filter(Listing.listing_id==Sale.listing_id).all()
    for each in listing_sold:
        each.status = 'Sold'

    session.commit()
except:
    session.rollback()
    raise
finally:
    session.close()
