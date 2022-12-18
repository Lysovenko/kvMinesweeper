from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from minefield import MineField


class RootWidget(GridLayout):

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.cols = 10
        self.rows = 10
        minefield = MineField()
        for i in range(100):
            btn = CustomBtn(text="?")
            btn.btn_r = i // 10
            btn.btn_c = i % 10
            btn.app_mf = minefield
            self.add_widget(btn)

    def btn_pressed(self, instance, pos):
        print('pos: printed from root widget: {pos}'.format(pos=pos))


class CustomBtn(Button):

    pressed = ListProperty([0, 0])
    calc_down = 3

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            v = self.app_mf.get(self.btn_r, self.btn_c)
            self.text = "Boom!" if v is None else str(v)
            self.calc_down -= 1
        return super().on_touch_down(touch)

    def on_pressed(self, instance, pos):
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
