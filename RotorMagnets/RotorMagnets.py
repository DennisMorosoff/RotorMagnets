
from math import pi, sin, cos, tan
import units  


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

    alfa = pi/8

    # xde = (De/2*sin(pi/(Count)))
    # yde = De/2*cos(pi/(Count)) 
    # xdi = Di/2*tan(pi/(Count)) 
    # ydi = Di/2 

    x0e_ = -De/2*sin(pi/Count)
    y0e_ = De/2*cos(pi/Count)  
    
    x1e_ = De/2*sin(pi/Count)
    y1e_ = De/2*cos(pi/Count) 
    
    x2i_ = Di/2*tan(pi/Count)
    y2i_ = Di/2
    
    x3i_ = -Di/2*tan(pi/Count)
    y3i_ = Di/2
    # nado zapretit vvod menshe 3
    ExtAPI.Log.WriteMessage("point0 x: " + x0e_.ToString() + "  y: " + y0e_.ToString())
    ExtAPI.Log.WriteMessage("point1 x: " + x1e_.ToString() + "  y: " + y1e_.ToString())
    ExtAPI.Log.WriteMessage("point2 x: " + x2i_.ToString() + "  y: " + y3i_.ToString())
    ExtAPI.Log.WriteMessage("point3 x: " + x3i_.ToString() + "  y: " + y3i_.ToString())
    
   
    for i in range(0, Count, 1):
        #i = j + 1
        
        # point 0
        x0e = x0e_*cos(2*i*pi/Count) - y0e_*sin(2*i*pi/Count)
        y0e = x0e_*sin(2*i*pi/Count) + y0e_*cos(2*i*pi/Count)
        ExtAPI.Log.WriteMessage("point0 x: " + x0e.ToString() + "  y: " + y0e.ToString())
        
        # point 1
        x1e = x1e_*cos(2*i*pi/Count) - y1e_*sin(2*i*pi/Count)
        y1e = x1e_*sin(2*i*pi/Count) + y1e_*cos(2*i*pi/Count)
        ExtAPI.Log.WriteMessage("point1 x: " + x1e.ToString() + "  y: " + y1e.ToString())
        
        # point 2
        x2i = x2i_*cos(2*i*pi/Count) - y2i_*sin(2*i*pi/Count)
        y2i = x2i_*sin(2*i*pi/Count) + y2i_*cos(2*i*pi/Count)
        ExtAPI.Log.WriteMessage("point2 x: " + x2i.ToString() + "  y: " + y2i.ToString())
        
        # point 3
        x3i = x3i_*cos(2*i*pi/Count) - y3i_*sin(2*i*pi/Count)
        y3i = x3i_*sin(2*i*pi/Count) + y3i_*cos(2*i*pi/Count)
        ExtAPI.Log.WriteMessage("point3 x: " + x3i.ToString() + "  y: " + y3i.ToString())
        
        ExtAPI.Log.WriteMessage("")
        
    
        try:
            #Creating Trapeze
            
            #Calculating point coords
            # xde = De/2*sin(alfa+pi/(Count))
            # yde = De/2*cos(alfa+pi/(Count))
            # xdi = Di/2*tan(alfa+pi/(Count))
            # ydi = Di/2
            
            # ExtAPI.Log.WriteMessage("pi: " + pi.ToString())
            # ExtAPI.Log.WriteMessage("xde: " + xde.ToString())
            # ExtAPI.Log.WriteMessage("yde: " + yde.ToString())
            # ExtAPI.Log.WriteMessage("xdi: " + xdi.ToString())
            # ExtAPI.Log.WriteMessage("ydi: " + ydi.ToString())
            
            ExtAPI.Log.WriteMessage("Primitives.Sheet.CreatePolygon")
            
            trapeze = ExtAPI.DataModel.GeometryBuilder.Primitives.Sheet.CreatePolygon([x0e, 0., y0e, x1e, 0., y1e, x2i, 0., y2i, x3i, 0., y3i])
            trapeze_generated = trapeze.Generate()
            
            #Extruding
            extrude = ExtAPI.DataModel.GeometryBuilder.Operations.CreateExtrudeOperation([0.,1.,0.],Thickness)
            bodies.Add(extrude.ApplyTo(trapeze_generated)[0])
            
            
            
        except:
            pass
        
    feature.Bodies = bodies
    feature.MaterialType = MaterialTypeEnum.Freeze

    return True
