# Calculator for Pythia

# Math stuff.

pi = 3.1416
def integrateTerm(coefficient, exponent):
    newCoefficient = coefficient / (exponent + 1)
    return(newCoefficient, (exponent + 1))

def getAntiderivative(termsList):
    newTerms = []
    for term in termsList:
        newTerms.append(integrateTerm(term[0], term[1]))
    return newTerms

def evaluatePolynomial(termsList, evaluationPoint):
    finalValue = 0
    for term in termsList:
        finalValue += (term[0] * (evaluationPoint ** term[1]))
    return finalValue

def numericIntegrate(termsList, startingPoint, endingPoint):
    antiderivative = getAntiderivative(termsList)
    return (evaluatePolynomial(antiderivative, endingPoint) - evaluatePolynomial(antiderivative, startingPoint))

# Chemistry and physics stuff.
ambient_temp = 25 # Degrees C when reaction starts. This should be 25 or close to it, because the script compares the energy expenditure from the ambient temperature to the target temp with the enthalpy of decomposition at 25C.
mole_constant = 0.000829249 # number of moles in 1 cm³ of gas at a pressure of 1 psi
kJ_per_kWh = 3600 # kilojoules in a kilowatt-hour

# some basic stats on the chemicals in question. Mostly from the NIST handbook

hydrogenStats = {
    'name': 'hydrogen',
    'molar mass': 2.02
}

CO2Stats = {
    'name': 'carbon dioxide',
    'molar mass': 44.01
}

methaneStats = {
    'name': 'methane',
    'molar mass': 16.04,
    '% carbon': 0.75,
    'specific heat': [(-0.0000009, 2), (0.004, 1), (2.085, 0)],
    'enthalpy of decomp': 55549, # joules per gram
    '$/kg': 0.255, # Assuming $0.50 a therm.

    # Other inputs and outputs per mole of methane in steam reforming. 1CH₄ + 2 H₂O → CO₂ + 2H₂
    'molar steam ratio': 2, 
    'molar CO2 ratio': 1,
    'molar hydrogen ratio': 2
}

propaneStats = {
    'name': 'propane',
    'molar mass': 44.1,
    '% carbon': 0.817,
    'specific heat': [(0.0000000007, 3), (-0.000003, 2), (0.005, 1), (1.5479, 0)], # A polynomial for specific heat in joules per gram
    'enthalpy of decomp': 50113, # joules per gram
    '$/kg' : 2.08, # Propane costs about $3.99 a gallon for a refill at UHaul. 

    # Molar ratios for steam reforming
    'molar steam ratio': 6,
    'molar CO2 ratio': 3,
    'molar hydrogen ratio': 10
}

waterStats = {
    'name': 'water',
    'molar mass': 18.02,
    'specific heat': [(-0.000008, 2), (-0.004, 1), (4.2444, 0)],
    'heat of vaporization': 2256, # joules per gram
    'density': 1 # g/cm³ or tons per m³
}

steamStats = {
    'name': 'steam',
    'molar mass': 18.02,
    'specific heat': [(0.00000008, 2), (0.00006, 1), (1.8225, 0)]
}

sootStats = {
    'name': 'soot',
    'density': 1.5 # an attempted underestimate
}

# Some other functions.

# Various other parameters as tuples. Prompt is used as an input if the boolean is set to True, otherwise the default value given is used. Defaults are set to constantan

ask_diameter = ('Inner diameter of tube, in cm: ', False, 5) # inner diameter of pipes in cm
ask_length = ('Length of tube, in cm: ', False, 100) # length of pipes in cm
ask_strength = ('Tensile strength of tube, in psi: ', False, 10000) # tensile strength of wall material
ask_density = ('Density of tube material, in g/cm³: ', False, 8.89) # density of wall material in g/cm³
ask_cost = ('Cost of tube material, in $/kg: ', False, 13) # cost of wall material per kilo in dollars
ask_num_pipes = ('Total number of pipe reactors: ', False, 441) # ask how many pipes there will be in the reactor

ask_feedstock_mass = ('Grams of hydrocarbon feedstock: ', False, 9000)
ask_pressure = ('Operating pressure: ', False, 15) # operating pressure in psi
ask_temperature = ('Operating temperature: ', False, 900) # operating temperature in celsius

ask_energy_efficiency = ('Energy efficiency: ', False, 0.6) 
ask_electricity_cost = ('Cost per kilowatt-hour: ', False, 0.10)
ask_carbon_intensity = ('Carbon intensity of your electricity source, in grams per kWh: ', False, 388) # American average as of 2021

# parameters for what it ought to calculate and give you
check_pyrolysis = True
check_steam_reforming = True

print_wall_specs = True
print_reaction_specs = True
print_soot_specs = True
print_energy_cost = True

def getFeedstockStats():
    feedstockID = input("Press 'm' for methane or 'p' for propane: ")
    match feedstockID:
        case 'm':
            return methaneStats
        case 'M':
            return methaneStats
        case 'p':
            return propaneStats
        case 'P':
            return propaneStats
        case _:
            getFeedstock()

def getParameter(settings):
    if settings[1] == False:
        return settings[2]
    else:
        dimension = input(settings[0])
        try:
            return int(dimension)
        except:
            return float(dimension)
        else:
            getParameter(prompt)

inner_diameter = getParameter(ask_diameter)
pipe_length = getParameter(ask_length)
pipe_strength = getParameter(ask_strength)
pipe_density = getParameter(ask_density)
pipe_cost = getParameter(ask_cost)
number_pipes = getParameter(ask_num_pipes)
operating_pressure = getParameter(ask_pressure)
operating_temperature = getParameter(ask_temperature)
feedstock_mass = getParameter(ask_feedstock_mass)
energy_efficiency = getParameter(ask_energy_efficiency)
electricity_cost = getParameter(ask_electricity_cost)
electric_carbon_intensity = getParameter(ask_carbon_intensity)

# Various useful unit conversions
inner_radius = inner_diameter / 2

wall_thickness = (operating_pressure * inner_diameter)/(2 * pipe_strength) # Both tensile strength and operating pressure are in psi, so no need to unit-convert inner diameter

outer_diameter = inner_diameter + (2 * wall_thickness)
outer_radius = outer_diameter / 2

outer_cylinder_volume = (pi * (outer_radius ** 2) * pipe_length) # in cm³
inner_cylinder_volume = (pi * (inner_radius ** 2) * pipe_length)

inner_surface_area = pipe_length * pi * inner_diameter # in cm²

wall_volume = outer_cylinder_volume - inner_cylinder_volume
wall_mass = pipe_density * wall_volume * number_pipes * 0.001 # 0.01 converts grams to kilograms
wall_cost = wall_mass * pipe_cost

temp_kelvin = operating_temperature + 273.15

def getHeatExpended(dictionary, startingTemp, endingTemp):
    if 'enthalpy of decomp' in dictionary:
    # Gives heat expended per gram
        return max(numericIntegrate(dictionary['specific heat'], startingTemp, endingTemp), dictionary['enthalpy of decomp'])
    else:
        return numericIntegrate(dictionary['specific heat'], startingTemp, endingTemp)

def pyrolysis(stats):
    totalJoulesExpended = feedstock_mass * getHeatExpended(stats, ambient_temp, operating_temperature)
    
    totalFeedstockMoles = feedstock_mass/stats['molar mass']

    totalHydrogenProduced = (1-stats['% carbon']) * feedstock_mass #in grams
    totalHydrogenKilos = totalHydrogenProduced / 1000

    total_electricity_usage = (totalJoulesExpended) / (3600000 * energy_efficiency) # in kWh
    total_electricity_cost = total_electricity_usage * electricity_cost
    total_electric_emissions = (total_electricity_usage * electric_carbon_intensity)/1000 # CO2 emissions from electricity, in kilos

    kWh_per_kilo = total_electricity_usage / totalHydrogenKilos
    electricity_cost_per_kilo = kWh_per_kilo * electricity_cost
    emissions_per_kilo = total_electric_emissions / totalHydrogenKilos

    feedstock_cost = 0.001 * stats['$/kg'] * feedstock_mass # 0.001 converts feedstock mass in grams to kilos
    feedstock_cost_per_kg_H2 = feedstock_cost / totalHydrogenKilos

    all_opex_cost = feedstock_cost + total_electricity_cost
    opex_cost_per_kilo = electricity_cost_per_kilo + feedstock_cost_per_kg_H2
    electric_cost_proportion = total_electricity_cost / all_opex_cost

    print("Total hydrogen produced from pyrolyzing " + str(feedstock_mass) + " grams of " + stats['name'] + ": " + str(round(totalHydrogenKilos, 3)) + " kg")
    print("Total electricity usage: " + str(round(total_electricity_usage, 3)) + " kWh, costing $" + str(round(total_electricity_cost, 2)))
    print("Per kilo of H₂ produced, " + str(round(kWh_per_kilo, 3)) + " kWh was expended at a cost of $" + str(round(electricity_cost_per_kilo, 2)) + ", resulting in " + str(round(emissions_per_kilo, 2)) + " kg of CO₂ emissions")
    print("Total CO₂ produced: " + str(round(total_electric_emissions, 2)) + " kg")
    print("Total feedstock expenditure: $" + str(round(feedstock_cost, 2)) + "\nFeedstock expenditure per kilo of H₂ produced: $" + str(round(feedstock_cost_per_kg_H2, 2)))
    
    print("Total opex expenditure: $" + str(round(all_opex_cost, 2)))
    print("Total opex cost per kilo: $" + str(round(opex_cost_per_kilo, 2)))
    print("Electricity comprised " + str(round(electric_cost_proportion, 3) * 100) + "% of opex expenditures")
    return

def gramOfSteam(startingTemp, endingTemp): 
    # Mass is in grams. Temps are in Celsius
    joulesPerGram = getHeatExpended(waterStats, startingTemp, 100) + waterStats['heat of vaporization'] + getHeatExpended(steamStats, 100, operating_temperature)
    return joulesPerGram

def steamReforming(stats):
    feedstock_moles = feedstock_mass / stats['molar mass']
    gramsWaterNeeded = feedstock_moles * stats['molar steam ratio'] * waterStats['molar mass']
    
    waterEnergyCost = gramOfSteam(ambient_temp, operating_temperature) * gramsWaterNeeded # gives a ginormous number of joules

    feedstockEnergyCost = feedstock_mass * getHeatExpended(stats, ambient_temp, operating_temperature)

    totalJoulesExpended = waterEnergyCost + feedstockEnergyCost

    totalHydrogenProduced = feedstock_moles * hydrogenStats['molar mass'] * stats['molar hydrogen ratio'] # in grams
    totalCO2Produced = feedstock_moles * CO2Stats['molar mass'] * stats['molar CO2 ratio']
    totalHydrogenKilos = totalHydrogenProduced / 1000
    totalCO2Kilos = totalCO2Produced/1000

    total_electricity_usage = (totalJoulesExpended) / (3600000 * energy_efficiency)
    total_electricity_cost = total_electricity_usage * electricity_cost
    total_electric_emissions = (total_electricity_usage * electric_carbon_intensity)/1000 # CO2 emissions from electricity, in kilos
    totalCO2Kilos = (totalCO2Produced / 1000) + total_electric_emissions

    kWh_per_kilo = total_electricity_usage / totalHydrogenKilos
    electricity_cost_per_kilo = kWh_per_kilo * electricity_cost
    emissions_per_kilo = totalCO2Kilos / (totalHydrogenKilos)

    feedstock_cost = 0.001 * stats['$/kg'] * feedstock_mass # 0.001 converts feedstock mass in grams to kilos
    feedstock_cost_per_kg_H2 = feedstock_cost / totalHydrogenKilos

    all_opex_cost = feedstock_cost + total_electricity_cost
    opex_cost_per_kilo = electricity_cost_per_kilo + feedstock_cost_per_kg_H2
    electric_cost_proportion = total_electricity_cost / all_opex_cost
    electric_CO2_proportion = total_electric_emissions / totalCO2Kilos

    print("Total hydrogen produced from steam reforming " + str(feedstock_mass) + " grams of " + stats['name'] + ": " + str(round(totalHydrogenKilos, 3)) + " kg")
    print("Total electricity usage: " + str(round(total_electricity_usage, 3)) + " kWh, costing $" + str(round(total_electricity_cost, 2)))
    print("Per kilo of H₂ produced, " + str(round(kWh_per_kilo, 3)) + " kWh was expended at a cost of $" + str(round(electricity_cost_per_kilo, 2)))

    print("Total CO₂ emissions: " + str(round(totalCO2Kilos, 2)) + " kg")
    print("Total CO₂ emissions per kilo of hydrogen: " + str(round(emissions_per_kilo, 2)) + " kg")

    print("Total feedstock expenditure: $" + str(round(feedstock_cost, 2)) + "\nFeedstock expenditure per kilo of H₂ produced: $" + str(round(feedstock_cost_per_kg_H2, 2)))
    
    print("Total opex expenditure: $" + str(round(all_opex_cost, 2)))
    print("Total opex cost per kilo: $" + str(round(opex_cost_per_kilo, 2)))
    print("Electricity comprised " + str(round(electric_cost_proportion, 3) * 100) + "% of opex expenditures")
    print("Electricity produced " + str(round(electric_CO2_proportion, 3) * 100) + "% of all CO₂ emissions")
    return





# pyrolysis(getFeedstockStats())

print("\n")
print("At an electricity cost of $" + str(electricity_cost) + " and an energy efficiency of " + str(100 * energy_efficiency) + "%:\n")
pyrolysis(methaneStats)
print("\n")
pyrolysis(propaneStats)
print("\n")
steamReforming(methaneStats)
print("\n")
steamReforming(propaneStats)
print("\n")