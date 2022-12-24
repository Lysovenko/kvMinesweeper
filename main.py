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
        reset = Button(text="Reset")
        reset.bind(on_press=fw.reset)
        child.add_widget(clust0)
        child.add_widget(reset)
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
        zeros = list(self.__mined.max_zeros())
        if zeros:
            self.btns[zeros[0][0] * self.cols + zeros[0][1]].pick()
        
    def reset(self, _btn):
        self.__mined = MineField()
        minefield = Opener(self.__mined)
        for b in self.btns:
            b.text = ""
            b.app_mf = minefield


class FieldBtn(Button):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pick()
        return super().on_touch_down(touch)

    def pick(self):
        v = self.app_mf.pick(self.btn_r, self.btn_c)
        self.text = "Boom!" if v is None else str(v)
        if v == 0:
            neibs = self.app_mf.around_zeros()
            self.change_neibs(neibs)


class MinesweeperApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MinesweeperApp().run()
