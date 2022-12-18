from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from minefield import MineField, Opener


class RootWidget(GridLayout):

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.cols = 10
        self.rows = 10
        minefield = Opener(MineField())
        self.btns = []
        for i in range(100):
            btn = CustomBtn(text="")
            btn.btn_r = i // 10
            btn.btn_c = i % 10
            btn.app_mf = minefield
            btn.change_neibs = self.change_btns
            self.add_widget(btn)
            self.btns.append(btn)

    def change_btns(self, btns):
        for r, c, v in btns:
            p = r * self.cols + c
            try:
                self.btns[p].text = str(v)
            except IndexError:
                pass


class CustomBtn(Button):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            v = self.app_mf.pick(self.btn_r, self.btn_c)
            self.text = "Boom!" if v is None else str(v)
            if v == 0:
                neibs = self.app_mf.around_zeros()
                self.change_neibs(neibs)
        return super().on_touch_down(touch)


class MinesweeperApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MinesweeperApp().run()
