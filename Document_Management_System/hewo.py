import cherrypy
import codecs
import os,time
import sys
import os.path
from cherrypy.lib import static
from stat import *


def headers():
    file = codecs.open(os.path.dirname(__file__) +"/header.html")
    return file.read()

def listFolder():

    lstDir = os.walk(os.path.dirname(__file__) +"/resources/Files")
    buttons = ""
    memoria=""
    protocolo=""

    for  root, dirs, files in lstDir:
       for directorio in dirs:
            cont = -2
            lstFil = os.walk(os.path.dirname(__file__) +"/resources/Files/"+directorio)
            for root, dirs, files in lstFil:
                for fichero in files:
                    cont += 1
                    if "Memoria" in fichero:
                        memoria = fichero
                        memname, memextension = os.path.splitext(memoria)
                        memextension = memextension.replace(".", "")
                        if "docx" in memextension:
                            memextension = "word"
                    else:
                        if "Protocolo" in fichero:
                            protocolo = fichero
                            protname, protextension = os.path.splitext(protocolo)
                            protextension = protextension.replace(".", "")
                            if "docx" in protextension:
                                protextension = "word"
                            
            buttons = buttons + """ 
                                    <tr>
                                   
                                        <td>
                                            <h5>"""+ directorio +"""</h5>
                                        </td>
                                        <td>
                                                <form method="get" action="download">
                                                    <input type="hidden"  name="name" value="""+ directorio +""">
                                                    <input type="hidden"  name="documento" value="""+ memoria +""">
                                                    <button type="submit" class="btn btn-primary btn-sm">
                                                        <i class="fa fa-file-"""+memextension+"""-o"></i>
                                                    </button>
                                                </form>
                                        </td>
                                        <td>

                                                <form method="get" action="download">
                                                    <input type="hidden"  name="name" value="""+ directorio +""">
                                                    <input type="hidden"  name="documento" value="""+ protocolo +""">
                                                    <button type="submit" class="btn btn-success btn-sm">
                                                        <i class="fa fa-file-"""+protextension+"""-o"></i>
                                                   </button>
                                                </form>
                                        </td>
                                        <td>
                                                <form method="get" action="details">
                                                    <input type="hidden"  name="name" value="""+ directorio +""">
                                                    <button type="submit" class="btn btn-info btn-sm">
                                                        <h6 style="font-size: .80em;">("""+str(cont)+""")</h6>
                                                    </button>
                                                </form>
                                        </td>
                                        <td>
                                                <form method="get" action="details">
                                                    <input type="hidden"  name="name" value="""+ directorio +""">
                                                     <button type="submit" class="btn btn-danger btn-sm">
                                                        <i class="fa fa-gear"></i>
                                                   </button>
                                                </form>
                                        </td>
                                    </tr>
                                """
    return buttons


def listFiles(name):

    lstDir = os.walk(os.path.dirname(__file__) +"/resources/Files/"+name)
    entries = ""
    for  root, dirs, files in lstDir:
        for file in files:    
            if "Memoria" in file or "Protocolo" in file:
                st = os.stat(os.path.dirname(__file__) +"/resources/Files/"+name+"/"+file)
                entries += """<br><br> 
                            <div class="card">
                                <div class="card-body">
                                    <div class="row">       
                                        <div class="col-sm-4" >
                                            <h4 class="card-title">"""+ file +"""</h4>
                                            <p class="card-text">
                                                Tamano: """+str(st[ST_SIZE])+""" Bytes<br>
                                                Fecha Creacion: """+ str(time.asctime(time.localtime(st[ST_CTIME])))+"""<br>
                                                Fecha Modificacion: """+str(time.asctime(time.localtime(st[ST_MTIME])))+"""
                                            </p>
                                        </div>

                                        <div class="col-sm-1">
                                        <form method="get" action="showPDF">
                                            <button type="submit" class="btn btn-primary btn-sm">
                                                <i class="material-icons">description</i>
                                                <input type="hidden"  name="directory" value="""+ name +""">
                                                <input type="hidden"  name="name" value="""+ file +""">
                                            </button>
                                        </form>
                                        </div>
                                        <div class="col-sm-1">
                                        <form method="get" action="uploadIndex">
                                            <button type="submit" class="btn btn-success btn-sm">
                                                <i class="material-icons">cloud_upload</i>
                                                <input type="hidden"  name="directorio" value="""+ name +""">
                                                <input type="hidden"  name="fichero" value="""+ file +""">

                                            </button>
                                        </form>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            """
    
    return entries


def listOthers(name):
    code = """<br><br>
                <div class="row">
                    <div class="col-sm-4">
                        <h2>Otros Documentos<h2>
                    </div>
                    <div class="col-sm-4">
                    <form method="get" action="addDoc">
                        <button type="submit" class="btn btn-primary btn-sm">
                            add
                        </button>
                        <input type="hidden" name="directorio" value="""+name+""">
                    </form>
                    </div>
                </div><br><br>
                <ul class="list-group list-group-flush">"""
    lstDir = os.walk(os.path.dirname(__file__) +"/resources/Files/"+name)
    for  root, dirs, files in lstDir:
        for file in files:    
            if "Memoria" in file or "Protocolo"in file:
                print(file)
            else:
                code += """<li class="list-group-item"> 
                            <div class="row">
                                <div class="col-sm-4">"""+file+"""</div>
                                <div class="col-sm-1">
                                    <form method="get" action="download">
                                        <input type="hidden"  name="name" value="""+ name +""">
                                        <input type="hidden"  name="documento" value="""+ file +""">
                                        <button type="submit" class="btn btn-primary btn-sm">
                                            <i class="fa fa-download" aria-hidden="true"></i>
                                        </button>
                                    </form>
                                </div>
                                <div class="col-sm-1">
                                    <form method="get" action="remove">
                                        <input type="hidden"  name="name" value="""+ name +""">
                                        <input type="hidden"  name="documento" value="""+ file +""">
                                        <button type="submit" class="btn btn-danger btn-sm">
                                            <i class="fa fa-remove"></i>
                                        </button>
                                    </form>
                                </div>
                            </li>"""
    code += "</ul>"
    return code



class WebServer(object):

    @cherrypy.expose
    def index(self): 
        head = headers()
        html = listFolder()
        return head + """<body>
                            <div class="container">
                                <img align="right" src="http://www.baitic.com/wp-content/uploads/2013/05/cropped-logo_trazado1.png"/>
		                        </br></br>                            
                                <h1>Sistema de Gestion Documental<h1>

                                <table class="table">
                                    <thead>
                                        <tr>
                                            <td><h5>Nombre Instalacion</h5></td>
                                            <td><h5>Memoria</h5></td>
                                            <td><h5>Protocolo</h5></td>
                                            <td><h5>Otros</h5></td>
                                            <td><h5>Detalles</h5></td>
                                        </tr>
                                    </thead>
                                    <tbody>""" + html +"""</tbody>
                                </div>
                        </body>"""
    
    @cherrypy.expose
    def details(self, name): 
        head = headers()
        html = listFiles(name)
        others = listOthers(name)
        return head+"""
                    <body>

                        <div class="container"><br><br>
                            <form method="get" action="index">
                                <span class="float-right">
                                    <button type="submit" class="btn btn-outline-primary">
                                        Pagina Principal
                                    </button>
                                </span>
                            </form>
                            <h1>"""+name+"""</h1>
                            """+html+others+"""
                        </div>
                    </body>"""
    
    @cherrypy.expose
    def download(self, name, documento): 

        localDir = os.path.dirname(__file__) +"/resources/Files/"+name+"/"
        absDir = os.path.join(os.getcwd(), localDir)
        path = os.path.join(absDir, documento)
        return static.serve_file(path, 'application/x-download', 'attachment', os.path.basename(path))

    @cherrypy.expose
    def remove(self, name, documento): 

        localDir = os.path.dirname(__file__) +"/resources/Files/"+name+"/"
        absDir = os.path.join(os.getcwd(), localDir)
        path = os.path.join(absDir, documento)
        os.remove(path)
        raise cherrypy.HTTPRedirect("/details?name="+name)
    
    @cherrypy.expose
    def uploadIndex(self, directorio,fichero):
        head = headers()
        return head+"""
        <body>
            <div class="container"><br><br>
                <h2>Upload a file</h2>
                <form action="upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="myFile" /><br><br>
                    <input type="submit" />
                    <input type="hidden"  name="directory" value="""+ directorio +""">
                    <input type="hidden"  name="prevFile" value="""+ fichero +""">
                </form>
            </div>
        </body>
        """
    
    @cherrypy.expose
    def upload(self,myFile,directory,prevFile):

        (filename, nothing) = os.path.splitext(prevFile)
        (notValid, extension) =  os.path.splitext(myFile.filename)

        localDir = os.path.dirname(__file__) +"/resources/Files/"+directory+"/"
        absDir = os.path.join(os.getcwd(), localDir)

        pathRemove = os.path.join(absDir, prevFile)
        pathWrite = os.path.join(absDir, filename+extension)

        os.remove(pathRemove)

        datos = myFile.file.read()

        fichero =file(pathWrite, "wb")
        fichero.write(datos)
        fichero.close

        raise cherrypy.HTTPRedirect("/details?name="+directory)
 
    @cherrypy.expose
    def showPDF(self, name, directory):
        src = "/static/Files/"+directory+"/"+name
        head = headers()
        html = """
                <body>
                    <iframe style="position:fixed; top:0; left:0; bottom:0; right:0; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden;" src="""+src+""" type="application/pdf"></iframe>
                </body>
                """
        return head + html

    @cherrypy.expose
    def addDoc(self,directorio):
        head = headers()
        return head+"""
        <body>
            <div class="container"><br><br>
                <h2>Upload a file</h2>
                <form action="uploadDoc" method="post" enctype="multipart/form-data">
                    <input type="file" name="myFile" /><br><br>
                    <input type="submit" />
                    <input type="hidden"  name="directorio" value="""+ directorio +""">
                </form>
            </div>
        </body>
        """

    @cherrypy.expose
    def uploadDoc(self,directorio,myFile):
        localDir = os.path.dirname(__file__) +"/resources/Files/"+directorio+"/"
        absDir = os.path.join(os.getcwd(), localDir)
        path = os.path.join(absDir, myFile.filename)
        datos = myFile.file.read()

        fichero =file(path, "wb")
        fichero.write(datos)
        fichero.close

        raise cherrypy.HTTPRedirect("/details?name="+directorio)



if __name__ == '__main__':
    conf = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './Document_Management_System/resources'
        },
    
    }
    cherrypy.quickstart(WebServer(),'/', conf)