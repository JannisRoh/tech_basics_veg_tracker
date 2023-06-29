from app import app, db
# Import of the created flask_wtf forms
from app.form import InputForm, DeleteForm
# Import of the created models for the database using Flask-SQLAlchemy
from app.models import Input, Co2, Water, Nr
#Import of the reference values used for calculations
from app.formulas import Constants
# Import of the Classes used for data manipulation and chart creation
from app.tables import Tabledf, Savedstats
from app.charts import Chart, Piechart, Barchart

# Import of the flask functons used
from flask import render_template, redirect, url_for
# Import of libraries for data visualisation
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns


def format_stat(stat, nr):
    """
    This function is used to ensure negative values are not displayed, as they would not make sense with the text used.
    It is also used to control the number of decimal places displayed.
    """
    if stat < 0:
        stat = 0
    stat = format(stat, f".{nr}f")
    return stat

@app.route("/index",methods=['GET','POST'])
@app.route("/",methods=['GET','POST'])
def index():
    db.create_all()

    """
    This for loop is used to create table objects for each entry in the variableList and runs the create_table() method for each object.
    In this function data is retrieved from the database and converted to a pandas dataframe, and formatted to allow further calculations.
    The loop makes it easy to adjust the code if new variables are added, since they must simply be added to the variableList.
    """
    table_df = None
    tablesDict = {}
    variableList = ["input", "co2", "water", "nr"]
    for variable in variableList:
        tablesDict[variable+"Table"] = Tabledf(table_df, f"{variable}poultry", f"{variable}pork", f"{variable}beef", f"{variable}total", f"{variable}")
        tablesDict[variable+"Table"].create_table()

    # The table attributes of the objects in the dictionary are stored in variables.
    input_df = tablesDict["inputTable"].table_df
    co2_df = tablesDict["co2Table"].table_df
    water_df = tablesDict["waterTable"].table_df
    nr_df = tablesDict["nrTable"].table_df

    # The number of days no meat is eaten is calculated
    noMeatDays = (input_df['Total'] == 0).sum()

    # An object for the kg data is created. Then the object runs a method to return the amount of meat in kg the user has eaten less than the german average.
    kgStats = Savedstats(input_df, Constants.avgKgTotalDay, 0, 0)
    savedKg = kgStats.calculate_stats()
    savedKg = format_stat(savedKg, 2)

    # An object of the same class is created for co2.
    # Here not only the amount of co2 in kg is output but also what that would be equivalent to in km traveled via car and plane.
    inCarKm = Constants.co2KmCar
    inPlaneKm = Constants.co2KmFlight
    co2Stats = Savedstats(co2_df, Constants.avgCo2TotalDay, inCarKm, inPlaneKm)
    savedCo2, inCarKm, inPlaneKm = co2Stats.calculate_stats()
    savedCo2 = format_stat(savedCo2, 2)
    inCarKm = format_stat(inCarKm, 0)
    inPlaneKm = format_stat(inPlaneKm, 0)

    # The same is done for water.
    inShowers = Constants.showerLiters
    inBathtubs = Constants.bathtubLiters
    waterStats = Savedstats(water_df, Constants.avgWaterTotalDay, inShowers, inBathtubs)
    savedWater, inShowers, inBathtubs = waterStats.calculate_stats()
    savedWater = format_stat(savedWater, 2)
    inBathtubs = format_stat(inBathtubs, 0)
    inShowers = format_stat(inShowers, 0)

    """
    For the number of animals we are not simply calculating the number of animals the user has saved, because that number would be small and not impactful.
    Instead we take the users current daily average of animals eaten and calculate how this would compare to the national average over the course of 10 years.
    Therefore we cannot use the same class as before, instead we calculate it here.
    If we were to use this 10 year method more frequently in the future, we would turn this into a function.
    """
    nrBeefAverage = nr_df['Beef'].mean()
    nrBeefAverage10Year = nrBeefAverage * 3650
    nrPorkAverage = nr_df['Pork'].mean()
    nrPorkAverage10Year = nrPorkAverage * 3650
    nrPoultryAverage = nr_df['Poultry'].mean()
    nrPoultryAverage10Year = nrPoultryAverage * 3650
    savedNrBeef10Year = Constants.avgNrBeef10Year - nrBeefAverage10Year
    savedNrPork10Year = Constants.avgNrPork10Year - nrPorkAverage10Year
    savedNrPoultry10Year = Constants.avgNrPoultry10Year - nrPoultryAverage10Year

    savedNrBeef10Year = format_stat(savedNrBeef10Year, 2)
    savedNrPork10Year = format_stat(savedNrPork10Year, 2)
    savedNrPoultry10Year = format_stat(savedNrPoultry10Year, 2)

    # All the formatted values are provided to the template, to display them on the page.
    return render_template('index.html', noMeatDays=noMeatDays, savedKg=savedKg, savedCo2=savedCo2, inCarKm=inCarKm, \
                            inPlaneKm=inPlaneKm, savedWater=savedWater, inShowers=inShowers, inBathtubs = inBathtubs, \
                            savedNrBeef10Year=savedNrBeef10Year, savedNrPork10Year=savedNrPork10Year, savedNrPoultry10Year=savedNrPoultry10Year)

@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
    """
    The start of this function is the same as for the index page, because the data must again be retrieved from the database and formatted.
    Calculating the saved value is also the same as in the index, except the reference values that the calculate_stats method can also output are not calculated.
    If the app were to be expanded it is likely that this code would have to be utilised in yet another route, in which case it would be beneficial to place it into a function.
    """
    table_df = None
    tablesDict = {}
    variableList = ["input", "co2", "water", "nr"]
    for variable in variableList:
        tablesDict[variable+"Table"] = Tabledf(table_df, f"{variable}poultry", f"{variable}pork", f"{variable}beef", f"{variable}total", f"{variable}")
        tablesDict[variable+"Table"].create_table()

    input_df = tablesDict["inputTable"].table_df
    co2_df = tablesDict["co2Table"].table_df
    water_df = tablesDict["waterTable"].table_df
    nr_df = tablesDict["nrTable"].table_df


    kgStats = Savedstats(input_df, Constants.avgKgTotalDay, 0, 0)
    savedKg = kgStats.calculate_stats()
    savedKg = format_stat(savedKg, 2)

    co2Stats = Savedstats(co2_df, Constants.avgCo2TotalDay, 0, 0)
    savedCo2 = co2Stats.calculate_stats()
    savedCo2 = format_stat(savedCo2, 2)

    waterStats = Savedstats(water_df, Constants.avgWaterTotalDay, 0, 0)
    savedWater = waterStats.calculate_stats()
    savedWater = format_stat(savedWater, 2)

    #This time we do create a class object for the number of animals
    animalStats = Savedstats(nr_df, Constants.avgNrTotalDay, 0, 0)
    savedAnimals = animalStats.calculate_stats()
    savedAnimals = format_stat(savedAnimals, 2)

    # The number of days the user has and has not eaten meat are calculated and stored in an array to use as data in the pie chart.
    noMeatDays = (input_df['Total'] == 0).sum()
    meatDays = (input_df['Total'] != 0).sum()
    meatDayData = [noMeatDays, meatDays]

    # Creation of variables to be used as arguments for a pie chart object.
    labels = ["Days as a vegetarian:", "Days you ate meat:"]
    pieChart = None
    fig = Figure()

    # Setting the theme to be used by charts using the Seaborn library.
    colors = ["#81c14b", "#7a28cb"]
    sns.set_theme(style = "whitegrid", palette = sns.color_palette(colors))

    # Creating a pie chart of the days meat is and is not eaten, then saving it to an image.
    meatDayChart = Piechart(meatDayData, labels, pieChart, fig)
    meatDayChart.make_pie_chart()
    pieChart = meatDayChart.save_chart()


    # The variables to be used as the arguments for the first bar chart is created.
    # The table is shortened to the last 30 days of entries and the mean derived, as this bar chart will show the users average consumption over the last 30 days.
    kgAvg30Days = input_df.iloc[-30:].mean()
    fig = plt.figure()
    kgConstants = [(Constants.avgKgPoultryDay*1000), (Constants.avgKgPorkDay*1000), (Constants.avgKgBeefDay*1000), (Constants.avgKgTotalDay*1000)]
    kgBarChart = None
    legendLabels = ['You', 'National Average']

    # A object is created that runs methods to create and then to save a bar chart.
    kgBarChart = Barchart(kgAvg30Days, legendLabels, kgBarChart, fig, kgConstants, 'Amount of meat in grams')
    kgBarChart.make_bar_chart()
    kgBarChart = kgBarChart.save_chart()

    # The same is done for water and co2, it would be more efficient to turn this into a for loop to have less repetition and make it easier if new varaibles are added.
    waterAvg30Days = water_df.iloc[-30:, water_df.columns != 'date'].div(1000).mean()
    fig = plt.figure()
    waterConstants = [(Constants.avgWaterPoultryDay), (Constants.avgWaterPorkDay), (Constants.avgWaterBeefDay), (Constants.avgWaterTotalDay)]
    waterBarChart = None

    waterBarChart = Barchart(waterAvg30Days, legendLabels, waterBarChart, fig, waterConstants, 'Amount of water in liters')
    waterBarChart.make_bar_chart()
    waterBarChart = waterBarChart.save_chart()


    co2Avg30Days = co2_df.iloc[-30:].mean()
    fig = plt.figure()
    co2Constants = [(Constants.avgCo2PoultryDay*1000), (Constants.avgCo2PorkDay*1000), (Constants.avgCo2BeefDay*1000), (Constants.avgCo2TotalDay*1000)]
    co2BarChart = None

    co2BarChart = Barchart(co2Avg30Days, legendLabels, co2BarChart, fig, co2Constants, 'Amount of co2 in grams')
    co2BarChart.make_bar_chart()
    co2BarChart = co2BarChart.save_chart()

    # The saved stats and the images of the charts are given to the template.
    return render_template('dashboard.html', pieChart=pieChart, savedKg=savedKg, savedCo2=savedCo2, savedWater=savedWater, savedAnimals=savedAnimals, \
                            kgBarChart=kgBarChart, co2BarChart=co2BarChart, waterBarChart=waterBarChart)


@app.route("/form",methods=['GET','POST'])
def form():
    # Initlaizing the flask-wtf form used to input daily meat consumption.
    form = InputForm()

    """
    When the form is submitted it is stored to a table in the databse per variable tracked.
    For everything but grams a conversion is done immediately by multiplying the input by a constant.
    The result is that each table directly has the correct value for the data its storing and these calculations do not have to occur each time data is requested.
    The idea is to reduce the loading times whenever a page is reloaded at the cost of increased loading times when data is stored and an overall larger database.
    """
    if form.validate_on_submit():
        inpForm = Input(date=form.date.data,inputpork=form.pork.data,inputbeef=form.beef.data, \
                    inputpoultry=form.poultry.data,inputtotal=form.pork.data+form.beef.data+form.poultry.data)
        db.session.add(inpForm)

        co2Form = Co2(date=form.date.data,co2pork=form.pork.data*Constants.co2PorkConst,\
                     co2beef=form.beef.data*Constants.co2BeefConst,co2poultry=form.poultry.data*Constants.co2PoultryConst,\
                     co2total=(form.pork.data*Constants.co2PorkConst) + (form.beef.data*Constants.co2BeefConst) + (form.poultry.data*Constants.co2PoultryConst))
        db.session.add(co2Form)

        waterForm = Water(date=form.date.data,waterpork=form.pork.data*Constants.waterPorkConst,\
                            waterbeef=form.beef.data*Constants.waterBeefConst,waterpoultry=form.poultry.data*Constants.waterPoultryConst,\
                            watertotal=(form.pork.data*Constants.waterPorkConst) + (form.beef.data*Constants.waterBeefConst) + (form.poultry.data*Constants.waterPoultryConst))
        db.session.add(waterForm)

        nrForm = Nr(date=form.date.data,nrpork=form.pork.data*Constants.nrPorkConst,\
                                    nrbeef=form.beef.data*Constants.nrBeefConst,nrpoultry=form.poultry.data*Constants.nrPoultryConst,\
                                    nrtotal=(form.pork.data*Constants.nrPorkConst) + (form.beef.data*Constants.nrBeefConst) + (form.poultry.data*Constants.nrPoultryConst))
        db.session.add(nrForm)
        db.session.commit()

        # The user is redirected to the dashboard after adding an entry.
        return redirect(url_for('dashboard'))
    return render_template('form.html',form=form)


@app.route("/delete",methods=['GET','POST'])
def deleteForm():
    # The input table is created once again and is converted to an html table to show the user what the input is for certain dates, to help them delete the correct entry.
    input_df = None
    input_df = Tabledf(input_df, "inputpoultry", "inputpork", "inputbeef", "inputtotal", "input")
    input_df = input_df.create_table().to_html(index=False, classes='data', header="true")

    #A delete form used to delete entries from the database.
    #The user can select a date and if the date exists in the input table, all entries for that date are deleted in all tables.
    form = DeleteForm()
    checker = Input.query.filter_by(date=form.date.data).first()
    if form.validate_on_submit():
        if checker != None:
            Input.query.filter_by(date=form.date.data).delete()
            Co2.query.filter_by(date=form.date.data).delete()
            Water.query.filter_by(date=form.date.data).delete()
            Nr.query.filter_by(date=form.date.data).delete()
            db.session.commit()
            return redirect(url_for('index'))
        else:
            print("Error")

    # The form and the table are given to the template.
    return render_template('delete.html', form=form,  table=input_df)
