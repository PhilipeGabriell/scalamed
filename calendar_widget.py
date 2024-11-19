from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import calendar

class CalendarWidget(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 7
        self.rows = 7
        self.create_calendar()

    def create_calendar(self, year=None, month=None):
        self.clear_widgets()
        if year is None or month is None:
            from datetime import datetime
            today = datetime.today()
            year, month = today.year, today.month

        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for day in days:
            self.add_widget(Button(text=day, background_color=(0.5, 0.5, 0.5, 1), size_hint=(0.5, 0.5)))

        month_days = calendar.monthcalendar(year, month)
        for week in month_days:
            for day in week:
                if day == 0:
                    self.add_widget(Button(text="", size_hint=(0.5, 0.5)))
                else:
                    self.add_widget(Button(text=str(day), on_press=self.on_day_press, size_hint=(0.5, 0.5)))

    def on_day_press(self, instance):
        print(f"Data selecionada: {instance.text}")
