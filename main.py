from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button
from kivy.uix.label import Label
import subprocess
import threading

class MyApp(App):
    def build(self):
        self.simulation_process = None

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.slider = Slider(min=1, max=100, value=10, step=1, size_hint=(1, 0.2))
        self.progress = ProgressBar(max=100, value=10, size_hint=(1, 0.2))
        self.slider.bind(value=self.on_slider_value_change)

        self.label = Label(text="Số lượng xe: 10", size_hint=(1, 0.1))

        run_button = Button(text='Run Simulation', size_hint=(1, 0.2))
        run_button.bind(on_press=self.run_simulation)

        layout.add_widget(self.label)
        layout.add_widget(self.slider)
        layout.add_widget(self.progress)
        layout.add_widget(run_button)

        return layout

    def on_slider_value_change(self, instance, value):
        self.progress.value = value
        self.label.text = f"Số lượng xe: {int(value)}"

    def run_simulation(self, instance):
        car_count = int(self.slider.value)
        threading.Thread(target=self.start_or_restart_simulation, args=(car_count,), daemon=True).start()

    def start_or_restart_simulation(self, car_count):
        if self.simulation_process and self.simulation_process.poll() is None:
            print("Đang tắt simulation cũ...")
            self.simulation_process.terminate()
            try:
                self.simulation_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.simulation_process.kill()

        print(f"Chạy simulation mới với số lượng xe: {car_count}")
        param = "totalCarCount = " + str(car_count)
        self.simulation_process = subprocess.Popen(['python', 'run_simulation.py', param])

    def on_stop(self):
        if self.simulation_process and self.simulation_process.poll() is None:
            print("Tắt simulation khi đóng app...")
            self.simulation_process.terminate()

if __name__ == '__main__':
    MyApp().run()
