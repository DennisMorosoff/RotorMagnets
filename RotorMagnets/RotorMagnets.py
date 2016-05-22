
from math import pi, sin, cos, tan


def createMyFeature(ag):
    ExtAPI.CreateFeature("RMagFeature")

def generateRMagGeometry(feature,fct):
    ExtAPI.Log.WriteMessage("Generating Rotor Magnets...")
    
    # Collect all property values in meter unit
    fromUnit, toUnit = ExtAPI.DataModel.CurrentUnitFromQuantityName("Length"), "m"
    
    #Get Length width and Thickness of the Box
    De = units.ConvertUnit(feature.Properties["De"].Value, fromUnit, toUnit)
    Di = units.ConvertUnit(feature.Properties["Di"].Value, fromUnit, toUnit)
    Thickness = units.ConvertUnit(feature.Properties["Thickness"].Value, fromUnit, toUnit)
    Count = feature.Properties["Count"].Value
    
    ExtAPI.Log.WriteMessage("De: "+De.ToString())
    ExtAPI.Log.WriteMessage("Di: "+Di.ToString())
    ExtAPI.Log.WriteMessage("Thickness: "+Thickness.ToString())
    ExtAPI.Log.WriteMessage("Count: "+Count.ToString())
    
    bodies=[]

    try:
        #Creating Trapeze
        
        #Calculating points coord
        xde = De/2*sin(pi/(Count))
        yde = De/2*cos(pi/(Count))
        xdi = Di/2*tan(pi/(Count))
        ydi = Di/2
        
        ExtAPI.Log.WriteMessage("pi: " + pi.ToString())
        ExtAPI.Log.WriteMessage("xde: " + xde.ToString())
        ExtAPI.Log.WriteMessage("yde: " + yde.ToString())
        ExtAPI.Log.WriteMessage("xdi: " + xdi.ToString())
        ExtAPI.Log.WriteMessage("ydi: " + ydi.ToString())
        
        ExtAPI.Log.WriteMessage("Primitives.Sheet.CreatePolygon")
        
        trapeze = ExtAPI.DataModel.GeometryBuilder.Primitives.Sheet.CreatePolygon([-xde, 0., yde, -xdi, 0., ydi, xdi, 0., ydi, xde, 0., yde])
        trapeze_generated = trapeze.Generate()
        
        #Extruding
        extrude = ExtAPI.DataModel.GeometryBuilder.Operations.CreateExtrudeOperation([0.,1.,0.],Thickness)
        bodies.Add(extrude.ApplyTo(trapeze_generated)[0])
        
    except:
        pass
        
    feature.Bodies = bodies
    feature.MaterialType = MaterialTypeEnum.Freeze

    return True
