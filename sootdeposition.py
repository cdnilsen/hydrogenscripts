# models the amount of soot you're gonna get in a pipe of a certain diameter

molar_mass = 44.1 # g/mol
fraction_deposited = 0.817 # how much of the molecule is carbon?
soot_density = 1.5 # g/cm³. we try to underestimate the density here

pressure = 5 # in bars
inner_diameter = 50 # in cm
temperature = 900 # degrees C
inner_radius = (inner_diameter / 2)

temp_kelvin = temperature + 273.15

# We will consider a section of pipe that's 1cm long
pi = 3.1416
pipe_length  = 1000 # in cm
cross_volume = pi * (inner_radius ** 2) * pipe_length
inner_surface = (2 * pipe_length * inner_diameter * pi)

mole_constant = 0.01202724 # number of moles in 1cm³ of gas at 1 bar at a temp of 1 kelvin

number_of_moles = (cross_volume * mole_constant * pressure) / (temp_kelvin)

total_grams = number_of_moles * molar_mass
total_soot_volume = (total_grams) * (soot_density) # in cm³
soot_thickness = (total_soot_volume / inner_surface) * 1000 # in mm




print("Pipe volume: " + str(cross_volume) + " cm³")
print(str(number_of_moles) + " moles")
print("Surface area: " + str(inner_surface) + " cm²")
print(str(total_grams) + " grams")
print("Total soot volume = " + str(total_soot_volume) + " cm³")
print("Total soot thickness: " + str(soot_thickness) + " mm")

# Soot thickness rises linearly with diameter. Amount deposited rises with the square of diameter
