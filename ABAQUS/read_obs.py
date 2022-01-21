import numpy as np
import time

for gk in range(11,12):
    #ob = session.openOdb(name="parameters"+str(gk)+".odb")
    ob = session.openOdb(name="Job-80.odb")
    list_maxS = []
    list_maxLE = []
    list_val_Sii = []
    list_val_LEii = []
    list_coordSx = []
    list_coordSy = []
    list_coordSz = []  
    list_coordLEx = []
    list_coordLEy = []
    list_coordLEz = []
    iter = 0
    for kk in ob.steps.keys():
        for j in range(len(ob.steps[kk].frames)):
            iter += 1
            val_max = 0
            val_maxLE = 0
            Sob = ob.steps[kk].frames[j].fieldOutputs['S'].values
            COORDob = ob.steps[kk].frames[j].fieldOutputs['COORD'].values
            jj = np.argmax([Sob[i].mises for i in range(len(Sob))])
            list_val_Sii.append(jj)
            aaa = open("__argS_par_" + str(gk) + ".txt","a")
            aaa.write(str(jj) + "\t")
            aaa.close()
            val_max = Sob[jj].mises
            #if iter == 1:
            #    coordSx = 0
            #    coordSy = 0
            #    coordSz = 0
            #else:
            #    coordSx = COORDob[jj].data[0]
            #    coordSy = COORDob[jj].data[1]
            #    coordSz = COORDob[jj].data[2]
            LEob = ob.steps[kk].frames[j].fieldOutputs['LE'].values
            jj = np.argmax([LEob[i].maxPrincipal for i in range(len(LEob))])
            list_val_LEii.append(jj)
            val_maxLE = LEob[jj].maxPrincipal
            #if iter == 1:
            #    coordLEx = 0
            #    coordLEy = 0
            #    coordLEz = 0
            #else:
            #    coordLEx = COORDob[jj].data[0]
            #    coordLEy = COORDob[jj].data[1]
            #    coordLEz = COORDob[jj].data[2]
            list_maxS.append(val_max)
            list_maxLE.append(val_maxLE)
            aaa = open("__S_par_" + str(gk) + ".txt","a")
            aaa.write(str(val_max) + "\t")
            aaa.close()
            aaa = open("__LE_par_" + str(gk) + ".txt","a")
            aaa.write(str(val_maxLE) + "\t")
            aaa.close()
            aaa = open("__argLE_par_" + str(gk) + ".txt","a")
            aaa.write(str(jj) + "\t")
            aaa.close()
            #aaa = open("__XS_par_" + str(gk) + ".txt","a")
            #aaa.write(str(coordSx) + "\t")
            #aaa.close()
            #aaa = open("__YS_par_" + str(gk) + ".txt","a")
            #aaa.write(str(coordSy) + "\t")
            #aaa.close()
            #aaa = open("__ZS_par_" + str(gk) + ".txt","a")
            #aaa.write(str(coordSz) + "\t")
            #aaa.close()
            #aaa = open("__XLE_par_" + str(gk) + ".txt","a")
            #aaa.write(str(coordLEx) + "\t")
            #aaa.close()
            #aaa = open("__YLE_par_" + str(gk) + ".txt","a")
            #aaa.write(str(coordLEy) + "\t")
            #aaa.close()
            #aaa = open("__ZLE_par_" + str(gk) + ".txt","a")
            #aaa.write(str(coordLEz) + "\t")
            #aaa.close()
            #list_coordSx.append(coordSx)
            #list_coordSx.append(coordSy)  
            #list_coordSx.append(coordSz)  
            #list_coordLEx.append(coordLEx)
            #list_coordLEx.append(coordLEy)  
            #list_coordLEx.append(coordLEz)        
