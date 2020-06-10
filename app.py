from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
import random as rd
app = Flask(__name__)

DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"

BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"


#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
   return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
   if request.method == 'GET':
      #gets current number of wheels
      con = sql.connect(DATABASE_FILE)
      con.row_factory = sql.Row
      cur = con.cursor()
      cur.execute("SELECT * FROM buggies")
      record = cur.fetchone();
      return render_template("buggy-form.html", buggy = record)
   elif request.method == 'POST':
      msg=""
      
      #all input
      power_type = request.form['power_type']
      qty_wheels = request.form['qty_wheels']
      flag_color = request.form['flag_color']
      flag_color_secondary = request.form['flag_color_secondary']
      flag_pattern = request.form['flag_pattern']
      hamster_booster = request.form['hamster_booster']
      power_units = request.form['power_units']
      aux_power_type = request.form['aux_power_type']
      aux_power_units = request.form['aux_power_units']
      tyres = request.form['tyres']
      qty_tyres = request.form['qty_tyres']
      
      #Validation of the input data
      if not qty_wheels.isdigit() or not hamster_booster.isdigit() or not power_units.isdigit() or not aux_power_units.isdigit() or not qty_tyres.isdigit():
         msg = "You have entered characters (string) instead of digits (integers). The buggy was not created. Please, return to the main menu"
         return render_template("updated.html", msg = msg)
      if int(qty_wheels) < 4:
         msg = "Buggy cannot have less then 4 wheels. The buggy was not created. Please, return to the main menu"
         return render_template("updated.html", msg = msg)
      if int(power_units) < 1 or int(aux_power_units) < 1:
         msg = "Buggy should have some power units. The buggy was not created. Please, return to the main menu"
         return render_template("updated.html", msg = msg)
      if int(qty_wheels)%2 != 0:
         msg = "Buggy cannot have odd number of wheels (sad). The buggy was not created. Please, return to the main menu"
         return render_template("updated.html", msg = msg)
      if int(qty_tyres) < int(qty_wheels):
         msg = "It does not work like that. The buggy was not created. Please, return to the main menu"
         return render_template("updated.html", msg = msg)
      
      #total_cost identification/formula
      total_cost = 0
      if power_type.find("Petrol") != (-1):
         total_cost += 4 * int(power_units)
      elif power_type.find("Fusion") != (-1):
         total_cost += 400*int(power_units)
      elif power_type.find("Steam") != (-1):
         total_cost += 3*int(power_units)
      elif power_type.find("Bio") != (-1):
         total_cost += 5*int(power_units)
      elif power_type.find("Electric") != (-1):
         total_cost += 20*int(power_units)
      elif power_type.find("Rocket") != (-1):
         total_cost += 16*int(power_units)
      elif power_type.find("Hamster") != (-1):
         total_cost += 3*int(power_units)
      elif power_type.find("Thermo") != (-1):
         total_cost += 300*int(power_units)
      elif power_type.find("Solar") != (-1):
         total_cost += 40*int(power_units)
      elif power_type.find("Wind") != (-1):
         total_cost += 20*int(power_units)
         
      if aux_power_type.find("Petrol") != (-1):
         total_cost += 4 * int(power_units)
      elif aux_power_type.find("Fusion") != (-1):
         total_cost += 400*int(power_units)
      elif aux_power_type.find("Steam") != (-1):
         total_cost += 3*int(power_units)
      elif aux_power_type.find("Bio") != (-1):
         total_cost += 5*int(power_units)
      elif aux_power_type.find("Electric") != (-1):
         total_cost += 20*int(power_units)
      elif aux_power_type.find("Rocket") != (-1):
         total_cost += 16*int(power_units)
      elif aux_power_type.find("Hamster") != (-1):
         total_cost += 3*int(power_units)
      elif aux_power_type.find("Thermo") != (-1):
         total_cost += 300*int(power_units)
      elif aux_power_type.find("Solar") != (-1):
         total_cost += 40*int(power_units)
      elif aux_power_type.find("Wind") != (-1):
         total_cost += 20*int(power_units)

      if tyres.find("Knobbly") != (-1):
         total_cost += 15*int(qty_tyres)
      elif tyres.find("Slick") != (-1):
         total_cost += 20*int(qty_tyres)
      elif tyres.find("Steelband") != (-1):
         total_cost += 30*int(qty_tyres)
      elif tyres.find("Reactive") != (-1):
         total_cost += 40*int(qty_tyres)
      elif tyres.find("Maglev") != (-1):
         total_cost += 50*int(qty_tyres)

      total_cost += int(hamster_booster)*5
   try:
      #uploads data to database
      with sql.connect(DATABASE_FILE) as con:
         cur = con.cursor()
         cur.execute("UPDATE buggies set qty_wheels=? WHERE id=?", (qty_wheels, DEFAULT_BUGGY_ID))
         cur.execute("UPDATE buggies set flag_color=? WHERE id=?", (flag_color, DEFAULT_BUGGY_ID))
         cur.execute("UPDATE buggies set flag_color_secondary=? WHERE id=?", (flag_color_secondary, DEFAULT_BUGGY_ID))
         cur.execute("UPDATE buggies set flag_pattern=? WHERE id=?", (flag_pattern, DEFAULT_BUGGY_ID))
         cur.execute("UPDATE buggies set hamster_booster=? WHERE id=?", (hamster_booster, DEFAULT_BUGGY_ID))
         cur.execute("UPDATE buggies set total_cost=? WHERE id=?", (total_cost, DEFAULT_BUGGY_ID))
         cur.execute("UPDATE buggies set power_type=? WHERE id=?", (power_type, DEFAULT_BUGGY_ID))
         cur.execute("UPDATE buggies set power_units=? WHERE id=?", (power_units, DEFAULT_BUGGY_ID))
         cur.execute("UPDATE buggies set aux_power_type=? WHERE id=?", (aux_power_type, DEFAULT_BUGGY_ID))
         cur.execute("UPDATE buggies set aux_power_units=? WHERE id=?", (aux_power_units, DEFAULT_BUGGY_ID))
         cur.execute("UPDATE buggies set tyres=? WHERE id=?", (tyres, DEFAULT_BUGGY_ID))
         cur.execute("UPDATE buggies set qty_tyres=? WHERE id=?", (qty_tyres, DEFAULT_BUGGY_ID))
         con.commit()
         msg = "Buggy was created. Record successfully saved"
   except:
      con.rollback()
      msg = "error in update operation"
   finally:
      con.close()
      return render_template("updated.html", msg = msg)

#------------------------------------------------------------
# This page randoms all values and returns to buggy.html to
# show the result. Theoretically.
#------------------------------------------------------------
@app.route('/new_random', methods = ['POST', 'GET'])
def create_buggy_random():
    #return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)
    msg=""
    #function that randoms value
    def randm (listik):
       return rd.choice(listik)
    #function that determines cost
    def find_cost(power_type, hamster_booster, power_units, aux_power_type, aux_power_units):
       total_cost = 0
       if power_type.find("Petrol") != (-1):
          total_cost += 4 * int(power_units)
       elif power_type.find("Fusion") != (-1):
          total_cost += 400*int(power_units)
       elif power_type.find("Steam") != (-1):
          total_cost += 3*int(power_units)
       elif power_type.find("Bio") != (-1):
          total_cost += 5*int(power_units)
       elif power_type.find("Electric") != (-1):
          total_cost += 20*int(power_units)
       elif power_type.find("Rocket") != (-1):
          total_cost += 16*int(power_units)
       elif power_type.find("Hamster") != (-1):
          total_cost += 3*int(power_units)
       elif power_type.find("Thermo") != (-1):
          total_cost += 300*int(power_units)
       elif power_type.find("Solar") != (-1):
          total_cost += 40*int(power_units)
       elif power_type.find("Wind") != (-1):
          total_cost += 20*int(power_units)
            
       if aux_power_type.find("Petrol") != (-1):
          total_cost += 4 * int(power_units)
       elif aux_power_type.find("Fusion") != (-1):
          total_cost += 400*int(power_units)
       elif aux_power_type.find("Steam") != (-1):
          total_cost += 3*int(power_units)
       elif aux_power_type.find("Bio") != (-1):
          total_cost += 5*int(power_units)
       elif aux_power_type.find("Electric") != (-1):
          total_cost += 20*int(power_units)
       elif aux_power_type.find("Rocket") != (-1):
          total_cost += 16*int(power_units)
       elif aux_power_type.find("Hamster") != (-1):
          total_cost += 3*int(power_units)
       elif aux_power_type.find("Thermo") != (-1):
          total_cost += 300*int(power_units)
       elif aux_power_type.find("Solar") != (-1):
          total_cost += 40*int(power_units)
       elif aux_power_type.find("Wind") != (-1):
          total_cost += 20*int(power_units)
         
       total_cost += int(hamster_booster)*5
       return total_cost

    #all available random stuff
    list_int = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    list_wheels = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 22, 24, 26, 28, 30]
    list_colours = ['Tomato, DodgerBlue, White, Black, Green, Purple']
    list_pattern = ['Plain', 'Vstripe', 'Hstripe', 'Dstripe', 'Checker', 'Spot']
    list_power = ['Petrol', 'Fusion', 'Hstripe', 'Electric', 'Rocket', 'Hamster', 'Thermo',  'Wind', 'Solar']

    #all input
    qty_wheels = randm(list_wheels)
    flag_color = randm(list_colours)
    flag_color_secondary = randm(list_colours)
    flag_pattern = randm(list_pattern)
    hamster_booster = randm(list_int)

    rules = False
    total_cost=50
    #it will take very long to find exact same value of total_cost.
    #total cost here does not inherit data from saved database, so now it is constant - 50
    #It loops through attributes that affect cost and determines whether new compilation is correct
    while rules != True:
        power_type = randm(list_power)
        hamster_booster = randm(list_int)
        power_units = randm(list_int)
        aux_power_type = randm(list_power)
        aux_power_units = randm(list_int)
        if total_cost > find_cost(power_type, hamster_booster, power_units, aux_power_type, aux_power_units):
            rules = True
    print (power_type)
    try:
       #uploads data to database
       with sql.connect(DATABASE_FILE) as con:
          cur = con.cursor()
          cur.execute("UPDATE buggies set qty_wheels=? WHERE id=?", (qty_wheels, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set flag_color=? WHERE id=?", (flag_color, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set flag_color_secondary=? WHERE id=?", (flag_color_secondary, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set flag_pattern=? WHERE id=?", (flag_pattern, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set hamster_booster=? WHERE id=?", (hamster_booster, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set total_cost=? WHERE id=?", (total_cost, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set power_type=? WHERE id=?", (power_type, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set power_units=? WHERE id=?", (power_units, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set aux_power_type=? WHERE id=?", (aux_power_type, DEFAULT_BUGGY_ID))
          cur.execute("UPDATE buggies set aux_power_units=? WHERE id=?", (aux_power_units, DEFAULT_BUGGY_ID))
          con.commit()
          msg = "Buggy was created. Record successfully saved"
    except:
       con.rollback()
       msg = "error in update operation"
    finally:
       con.close()
       return render_template("buggy.html", buggy = 1)
   
#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies")
  record = cur.fetchone(); 
  return render_template("buggy.html", buggy = record)

#------------------------------------------------------------
# a page for edit the buggy
#
# It should edit, but currently it just opens creating window
# and does not change anything
#------------------------------------------------------------
@app.route('/edit/<buggy_id>')
def edit_buggy(buggy_id):
   con = sql.connect(DATABASE_FILE)
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("SELECT * FROM buggies WHERE id=?", (buggy_id,))
   record = cur.fetchone(); 
   return render_template("buggy-form.html", buggy = record) 


#------------------------------------------------------------
# get JSON from current record
#   this is still probably right, but we won't be
#   using it because we'll be dipping diectly into the
#   database
#------------------------------------------------------------
@app.route('/json')
def summary():
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))
  return jsonify(
      {k: v for k, v in dict(zip(
        [column[0] for column in cur.description], cur.fetchone())).items()
        if (v != "" and v is not None)
      }
    )

#------------------------------------------------------------
# delete the buggy
#   In vanilla version of the project, it was working good. 
#   But here it behaves differently, so to restore data, you
#   should start init.py
#------------------------------------------------------------
@app.route('/delete/<buggy_id>')
def delete_buggy(buggy_id):
   try:
      msg = "deleting buggy"
      with sql.connect(DATABASE_FILE) as con:
         cur = con.cursor()
         cur.execute("DELETE FROM buggies WHERE id=?", (buggy_id,))
         con.commit()
         msg = "Buggy deleted"
   except:
      con.rollback()
      msg = "error in delete operation"
   finally:
      con.close()
      return render_template("updated.html", msg = msg)

@app.route('/poster')
def poster():
   return render_template('poster.html')


if __name__ == '__main__':
   app.run(debug = True, host="0.0.0.0")

