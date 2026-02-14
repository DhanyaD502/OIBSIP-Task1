import tkinter as tk
from tkinter import ttk, messagebox
import requests


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌦️ Clean Weather App - No Icons")
        self.root.geometry("600x650")
        self.root.minsize(550, 600)
        self.root.configure(bg='#1e1e2e')

        self.api_key = "c4ac85cfd09da5fa078e8846342ff5ee"
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.units = "metric"
        self.unit_symbol = "°C"

        self.cities = [
            "Delhi,IN", "Mumbai,IN", "Bangalore,IN", "Chennai,IN", "Kolkata,IN",
            "Hyderabad,IN", "Pune,IN", "Jaipur,IN", "Lucknow,IN", "Ahmedabad,IN",
            "Mangalore,IN", "Goa,IN", "Kochi,IN", "Mysore,IN", "Nagpur,IN"
        ]

        self.setup_clean_ui()
        self.get_weather("Mangalore,IN")

    def setup_clean_ui(self):
        # Header
        tk.Label(self.root, text="🌡️ Weather Dashboard",
                 font=('Arial', 22, 'bold'), bg='#1e1e2e', fg='white').pack(pady=20)

        # Input
        input_frame = tk.Frame(self.root, bg='#1e1e2e')
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="City:", font=('Arial', 12), bg='#1e1e2e', fg='white').pack(side='left')
        self.city_entry = tk.Entry(input_frame, font=('Arial', 12), width=20)
        self.city_entry.pack(side='left', padx=10)
        self.city_entry.insert(0, "Mangalore,IN")
        tk.Button(input_frame, text="Search", command=self.get_weather_manual,
                  bg='#0891b2', fg='white', font=('Arial', 11, 'bold')).pack(side='left', padx=10)

        self.unit_btn = tk.Button(input_frame, text="°F", command=self.toggle_units,
                                  bg='#10b981', fg='white', font=('Arial', 10, 'bold'), width=6)
        self.unit_btn.pack(side='right', padx=10)

        # City buttons
        cities_frame = tk.Frame(self.root, bg='#1e1e2e')
        cities_frame.pack(pady=15)
        for i, city in enumerate(self.cities):
            row = i // 5
            col = i % 5
            btn = tk.Button(cities_frame, text=city.replace(",IN", ""),
                            command=lambda c=city: self.quick_city(c),
                            bg='#3b82f6' if i < 5 else '#10b981', fg='white',
                            font=('Arial', 9, 'bold'), width=9, height=1)
            btn.grid(row=row, column=col, padx=3, pady=4)

        # Results
        self.result_frame = tk.Frame(self.root, bg='#2d3748', relief='ridge', bd=2)
        self.result_frame.pack(pady=20, padx=30, fill='both', expand=True)

        self.location_lbl = tk.Label(self.result_frame, text="Loading...",
                                     font=('Arial', 24, 'bold'), bg='#2d3748', fg='white')
        self.location_lbl.pack(pady=20)

        # BIG TEMP DISPLAY (No icon space needed)
        self.temp_lbl = tk.Label(self.result_frame, text="--°C",
                                 font=('Arial', 60, 'bold'), bg='#2d3748', fg='#fbbf24')
        self.temp_lbl.pack(pady=10)

        self.condition_lbl = tk.Label(self.result_frame, text="Click a city!",
                                      font=('Arial', 16, 'bold'), bg='#2d3748', fg='#cbd5e1')
        self.condition_lbl.pack(pady=10)

        # Details - Perfect grid
        details_frame = tk.Frame(self.result_frame, bg='#2d3748')
        details_frame.pack(pady=25, padx=40, fill='x')

        self.humidity_lbl = tk.Label(details_frame, text="💧 Humidity: --",
                                     font=('Arial', 14, 'bold'), bg='#2d3748', fg='white')
        self.humidity_lbl.grid(row=0, column=0, sticky='w', pady=10)

        self.wind_lbl = tk.Label(details_frame, text="💨 Wind: --",
                                 font=('Arial', 14, 'bold'), bg='#2d3748', fg='white')
        self.wind_lbl.grid(row=1, column=0, sticky='w', pady=10)

        self.pressure_lbl = tk.Label(details_frame, text="📊 Pressure: --",
                                     font=('Arial', 14, 'bold'), bg='#2d3748', fg='white')
        self.pressure_lbl.grid(row=2, column=0, sticky='w', pady=10)

        self.status_lbl = tk.Label(self.result_frame, text="Status: Ready!",
                                   font=('Arial', 13, 'bold'), bg='#2d3748', fg='#10b981')
        self.status_lbl.pack(pady=20)

    def quick_city(self, city):
        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, city)
        self.status_lbl.config(text=f"Loading {city}...")
        self.root.update()
        self.get_weather(city)

    def get_weather_manual(self):
        city = self.city_entry.get().strip()
        if ",IN" not in city.upper():
            city = f"{city},IN"
        self.get_weather(city)

    def get_weather(self, city):
        self.status_lbl.config(text=f"📡 Fetching {city}...")
        self.root.update()

        try:
            url = f"{self.base_url}/weather?q={city}&appid={self.api_key}&units={self.units}"
            print(f"🌐 {city}: {url}")
            response = requests.get(url, timeout=12)
            data = response.json()

            if data.get('cod') == 200:
                self.status_lbl.config(text=f"✅ {data['name']} loaded!")
                self.display_weather(data)
            else:
                error_msg = data.get('message', 'Unknown error')
                self.status_lbl.config(text=f"❌ {error_msg}")
                messagebox.showerror("Error", f"{city}: {error_msg}")
        except Exception as e:
            self.status_lbl.config(text="🌐 Network error")
            messagebox.showerror("Network", str(e))

    def display_weather(self, data):
        city_name = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data.get('wind', {}).get('speed', 0)
        condition = data['weather'][0]['main']
        desc = data['weather'][0]['description']

        self.location_lbl.config(text=f"{city_name}, {country}")
        self.condition_lbl.config(text=f"{condition}: {desc.title()}")
        self.temp_lbl.config(text=f"{temp:.1f}{self.unit_symbol}")
        self.humidity_lbl.config(text=f"💧 Humidity: {humidity}%")
        self.wind_lbl.config(text=f"💨 Wind: {wind:.1f} km/h")
        self.pressure_lbl.config(text=f"📊 Pressure: {pressure} hPa")

    def toggle_units(self):
        if self.units == "metric":
            self.units = "imperial"
            self.unit_symbol = "°F"
            self.unit_btn.config(text="°C")
        else:
            self.units = "metric"
            self.unit_symbol = "°C"
            self.unit_btn.config(text="°F")

        city = self.city_entry.get().strip()
        if ",IN" not in city.upper():
            city = f"{city},IN"
        if city:
            self.get_weather(city)


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
