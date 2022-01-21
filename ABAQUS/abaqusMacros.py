# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__, os, section, regionToolset, part, material, assembly, step, interaction, load, mesh, optimization, job, sketch, visualization, xyPlot, connectorBehavior
import displayGroupMdbToolset as dgm
import displayGroupOdbToolset as dgo
for hh in range(7,9):
    dir_string_main = "MProp"
    txtnome = "parameters" + str(hh)
    dir_aux1 = dir_string_main + '/' + txtnome + '.txt'
    
    dir_string_mat = dir_string_main + '/mat/'
    ok = os.listdir(dir_string_mat)
    
    for i in ok:
        mat1 = open(dir_string_mat + i)
        kk = mat1.readlines()
        nome = kk[0].split(":")[1].strip()
        D1111,D1122,D2222,D1133,D2233,D3333,D1112,D2212,D3312,D1212,D1113,D2213,D3313,D1213,D1313,D1123,D2223,D3323,D1223,D1323,D2323 = [float(kk[i].split(":")[1].strip()) for i in range(1,22)]
        mdb.models['Model-1'].Material(name=nome)
        mdb.models['Model-1'].materials[nome].Elastic(type=ANISOTROPIC,
        table=((D1111, D1122, D2222, D1133, D2233, D3333, D1112, D2212, D3312, D1212, D1113, 
        D2213, D3313, D1213, D1313, D1123, D2223, D3323, D1223, D1323, D2323), ))
        mat1.close()
    try:
        del mdb.models['Model-1'].parts['G1'].compositeLayups['CompositeLayup-1']
        del mdb.models['Model-1'].parts['G2'].compositeLayups['CompositeLayup-1']
    except:
        print("warning: no layups to remove")
    aaa = open(dir_aux1)
    kk = aaa.readlines()
    F1 = float(kk[0].split(":")[1].strip())
    mesh1 = float(kk[1].split(":")[1].strip())
    mesh2 = int(kk[2].split(":")[1].strip())
    N_cam = int(kk[3].split(":")[1].strip())
    simetrico = int(kk[4].split(":")[1].strip())
    nome = kk[5].split(":")[1].strip()
    ipontos = int(kk[6].split(":")[1].strip())
    layupOrientation = mdb.models['Model-1'].parts['G1'].datums[4]
    p = mdb.models['Model-1'].parts['G1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    region1 = regionToolset.Region(cells=cells)
    layupOrientation2 = mdb.models['Model-1'].parts['G2'].datums[10]
    p = mdb.models['Model-1'].parts['G2']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    region2 = regionToolset.Region(cells=cells)
    if simetrico == 0:
        simetrico = False
    else:
        simetrico = True
        
    mdb.models['Model-1'].interactionProperties['IntProp-1'].tangentialBehavior.setValues(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, 
        table=((F1, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    p1 = mdb.models['Model-1'].parts['G1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    layupOrientation = mdb.models['Model-1'].parts['G1'].datums[4]
    compositeLayup = mdb.models['Model-1'].parts['G1'].CompositeLayup(
        name='CompositeLayup-1', description='', elementType=SOLID, 
        symmetric=simetrico, thicknessAssignment=FROM_SECTION)
    compositeLayup.ReferenceOrientation(orientationType=SYSTEM, 
        localCsys=layupOrientation, fieldName='', 
        additionalRotationType=ROTATION_NONE, angle=0.0, 
        additionalRotationField='', axis=AXIS_3, stackDirection=STACK_3)
    compositeLayup.suppress()
    compositeLayup2 = mdb.models['Model-1'].parts['G2'].CompositeLayup(
        name='CompositeLayup-1', description='', elementType=SOLID, 
        symmetric=simetrico, thicknessAssignment=FROM_SECTION)
    compositeLayup2.ReferenceOrientation(orientationType=SYSTEM, 
        localCsys=layupOrientation2, fieldName='', 
        additionalRotationType=ROTATION_NONE, angle=0.0, 
        additionalRotationField='', axis=AXIS_3, stackDirection=STACK_3)
    compositeLayup2.suppress()
    for jj in range(N_cam):
        matmat = kk[7 + 3*jj].split(":")[1].strip()
        oo1 = float(kk[8 + 3*jj].split(":")[1].strip())
        tt1 = float(kk[9 + 3*jj].split(":")[1].strip())
        
        for c, r in zip([compositeLayup,compositeLayup2], [region1,region2]):
            c.CompositePly(suppressed=False, plyName='Ply-' + str(jj+1), region=r, material=matmat, thicknessType=SPECIFY_THICKNESS, thickness=tt1, orientationType=SPECIFY_ORIENT, orientationValue=oo1, additionalRotationType=ROTATION_NONE, additionalRotationField='', axis=AXIS_3, angle=0.0, numIntPoints=ipontos)
        pause
    compositeLayup.resume()
    compositeLayup2.resume()
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=ON)
    a = mdb.models['Model-1'].rootAssembly
    c1 = a.instances['G2'].cells
    cells1 = c1.getSequenceFromMask(mask=('[#1 ]', ), )
    c2 = a.instances['G1'].cells
    cells2 = c2.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions = cells1+cells2
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models['Model-1'].rootAssembly
    e1 = a.instances['G2'].edges
    e2 = a.instances['G1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=(
        '[#ffffff00 #37ffff #0:10 #fffffff4 #fb007fff #f #7000000', 
        ' #5 #0:2 #fffff000 #af ]', ), )+e2.getSequenceFromMask(mask=(
        '[#17fff #0:2 #60000000 #ff3ffffe #31ffff #0:3 #3ff3fe4', 
        ' #38000000 #bc00 #0 #ffd40000 #3f ]', ), )
    a.seedEdgeBySize(edges=pickedEdges, size=mesh1, deviationFactor=0.1, 
        constraint=FINER)
    session.viewports['Viewport: 1'].view.setValues(session.views['Top'])
    a = mdb.models['Model-1'].rootAssembly
    e1 = a.instances['G1'].edges
    e2 = a.instances['G2'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#0:10 #10000 ]', ), )+\
        e2.getSequenceFromMask(mask=('[#0:15 #400 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=mesh2, constraint=FINER)
    a = mdb.models['Model-1'].rootAssembly
    partInstances =(a.instances['G2'], a.instances['G1'], )
    a.generateMesh(regions=partInstances)
    session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
    aaa.close()
    #mdb.Job(name=txtnome, model='Model-1', description='', type=ANALYSIS, 
    #        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    #        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    #        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    #        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    #        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=4, 
    #        numDomains=4, numGPUs=1)
    #mdb.jobs[txtnome].submit(consistencyChecking=OFF)
    #mdb.jobs[txtnome].waitForCompletion()
    pause