# 	MISION RURAL
#	ANALISIS DE MAPAS
#	NOMBRE			:	DistTo_Linear
#	Autor			:	Jaime Millan
#	Fecha Creado 	:	140411
#	Ultimo Cambio	:	140411
#		Por			:	Jaime Millan

#################

""" 
	Descripcion:
		En este archivo se calcula la distancia lineal entre el centro de 
		cada predio y diferentes puntos como:
			la cabecera municipal
			la via pavimentada más cercana
			la via no pavimentada 
			capital de departamento

		El resultado de cada corrida es una base q tiene la informacion basica
		de cada region (con base en el .shp original) y dos columnas mas:
			La primera identifica el codigo del punto mas cercano (depende de que sea).
			La segunda tiene la distancia en km.
	
		Lo preparo como un loop the destinos y un loop de zonas.

		Este archivo compila las versiones anteriores de DistTo*_Lineal.py
"""

# Import system modules  (Importa ArcGis)
import arcpy
from arcpy import env

# Folders de trabajo
FldOn = "C:/MyWork/Dropbox/MisionRural/"
# FldOn = "C:/Users/nury.bejarano/Dropbox/MisionRural/"
FldIn = FldOn + "Input/PREDIOS/"
FldWork = FldOn + "Working/"
FldOut = FldWork + "DistanciasLineal/"
FolderDest = FldOn + "Input/MapaDigitalIntegrado_MDI/proyectados/"
NearRange = "1000 Kilometers"
# Lista de layers destinos
ListaDest = ['cabecera', 'carretera_pavimentada', 'carretera_sinpavimentar']

# Lista de zonas (layers origen)
ListaPredios = ['CORDOBA', 'BUENAVISTA', 'EL_CERRITO', 'PALMIRA']
#'BUENAVISTA', 'EL_CERRITO', 'PALMIRA'

# Iterar sobre destinos
for dest in ListaDest :
	LayerDest = FolderDest + dest + ".shp"
	
	# Iterar sobre los predios
	for zona in ListaPredios :
		LayerOn = FldIn + zona + "/RURAL/TPR_" + zona + ".shp" 
		# Eliminar PointsShape.shp
		PointsShape = FldWork + "PointsShape.shp" # Este .shp es temporal 
		try:
			arcpy.Delete_management(PointsShape , "")
		except: 
			arcpy.AddMessage('Points no existe')

		# Transformar los predios en puntos - Nombre temporal PointsShape.shp
		arcpy.FeatureToPoint_management(LayerOn, PointsShape, "CENTROID")

		# Calcular la distancia a la cabecera más cercana
		arcpy.Near_analysis(PointsShape,LayerDest,NearRange,"NO_LOCATION","NO_ANGLE")
		
		# Exportar a dbf (Primero debo borrar el archivo.dbf si existe)
		FileOut =  FldOut + zona + "_DistTo_" + dest + "_Linear.dbf"
		try:
			arcpy.Delete_management(FileOut, "")
		except:
			arcpy.AddMessage('No existia')

		arcpy.TableToDBASE_conversion(PointsShape,FldOut)
		arcpy.Rename_management(FldOut + "PointsShape.dbf",FileOut)

# Finaliza
Fin = 'LISTO EL BURRO CABALLERO'
print Fin

########

