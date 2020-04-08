### Structure of the project
1. `README.md`
This is the README.md file that explains basically everything one should know about the project, including its structure, how to run it, what's in each file, etc.
2. `__init__`.py
This is the file that makes Python know that other Python files in the current directory can be considered a package, so that we can import them into other files later.
3. requirements.txt
This file lists out all the dependencies that we need to install in order to run the project.
4. `create.py`
This is where all the models for the tables in the database are created.
5. `insert_data.py`
This is where all the data is inserted into the tables.
6. `query_data.py`
This is where all the queries are made.

### How to run the project
```$ python3.6 -m venv .venv``` - to create a virtual environment

```$ source .venv/bin/activate``` - to activate the virtual environment

```$ pip3 install -r requirements.txt``` - to install all the necessary packages

```$ python3 create.py``` - to create the database and the tables in it

```$ python3 insert_data.py``` - to insert the data into the database

```$ python3 query_data.py``` - to query the database

### Structure of the database (`create.py`)
There are 8 tables in the database:
- Agent stores all info about the agents, the primary key is agent_id;
- Office stores all info about the offices, the primary key is office_id;
- AgentOffice is the association table to demonstrate the many-to-many relationship between agents and offices;
- Listing stores all the info about the listings, the primary key is listing_id, the foreign keys are agent_id and office_id;
- Sale stores all the info about the sold houses, the primary key is sale_id, the foreign keys are listing_id, agent_id;
- Commission stores the commission that corresponds to each sale, the primary key is sale_id, the foreign key is agent_id;
- AgentCom stores the monthly commissions for each agent, the primary key is agent_id
- Summary stores the total number of sales and the total prices over time

Some assumptions about the system:
- Each property has one listing agent, and if sold, one selling agent.
- The listing agent for one property is not necessarily the same as the selling agent, as long as they all work at the same office in the area of the property (i.e., sharing the same zip code).
- Each area with a distinct zip code only has one office.

Most the tables are in standard 4th normalization form (4NF). Take the table Sale for example. It is in the first normalization form (1NF) because each cell only has one value, all the entries in the same field are the same data type, and each row is uniquely identified with a primary key. It is in the second normalization form because it is already in 1NF, and all the non-key columns are dependent on the key column. If we had added the number of bedrooms to the Sale table, this would have been violated, because the number of bedroom depends on the actual property which is the listing. The table is in the third normal form (3NF) because it is in 2NF, and all fields only depend on the key, not other fields. For example, by looking at the the sale price or the sale agent, we wouldn't be able to figure out the sale date. Finally, it is in 4NF because it is already in 3NF, and there are no multi-valued dependencies. This would have been violated if I had added agent's emails to the table, so if the agent was changed, the email would have to change. That's why we have a separate table to store all info about agents.

The Listing table is not in 4NF because we have zip_code and office_id in it, which violated the last rule, and it is kinda redundant because from the office_id we can totally figure out the zip_code by using the Office table. But in the instructions, it is said that whenever a listing is made, both info should be captured. This could be useful if an area of a zip code had multiple offices.

It is important to notice that a Commission table was created outside of the Sale table (even though it would make total sense to merge them into one). The reason I separated them was because of the different commission rate. It would be tedious and not efficient to hard-code the commission given a selling price if we had such different rates, and because we can't do the calculations when we insert the data about the sale, a separate commission table was needed. In practice, if we had a mechanism such that once a property is sold, all the info is stored, together with the commission already calculated somewhere before it was put into the database, then we wouldn't need 2 tables. Then I created AgentCom table to store the total commission of each agent for that particular month as instructed.

### Inserting and updating (`insert_data.py`)
Each change created to the database, either insertion or update, is wrapped in a transaction with the following structure:

```
try:
  <insertion/update>
  session.commit()
except:
  session.rollback()
  raise
finally:
  session.close()
```

This is to ensure that unless everything in the transaction is successfully carried out, nothing will be carried out and saved at all. This is to ensure the consistency of the database, so that for example, once a house is sold, it would be marked as sold in the Listing table. Without such a transaction, if a disruption happens in the process, such a house might appear in the Sale table but its status in the Listing won't be updated yet.

### Querying (`query_data.py`)
All the data is queried for March, 2020 only. All the query functions are neatly constructed and very simple to understand. Most of them take y and m as parameters because we want to do this report monthly, so it makes sense to have the year and the month as parameters so we could easily filter out only the sales that happen in that month.
