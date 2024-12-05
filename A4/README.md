# THE VIDEO 
part 1 https://www.youtube.com/watch?v=ziw4qH928EE
part 2 https://www.youtube.com/watch?v=Gs3V-AdHwMI

# Markdown of the code 
## LCA data: CO₂ footprint per cubic meter for each material
    #material_co2_footprint = {
    "Steel": 7.8,  # Example values: Replace with accurate data
    "Concrete": 0.2,
    "Wood": 0.03


## Function to calculate and sum surface area, volume, and identify materials for specified element ty. This part will loop through the model and extract volumes and areas. 
    #def calculate_surface_area_volume_and_materials(element_type):
    # Clear previous totals
    area_totals.clear()
    volume_totals.clear()
    materials.clear()
    

## Function to perform LCA calculations, this part calculate the CO2 footprint 

    #def perform_lca(material_type, element_type):
    total_co2 = 0
    normalized_material = material_type.strip().lower()  # Normalize the material type for matching
    for subtype, volume in volume_totals.items():
        if any(normalized_material in mat for mat in materials[subtype]):
            co2 = volume * material_co2_footprint.get(material_type, 0)
            total_co2 += co2
    
    print(f"\nLCA Calculation for {element_type}s using {material_type}:")
    print(f"Total CO₂ Footprint = {total_co2:.2f} kg CO₂")
  


## Function to export data to an HTML file with Plotly.js
    #def export_to_html(data, file_name="LCA_results.html"):
 

## Menu to prompt user for material type and element type 
    #def prompt_for_material_type(element_type):
    #def prompt_for_element_type():

# Short summary
Title: CO2 footprint of building element\\
The tool should be able to calculate the CO2 footprint for an IFC-element. It will then visualize it for the user with a bar plot.   
