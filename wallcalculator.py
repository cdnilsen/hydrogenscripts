# Calculator for wall thickness
# a constant!
pi = 3.1416

input_diameter = True
input_length = False
input_strength = False
input_pressure = True
input_density = False

def getDimension(prompt):
    dimension = input(prompt)
    if dimension.isdigit() == True:
        return int(dimension)
    else: getDimension(prompt)
        
if (input_diameter == True):
    inner_diameter = getDimension("Enter the inner diameter of the chamber in centimeters: ")
else: inner_diameter = 100 # dummy value

if input_length == True:
    vessel_length = getDimension("Enter the length of the vessel, in cm: ")
else: vessel_length = 100

if input_strength == True:
    tensile_strength = getDimension("Enter the tensile strength of the material, in psi: ")
else: tensile_strength = 1000 

if input_pressure == True:
    operating_pressure = getDimension("Enter the operating pressure, in psi: ")
else: operating_pressure = 100

if input_density == True:
    density = getDimension("Enter the density of the wall material, in g/cm³: ")
else: density = 3

inner_diameter_inches = inner_diameter / 2.54
wall_thickness = (operating_pressure * inner_diameter_inches * 2.54)/(2 * tensile_strength) # the 2.54 constant gives cm

outer_diameter = inner_diameter + wall_thickness
outer_radius = outer_diameter / 2
inner_radius = inner_diameter / 2

outer_cylinder = (pi * (outer_radius ** 2) * vessel_length)
inner_cylinder = (pi * (inner_radius ** 2) * vessel_length)

wall_volume = outer_cylinder - inner_cylinder
wall_mass = wall_volume * density

print("\nYour wall will be " + str(wall_thickness) + " cm thick \nand weigh " + str(wall_mass) + " grams\n")
print("Propane per run: " + str(only_propane_per_run) + " grams")
print("Runs to empty a propane tank: " + str(9000/(only_propane_per_run))) # 9 kilos propane in a tank.
print("Versus with steam reforming: " + str(9000/(propane_per_run)))
