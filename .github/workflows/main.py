from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup


class SmartDemoApp(App):

    def build(self):
        self.title = "BORHAN DARK"

        self.balance = 10000
        self.trade_amount = 100
        self.total_trades = 0
        self.wins = 0
        self.losses = 0

        main = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        title = Label(
            text="BORHAN DARK",
            font_size=28,
            bold=True,
            size_hint_y=None,
            height=55
        )
        main.add_widget(title)

        self.balance_label = Label(
            text=f"Demo Balance: {self.balance}",
            font_size=20,
            size_hint_y=None,
            height=40
        )
        main.add_widget(self.balance_label)

        self.price_input = TextInput(
            hint_text="Enter prices: 100 102 104 106...",
            multiline=False,
            size_hint_y=None,
            height=50
        )
        main.add_widget(self.price_input)

        analyze = Button(
            text="ANALYZE",
            size_hint_y=None,
            height=50
        )
        analyze.bind(on_press=self.analyze)
        main.add_widget(analyze)

        self.signal_label = Label(
            text="Signal: WAIT",
            font_size=22,
            size_hint_y=None,
            height=45
        )
        main.add_widget(self.signal_label)

        trade = Button(
            text="VIRTUAL TRADE",
            size_hint_y=None,
            height=50
        )
        trade.bind(on_press=self.virtual_trade)
        main.add_widget(trade)

        history = Button(
            text="TRADE HISTORY",
            size_hint_y=None,
            height=50
        )
        history.bind(on_press=self.show_history)
        main.add_widget(history)

        statistics = Button(
            text="STATISTICS",
            size_hint_y=None,
            height=50
        )
        statistics.bind(on_press=self.show_statistics)
        main.add_widget(statistics)

        settings = Button(
            text="SETTINGS",
            size_hint_y=None,
            height=50
        )
        settings.bind(on_press=self.show_settings)
        main.add_widget(settings)

        reset = Button(
            text="RESET DEMO",
            size_hint_y=None,
            height=50
        )
        reset.bind(on_press=self.reset_demo)
        main.add_widget(reset)

        self.result = Label(
            text="Enter prices and press ANALYZE",
            font_size=16
        )
        main.add_widget(self.result)

        warning = Label(
            text="DEMO / VIRTUAL BALANCE ONLY",
            font_size=14,
            size_hint_y=None,
            height=35
        )
        main.add_widget(warning)

        return main

    def analyze(self, instance):
        try:
            prices = [
                float(x)
                for x in self.price_input.text.split()
            ]

            if len(prices) < 3:
                self.result.text = "Please enter at least 3 prices."
                return

            current = prices[-1]

            if prices[-1] > prices[0]:
                trend = "UP"
            elif prices[-1] < prices[0]:
                trend = "DOWN"
            else:
                trend = "SIDEWAYS"

            if prices[-1] > prices[-2]:
                recent = "UP"
            elif prices[-1] < prices[-2]:
                recent = "DOWN"
            else:
                recent = "FLAT"

            momentum = prices[-1] - prices[-3]

            if momentum > 0:
                signal = "UP"
            elif momentum < 0:
                signal = "DOWN"
            else:
                signal = "WAIT"

            self.signal_label.text = f"Signal: {signal}"

            self.result.text = (
                f"Current Price: {current}\n"
                f"Overall Trend: {trend}\n"
                f"Recent Trend: {recent}\n"
                f"Momentum: {momentum:.2f}\n\n"
                f"DEMO SIGNAL: {signal}"
            )

        except:
            self.result.text = "Invalid price input."

    def virtual_trade(self, instance):
        signal = self.signal_label.text.replace("Signal: ", "")

        if signal == "WAIT":
            self.result.text = "WAIT signal — no virtual trade."
            return

        if self.balance < self.trade_amount:
            self.result.text = "Demo balance is too low."
            return

        self.total_trades += 1
        self.balance -= self.trade_amount

        if signal == "UP":
            self.wins += 1
            self.balance += self.trade_amount * 1.8
            result = "DEMO WIN"
        else:
            self.losses += 1
            result = "DEMO LOSS"

        self.balance_label.text = f"Demo Balance: {self.balance:.2f}"

        self.result.text = (
            f"{result}\n\n"
            f"Virtual Trade Amount: {self.trade_amount}\n"
            f"Demo Balance: {self.balance:.2f}\n\n"
            f"REMINDER: DEMO ONLY"
        )

    def show_history(self, instance):
        self.result.text = (
            "TRADE HISTORY\n\n"
            f"Total Virtual Trades: {self.total_trades}\n"
            f"Wins: {self.wins}\n"
            f"Losses: {self.losses}"
        )

    def show_statistics(self, instance):
        if self.total_trades == 0:
            win_rate = 0
        else:
            win_rate = (self.wins / self.total_trades) * 100

        self.result.text = (
            "STATISTICS\n\n"
            f"Total Trades: {self.total_trades}\n"
            f"Wins: {self.wins}\n"
            f"Losses: {self.losses}\n"
            f"Demo Win Rate: {win_rate:.1f}%\n\n"
            "This is only a simulated demo."
        )

    def show_settings(self, instance):
        content = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        amount_input = TextInput(
            text=str(self.trade_amount),
            hint_text="Virtual trade amount",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=50
        )

        save = Button(
            text="SAVE",
            size_hint_y=None,
            height=50
        )

        close = Button(
            text="CLOSE",
            size_hint_y=None,
            height=50
        )

        content.add_widget(
            Label(
                text="BORHAN DARK SETTINGS",
                font_size=20
            )
        )

        content.add_widget(
            Label(
                text="Virtual Trade Amount"
            )
        )

        content.add_widget(amount_input)
        content.add_widget(save)
        content.add_widget(close)

        popup = Popup(
            title="SETTINGS — DEMO",
            content=content,
            size_hint=(0.9, 0.6)
        )

        def save_settings(instance):
            try:
                amount = float(amount_input.text)

                if amount <= 0:
                    return

                self.trade_amount = amount
                popup.dismiss()

                self.result.text = (
                    "Settings Saved\n\n"
                    f"Virtual Trade Amount: {self.trade_amount}\n\n"
                    "DEMO MODE ONLY"
                )

            except:
                amount_input.text = str(self.trade_amount)

        save.bind(on_press=save_settings)
        close.bind(on_press=popup.dismiss)

        popup.open()

    def reset_demo(self, instance):
        self.balance = 10000
        self.total_trades = 0
        self.wins = 0
        self.losses = 0

        self.balance_label.text = "Demo Balance: 10000"

        self.result.text = (
            "Demo Reset Successfully\n\n"
            "Balance: 10000\n"
            "Virtual Trade Amount: "
            f"{self.trade_amount}"
        )


SmartDemoApp().run()from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from datetime import datetime
import os


class BorhanDarkApp(App):

    def build(self):
        self.balance = 10000
        self.last_signal = "WAIT"
        self.history_file = "demo_trade_history.txt"
        self.history = self.load_history()

        main = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=8
        )

        # HEADER
        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=105
        )

        header.add_widget(Label(
            text="BORHAN DARK",
            font_size=30,
            size_hint_y=None,
            height=55
        ))

        header.add_widget(Label(
            text="DEMO TRADING SYSTEM",
            font_size=14,
            size_hint_y=None,
            height=30
        ))

        header.add_widget(Label(
            text="● DEMO MODE",
            font_size=12,
            size_hint_y=None,
            height=20
        ))

        main.add_widget(header)

        # BALANCE
        self.balance_label = Label(
            text=f"Demo Balance: {self.balance:.2f}",
            font_size=20,
            size_hint_y=None,
            height=50
        )

        main.add_widget(self.balance_label)

        # PRICE
        main.add_widget(Label(
            text="MARKET PRICE",
            font_size=17,
            size_hint_y=None,
            height=30
        ))

        self.price_input = TextInput(
            hint_text="Enter 8 or more prices",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        main.add_widget(self.price_input)

        # ANALYZE
        analyze = Button(
            text="ANALYZE MARKET",
            size_hint_y=None,
            height=50
        )

        analyze.bind(on_press=self.analyze)

        main.add_widget(analyze)

        # SIGNAL
        self.signal_label = Label(
            text="SIGNAL: WAIT",
            font_size=25,
            size_hint_y=None,
            height=55
        )

        main.add_widget(self.signal_label)

        # RESULT
        self.result = Label(
            text="Enter prices and press ANALYZE MARKET",
            font_size=15
        )

        main.add_widget(self.result)

        # VIRTUAL TRADE
        trade = Button(
            text="VIRTUAL TRADE",
            size_hint_y=None,
            height=50
        )

        trade.bind(on_press=self.virtual_trade)

        main.add_widget(trade)

        # MENU
        menu = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=5
        )

        history = Button(text="HISTORY")
        history.bind(on_press=self.show_history)

        statistics = Button(text="STATISTICS")
        statistics.bind(on_press=self.show_statistics)

        reset = Button(text="RESET")
        reset.bind(on_press=self.reset_demo)

        menu.add_widget(history)
        menu.add_widget(statistics)
        menu.add_widget(reset)

        main.add_widget(menu)

        # WARNING
        main.add_widget(Label(
            text="DEMO / VIRTUAL BALANCE ONLY",
            font_size=12,
            size_hint_y=None,
            height=25
        ))

        return main

    def load_history(self):

        if not os.path.exists(self.history_file):
            return []

        try:
            with open(
                self.history_file,
                "r",
                encoding="utf-8"
            ) as f:

                return [
                    line.strip()
                    for line in f
                    if line.strip()
                ]

        except:
            return []

    def save_history(self, record):

        try:
            with open(
                self.history_file,
                "a",
                encoding="utf-8"
            ) as f:

                f.write(record + "\n")

        except:
            pass

    def analyze(self, instance):

        try:

            prices = [
                float(x)
                for x in self.price_input.text
                .replace(",", " ")
                .split()
            ]

        except:

            self.signal_label.text = "SIGNAL: ERROR"

            self.result.text = (
                "Please enter numbers only."
            )

            return

        if len(prices) < 8:

            self.signal_label.text = "SIGNAL: WAIT"

            self.result.text = (
                "Please enter at least 8 prices."
            )

            return

        last8 = prices[-8:]

        # OVERALL TREND
        old_trend = (
            last8[-1] -
            last8[0]
        )

        # RECENT TREND
        recent_trend = (
            last8[-1] -
            last8[-4]
        )

        # MOMENTUM
        momentum = (
            last8[-1] -
            last8[-2]
        )

        # TREND
        if old_trend > 3:
            trend = "UP"

        elif old_trend < -3:
            trend = "DOWN"

        else:
            trend = "SIDEWAYS"

        # RECENT
        if recent_trend > 1:
            recent = "UP"

        elif recent_trend < -1:
            recent = "DOWN"

        else:
            recent = "SIDEWAYS"

        # MOMENTUM
        if momentum > 0:
            momentum_status = "POSITIVE"

        elif momentum < 0:
            momentum_status = "NEGATIVE"

        else:
            momentum_status = "NEUTRAL"

        # SIGNAL
        if (
            trend == "UP"
            and recent == "UP"
            and momentum > 0
        ):

            self.last_signal = "UP"

        elif (
            trend == "DOWN"
            and recent == "DOWN"
            and momentum < 0
        ):

            self.last_signal = "DOWN"

        else:

            self.last_signal = "WAIT"

        self.signal_label.text = (
            f"SIGNAL: {self.last_signal}"
        )

        self.result.text = (
            f"Current Price: {last8[-1]:.2f}\n"
            f"Overall Trend: {trend}\n"
            f"Recent Trend: {recent}\n"
            f"Momentum: {momentum_status}\n"
            f"Momentum Value: {momentum:.2f}"
        )

    def virtual_trade(self, instance):

        if self.last_signal == "WAIT":

            self.result.text = (
                "No virtual trade.\n"
                "Signal is WAIT."
            )

            return

        amount = 100

        if self.balance < amount:

            self.result.text = (
                "Demo balance is too low."
            )

            return

        self.balance -= amount

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        record = (
            f"{now} | "
            f"Signal={self.last_signal} | "
            f"Amount={amount} | "
            f"Balance={self.balance:.2f}"
        )

        self.history.append(record)

        self.save_history(record)

        self.balance_label.text = (
            f"Demo Balance: "
            f"{self.balance:.2f}"
        )

        self.result.text = (
            "VIRTUAL TRADE RECORDED\n\n"
            f"Signal: {self.last_signal}\n"
            f"Demo Amount: {amount}\n"
            f"Remaining Balance: "
            f"{self.balance:.2f}"
        )

    def show_history(self, instance):

        if not self.history:

            self.result.text = (
                "TRADE HISTORY\n\n"
                "No trades yet."
            )

            return

        self.result.text = (
            "TRADE HISTORY\n\n"
            + "\n".join(
                self.history[-10:]
            )
        )

    def show_statistics(self, instance):

        total = len(self.history)

        up_count = 0
        down_count = 0

        for record in self.history:

            if "Signal=UP" in record:
                up_count += 1

            elif "Signal=DOWN" in record:
                down_count += 1

        self.result.text = (
            "STATISTICS\n\n"
            f"Total Virtual Trades: {total}\n"
            f"UP Trades: {up_count}\n"
            f"DOWN Trades: {down_count}\n"
            f"Current Demo Balance: "
            f"{self.balance:.2f}"
        )

    def reset_demo(self, instance):

        self.balance = 10000
        self.last_signal = "WAIT"

        self.balance_label.text = (
            "Demo Balance: 10000.00"
        )

        self.signal_label.text = (
            "SIGNAL: WAIT"
        )

        self.price_input.text = ""

        self.result.text = (
            "Demo balance reset.\n"
            "Trade history is preserved."
        )


BorhanDarkApp().run()
