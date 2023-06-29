from app import db
"""
A model is created for each variable measured, the grams of meat and its equivalent in CO2, water and animal lives.
Each row in the model will represent one form submission consisting of a date, the quantity of the variable per animal and total.
The values for CO2, water and animals were calculated by multiplying the input with a constant and therefore stored as floats and only converted to integers once the final output value is derived.
"""
class Input(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date())
    inputpoultry = db.Column(db.Integer())
    inputpork = db.Column(db.Integer())
    inputbeef = db.Column(db.Integer())
    inputtotal = db.Column(db.Integer())

    def __repr__(self):
        return '<Date {}>'.format(self.date)

class Co2(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date())
    co2poultry = db.Column(db.Float())
    co2pork = db.Column(db.Float())
    co2beef = db.Column(db.Float())
    co2total = db.Column(db.Float())

    def __repr__(self):
        return '<Date {}>'.format(self.date)

class Water(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date())
    waterpoultry = db.Column(db.Float())
    waterpork = db.Column(db.Float())
    waterbeef = db.Column(db.Float())
    watertotal = db.Column(db.Float())

    def __repr__(self):
        return '<Date {}>'.format(self.date)

class Nr(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date())
    nrpoultry = db.Column(db.Float())
    nrpork = db.Column(db.Float())
    nrbeef = db.Column(db.Float())
    nrtotal = db.Column(db.Float())

    def __repr__(self):
        return '<Date {}>'.format(self.date)
