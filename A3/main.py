import bpy
import os
import webbrowser
import xml.etree.ElementTree as ET

# Dictionaries to store total surface area, volume, and materials of each element type
area_totals = {}
volume_totals = {}
materials = {}

# LCA data: CO₂ footprint per cubic meter for each material
material_co2_footprint = {
    "Steel": 7.8,  # Example values: Replace with accurate data
    "Concrete": 0.2,
    "Wood": 0.03
}

# Data structure to store results for visualization and export
lca_data_for_visualization = {
    "Surface Area": {},
    "Volume": {},
    "CO2 Footprint": {},
}

# Function to calculate and sum surface area, volume, and identify materials for specified element types
def calculate_surface_area_volume_and_materials(element_type):
    # Clear previous totals
    area_totals.clear()
    volume_totals.clear()
    materials.clear()
    
    # Loop through all objects in the scene
    for obj in bpy.context.scene.objects:
        # Check if the object is a mesh (assumed to be an element)
        if obj.type == 'MESH' and obj.data:
            # Check if the chosen element type is in the object name
            if element_type in obj.name:
                # Calculate surface area as length * width (assuming Z dimension is height)
                length = obj.dimensions.x
                width = obj.dimensions.y
                height = obj.dimensions.z
                surface_area = length * width
                volume = length * width * height

                # Identify element subtype based on naming convention
                element_subtype = obj.name.split(":")[0]  # Adjust this according to your naming convention

                # Collect materials for the element
                element_materials = [mat.name.strip().lower() for mat in obj.data.materials if mat]  # Normalize material names

                # Sum the surface area, volume, and store materials for each subtype
                if element_subtype not in area_totals:
                    area_totals[element_subtype] = 0
                    volume_totals[element_subtype] = 0
                    materials[element_subtype] = set()  # Using a set to avoid duplicate materials
                area_totals[element_subtype] += surface_area
                volume_totals[element_subtype] += volume
                materials[element_subtype].update(element_materials)  # Add normalized materials to the set

    # Store results for visualization
    for subtype in area_totals:
        # Store the results in the global lca_data_for_visualization dictionary
        lca_data_for_visualization["Surface Area"][subtype] = area_totals[subtype]
        lca_data_for_visualization["Volume"][subtype] = volume_totals[subtype]
        lca_data_for_visualization["CO2 Footprint"][subtype] = volume_totals[subtype] * material_co2_footprint.get('Steel', 0)

    print(f"\nTotal Surface Area, Volume, and Materials for {element_type}s:")
    for subtype in area_totals:
        material_list = ", ".join(materials[subtype]) if materials[subtype] else "No material assigned"
        print(f"{subtype}: Surface Area = {area_totals[subtype]:.2f} m², Volume = {volume_totals[subtype]:.2f} m³, Materials = {material_list}")


# Function to perform LCA calculations
def perform_lca(material_type, element_type):
    total_co2 = 0
    normalized_material = material_type.strip().lower()  # Normalize the material type for matching
    for subtype, volume in volume_totals.items():
        if any(normalized_material in mat for mat in materials[subtype]):
            co2 = volume * material_co2_footprint.get(material_type, 0)
            total_co2 += co2
    
    print(f"\nLCA Calculation for {element_type}s using {material_type}:")
    print(f"Total CO₂ Footprint = {total_co2:.2f} kg CO₂")
    
    return total_co2


# Function to export data to an HTML file with Plotly.js
def export_to_html(data, file_name="LCA_results.html"):
    # Get the current project directory
    save_path = bpy.path.abspath("//")

    # Check if the current project directory is valid
    if not save_path or not os.path.exists(save_path):
        print("The current project directory is not valid. Using the Desktop as the fallback.")
        save_path = os.path.expanduser("~\\Desktop\\BIM")
    
    # Ensure the directory exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # Ensure the file name is correct
    file_path = os.path.join(save_path, file_name)
    
    try:
        # Create the HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>LCA Results - CO2 Footprint</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .chart-container {{
                    width: 100%;
                    max-width: 1000px;
                    margin: auto;
                }}
            </style>
        </head>
        <body>
            <h1>LCA Results - CO₂ Footprint</h1>
            <div class="chart-container">
                <div id="bar-chart"></div>
            </div>
            <script>
                var surface_area_data = {list(lca_data_for_visualization["Surface Area"].values())};
                var volume_data = {list(lca_data_for_visualization["Volume"].values())};
                var co2_data = {list(lca_data_for_visualization["CO2 Footprint"].values())};
                var labels = {list(lca_data_for_visualization["Surface Area"].keys())};

                var data = [
                    {{
                        x: labels,
                        y: surface_area_data,
                        type: 'bar',
                        name: 'Surface Area (m²)',
                        marker: {{color: 'rgb(76, 175, 80)'}}
                    }},
                    {{
                        x: labels,
                        y: volume_data,
                        type: 'bar',
                        name: 'Volume (m³)',
                        marker: {{color: 'rgb(0, 123, 255)'}}
                    }},
                    {{
                        x: labels,
                        y: co2_data,
                        type: 'bar',
                        name: 'CO₂ Footprint (kg)',
                        marker: {{color: 'rgb(255, 99, 71)'}}
                    }},
                ];

                var layout = {{
                    title: 'CO₂ Footprint, Surface Area, and Volume for Construction Elements',
                    barmode: 'group',
                    xaxis: {{
                        title: 'Element Type',
                    }},
                    yaxis: {{
                        title: 'Values',
                        rangemode: 'tozero',
                    }},
                    showlegend: true,
                }};
                
                Plotly.newPlot('bar-chart', data, layout);
            </script>
        </body>
        </html>
        """

        # Write HTML to file
        with open(file_path, 'w') as f:
            f.write(html_content)
        
        print(f"Data exported to {file_path}")
        
        # Automatically open the HTML file in the default browser
        webbrowser.open(f'file://{file_path}')

    except PermissionError:
        print(f"PermissionError: Unable to write to the file {file_path}. Please check file permissions.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Menu to prompt user for material type
def prompt_for_material_type(element_type):
    while True:
        print("\nChoose the material type for LCA calculation or go back:")
        print("1. Steel")
        print("2. Concrete")
        print("3. Wood")
        print("4. Go Back")
        choice = input("Enter the number corresponding to your choice: ").strip()
        
        material_mapping = {"1": "Steel", "2": "Concrete", "3": "Wood"}
        if choice == "4":
            return  # Go back to the previous menu
        material_type = material_mapping.get(choice)
        if material_type:
            total_co2 = perform_lca(material_type, element_type)
            return total_co2
        else:
            print("Invalid choice. Please try again.")


# Prompt user for the element type to analyze
def prompt_for_element_type():
    while True:
        print("\nChoose the element type to analyze:")
        print("1. Slabs")
        print("2. Beams")
        print("3. Columns")
        print("4. Exit")
        choice = input("Enter the number corresponding to your choice: ").strip()
        
        element_mapping = {"1": "Slab", "2": "Beam", "3": "Column"}
        if choice == "4":
            print("Exiting the script.")
            break
        element_type = element_mapping.get(choice)
        if element_type:
            calculate_surface_area_volume_and_materials(element_type)
            total_co2 = prompt_for_material_type(element_type)
            print(f"Total CO2 Footprint for {element_type}: {total_co2:.2f} kg CO₂")
            
            # Export the results to an HTML bar chart
            export_to_html(lca_data_for_visualization)
        else:
            print("Invalid choice. Please try again.")


# Clear previous selections
bpy.ops.object.select_all(action='DESELECT')

# Execute the element type prompt
prompt_for_element_type()

