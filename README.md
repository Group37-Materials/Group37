# BIManalyst group 37
#importing the file
import bpy
from bonsai.bim.ifc import IfcStore
model = IfcStore.get_file()
# here going through wall, but can change it to beam or column 
wall = model.by_type('IfcWall')[0]
for definition in wall.IsDefinedBy:
    for prop in definition.RelatingPropertyDefinition.HasProperties:
        print(prop.Name)
        if prop.Name == "Volume":
            #print("si")
            print("the volume is", prop.NominalValue.wrappedValue)
        if prop.Name == "Area":
            print("the area is", prop.NominalValue.wrappedValue)
        if prop.Name == "Length":
            print("the length is", prop.NominalValue.wrappedValue)
        
print(wall)





#####


"import ifcopenshell

# Load the IFC file
model = ifcopenshell.open("C:\\Users\\Administrator\\Desktop\\BIM\\CES_BLD_24_06_STR.ifc")

def get_property_value(properties, property_name):
    """
    Get the value of a specified property from a list of properties.
    """
    for prop in properties:
        if prop.Name == property_name:
            return prop.NominalValue.wrappedValue
    return None

def get_ifc_units(model):
    """
    Get the unit of measurement from the IFC model.
    """
    units = {}
    for unit in model.by_type('IfcUnitAssignment'):
        for unit_type in unit.Units:
            if unit_type.is_a('IfcSIUnit'):
                units[unit_type.UnitType] = unit_type.Prefix
    return units

def convert_to_meters(value, unit_type, prefix):
    """
    Convert a measurement to meters based on unit type and prefix.
    """
    unit_conversions = {
        'LENGTHUNIT': {'MILLI': 1e-3, 'CENTI': 1e-2, 'DECI': 1e-1, 'KILO': 1e3, 'MEGA': 1e6},
        'AREAUNIT': {'SQUARE_METRE': 1, 'HECTARE': 1e4},
        'VOLUMEUNIT': {'CUBIC_METRE': 1}
    }
    
    factor = unit_conversions.get(unit_type, {}).get(prefix, 1)
    return value * factor

def calculate_properties(entity_type):
    """
    Calculate the total length and volume of entities of a specified type.
    """
    total_length = 0
    total_volume = 0

    # Get the IFC units
    units = get_ifc_units(model)
    
    # Loop through all entities of the specified type
    for entity in model.by_type(entity_type):
        for definition in entity.IsDefinedBy:
            if definition.is_a('IfcRelDefinesByProperties'):
                property_set = definition.RelatingPropertyDefinition
                properties = property_set.HasProperties

                # Get the length and volume properties
                length = get_property_value(properties, "Length")
                volume = get_property_value(properties, "Volume")

                # Convert to meters if units are not meters
                if length is not None:
                    unit_prefix = units.get('LENGTHUNIT', 'METRE')
                    length_in_meters = convert_to_meters(length, 'LENGTHUNIT', unit_prefix)
                    total_length += length_in_meters
                    print(f"{entity_type} ID {entity.id()} has length: {length_in_meters:.2f} meters")
                
                if volume is not None:
                    unit_prefix = units.get('VOLUMEUNIT', 'CUBIC_METRE')
                    volume_in_cubic_meters = convert_to_meters(volume, 'VOLUMEUNIT', unit_prefix)
                    total_volume += volume_in_cubic_meters
                    print(f"{entity_type} ID {entity.id()} has volume: {volume_in_cubic_meters:.2f} cubic meters")
    
    return total_length, total_volume

# Calculate for columns
print("\nCalculating for columns:")
total_column_length, total_column_volume = calculate_properties('IfcColumn')
print(f"\nTotal length of columns: {total_column_length:.2f} meters")
print(f"Total volume of columns: {total_column_volume:.2f} cubic meters")

# Calculate for beams
print("\nCalculating for beams:")
total_beam_length, total_beam_volume = calculate_properties('IfcBeam')
print(f"\nTotal length of beams: {total_beam_length:.2f} meters")
print(f"Total volume of beams: {total_beam_volume:.2f} cubic meters")






######
# Given data
total_volume = 2780.41  # cubic meters
emission_factor = 200  # kg CO₂ per cubic meter
service_life = 50  # years

# Calculate total CO₂ emissions
total_co2_emissions = total_volume * emission_factor

# Calculate annual CO₂ emissions
annual_co2_emissions = total_co2_emissions / service_life

# Example: Estimate surface area (for demonstration, assume cross-sectional area of 0.5 m² and average length)
# Modify according to actual cross-sectional dimensions
average_length = total_volume / 0.5  # m (if we assume cross-sectional area is 0.5 m²)

# Total Surface Area (Assume width and height, adjust as needed)
# Here, height and width are assumed for demonstration purposes
width = 0.6  # meters
height = 0.6  # meters
total_surface_area = average_length * (width + height)  # m²

# Calculate CO₂ emissions per square meter per year
co2_per_m2_per_year = annual_co2_emissions / total_surface_area

print(f"Total CO₂ Emissions: {total_co2_emissions:.2f} kg CO₂")
print(f"Annual CO₂ Emissions: {annual_co2_emissions:.2f} kg CO₂/year")
print(f"CO₂ Emissions per m²/year: {co2_per_m2_per_year:.2f} kg CO₂/m²/year")


"
