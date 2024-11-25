#About the tool
The tool is designed to solve the claim from A2: the calculation of the CO2 footprint for building elements in the building.
The claim is found on page 21 of the building project 2410, PM report, where a figure shows the CO2 footprint for building materials.

While working with the IFC models, a few problems appeared due to missing information in the models. 
Initially, a code was created to retrieve information about the volumes of building elements. 
During this process, it was noticed that the model CES_BLD_24_06_STR did not distinguish between slabs and beams. 
This issue is assumed to be specific to this model, and the final code does not account for this problem.
This decision was made to ensure the code remains general and not tailored to a single model. 
Additionally, some elements lacked properties for area or volume. 
Therefore, the code calculates these properties using the x, y, and z dimensions, ensuring it works more generally.

A second issue occurred when attempting to extract the material property for the element "Beam." 
No material was associated with the beams. Since the code should be as general as possible, it was decided to test it on another element where the material could be retrieved. 
The code should work for any building element, provided the model contains the correct information.
If the code is used on the element Slab instead of Beam, the material and volume can be retrieved correctly.
The areas of the materials are then converted to CO2 footprints, based on the material properties of the element. 
Finally, a plot is generated to visualize the distribution of CO2 for the building elements.

#Runnning the tool
The user will be prompted to choose an element type. 
Afterward, the user will be prompted to choose whether to include material or not.
The calculations of the CO2 footprint are then visualized.

#Advanced building Design 
Assuming that the BIM model is completed in Stage B, this tool should be applied at this stage.
As stated above, the tool will only work properly if there is information about the dimensions and material of the element being investigated. 
Additionally, the model should correctly distinguish between building elements.





