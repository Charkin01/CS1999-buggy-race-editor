import sqlite3

DATABASE_FILE = "database.db"

# important:
#-------------------------------------------------------------
# This script initialises your database for you using SQLite,
# just to get you started... there are better ways to express
# the data you're going to need... especially outside SQLite.
# For example... maybe flag_pattern should be an ENUM (which
# is available in most other SQL databases), or a foreign key
# to a pattern table?
#
# Also... the name of the database (here, in SQLite, it's a
# filename) appears in more than one place in the project.
# That doesn't feel right, does it?
#
#-------------------------------------------------------------

con = sqlite3.connect(DATABASE_FILE)
print("- Opened database successfully in file \"{}\"".format(DATABASE_FILE))

# using Python's triple-quote for multi-line strings:
'''
Wheels and flags inherit previous value.
The rest are set to default settings
Special rendomises all values that do not have cost



'''

con.execute("""

  CREATE TABLE IF NOT EXISTS buggies (
    id                    INTEGER PRIMARY KEY,
    qty_wheels            INTEGER DEFAULT 4,
    flag_color            VARCHAR(20) DEFAULT White,
    flag_color_secondary  VARCHAR(20) DEFAULT Black,
    flag_pattern          VARCHAR(20) DEFAULT Plain,
    hamster_booster       INTEGER DEFAULT 0,
    total_cost            INTEGER,
    power_type            VARCHAR(20) DEFAULT Petrol,
    power_units           INTEGER DEFAULT 1,
    aux_power_type        VARCHAR(20) DEFAULT Petrol,
    aux_power_units       INTEGER DEFAULT 0,
    tyres                 VARCHAR(20) DEFAULT Knobbly,
    qty_tyres             INTEGER DEFAULT 4,
    armour                VARCHAR(20) DEFAULT None,
    attack                VARCHAR(20) DEFAULT None,
    qty_attacks           INTEGER DEFAULT 0,
    fireproof             BOOLEAN DEFAULT FALSE,
    insulated             BOOLEAN DEFAULT FALSE,
    antibiotic            BOOLEAN DEFAULT FALSE,
    banging               BOOLEAN DEFAULT FALSE,
    algo                  VARCHAR(20) DEFAULT Steady
  )

""")

print("- Table \"buggies\" exists OK")

cur = con.cursor()

cur.execute("SELECT * FROM buggies LIMIT 1")
rows = cur.fetchall()
if len(rows) == 0:
  cur.execute("INSERT INTO buggies (qty_wheels) VALUES (4)")
  con.commit()
  print("- Added one 4-wheeled buggy")
else:
  print("- Found a buggy in the database, nice")
print("- done")

con.close()
