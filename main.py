from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy import platform
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, ReferenceListProperty
from kivy.uix.codeinput import CodeInput
from pygments.lexers import CythonLexer
from kivy.clock import Clock

import time
from duinobot import *
#from plyer import accelerometer

#~ if platform == 'android':
    #~ from plyer import orientation
    #~ orientation.set_sensor(mode='any')
#class AccelerometerTest(BoxLayout):
    #def __init__(self):
        #super(AccelerometerTest, self).__init__()


class DuinoSocks(FloatLayout):
    screen_manager = ObjectProperty(None)
    #~ velocidades = ObjectProperty(None)
    freq = ListProperty(map( str, range(300,900,100)))
    #~ tiempo = NumericProperty(0)
    tiempoFreq = ListProperty(map( str, range(2,60)))
    idRobot = ListProperty(map( str, range(20)))
    servo_ang_min = NumericProperty(0)
    servo_ang_max = NumericProperty(140)
    servo_range = ReferenceListProperty(servo_ang_min, servo_ang_max)
    textinput = ObjectProperty(20, 100)

    #~ def set_command(self, comando, *args):
        #~ self.ids.comando.text = '{}({})'.format(
            #~ comando,
            #~ ', '.join(map(str, args)),
        #~ )

    def __init__(self, *args, **kwargs):
        super(DuinoSocks, self).__init__(**kwargs)
        # self.icon = 'pin_1.png'
        self.title = 'Moviendo el robot'
        self.b = TCPBoard(debug=True)
        self.indent = ""
        self.tiempo = self.ids["tiemp"]
        self.velocidades = self.ids["velo"]


        self.sensorEnabled = False
        self.list_of_prev_screens = []

        self.vent1 = self.ids['botones']
        self.vent0 = self.ids['ventjuego'].children[0]

        self.botones = self.ids['botones']

        self.textinput = self.ids['textinput']
        self.textinput.lexer = CythonLexer()

        self.pila_accion = [""] #historico de acciones
        self.acciones = {"Sonar": self.sonar,
                         "Avanzar": self.avanzar,
                         "Retroceder": self.retroceder,
                         "Derecha": self.doblarizquierda,
                         "Izquierda": self.doblarderecha
                        }
        self.continue_f = True
        self.continue_w = True



    def iniciar(self, actual_screen, next_screen):

        try:
            self.r = Robot(self.b, int(self.ids.idR.text))
            if int(self.ids.idR.text) == 7:
                self.r.configServo(9)
                self.r.moveServo(9, 40)
            self.onNextScreen(actual_screen, next_screen)

            #if (self.ids['usuario'].text != ''):
                #self.onNextScreen(actual_screen, next_screen)
        except:
            self.ids['conectar'].text = 'Seleccionar un id'
            wait(2)
            self.ids['conectar'].text = 'Conectar'


    def sonar(self, frecuencia=300, tiempo=2):
		try:
			frecuencia = int(self.ids.frecuencia.text)
		except:
			frecuencia = 800
		#~ txt_pila = "\n"+self.indent+"r.beep("+str(self.ids["frecuencia"].text)+","+str(self.tiempo.value)+")"
		#~ txt = "\n"+self.indent+"robot.beep("+str(self.ids["frecuencia"].text)+","+str(self.tiempo.value)+")"
		txt_pila = "\n"+self.indent+"r.beep("+str(frecuencia)+","+str(self.tiempo.value)+")"
		txt = "\n"+self.indent+"robot.beep("+str(frecuencia)+","+str(self.tiempo.value)+")"
		self.pila_accion.append(txt_pila)
		self.textinput.text += txt
		#~ try:
			#~ frecuencia = int(self.ids.frecuencia.text)
		#~ except:
			#~ frecuencia = 800
		try:
			tiempo = float(self.tiempo.value)
		except:
			print('sin valor')
		#~ self.set_command('r.beep', frecuencia, tiempo)
		if self.continue_f and self.continue_w:
			self.r.beep(frecuencia, tiempo)

    def getText(self, movimiento):
		return "\n"+self.indent+movimiento+str(self.velocidades.value)+","+str(self.tiempo.value)+")"

    def avanzar(self, velocidad=50, localtiempo= 2):
		self.pila_accion.append(self.getText("r.forward("))
		self.textinput.text += self.getText("robot.forward(")
		try:
			velocidad = int(self.velocidades.value)
		except:
			pass
		try:
			localtiempo = float(self.tiempo.value)
		except:
			pass

		#~ self.set_command('r.forward', velocidad, localtiempo)
		if self.continue_w and self.continue_f:
			self.r.forward(velocidad,localtiempo)

    def doblarizquierda(self, velocidad=50, localtiempo= 2):
		self.pila_accion.append(self.getText("r.turnLeft("))
		self.textinput.text += self.getText("robot.turnLeft(")
		try:
			velocidad = int(self.velocidades.value)
		except:
			pass
		try:
			localtiempo = float(self.tiempo.value)
		except:
			print('sin valor')
		#~ self.set_command('r.turnLeft', velocidad, localtiempo)
		if self.continue_w and self.continue_f:
			self.r.turnLeft(velocidad,localtiempo)

    def doblarderecha(self,velocidad=50, localtiempo= 2):
		self.pila_accion.append(self.getText("r.turnRight("))
		self.textinput.text += self.getText("robot.turnRight(")
		try:
			velocidad = int(self.velocidades.value)
		except:
			pass
		try:
			localtiempo = float(self.tiempo.value)
		except:
			pass
		#~ self.set_command('r.turnRight', velocidad, localtiempo)
		if self.continue_w and self.continue_f:
			self.r.turnRight(velocidad, localtiempo)


    def retroceder(self, velocidad=50, localtiempo= 2):
		self.pila_accion.append(self.getText("r.backward("))
		self.textinput.text += self.getText("robot.backward(")
		try:
			velocidad = int(self.velocidades.value)
		except:
			pass
		try:
			localtiempo = float(self.tiempo.value)
		except:
			print('sin valor')
		#~ self.set_command('r.backward', velocidad, localtiempo)
		if self.continue_w and self.continue_f:
			self.r.backward(velocidad, localtiempo)

    def dump(self, obj):
        for attr in dir(obj):
            if attr != 'orientation':
                print "obj.%s = %s" % (attr, getattr(obj, attr))

    def mover_servo(self, pos):
		#~ self.set_command('r.moveServo', 9, pos)
		self.pila_accion.append("\n"+self.indent+"r.moveServo(9,"+str(int(pos))+")")
		self.pila_accion.append("wait(.2)")
		self.textinput.text += "\n"+self.indent+"robot.moveServo(9,"+str(int(pos))+")"
		if self.continue_f and self.continue_w:
			self.r.moveServo(9, int(pos))

    def parar(self):
        #~ self.set_command('r.stop')
        self.r.stop()

    def salir_for(self):
		self.indent = ""
		self.ids["btn_rep"].text = "Repetir"
		self.continue_f = True
		self.ids["rep_slide"].disabled = False
		self.ids["btn_rep"].disabled = False
		self.ids["btn_iter"].disabled = False

    def add_for(self):#, val):#, slid, val):
		if self.ids["btn_rep"].text == "Repetir":
			#~ self.textinput.padding_x = 30
			self.pila_accion.append("\nfor i in range("+str(int(self.ids["rep_slide"].value))+"):")
			self.textinput.text += "\nfor i in range("+str(int(self.ids["rep_slide"].value))+"):"
			self.indent = "    "
			self.ids["btn_rep"].text = "Detener repetir"
			self.iter_id = len(self.pila_accion) #donde comenzar la repeticion de los comandos
			self.continue_f = False
			self.ids["rep_slide"].disabled = True
			self.ids["btn_iter"].disabled = True
		else:
			self.ids["btn_rep"].disabled = True
			for i in range(int(self.ids["rep_slide"].value)):
				for e in range(self.iter_id,len(self.pila_accion)-1):
					command = "self."+self.pila_accion[e][2:]
					try:
						eval(command)
					except:
						eval(self.pila_accion[e])
			else:
				self.salir_for()

    def salir_while(self):
		self.continue_w = True
		self.indent = ""
		self.ids["btn_iter"].text = "Mientras no hay obstaculo"
		self.ids["btn_iter"].disabled = False
		self.ids["btn_rep"].disabled = False

    def add_while(self):
		if self.ids["btn_iter"].text != "Detener iteracion":
			self.iter_idw = len(self.pila_accion) #donde comenzar la repeticion de los comandos
			self.pila_accion.append("\nwhile (not r.getObstacle(30)):")
			self.textinput.text += "\nwhile (not robot.getObstacle(30)):"
			self.indent = "    "
			self.ids["btn_iter"].text = "Detener iteracion"
			self.continue_w = False
			self.ids["btn_rep"].disabled = True
		else:
			self.ids["btn_iter"].disabled = True
			while (not self.r.getObstacle()):
				#~ eval(self.pila_accion[self.iter_idw])
				for e in range(self.iter_idw+2,len(self.pila_accion)-1):
					command = "self."+self.pila_accion[e][2:]
					try:
						eval(command)
					except:
						eval(self.pila_accion[e])
			else:
				self.salir_while()


    def descontar(self, cant, ultimo):
		self.textinput.text = self.textinput.text[:-(len(ultimo)+cant)]

    def deshacer(self):#, event):
		if len(self.pila_accion) > 0:
			ultimo = self.pila_accion.pop(-1)

			if ultimo == "wait(.2)":
				ultimo = self.pila_accion.pop(-1)
				self.descontar(4, ultimo)
			elif ultimo[:4] == "\nfor":
				self.descontar(0, ultimo)
				self.salir_for()
			elif ultimo[:6] == "\nwhile":
				self.descontar(4, ultimo)
				self.salir_while()
			else:
				self.descontar(4, ultimo)
		else:
			self.pila_accion.append("")

    def exportar(self, *event):
		arch = open("programaRobot.py", "w")
		arch.write("from duinobot import *\nb = Board()\nrobot = Robot(b,3)")
		arch.write(self.textinput.text)
		arch.close()
    # --------------------------------------------------------------------------
    def onNextScreen(self, actual_screen, next_screen):
        # add screen we were just in
        self.list_of_prev_screens.append(actual_screen.name)
        # Go to next screen
        self.screen_manager.current = next_screen

    def onBackBtn(self):
        # Check if there are any screens to go back to
        if self.list_of_prev_screens:
            # If there are then just go back to it
            self.screen_manager.current = self.list_of_prev_screens.pop()
            # We don't want to close app
            return True
        # No more screens so user must want to exit app
        return False


class Error(FloatLayout):
#~ #~
	def __init__(self, *args, **kwargs):
		super(Error, self).__init__(**kwargs)
		self.l = Label(text="Conectandose al robot.")
		self.add_widget(self.l)
		#~ time.sleep(1)
		#~ self.connect()
		Clock.schedule_once(self.connect, 1)
#~ #~
	def connect(self, *event):
		d = None
		once = True
		while not d:
			try:
				d = DuinoSocks()
			except:
				time.sleep(.2)
				#~ if once:
					#~ once = False
					#~ self.l.text = "No se pudo conectar al robot.\n Reintentando."
					#~ self.l.texture_update()
		self.remove_widget(self.l)
		self.add_widget(d)

################################################################################
class DuinobotApp(App):
    """ App to show how to use back button """

    def __init__(self, *args, **kwargs):
        super(DuinobotApp, self).__init__(*args, **kwargs)
        #Window.bind(on_keyboard=self.onBackBtn)


    # --------------------------------------------------------------------------
    def build(self):
		return Error()

    def onBackBtn(self, window, key, *args):
        """ To be called whenever user presses Back/Esc Key """
        # If user presses Back/Esc Key
        if key == 27:
            return self.root.onBackBtn()
        return False

    def on_pause(self):
		return True

    def on_resume(self):
		pass



if __name__ == "__main__":
    d = DuinobotApp().run()
    #~ d.e.connect()
