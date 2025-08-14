import vtk

def gmsh2VTU(gmshModel):
    nodeTags, coords, _ = gmshModel.mesh.getNodes()
    all2DElements = gmshModel.mesh.getElements(2)
    elemType = all2DElements[0][0]
    elemTags = all2DElements[1][0]
    elemNodeTags = all2DElements[2][0]

    print("Element types:", elemType)
    # Create a mapping from nodeTags to their positions
    nodeTagToIndex = {nodeTag: idx for idx, nodeTag in enumerate(nodeTags)}

    # Create an ordered elemNodeTags array
    orderedElemNodeTags = [nodeTagToIndex[nodeTag] for nodeTag in elemNodeTags]

    vtk_points = vtk.vtkPoints()
    for i in range(len(nodeTags)):
        vtk_points.InsertNextPoint(coords[3 * i], coords[3 * i + 1], coords[3 * i + 2])

    unstructuredGrid = vtk.vtkUnstructuredGrid()
    unstructuredGrid.SetPoints(vtk_points)

    # Initialize the region array
    regionArray = vtk.vtkFloatArray()
    regionArray.SetName("Region")
    regionArray.SetNumberOfComponents(1)
    regionArray.SetNumberOfTuples(len(elemTags))

    # Get physical groups and their elements
    physicalGroups = gmshModel.getPhysicalGroups(2)
    physicalGroupMap = {}
    for dim, tag in physicalGroups:
        elementaryTags= gmshModel.getEntitiesForPhysicalGroup(dim, tag)
        for elemTag in elementaryTags:
            # Get the mesh elements of the elementary entity
            _, elementTags, _ = gmshModel.mesh.getElements(dim, elemTag)
            for elemTag in elementTags[0]:
                physicalGroupMap[elemTag] = tag

    regionValues = []
    for i in range(len(elemTags)):
        if elemType == 3:
            quad = vtk.vtkQuad()
            nodes = orderedElemNodeTags[4 * i:4 * (i + 1)]
            for j in range(4):  # Quadrangle has 4 vertices
                node_id = int(nodes[j])
                quad.GetPointIds().SetId(j, node_id)
            unstructuredGrid.InsertNextCell(quad.GetCellType(), quad.GetPointIds())
        elif elemType == 2:
            tri = vtk.vtkTriangle()
            nodes = orderedElemNodeTags[3 * i:3 * (i + 1)]
            for j in range(3):
                node_id = int(nodes[j])
                tri.GetPointIds().SetId(j, node_id)
            unstructuredGrid.InsertNextCell(tri.GetCellType(), tri.GetPointIds())

        # Assign region based on physical group
        region = physicalGroupMap.get(elemTags[i], -1)  # Default to -1 if not found
        regionValues.append(region)

    # Normalize the region values
    min_region = min(regionValues)
    max_region = max(regionValues)
    if min_region == max_region:
        normalizedRegions = [1.0] * len(regionValues)
    else:
        normalizedRegions = [1 - (region - min_region) / (max_region - min_region) for region in regionValues]

    for i, normalizedRegion in enumerate(normalizedRegions):
        regionArray.SetValue(i, normalizedRegion)

    # Add the region array to the unstructured grid
    unstructuredGrid.GetCellData().AddArray(regionArray)

    return unstructuredGrid