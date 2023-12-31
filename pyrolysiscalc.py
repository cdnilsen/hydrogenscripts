# Calculator for pressure, wall thickness, etc.

# random math stuff
pi = 3.1416
def integrateTerm(coefficient, exponent, start, end):
    newCoefficient = coefficient / (exponent + 1)
    return(newCoefficient * ((end ** (exponent + 1)) - (start ** (exponent + 1))))

def integratePolynomial(termsList, startingX, endingX):
    finalValue = 0
    for term in termsList:
        finalValue += integrateTerm(term[0], term[1], startingX, endingX)
    return finalValue




feedstock_name = "propane"
feedstock_molar_mass = 44.1 # for propane
ambient_temp = 25 # Degrees C when reaction starts. This should be 25 or close to it, because the script compares the energy expenditure from the ambient temperature to the target temp with the enthalpy of decomposition at 25C.
mole_constant = 0.000829249 # number of moles in 1 cm³ of gas at a pressure of 1 psi
kJ_per_kWh = 0.000277778 # kilojoules to kilowatt-hours
cost_per_kWh = 0.15 # in dollars


# Feedstock specific heat equation. For propane, a cubic polynomial fits almost perfectly so we'll use it. Equation from Excel, with data from here: https://webbook.nist.gov/cgi/cbook.cgi?ID=C74986&Mask=1. Represented as a list of tuples: first term is the coefficient, second the exponent

specific_heat_polynomial = [(0.0000001, 3), (-0.0005, 2), (0.9209, 1), (280, 0)]

# Feedstock-specific enthalpy of decomposition. For propane, data from here:  https://webbook.nist.gov/cgi/cbook.cgi?ID=C74986&Mask=1, averaged to -2210 kJ/mol, with sign switched (formation -> decomposition), then converted to kilojoules per gram.

enthalpy_of_decomp = 50113 # Joules per *gram* at 298K.

energy_efficiency = 0.25 # How efficient is your energy usage?

gaseous_mole_ratio = 4 # This is the ratio of output mole gases to input mole gases. For complete pyrolysis of propane (C₃H₈ → 3C + 4H₂), it has a value of 4.


# Some input parameters that should make it easy to tweak this
input_diameter = True
input_length = False
input_strength = False
input_pressure = True
input_temperature = False
input_density = False


print_wall_specs = True
print_reaction_specs = True
print_soot_specs = True
print_energy_cost = True



def getDimension(prompt):
    dimension = input(prompt)
    if dimension.isdigit() == True:
        return int(dimension)
    else: getDimension(prompt) # Returns a dummy value.
        
if (input_diameter == True):
    inner_diameter = getDimension("Enter the inner diameter of the chamber in centimeters: ")
else: inner_diameter = 100

if input_length == True:
    vessel_length = getDimension("Enter the length of the vessel, in cm: ")
else: vessel_length = 100

if input_strength == True:
    tensile_strength = getDimension("Enter the tensile strength of the material, in psi: ")
else: tensile_strength = 1000 

# For reasons explained below, the operating pressure of the feedstock and that of the hydrogen won't be the same. Assume 
if input_pressure == True:
    operating_pressure = getDimension("Enter the operating pressure, in psi: ")
else: operating_pressure = 100

if input_temperature == True:
    operating_temp = getDimension("Enter the operating temperature, in Celsius: ")
else: operating_temp = 900

if input_density == True:
    density = getDimension("Enter the density of the wall material, in g/cm³: ")
else: density = 3

# We only take the imperial version of this so it'll comport with pressure in psi
inner_diameter_inches = inner_diameter / 2.54

wall_thickness = (operating_pressure * inner_diameter_inches * 2.54)/(2 * tensile_strength) # the 2.54 constant gives cm

# from here on out we're back in metric: centimeters below
outer_diameter = inner_diameter + wall_thickness
outer_radius = outer_diameter / 2
inner_radius = inner_diameter / 2

outer_cylinder = (pi * (outer_radius ** 2) * vessel_length) # volume in cm³
inner_cylinder = (pi * (inner_radius ** 2) * vessel_length) # volume in cm³

wall_volume = outer_cylinder - inner_cylinder # cm³
wall_mass = wall_volume * density # grams


# Easy calculator for these values, in case you wanted to use butane or something: https://www.lenntech.com/calculators/molecular/molecular-weight-calculator.htm
molar_mass = 44.1 # grams per mole. this value is for propane.
percent_carbon = 0.817 # Propane is about 81.7% carbon *by mass*.

soot_density =  1.5 # grams per cm³. The value seems to vary from about 1.6-2.3ish per Google so I've made a slightly pessimistic assumption about how much volume it'll take up (yes, pessimistic, because more soot means problems)
temp_kelvin = operating_temp + 273.15


inner_surface_area = 2 * pi * vessel_length * inner_diameter

# Gives the number of feedstock moles per run. Gaseous mole ratio is necessary in the denominator here because pressure is a function of moles, so if you're pyrolyzing propane to hydrogen (ratio = 4) and pressure is 5psi at t = 0 (all propane), it'll be 20psi if it's all converted. Operating pressure should assume all hydrogen.

number_of_intake_moles = (inner_cylinder * mole_constant * operating_pressure) / (temp_kelvin * gaseous_mole_ratio)

feedstock_mass = number_of_intake_moles * feedstock_molar_mass # in grams

soot_mass = feedstock_mass * percent_carbon # in grams
total_soot_volume = soot_mass * soot_density # in cm³

hydrogen_mass = feedstock_mass - soot_mass # in grams

soot_thickness = (total_soot_volume / inner_surface_area) * 10 # the "10" here should convert soot density to millimeters

energy_per_gram = max(integratePolynomial(specific_heat_polynomial, ambient_temp, operating_temp), enthalpy_of_decomp) # In joules.

kilojoules_expended = energy_per_gram * feedstock_mass * 0.001 # Direct efficiency conversion. The 0.001 is to convert the specific heat from kJ per kilo per kelvin to kJ per **gram** per kelvin

# now energy costs
electricity_used = kilojoules_expended * kJ_per_kWh * energy_efficiency
electricity_cost = (electricity_used * cost_per_kWh)
runs_per_dollar = 1 / (electricity_cost)
electricity_per_dollar = (runs_per_dollar * electricity_used)
feedstock_per_dollar = feedstock_mass * runs_per_dollar
soot_per_dollar = soot_mass * runs_per_dollar
hydrogen_per_dollar = hydrogen_mass * runs_per_dollar


print("\n")
if print_wall_specs == True:
    print("Your wall will be " + str(wall_thickness) + " cm thick \nand weigh " + str(wall_mass) + " grams\n")

if print_reaction_specs == True:
    print("You will have reacted " + str(feedstock_mass) + " grams of " + feedstock_name + ",\nand produced " + str(soot_mass) + " grams of soot and " + str(hydrogen_mass) + " grams of H₂\n")

if print_soot_specs == True:
    print("There will be a layer of soot " + str(soot_thickness) + "mm thick on the sides of the pipe\nTotal amount of soot: " + str(soot_mass) + " grams\n")

if print_energy_cost == True:
    print("A dollar of electricity will convert " + str(feedstock_per_dollar) + " grams of " + feedstock_name + ",\nproducing " + str(hydrogen_per_dollar) + " grams of hydrogen and " + str(soot_per_dollar) + " grams of soot\n")
