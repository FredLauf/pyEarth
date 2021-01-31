import shapefile
import shapely.geometry
import sys
import math
from math import cos, pi, sin
from sgp4.api import Satrec
from sgp4.api import jday
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class View(QOpenGLWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        for coord in ('x', 'y', 'z', 'cx', 'cy', 'cz', 'rx', 'ry', 'rz'):
            setattr(self, coord, 50 if coord == 'z' else 0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)

    def initializeGL(self):
        glMatrixMode(GL_PROJECTION)
        glEnable(GL_LINE_SMOOTH)  
        glEnable(GL_BLEND)  
        #self.create_polygons(0,0,0)
        glFrustum(self.frustL, self.frustR, self.frustB, self.frustT, 5, 1000)
        self.polygons = glGenLists(1)
        self.lake_polygons = glGenLists(1)
        self.river_polylines = glGenLists(1)
        self.points = glGenLists(1)

    def paintGL(self):
        #glFrustum(-1, 1, -1, 1, 5, 1000)
        glColor(0, 0, 255)
        glEnable(GL_DEPTH_TEST)
        glPushMatrix()
        glTranslatef(0, 0, 0) #Move to the place
        glColor(0, 0, 255)
        gluSphere(gluNewQuadric(), 6.35, 128, 128) #Draw sphere

        glPopMatrix()

        if hasattr(self, 'polygons'):
           glPushMatrix()
           glRotated(self.rx/16, 1, 0, 0)
           glRotated(self.ry/16, 0, 1, 0)
           glRotated(self.rz/16, 0, 0, 1)
           glCallList(self.polygons)
           glPopMatrix()
        if hasattr(self, 'lake_polygons'):
           glPushMatrix()
           glRotated(self.rx/16, 1, 0, 0)
           glRotated(self.ry/16, 0, 1, 0)
           glRotated(self.rz/16, 0, 0, 1)
           glCallList(self.lake_polygons)
           glPopMatrix()
        if hasattr(self, 'river_polylines'):
           glPushMatrix()
           glRotated(self.rx/16, 1, 0, 0)
           glRotated(self.ry/16, 0, 1, 0)
           glRotated(self.rz/16, 0, 0, 1)
           glCallList(self.river_polylines)
           glPopMatrix()
        if hasattr(self, 'points'):
           glPushMatrix()
           glRotated(self.rx/16, 1, 0, 0)
           glRotated(self.ry/16, 0, 1, 0)
           glRotated(self.rz/16, 0, 0, 1)
           glCallList(self.points)
           glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.x, self.y, self.z, self.cx, self.cy, self.cz, self.upx, self.upy, self.upz)
        self.update()

    def mousePressEvent(self, event):
        self.last_pos = event.pos()
        
    def wheelEvent(self, event):
        self.z += -2 if event.angleDelta().y() > 0 else 2

    def mouseMoveEvent(self, event):
        dx, dy = event.x() - self.last_pos.x(), event.y() - self.last_pos.y()
        if event.buttons() == Qt.LeftButton:
            self.rx, self.ry = self.rx + 8*dy, self.ry + 8*dx
        elif event.buttons() == Qt.RightButton:
            self.cx, self.cy = self.cx - dx/50, self.cy + dy/50
        self.last_pos = event.pos()
         
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.lon = self.lon + 1.5
            self.x,self.y,self.z= self.LLH_to_ECEF(self.lat, self.lon, self.cam_height , 1, False)
        if event.key() == Qt.Key_Left:
            self.lon = self.lon - 1.5
            self.x,self.y,self.z= self.LLH_to_ECEF(self.lat, self.lon, self.cam_height , 1, False)
        if event.key() == Qt.Key_Up:
            self.lat = self.lat + 1.5
            self.x,self.y,self.z= self.LLH_to_ECEF(self.lat, self.lon, self.cam_height , 1, False)
        if event.key() == Qt.Key_Down:
            self.lat = self.lat - 1.5
            self.x,self.y,self.z= self.LLH_to_ECEF(self.lat, self.lon, self.cam_height , 1, False)
        if event.key() == Qt.Key_Control:
            self.cam_height = self.cam_height - 50
            self.x,self.y,self.z= self.LLH_to_ECEF(self.lat, self.lon, self.cam_height , 1, False)
        if event.key() == Qt.Key_Shift:
            self.cam_height = self.cam_height + 50
            self.x,self.y,self.z= self.LLH_to_ECEF(self.lat, self.lon, self.cam_height , 1, False)
            2
        if event.key() == Qt.Key_Space:
            if self.timer.isActive():
                self.timer.stop()
            else:
                self.timer.start()

    def rotate(self):  
        self.rx, self.ry = self.rx + 6, self.ry + 6
            
    def vertices_generator(self,input,height):
        vertices_new=[]
        #height=height/1000000
        for i in range(0,len(input),3):
            A=input[i]
            B=input[i+1]
            C=input[i+2]     
            D=[]
            x=(A[0]+B[0])/2
            y=(A[1]+B[1])/2
            z=(A[2]+B[2])/2
            vector_length= math.sqrt((x*x)+(y*y)+(z*z))
            x=x/vector_length
            y=y/vector_length
            z=z/vector_length
            x=x*6.378137*height
            y=y*6.378137*height
            z=z*6.378137*height
            D.append(x) #x
            D.append(y) #y
            D.append(z) #z
            E=[]
            x=(C[0]+B[0])/2
            y=(C[1]+B[1])/2
            z=(C[2]+B[2])/2
            vector_length= math.sqrt((x*x)+(y*y)+(z*z))
            x=x/vector_length
            y=y/vector_length
            z=z/vector_length
            x=x*6.378137*height
            y=y*6.378137*height
            z=z*6.378137*height
            E.append(x) #x
            E.append(y) #y
            E.append(z) #z
            F=[]
            x=(C[0]+A[0])/2
            y=(C[1]+A[1])/2
            z=(C[2]+A[2])/2
            vector_length= math.sqrt((x*x)+(y*y)+(z*z))
            x=x/vector_length
            y=y/vector_length
            z=z/vector_length
            x=x*6.378137*height
            y=y*6.378137*height
            z=z*6.378137*height
            F.append(x) #x
            F.append(y) #y
            F.append(z) #z

            vertices_new.append(A)
            vertices_new.append(D)
            vertices_new.append(F)

            vertices_new.append(D)
            vertices_new.append(B)
            vertices_new.append(E)

            vertices_new.append(E)
            vertices_new.append(C)
            vertices_new.append(F)

            vertices_new.append(F)
            vertices_new.append(D)
            vertices_new.append(E)
        return vertices_new
    
    def create_polygons(self,r,g,b,height):
        glNewList(self.polygons,GL_COMPILE)
        for polygon in self.extract_polygons():
            glLineWidth(1.2)
            glBegin(GL_LINE_LOOP)
            #line colour
            glColor(0, 0,0)
            for lon, lat in polygon.exterior.coords:
                glVertex3f(*self.LLH_to_ECEF(lat, lon, 1 , height, True))
            glEnd()
            #fill colour
            glColor(r, g, b)
            glBegin(GL_TRIANGLES)
            for vertex in self.polygon_tesselator(polygon , height , True ):
                glVertex(*vertex)
            glEnd()
        glEndList()

    def create_lake_polygons(self,r,g,b,height):
        glNewList(self.lake_polygons,GL_COMPILE)
        for polygon in self.extract_polygons():
            glLineWidth(1.2)
            glBegin(GL_LINE_LOOP)
            #line colour
            glColor(0, 0,0)
            for lon, lat in polygon.exterior.coords:
                glVertex3f(*self.LLH_to_ECEF(lat, lon, height, height , True))
            glEnd()

            #fill colour
            glColor(r, g, b)
            glBegin(GL_TRIANGLES)
            for vertex in self.polygon_tesselator(polygon , height, True):
                glVertex(*vertex)
            glEnd()

        glEndList()

    def create_river_polylines(self,r,g,b,height):

        glNewList(self.river_polylines,GL_COMPILE)
        i=1
        for polyline in self.extract_polylines():
            glLineWidth(1)
            glBegin(GL_LINE_STRIP)
            
            #line colour
            glColor(r, g,b)
            for lon, lat in polyline.coords:
                glVertex3f(*self.LLH_to_ECEF(lat, lon, 1 , height, True))
            glEnd()
            i=i+1
        print("All rivers done")
        glEndList()


    def create_points(self,r,g,b,height):
        glNewList(self.points,GL_COMPILE)

        for point in self.extract_points():
            glPointSize(3)
            glColor(r, g, b)
            glBegin(GL_POINTS)
            for lon, lat in point.coords:
                glVertex3f(*self.LLH_to_ECEF(lat, lon, height , height, True))
            glEnd()
        glEndList()

    def extract_points(self):
        if not hasattr(self, 'shapefile'):
                    return
        sf = shapefile.Reader(self.shapefile)       
        points = sf.shapes() 
        for point in points:
            point = shapely.geometry.shape(point)
            yield from [point] if point.geom_type == 'Point' else point

    def polygon_tesselator(self, polygon,height , norm):    
        vertices, tess = [], gluNewTess()
        gluTessCallback(tess, GLU_TESS_EDGE_FLAG_DATA, lambda *args: None)
        gluTessCallback(tess, GLU_TESS_VERTEX, lambda v: vertices.append(v))
        gluTessCallback(tess, GLU_TESS_COMBINE, lambda v, *args: v)
        gluTessCallback(tess, GLU_TESS_END, lambda: None)
        
        gluTessBeginPolygon(tess, 0)
        gluTessBeginContour(tess)
        #Get the coordinates of the outside of the polygon/country
        for lon, lat in polygon.exterior.coords:
            point = self.LLH_to_ECEF(lat, lon, 0,height, norm)
            gluTessVertex(tess, point, point)
        gluTessEndContour(tess)
        gluTessEndPolygon(tess)
        gluDeleteTess(tess)
        
        aliasing = self.aliasing

        for i in range(0, aliasing):
            vertices=self.vertices_generator(vertices,height)
        return vertices

    def extract_polygons(self):
        if not hasattr(self, 'shapefile'):
            return
        sf = shapefile.Reader(self.shapefile)       
        polygons = sf.shapes() 
        for polygon in polygons:
            polygon = shapely.geometry.shape(polygon)
            yield from [polygon] if polygon.geom_type == 'Polygon' else polygon

    def extract_polylines(self):
        if not hasattr(self, 'shapefile'):
            return
        sf = shapefile.Reader(self.shapefile)
        polylines = sf.shapes()
        for polyline in polylines:
            try:
                polyline = shapely.geometry.shape(polyline)
            
                if polyline.geom_type == "LineString":
                    yield from [polyline] if polyline.geom_type == 'LineString' else linestring

                elif polyline.geom_type == "MultiLineString":
                    mls = [polyline]
                    for mlsriver in mls:
                        for mlsline in mlsriver:
                            yield from [mlsline] if mlsline.geom_type == 'LineString' else linestring
            except:
                print("Error: Polyline could not be loaded")
                continue 


    def LLH_to_ECEF(self, lat, lon, alt,height, norm):
        rad_lat = lat * (math.pi / 180.0)
        rad_lon = lon * (math.pi / 180.0)
        alt= alt*1000
        alt = 6378137 + alt
        a = 6378137.0 
        finv = 298.257223563
        f = 1 / finv
        e2 = 1 - (1 - f) * (1 - f)
        v = a / math.sqrt(1 - e2 * math.sin(rad_lat) * math.sin(rad_lat))

        x = (v + alt) * math.cos(rad_lat) * math.cos(rad_lon)
        y = (v + alt) * math.cos(rad_lat) * math.sin(rad_lon)
        z = (v * (1 - e2) + alt) * math.sin(rad_lat)
        
        if norm == True:
            vector_length= math.sqrt((x*x)+(y*y)+(z*z))
            x=x/vector_length
            y=y/vector_length
            z=z/vector_length
            x=x*6378137*height
            y=y*6378137*height
            z=z*6378137*height
        return x/1000000, y/1000000, z/1000000

class PyEarth(QMainWindow):
    
    def __init__(self):
        aliasing = 0
        while  1 > aliasing or aliasing > 4 :
            aliasing = int(input("Set aliasing factor from 1 to 4 (2 Recommended): "))
        
        
        longitude = 200 
        while  -180 > longitude or longitude > 180 :
            longitude = int(input("Set camera position longitude (-180 180): "))

        latitude = 200 
        while -90 > latitude or latitude > 90:
            latitude = int(input("Set camera position latitude (-90 90): "))

        fov = -1 
        while 0 > fov or fov > 45:
            print("The camera is set as a fixed height. Can be slightly adjusted using the Shift and Ctrl keys")
            print("The FOV of the camera can be set by entering the longitudinal angle.")
            print("Example: Showing Europe would require roughly 60 degrees. Germany would require 10 degrees")
            print("This is just a rough value, pick a smaller angle and then zoom out for best result")
            fov = int(input("Set camera FOV in longitude degrees at equator (1-45): "))

        super().__init__()
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        menu_bar = self.menuBar()

        import_shapefile = QAction('Import shapefile', self)
        import_shapefile.triggered.connect(self.import_shapefile)
        menu_bar.addAction(import_shapefile)

        import_lake_shapefile = QAction('Import Lake shapefile', self)
        import_lake_shapefile.triggered.connect(self.import_lake_shapefile)
        menu_bar.addAction(import_lake_shapefile)

        import_river_shapefile = QAction('Import River shapefile', self)
        import_river_shapefile.triggered.connect(self.import_river_shapefile)
        menu_bar.addAction(import_river_shapefile)

        import_points_shapefile = QAction('Import Points shapefile', self)
        import_points_shapefile.triggered.connect(self.import_points_shapefile)
        menu_bar.addAction(import_points_shapefile)

        self.view = View()
        self.view.setFocusPolicy(Qt.StrongFocus)
        self.view.aliasing = aliasing
        self.view.longitude = longitude

        self.view.lat=latitude
        self.view.lon=longitude
        self.view.cam_height = 20


        fov = fov/40
        self.view.frustL = - fov
        self.view.frustR = fov
        self.view.frustB = -fov
        self.view.frustT = fov

        print(self.view.LLH_to_ECEF(latitude, longitude, 20 , 1, False))
        self.view.x,self.view.y,self.view.z= self.view.LLH_to_ECEF(latitude, longitude, 20 , 1, False)
        self.view.cx=0
        self.view.cy=0
        self.view.cz=0
        self.view.upx = 0
        self.view.upy = 0
        self.view.upz = 1

        layout = QGridLayout(central_widget)
        layout.addWidget(self.view, 0, 0)

    def import_shapefile(self):
        self.view.shapefile = QFileDialog.getOpenFileName(self, 'Import')[0]
        self.view.create_polygons(0,250,0,1.00)
        self.update()
        
    def import_lake_shapefile(self):
        self.view.shapefile = QFileDialog.getOpenFileName(self, 'Import')[0]
        self.view.create_lake_polygons(0,0,250,1.001)
        self.update()

    def import_river_shapefile(self):
        self.view.shapefile = QFileDialog.getOpenFileName(self, 'Import')[0]
        self.view.create_river_polylines(0,0,250,1.001)
        self.update()

    def import_points_shapefile(self):
        self.view.shapefile = QFileDialog.getOpenFileName(self, 'Import')[0]
        self.view.create_points(0,0,0,1.005)
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PyEarth()
    window.setWindowTitle('pyEarth: a lightweight 3D visualization of the earth')
    window.setFixedSize(900, 900)
    window.show()
    sys.exit(app.exec_())    
