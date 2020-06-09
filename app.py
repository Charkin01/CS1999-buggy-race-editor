from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
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
      
      #Validation of the input data
      if not qty_wheels.isdigit() or not hamster_booster.isdigit() or not power_units.isdigit() or not aux_power_units.isdigit():
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
         
      total_cost += int(hamster_booster)*5
         
      msg = f"qty_wheels={qty_wheels}"
   try:
      #make a for loop from this
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
      return render_template("updated.html", msg = msg)
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
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/new')
def edit_buggy():
  return render_template("buggy-form.html")


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
#   don't want DELETE here, because we're anticipating
#   there always being a record to update (because the
#   student needs to change that!)
#------------------------------------------------------------
@app.route('/delete', methods = ['POST'])
def delete_buggy():
  try:
    msg = "deleting buggy"
    with sql.connect(DATABASE_FILE) as con:
      cur = con.cursor()
      cur.execute("DELETE FROM buggies")
      con.commit()
      msg = "Buggy deleted"
  except:
    con.rollback()
    msg = "error in delete operation"
  finally:
    con.close()
    return render_template("updated.html", msg = msg)


if __name__ == '__main__':
   app.run(debug = True, host="0.0.0.0")
