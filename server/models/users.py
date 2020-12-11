import bcrypt
from config.db import getDb
import config.utils as utils
import yagmail as yag

class User:
    def __init__(self):
        
        self.register = False
        self.mydb = getDb()
        self.errors = []

    def Registrar(self, nombre, usuario, clave, cclave, ccorreo, correo):

        if not utils.isUsernameValid(usuario):
            self.errors.append("El usuario no es valido")

        if clave != cclave or not utils.isPasswordValid(clave):
            self.errors.append("Claves no coinciden o no son validas")

        if correo != ccorreo or not utils.isEmailValid(correo):
            self.errors.append("Correos electronicos no coinciden o son invalidos")

        
        cur = self.mydb.cursor()
        cur.execute("SELECT usuario FROM usuarios WHERE correo = '" + correo + "';")
        existEmail = cur.fetchall()
        if len(existEmail) >= 1:
            self.errors.append("Ya existe un usuario registrado con este correo electronico")
        
        cur.execute("SELECT usuario FROM usuarios WHERE usuario = '" + usuario + "';")
        existUser = cur.fetchall()
        if len(existUser) >= 1:
            self.errors.append("El usuario ya esta en uso")
        
        if len(self.errors) < 1:
            password = clave.encode(encoding='UTF-8',errors='strict')
            clave = bcrypt.hashpw(password, bcrypt.gensalt()).decode()
            cur.execute("INSERT INTO usuarios (nombre, usuario, contraseña, correo) VALUES ('%s', '%s', '%s', '%s');" % (nombre, usuario, clave, correo))
            self.mydb.commit()
            self.register = True
            
        self.mydb.close()
    
    def IniciarSesion(self, usuario, clave):
        cur = self.mydb.cursor()
        cur.execute("SELECT usuario FROM usuarios WHERE usuario = '" + usuario + "';")
        existUser = cur.fetchall()
        if len(existUser) >= 1:
            cur.execute("SELECT contraseña FROM usuarios WHERE usuario = '" + usuario + "';")
            password = cur.fetchall()
            trueClave = password[0][0]
            print(utils.comparePassword(clave, trueClave))
            
    def Activate(self, email, usuario):
        #Aqui debemos colocar la activacion del Usuario
        print("Activar Usuario")
