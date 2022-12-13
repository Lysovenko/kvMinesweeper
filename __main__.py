from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty

class RootWidget(GridLayout):

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.cols = 10
        self.rows = 10
        self.add_widget(Button(text='btn 1'))
        cb = CustomBtn(text="X")
        cb.bind(pressed=self.btn_pressed)
        self.add_widget(cb)
        self.add_widget(Button(text='btn 2'))
        for i in range(97):
            self.add_widget(CustomBtn(text=str(i)))

    def btn_pressed(self, instance, pos):
        print('pos: printed from root widget: {pos}'.format(pos=pos))

class CustomBtn(Button):

    pressed = ListProperty([0, 0])
    calc_down = 3
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            self.text = str(int(touch.pos[0]))
            self.calc_down -= 1
        return super().on_touch_down(touch)

    def on_pressed(self, instance, pos):
        print('pressed at {pos}'.format(pos=pos))
        if self.calc_down <= 0:
            print("Remove myself")
            print(self.get_root_window())
            print(self.get_parent_window())
            self.get_root_window().remove_widget(self)

class MinesweeperApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MinesweeperApp().run()
