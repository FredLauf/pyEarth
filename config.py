#parameters for the camera
camera = dict(
    #Sets the cameras x,y,z position using LLH to ECEF transformation
    latitude = 0, #[deg] Latitude of the camera position. Default: 0
    longitude = 0, #[deg] Latitude of the camera position. Default: 0
    height=36000, # [km] Sets the height of the camera above the latitude and longitude coordinates. Default: 36000

    #glFrustrum Settings. Only change if you know what you are doing
    frustL = -1, #Specify the coordinates for the left vertical clipping planes.
    frustR = 1,     #Specify the coordinates for the right vertical clipping planes.
    frustB = -1, #Specify the coordinates for the bottom horizontal clipping planes.
    frustT = 1, #Specify the coordinates for the top horizontal clipping planes.
    nearVal = 5, #Specify the distance to the near clipping plane
    farVal= 1000, #Specify the distance to the far clipping plane

    #Keyboard mouse movement settings
    rotationFactor= 1.5, #[deg] defines the amount of lat/lon change in degrees when using the arrow keys. Can be adjusted as desired
    zoomFactor = 500, #[km] adjusts the height change of the camera when using Shift/Ctrl keys to zoom in and out
)
#parameters for shapefile config
shapefile_paraments = dict(
    aliasing = 2, # Sets the number of polygon subdivisions. Recommended: 2. NOTICE: LARGE EFFECT ON PERFORMANCE!
    landmassRgb =[0,250,0], #[R,G,B] Sets the colour of the landmasses
)
#parameters for the window
window = dict(
    heightres = 1400, #[pixels] Sets the height of the window
    widthres= 1400, #[pixels] Sets the width of the window
)
#parameters of the satellite
satellite = dict(
    tle1 = "1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927", #Set the first and second line of the TLE
    tle2 = "2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537",
    date = "DATE PLACEHOLDER",
    deltaTime = "DATETIME PLACEHOLDER",
)


#TO DO:
#Add shapefile selection to the config for full automation 
