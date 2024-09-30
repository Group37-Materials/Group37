def calc_beam_length(model):
    # Initialize counters for different types of beams listed in the appendix page 2
    DR22250 = 0  # Counter for "Edge beam (DR): STR - Edge Deltabeam - DR22-250"
    DR26230 = 0  # Counter for "Edge beam (DR): STR - Edge Deltabeam - DR26-230"
    D50500 = 0   # Counter for "Intermediate beam (D): STR - Intermediate Deltabeam - D50-500"
    D22400 = 0   # Counter for "Intermediate beam (D): STR - Intermediate Deltabeam - D22-400"

    # Loop through all IfcBeam entities in the model
    for entity in model.by_type("IfcBeam"):
        # Loop through all property sets associated with the current beam entity
        for relDefinesByProperties in entity.IsDefinedBy:
            # Loop through each property in the property set
            for prop in relDefinesByProperties.RelatingPropertyDefinition.HasProperties:
                # Check if the property value matches a specific beam type and update the corresponding length counter
                if prop.NominalValue.wrappedValue == "Edge beam (DR): STR - Edge Deltabeam - DR22-250":
                    # Loop again through properties to find the Length property and update the DR22250 counter
                    for relDefinesByProperties in entity.IsDefinedBy:
                        for prop in relDefinesByProperties.RelatingPropertyDefinition.HasProperties:
                            if prop.Name == "Length":
                                DR22250 += prop.NominalValue.wrappedValue
                if prop.NominalValue.wrappedValue == "Intermediate beam (D): STR - Intermediate Deltabeam - D22-400":
                    # Loop again through properties to find the Length property and update the D22400 counter
                    for relDefinesByProperties in entity.IsDefinedBy:
                        for prop in relDefinesByProperties.RelatingPropertyDefinition.HasProperties:
                            if prop.Name == "Length":
                                D22400 += prop.NominalValue.wrappedValue
                if prop.NominalValue.wrappedValue == "Intermediate beam (D): STR - Intermediate Deltabeam - D50-500":
                    # Loop again through properties to find the Length property and update the D50500 counter
                    for relDefinesByProperties in entity.IsDefinedBy:
                        for prop in relDefinesByProperties.RelatingPropertyDefinition.HasProperties:
                            if prop.Name == "Length":
                                D50500 += prop.NominalValue.wrappedValue
                if prop.NominalValue.wrappedValue == "Edge beam (DR): STR - Edge Deltabeam - DR26-230":
                    # Loop again through properties to find the Length property and update the DR26230 counter
                    for relDefinesByProperties in entity.IsDefinedBy:
                        for prop in relDefinesByProperties.RelatingPropertyDefinition.HasProperties:
                            if prop.Name == "Length":
                                DR26230 += prop.NominalValue.wrappedValue

    # Print the total lengths of each type of beam, converted to meters (from millimeters)
    print(f"\nThere are {round(D22400/1000)} meters of D22-400 in the model")
    print(f"\nThere are {round(D50500/1000)} meters of D50-500 in the model")
    print(f"\nThere are {round(DR26230/1000)} meters of DR26-230 in the model")
    print(f"\nThere are {round(DR22250/1000)} meters of DR22-250 in the model")

    # Return from the function
    return
