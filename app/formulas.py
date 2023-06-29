class Constants():
    """
    Here all the reference values, found in our research and values derived thereof, are stored.
    These consist of the values used to convert kg of meat to the other variables and the meat consumption habits of the average german.
    The setup of this module makes it easy to update the values if newer numbers are released, for example for national meat consumption.
    """
    # Average kilograms of co2 produced per kilogram of meat eaten
    co2BeefConst = 13.6
    co2PorkConst = 4.6
    co2PoultryConst = 5.5

    # Average milliters of Water used per kilogram of meat eaten
    waterBeefConst = 15415
    waterPorkConst = 5988
    waterPoultryConst = 4325

    # Average carcass weight of animal in kilograms
    weightBeef = 330.64
    weightPork = 97.7
    weightPoultry = 1.55

    # Average percentage of carcass weight eaten
    usageCoefficentBeef = 77
    usageCoefficentPork = 52.75
    usageCoefficentPoultry = 73

    # Average amount of animal eaten per gram
    nrBeefConst = 1/((weightBeef*1000)*(usageCoefficentBeef/100))
    nrPorkConst = 1/((weightPork*1000)*(usageCoefficentPork/100))
    nrPoultryConst = 1/((weightPoultry*1000)*(usageCoefficentPoultry/100))

    # Consumption values of the average German per year
    avgKgBeefYear = 9.36903501575889
    avgKgPorkYear = 30.9539930445691
    avgKgPoultryYear = 13.0507416954687
    avgKgTotalYear = avgKgPoultryYear + avgKgPorkYear + avgKgBeefYear

    # Consumption values of the average German per day
    avgKgBeefDay = avgKgBeefYear/365
    avgKgPorkDay = avgKgPorkYear/365
    avgKgPoultryDay = avgKgPoultryYear/365
    avgKgTotalDay = avgKgBeefDay + avgKgPorkDay + avgKgPoultryDay

    # Average amount of CO2 produced by the average German per day
    avgCo2BeefDay = avgKgBeefDay*co2BeefConst
    avgCo2PorkDay = avgKgPorkDay*co2PorkConst
    avgCo2PoultryDay = avgKgPoultryDay*co2PoultryConst
    avgCo2TotalDay = avgCo2BeefDay + avgCo2PorkDay + avgCo2PoultryDay

    # Average amount of water produced by the average German per day
    avgWaterBeefDay = avgKgBeefDay*waterBeefConst
    avgWaterPorkDay = avgKgPorkDay*waterPorkConst
    avgWaterPoultryDay = avgKgPoultryDay*waterPoultryConst
    avgWaterTotalDay = avgWaterBeefDay + avgWaterPorkDay + avgWaterPoultryDay

    # Average amount of animals produced by the average German per 10 years
    avgNrBeef10Year = avgKgBeefYear * 10000 * nrBeefConst
    avgNrPork10Year = avgKgPorkYear * 10000 * nrPorkConst
    avgNrPoultry10Year = avgKgPoultryYear * 10000 *nrPoultryConst

    # Average amount of animals produced by the average German per day
    avgNrTotalDay = (avgKgBeefDay * 1000 * nrBeefConst) + (avgKgPorkDay * 1000 * nrPorkConst) + (avgKgPoultryDay * 1000 * nrPoultryConst)

    #Quantity Reference points
    showerLiters = 150 #Liters of water in average showers
    bathtubLiters = 175 #Liters of water in average bathtub

    co2KmCar = 0.15 #Average Co2 in kg per km of travel with the car
    co2KmFlight = 0.380 #Average Co2 in kg per km of travel with plane per person
