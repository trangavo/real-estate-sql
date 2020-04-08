from create import Agent, AgentCom, Office, Sale, Listing, Commission, Summary, engine, metadata
from insert_data import session, engine
import sqlalchemy, datetime
from datetime import datetime, date
from sqlalchemy import create_engine, Table, Column, Text, Integer, ForeignKey, Float, DateTime, MetaData, func, extract
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Actually create the tables
Agent = Table('Agent', metadata, autoload=True, autoload_with=engine)
Office = Table('Office', metadata, autoload=True, autoload_with=engine)
Listing = Table('Listing', metadata, autoload=True, autoload_with=engine)
Sale = Table('Sale', metadata, autoload=True, autoload_with=engine)
Commission = Table('Commission', metadata, autoload=True, autoload_with=engine)
Summary = Table('Summary', metadata, autoload=True, autoload_with=engine)

# Print out all the tables
print('Listing Table', session.query(Listing).all())
print('-----------')
print('Office Table', session.query(Office).all())
print('-----------')
print('Agent Table', session.query(Agent).all())
print('-----------')
print('Sale Table', session.query(Sale).all())
print('-----------')
print('Commission Table', session.query(Commission).all())
print('-----------')
print('Summary Table', session.query(Summary).all())
print('-----------')

y = 2020
m = 3
n = 5

# Top 5 offices with most sales for a particular month
def top_office(y, m, n):
    print('Top 5 offices with most sales', session.query(Listing.columns.office_id,\
    func.count(Listing.columns.office_id)).join(Sale).\
    filter(Sale.columns.listing_id==Listing.columns.listing_id).\
    filter(extract('year', Sale.columns.sale_date) == 2020).filter(extract('month', Sale.columns.sale_date) == 3).\
    group_by(Listing.columns.office_id).order_by(func.count(Listing.columns.office_id).desc()).all()[:n])
top_office(y, m, n)
print('-----------')

# Top 5 agents with mose sales and their info
def top_agent(y, m, n):
    print('Top 5 agents with mose sales and their info', session.query(Agent.columns.agent_id, Agent.columns.email,\
    func.count(Agent.columns.agent_id)).join(Sale).\
    filter(Sale.columns.agent_id==Agent.columns.agent_id).\
    filter(extract('year', Sale.columns.sale_date) == y).filter(extract('month', Sale.columns.sale_date) == m).\
    group_by(Agent.columns.agent_id).order_by(func.count(Agent.columns.agent_id).desc()).all()[:n])
top_agent(y, m, n)
print('-----------')

# Calculate the commission for each agent and store in a separate table
def agent_com(y, m):
    agent_com = session.query(Sale.columns.agent_id, func.sum(Commission.columns.commission)).\
    join(Commission).filter(Sale.columns.agent_id==Commission.columns.agent_id).\
    filter(extract('year', Sale.columns.sale_date) == y).filter(extract('month', Sale.columns.sale_date) == m).\
    group_by(Sale.columns.agent_id).order_by(func.sum(Commission.columns.commission).desc()).all()

    print('Agents and commission', agent_com)

    agent_ls = []
    for agent in agent_com:
        agent_ls.append(AgentCom(agent_id=agent[0], monthly_com=agent[1]))
    try:
        session.add_all(agent_ls)
        session.commit
    except:
        session.rollback()
        raise
    finally:
        session.close()

    Agentcom = Table('AgentCom', metadata, autoload=True, autoload_with=engine)

agent_com(y, m)
print('-----------')

# For all houses that were sold that month, calculate the average number of days that the house was on the market.
def avg_time(y, m):
    houses = session.query(Listing.columns.listing_date, Sale.columns.sale_date).join(Sale).\
    filter(Listing.columns.listing_id==Sale.columns.listing_id).\
    filter(extract('year', Sale.columns.sale_date) == y).filter(extract('month', Sale.columns.sale_date) == m).all()
    time_on_market = 0
    for house in houses:
        time_on_market += (house[1]-house[0]).days
    print('Average time on market', time_on_market / len(houses))
avg_time(y, m)
print('-----------')

# For all houses that were sold that month, calculate the average selling price
def avg_price(y, m):
    print('Average selling price', session.query(func.avg(Sale.columns.sale_price)).\
    filter(extract('year', Sale.columns.sale_date) == y).\
    filter(extract('month', Sale.columns.sale_date) == m).all()[0][0])
avg_price(y, m)
print('-----------')

# Find the zip codes with the top 5 average sales prices
def top_area(y, m):
    print('Zip codes with the top 5 average sales prices', session.query(Listing.columns.zip_code, func.avg(Sale.columns.sale_price)).\
    filter(Listing.columns.listing_id==Sale.columns.listing_id).\
    filter(extract('year', Sale.columns.sale_date) == y).filter(extract('month', Sale.columns.sale_date) == m).\
    group_by(Listing.columns.zip_code).order_by(func.avg(Sale.columns.sale_price).desc()).all()[:n])
top_area(y, m)
print('-----------')
