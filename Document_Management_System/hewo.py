import cherrypy
import codecs
import os,time
import sys
import os.path
from cherrypy.lib import static
from stat import *
import re
import shutil
import json
import datetime

from tempfile import mkstemp
from os import fdopen, remove



def headers():
    file = codecs.open(os.path.dirname(__file__) +"/header.html")
    return file.read()



def listFolder():

    lstDir = os.listdir(os.path.dirname(__file__) +"/resources/Files")

    memoria=""
    protocolo=""
    buttons=""
    for  directorio in lstDir:
        path, dirs, files = next(os.walk(os.path.dirname(__file__) +"/resources/Files/"+directorio+"/others"))
        count = len(files)
        with open(os.path.dirname(__file__)+"/resources/Files/"+directorio+"/info.txt","r") as infoFile:
            info = json.load(infoFile)

        memoria = info['MEMORIA_CURRENT_VERSION']
        protocolo = info['PROTOCOLO_CURRENT_VERSION']
        memname, memextension = os.path.splitext(memoria)
        memextension = memextension.replace(".", "")
        if "docx" in memextension:
            memextension = "word"
 
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
                                        <input type="hidden"  name="name" value="""+ directorio +"""/memoria/>
                                        <input type="hidden"  name="documento" value="""+ memoria +""">
                                        <button type="submit" class="btn btn-primary btn-sm">
                                            <i class="fa fa-file-"""+memextension+"""-o"></i>
                                        </button>
                                    </form>
                                </td>
                                <td>

                                        <form method="get" action="download">
                                            <input type="hidden"  name="name" value="""+ directorio +"""/protocolo/>
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
                                                <h6 style="font-size: .80em;">("""+str(count)+""")</h6>
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

    with open(os.path.dirname(__file__)+"/resources/Files/"+name+"/info.txt","r") as infoFile:
            info = json.load(infoFile)
            
    paths=[[info['MEMORIA_PATH']+"/"+info['MEMORIA_CURRENT_VERSION'],'memoria',info['MEMORIA_CURRENT_VERSION_DATE']],[info['PROTOCOLO_PATH']+"/"+info['PROTOCOLO_CURRENT_VERSION'],'protocolo',info['PROTOCOLO_CURRENT_VERSION_DATE']]]
    entries = ""
    for fichero in paths:
        filename = fichero[0].split("/")[1]
        st = os.stat(os.path.dirname(__file__) +"/resources/Files/"+name+"/"+fichero[0])
        entries += """<br><br> 
                    <div class="card">
                        <div class="card-body">
                            <div class="row">       
                                <div class="col-sm-4" >
                                    <h4 class="card-title">"""+ filename +"""</h4>
                                    <p class="card-text">
                                        Tamano: """+str(st[ST_SIZE])+""" Bytes<br>
                                        Fecha Creacion: """+ str(time.asctime(time.localtime(st[ST_CTIME])))+"""<br>
                                        Fecha Modificacion: """+str(time.asctime(time.localtime(st[ST_MTIME])))+"""<br>
                                        Fecha de Subida: """+fichero[2]+"""
                                    </p>
                                </div>

                                <div class="col-sm-1">
                                <form method="get" action="showPDF">
                                    <button type="submit" class="btn btn-primary btn-sm">
                                        <i class="material-icons">description</i>
                                        <input type="hidden"  name="directory" value="""+ name +""">
                                        <input type="hidden"  name="name" value="""+ fichero[0] +""">
                                    </button>
                                </form>
                                </div>
                                <div class="col-sm-1">
                                <form method="get" action="uploadIndex">
                                    <button type="submit" class="btn btn-success btn-sm">
                                        <i class="material-icons">cloud_upload</i>
                                        <input type="hidden"  name="directorio" value="""+ name +""">
                                        <input type="hidden"  name="fichero" value="""+ fichero[0] +""">
                                        <input type="hidden"  name="tipo" value="""+ fichero[1] +""">

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
    lstDir = os.walk(os.path.dirname(__file__) +"/resources/Files/"+name+"/others")
    for  root, dirs, files in lstDir:
        for file in files:    
            code += """<li class="list-group-item"> 
                        <div class="row">
                            <div class="col-sm-4">"""+file+"""</div>
                            <div class="col-sm-1">
                                <form method="get" action="download">
                                    <input type="hidden"  name="name" value="""+ name +"""/others>
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

        localDir = os.path.dirname(__file__) +"/resources/Files/"+name
        absDir = os.path.join(os.getcwd(), localDir)
        path = os.path.join(absDir, documento)
        return static.serve_file(path, 'application/x-download', 'attachment', os.path.basename(path))

    @cherrypy.expose
    def remove(self, name, documento): 

        localDir = os.path.dirname(__file__) +"/resources/Files/"+name+"/others"
        absDir = os.path.join(os.getcwd(), localDir)
        path = os.path.join(absDir, documento)
        os.remove(path)
        raise cherrypy.HTTPRedirect("/details?name="+name)
    
    @cherrypy.expose
    def uploadIndex(self, directorio,fichero,tipo):
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
                    <input type="hidden"  name="tipo" value="""+ tipo +""">
                </form>
            </div>
        </body>
        """
    
    @cherrypy.expose
    def upload(self,myFile,directory,prevFile,tipo):


        with open(os.path.dirname(__file__)+"/resources/Files/"+directory+"/info.txt","r") as infoFile:
            info = json.load(infoFile)

        prevFilename = prevFile.split("/")[1]
        prevPath = prevFile.split("/")[0]


        localDir = os.path.dirname(__file__) +"/resources/Files/"+directory+"/"+prevPath+"/"
        absDir = os.path.join(os.getcwd(), localDir)
         
        pathOldVersion = os.path.join(absDir, prevFilename)
        pathNewVersion= os.path.join(absDir, myFile.filename)

        localVers = os.path.dirname(__file__) +"/resources/Files/"+directory+"/"+prevPath+"/versions/"
        absDirVers = os.path.join(os.getcwd(), localVers)  
        pathVersions = os.path.join(absDirVers, prevFilename)

        now = datetime.datetime.now()
        if(tipo=="memoria"):
            info['MEMORIA_CURRENT_VERSION']=myFile.filename
            oldDate = info['MEMORIA_CURRENT_VERSION_DATE']
            info['MEMORIA_CURRENT_VERSION_DATE']=now.strftime("%Y-%m-%d %H:%M")
            info['MEMORIA_VERSIONS'].append({"NAME":prevFilename,"DATE":oldDate})
        else:
            if(tipo=="protocolo"):
                info['PROTOCOLO_CURRENT_VERSION']=myFile.filename
                oldDate = info['PROTOCOLO_CURRENT_VERSION_DATE']
                info['PROTOCOLO_CURRENT_VERSION_DATE']=now.strftime("%Y-%m-%d %H:%M")
                info['PROTOCOLO_VERSIONS'].append({"NAME":prevFilename,"DATE":oldDate})

        with open(os.path.dirname(__file__)+"/resources/Files/"+directory+"/info.txt", "w") as jsonFile:
            json.dump(info, jsonFile)

        shutil.move(pathOldVersion,pathVersions)




        datos = myFile.file.read()
        fichero =file(pathNewVersion, "wb")
        fichero.write(datos)
        fichero.close

        
        #return "Path version anterior:" +pathOldVersion +"<br>Path nueva version:"+pathNewVersion+"<br>path versiones:"+pathVersions
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
        localDir = os.path.dirname(__file__) +"/resources/Files/"+directorio+"/others/"
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
        'tools.staticdir.dir': './resources'
        },
    
    }
    cherrypy.quickstart(WebServer(),'/', conf)