from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from minefield import MineField, Opener


class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        child = BoxLayout(orientation="horizontal", size_hint_y=0.1)
        self.vertical = True
        self.orientation = "vertical"
        fw = FieldWidget()
        clust0 = Button(text="Zero cluster")
        clust0.bind(on_press=fw.clust0)
        child.add_widget(clust0)
        child.add_widget(Button(text="baton 2"))
        child.add_widget(Button(text="baton 3"))
        self.add_widget(child)
        self.add_widget(fw)


class FieldWidget(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 10
        self.rows = 10
        self.__mined = MineField()
        minefield = Opener(self.__mined)
        self.btns = []
        for i in range(100):
            btn = FieldBtn(text="")
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

    def clust0(self, dummy):
        print(self.__mined.zero_clusters())
        zeros = self.__mined.max_zeros()
        print(zeros)
        print(dummy)
        self.change_btns([v + (0,) for v in zeros])


class FieldBtn(Button):

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
