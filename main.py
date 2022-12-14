from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
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
        switch_mode = Button(text="Open")
        switch_mode.bind(on_press=fw.switch_mode)
        child.add_widget(switch_mode)
        for name in ("Beginner", "Intermediate", "Expert"):
            modifier = Button(text=name)
            modifier.bind(on_press=fw.change_profile)
            child.add_widget(modifier)
        self.add_widget(child)
        self.add_widget(fw)


class FieldWidget(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__open_mode = True
        self._change_profile("Beginner")

    def change_btns(self, btns):
        for r, c, v in btns:
            p = r * self.cols + c
            try:
                self.btns[p].set_digit(v)
            except IndexError:
                pass

    def clust0(self, dummy):
        zeros = list(self.__mined.max_zeros())
        if zeros:
            self.btns[zeros[0][0] * self.cols + zeros[0][1]].pick()

    def reset(self, _btn):
        self.__mined = MineField(*self.__profile)
        self.minefield = Opener(self.__mined)
        for b in self.btns:
            b.reset()

    def switch_mode(self, btn):
        self.__open_mode = not self.__open_mode
        btn.text = "Open" if self.__open_mode else "Mark"

    @property
    def open_mode(self):
        return self.__open_mode

    def change_profile(self, btn):
        self._change_profile(btn.text)

    def _change_profile(self, text):
        profiles = {"Beginner": (10, 10, 10),
                    "Intermediate": (16, 16, 40),
                    "Expert": (16, 30, 99)}
        profile = profiles.get(text, (10, 10, 10))
        self.__profile = profile
        self.__mined = MineField(*profile)
        self.minefield = Opener(self.__mined)
        self.btns = []
        self.clear_widgets()
        rows, cols, m = profile
        self.cols = cols
        self.rows = rows
        for i in range(rows * cols):
            btn = CellBtn(self)
            btn.btn_r = i // cols
            btn.btn_c = i % cols
            self.add_widget(btn)
            self.btns.append(btn)

    def cards_on_the_table(self):
        for r, c, player, game in self.minefield.comparison():
            p = r * self.cols + c
            try:
                self.btns[p].compare(player, game)
            except IndexError:
                pass


class CellBtn(Button):
    __colors = {0: "ADFF2F", 1: "0000FF", 2: "EE82EE",
                3: "FF0000", 4: "FF00FF", 5: "FF6600",
                6: "1E90FF", 7: "00FFFF", 8: "DC143C"}

    def __init__(self, parent, **kwargs):
        kwargs.update({"text": "", "valign": "middle", "halign": "center",
                       "markup": True})
        self.__parent = parent
        self.__inactive = False
        super().__init__(**kwargs)
        self.__bg = self.background_color

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.__inactive:
                return
            if self.__parent.open_mode:
                self.pick()
            else:
                self.mark()
        return super().on_touch_down(touch)

    def pick(self):
        v = self.__parent.minefield.pick(self.btn_r, self.btn_c)
        if v is None:
            self._game_over("Loss", "You lost!")
        else:
            self.set_digit(v)
        if v == 0:
            neibs = self.__parent.minefield.around_zeros()
            self.__parent.change_btns(neibs)
        if self.__parent.minefield.is_clear():
            self._game_over("Congratulations", "You won!!!")

    def _game_over(self, title, message):
        b = Button(text=message)
        p = Popup(title=title, content=b, size_hint=(.5, .5))
        b.bind(on_press=p.dismiss)
        b.font_size = b.font_size * 3
        p.open()
        self.__parent.cards_on_the_table()

    def mark(self):
        if self.__parent.minefield.user_mark(self.btn_r, self.btn_c):
            self.text = "M"
        else:
            self.text = ""

    def set_digit(self, digit):
        self.__inactive = True
        self.text = "[color=%s][b]%d[/b][/color]" % (
            self.__colors.get(digit, "000000"), digit)
        self.background_color = (1, 1, 1, .8)
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, .9, .9)
            Rectangle(size=self.size, pos=self.pos)

    def compare(self, player, game):
        self.__inactive = True
        if game is None:
            self.text = "*"
            if player == "B":
                self.background_color = (1, 0, 0, 1)
        elif isinstance(game, int):
            self.set_digit(game)
            if player is not None:
                self.background_color = (1, 0.5, 0.5, 1)

    def on_size(self, btn, sz):
        self.font_size = min(sz)
        if self.__inactive:
            self.canvas.before.clear()
            with self.canvas.before:
                Color(1, 1, .9, .9)
                Rectangle(size=self.size, pos=self.pos)

    def reset(self):
        self.text = ""
        self.__inactive = False
        self.canvas.before.clear()
        self.background_color = self.__bg


class MinesweeperApp(App):
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MinesweeperApp().run()
