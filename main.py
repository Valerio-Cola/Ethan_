from kivymd.app import MDApp
from kivy.lang import Builder


KV = """
Screen:

    MDRectangleFlatButton:
        text: "Buongiornissimo"
        pos_hint: {"center_x" : 0.5, "center_y" : 0.5}
"""
class MainApp(MDApp):
    def build(self):
        self.title = "Buongiornissimo"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)


MainApp().run()