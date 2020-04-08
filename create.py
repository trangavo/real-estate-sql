import sqlalchemy, datetime
from datetime import datetime, date
from sqlalchemy import create_engine, Table, Column, Text, Integer, ForeignKey, Float, DateTime, MetaData, func, extract
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Create and connect engine to the database
engine = create_engine('sqlite:///:memory:', echo = True)
engine.connect()
connection = engine.connect()
metadata = MetaData()
Base = declarative_base()

# Define Listing table
class Listing(Base):
    __tablename__ = 'Listing'
    listing_id = Column(Integer, primary_key=True)
    seller_id = Column(Integer)
    num_bed = Column(Integer)
    num_bath = Column(Integer)
    listing_price = Column(Float(15, 2))
    zip_code = Column(Integer)
    listing_date = Column(DateTime)
    agent_id = Column(Integer, ForeignKey('Agent.agent_id'))
    office_id = Column(Integer, ForeignKey('Office.office_id'))
    status = Column(Text)

    def __repr__(self):
        return '<Listing(id: {0}, seller: {1}, date: {2}, agent: {3}, status: {4})>'.format(self.listing_id,\
        self.seller_id, self.listing_date, self.agent_id, self.status)

agent_office = Table('AgentOffice', Base.metadata,
    Column('agent_id', Integer, ForeignKey('Agent.agent_id')),
    Column('office_id', Integer, ForeignKey('Office.office_id'))
)

# Create Office table
class Office(Base):
    __tablename__ = 'Office'
    office_id = Column(Integer, primary_key=True)
    zip_code = Column(Integer)
    listing = relationship("Listing")
    agent = relationship("Agent", secondary='AgentOffice')
    def __repr__(self):
        return '<Office(id: {0}, zip_code: {1})>'.format(self.office_id, self.zip_code)

# Create Agent table
class Agent(Base):
    __tablename__ = 'Agent'
    agent_id = Column(Integer, primary_key=True)
    name = Column(Text)
    email = Column(Text)
    phone = Column(Text)
    listing = relationship("Listing")
    office = relationship("Office", secondary='AgentOffice')
    commission = relationship("Commission")
    agentcom = relationship("AgentCom")

    def __repr__(self):
        return '<Agent(id: {0},name: {1},email: {2})>'\
        .format(self.agent_id, self.name, self.email)

# Create AgentCom table
class AgentCom(Base):
    __tablename__ = 'AgentCom'
    agent_id = Column(Integer, ForeignKey('Agent.agent_id'), primary_key=True)
    monthly_com = Column(Float(15, 2))

    def __repr__(self):
        return '<AgentCom(id: {0}, monthly_com: {1})>'.format(self.agent_id, self.monthly_com)

# Create Sale table
class Sale(Base):
    __tablename__ = 'Sale'
    sale_id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('Listing.listing_id'))
    sale_price = Column(Float(15,2))
    sale_date = Column(DateTime)
    agent_id = Column(Integer, ForeignKey('Agent.agent_id'))
    commission = relationship('Commission')

    def __repr__(self):
        return '<Sale(id: {0}, listing: {1}, price: {2}, date:{3})>'.format(self.sale_id,\
        self.listing_id, self.sale_price, self.sale_date)

# Create Commission table
class Commission(Base):
    __tablename__ = 'Commission'
    sale_id = Column(Integer, ForeignKey('Sale.sale_id'), primary_key=True)
    agent_id = Column(Integer, ForeignKey('Agent.agent_id'))
    commission = Column(Float(15, 2))

    def __repr__(self):
        return '<Commission(sale: {0}, agent: {1}, commission: {2})>'.format(self.sale_id, self.agent_id, self.commission)

# Create Summary table
class Summary(Base):
    __tablename__ = 'Summary'
    id = Column(Integer, primary_key=True)
    num_sale = Column(Integer)
    tot_price = Column(Float(15,2))

    def __repr__(self):
        return '<Summary(num_sale: {0}, total_price: {1})>'.format(self.num_sale, self.tot_price)

Base.metadata.create_all(engine)
