# Pressure Vessel Calculator

tensile_strength = 1000 # in psi. 
diameter_metric = 100 # inner diameter, in centimeters
diameter_inches = (diameter_metric)/2.54
pressure = 100 # operating pressure in psi
wall_thickness = (pressure * diameter_inches)/(2 * tensile_strength) # in inches

material_density = 2.2 # g/cm³, or tonnes/m³ if you'd like

# We'll assume a pressure vessel built as a cylinder capped by hemispheres. Hoop stress is twice as high as longitudinal stress for thin-walled vessels so we'll mostly worry about hoop stress. 
pi = 3.1416
cylinder_length = 100 # centimeters
wall_thickness_metric = wall_thickness * 2.54 # centimeters
outer_diameter = diameter_metric + (2 * wall_thickness_metric)
outer_radius = (outer_diameter / 2)
inner_radius = (diameter_metric / 2)

outer_cylinder = (pi * (outer_radius ** 2) * cylinder_length)
inner_cylinder = (pi * (inner_radius ** 2) * cylinder_length)

cylinder_wall_volume = (outer_cylinder - inner_cylinder)
hemisphere_wall_volume = (wall_thickness_metric * 4 * pi * (outer_radius ** 2))

total_wall_volume = cylinder_wall_volume + hemisphere_wall_volume

total_wall_weight = (material_density * total_wall_volume) / 1000 # in kilos

chamber_volume = (inner_cylinder + ((4/3) * pi * (inner_radius ** 3))) / (1000000) # in m³

# now we do the gas math
# molar masses in grams
h2_mass = 2.02 
co2_mass = 44.01
h2o_mass = 18.02
propane_mass = 44.1

operating_temp = 900 # celsius
operating_kelvin = operating_temp + 273.15

molarity_constant = 829.25 # number of moles in a volume of 1m³ at 1 kelvin at a pressure of 1 psi

actual_molarity = (molarity_constant * chamber_volume * pressure) / (operating_kelvin)

# One mole of propane and six moles of water go in; 3 moles CO₂ and 10 moles of H₂ leave. Therefore, "actual molarity" tells us how much H₂ and CO₂ we can fit in, the number of moles for H₂O and propane will be smaller

input_molarity = (actual_molarity * 7)/13

propane_molarity = input_molarity/7
water_molarity = input_molarity - propane_molarity

co2_molarity = (actual_molarity*3)/13
h2_molarity = (actual_molarity - co2_molarity)

propane_per_run = propane_molarity * propane_mass # in grams
water_per_run = water_molarity * h2o_mass

co2_per_run = co2_molarity * co2_mass
h2_per_run = h2_molarity * h2_mass

'''
print("Propane per run: " + str(propane_per_run) + " grams")
print("Water per run: " + str(water_per_run) + " grams")
print("Total input mass: " + str(water_per_run + propane_per_run) + "grams")
print("Total output mass: " + str(co2_per_run + h2_per_run) + "grams") # Sanity check, these should be within a fraction of a gram
print("Runs to empty a propane tank: " + str(9000/(propane_per_run))) # 9 kilos propane in a tank.

print("Volume of chamber = " + str(chamber_volume) + " m³")
'''
print("At " + str(pressure) + " psi:")
print("Needed wall thickness = " + str(wall_thickness) + " inches")
print("Total volume of wall: " + str(total_wall_volume/1000000) + " m³")
print("Total mass of vessel walls: " + str(total_wall_weight) + " kg")

# now let's try pyrolysis: 
propane_only_molarity = actual_molarity / 4 # C3H8 -> 3C + 4H2
only_propane_per_run = propane_only_molarity * propane_mass
print("Propane per run: " + str(only_propane_per_run) + " grams")
print("Runs to empty a propane tank: " + str(9000/(only_propane_per_run))) # 9 kilos propane in a tank.
print("Versus with steam reforming: " + str(9000/(propane_per_run)))