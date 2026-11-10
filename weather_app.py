import os
import tkinter as tk
import requests


class weather_app:
    def __init__(self, master):
        self.master = master
        self.master.title("Weather App")
        self.master.geometry("400x300")
        self.master.resizable(False, False)
        self.master.configure(bg="#111827")

        self.api_key = os.environ.get("OPENWEATHER_API_KEY")
        self.weather_url = "https://api.openweathermap.org/data/2.5/weather"

        self.city_label = tk.Label(self.master, text="Enter a city name:", bg="#111827", fg="white")
        self.city_label.pack(pady=10)

        self.city_entry = tk.Entry(self.master, width=30, bg="black", fg="white", insertbackground="white")
        self.city_entry.pack(pady=5)

        self.fetch_button = tk.Button(self.master, text="Fetch Weather", command=self.fetch_weather, bg="black", fg="white")
        self.fetch_button.pack(pady=10)

        self.result_label = tk.Label(self.master, text="", bg="#111827", fg="white")
        self.result_label.pack(pady=10)

    def fetch_weather(self):
        city_name = self.city_entry.get().strip()
        if not city_name:
            self.result_label.config(text="Please enter a city name.")
            return

        if not self.api_key:
            self.result_label.config(text="API key missing. Set OPENWEATHER_API_KEY.")
            return

        try:
            response = requests.get(
                self.weather_url,
                params={"q": city_name, "appid": self.api_key, "units": "metric"},
                timeout=10,
            )
            if response.status_code == 404:
                self.result_label.config(text="City not found.")
                return
            if response.status_code == 401:
                self.result_label.config(text="API key invalid or not active yet.")
                return
            response.raise_for_status()
            weather = response.json()
            weather_description = weather["weather"][0]["description"]
            temperature = weather["main"]["temp"]
            self.result_label.config(
                text=f"Weather in {weather['name']}: {weather_description}\nTemperature: {temperature}°C"
            )
        except requests.RequestException:
            self.result_label.config(text="Network error. Check your connection.")
        except (ValueError, KeyError):
            self.result_label.config(text="Unexpected response from the server.")

if __name__ == "__main__":
    root = tk.Tk()
    app = weather_app(root)
    root.mainloop()