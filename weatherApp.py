import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
import io
import threading

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌦️ Perfect Weather App")
        self.root.geometry("600x700")
        self.root.minsize(550, 650)
        self.root.configure(bg='#1e1e2e')
        self.api_key = "c4ac85cfd09da5fa078e8846342ff5ee"
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.icon_url = "https://openweathermap.org/img/wn/{}@2x.png"
        self.units = "metric"
        self.unit_symbol = "°C"
        self.current_icon = None
        self.cities = [
            "Delhi,IN", "Mumbai,IN", "Bangalore,IN", "Chennai,IN", "Kolkata,IN",
            "Hyderabad,IN", "Pune,IN", "Jaipur,IN", "Lucknow,IN", "Ahmedabad,IN",
            "Mangalore,IN", "Goa,IN", "Kochi,IN", "Mysore,IN", "Nagpur,IN",
            "London,UK", "New York,US", "Dubai,AE", "Singapore,SG", "Paris,FR"
        ]
        self.setup_perfect_ui()
        self.get_weather("Mangalore,IN")

    def setup_perfect_ui(self):
        # Header
        tk.Label(self.root, text="🌡️ Weather Dashboard",
                 font=('Arial', 20, 'bold'), bg='#1e1e2e', fg='white').pack(pady=15)
        input_frame = tk.Frame(self.root, bg='#1e1e2e')
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="City:", font=('Arial', 11),
                 bg='#1e1e2e', fg='white').pack(side='left')
        self.city_entry = tk.Entry(input_frame, font=('Arial', 11), width=18)
        self.city_entry.pack(side='left', padx=10)
        self.city_entry.insert(0, "Mangalore,IN")
        tk.Button(input_frame, text="Search", command=self.get_weather_manual,
                  bg='#0891b2', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        self.unit_btn = tk.Button(input_frame, text="°F", command=self.toggle_units,
                                  bg='#10b981', fg='white', font=('Arial', 9, 'bold'), width=5)
        self.unit_btn.pack(side='right', padx=10)
        cities_frame = tk.Frame(self.root, bg='#1e1e2e')
        cities_frame.pack(pady=10)
        for i, city in enumerate(self.cities[:10]):
            row = i // 5
            col = i % 5
            btn = tk.Button(cities_frame, text=city.replace(",IN", ""),
                            command=lambda c=city: self.quick_city(c),
                            bg='#3b82f6' if i < 5 else '#10b981', fg='white',
                            font=('Arial', 8, 'bold'), width=8)
            btn.grid(row=row, column=col, padx=2, pady=3)
        self.result_frame = tk.Frame(self.root, bg='#2d3748', relief='ridge', bd=2)
        self.result_frame.pack(pady=15, padx=25, fill='both', expand=True)

        self.location_lbl = tk.Label(self.result_frame, text="Loading...",
                                     font=('Arial', 22, 'bold'), bg='#2d3748', fg='white')
        self.location_lbl.pack(pady=15)
        icon_temp_frame = tk.Frame(self.result_frame, bg='#2d3748')
        icon_temp_frame.pack(pady=10)
        self.icon_lbl = tk.Label(icon_temp_frame, text="🌤️", font=('Arial', 60),
                                 bg='#2d3748')
        self.icon_lbl.pack(side='left', padx=20)
        self.temp_lbl = tk.Label(icon_temp_frame, text="--°C", font=('Arial', 48, 'bold'),
                                 bg='#2d3748', fg='#fbbf24')
        self.temp_lbl.pack(side='left')
        self.condition_lbl = tk.Label(self.result_frame, text="Click a city!",
                                      font=('Arial', 14, 'bold'), bg='#2d3748', fg='#cbd5e1')
        self.condition_lbl.pack(pady=10)
        details_frame = tk.Frame(self.result_frame, bg='#2d3748')
        details_frame.pack(pady=20, padx=30, fill='x')
        self.humidity_lbl = tk.Label(details_frame, text="Humidity: --",
                                     font=('Arial', 13, 'bold'), bg='#2d3748', fg='white')
        self.humidity_lbl.grid(row=0, column=0, sticky='w', pady=8, padx=(0, 20))
        self.wind_lbl = tk.Label(details_frame, text="Wind: --",
                                 font=('Arial', 13, 'bold'), bg='#2d3748', fg='white')
        self.wind_lbl.grid(row=1, column=0, sticky='w', pady=8)
        self.pressure_lbl = tk.Label(details_frame, text="Pressure: --",
                                     font=('Arial', 13, 'bold'), bg='#2d3748', fg='white')
        self.pressure_lbl.grid(row=2, column=0, sticky='w', pady=8)
        self.status_lbl = tk.Label(self.result_frame, text="Status: Ready!",
                                   font=('Arial', 12, 'bold'), bg='#2d3748', fg='#10b981')
        self.status_lbl.pack(pady=15)

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
        self.status_lbl.config(text=f"Fetching {city}...")
        self.root.update()

        def fetch_data():
            try:
                url = f"{self.base_url}/weather?q={city}&appid={self.api_key}&units={self.units}"
                print(f"🌐 {city}: {url}")
                response = requests.get(url, timeout=12)
                data = response.json()
                if data.get('cod') == 200:
                    self.root.after(0, lambda: self.display_weather(data, city))
                else:
                    self.root.after(0, lambda: self.show_error(city, data))
            except Exception as e:
                self.root.after(0, lambda: self.show_network_error(str(e)))
        threading.Thread(target=fetch_data, daemon=True).start()

    def show_error(self, city, data):
        error_msg = data.get('message', 'Unknown error')
        self.status_lbl.config(text=f"❌ {error_msg}")
        messagebox.showerror("Error", f"{city}\n{error_msg}")

    def show_network_error(self, error):
        self.status_lbl.config(text="🌐 Network error")
        messagebox.showerror("Network", error)

    def display_weather(self, data, city):
        city_name = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data.get('wind', {}).get('speed', 0)
        condition = data['weather'][0]['main']
        desc = data['weather'][0]['description']
        icon_code = data['weather'][0]['icon']
        self.location_lbl.config(text=f"{city_name}, {country}")
        self.condition_lbl.config(text=f"{condition}: {desc.title()}")
        self.temp_lbl.config(text=f"{temp:.1f}{self.unit_symbol}")
        self.humidity_lbl.config(text=f"💧 Humidity: {humidity}%")
        self.wind_lbl.config(text=f"💨 Wind: {wind:.1f} km/h")
        self.pressure_lbl.config(text=f"📊 Pressure: {pressure} hPa")
        self.status_lbl.config(text=f"✅ {city_name} loaded!")
        def load_icon():
            try:
                self.icon_lbl.config(image="", text="⏳")
                self.root.update()
                icon_response = requests.get(f"{self.icon_url}{icon_code}", timeout=6)
                icon_img = Image.open(io.BytesIO(icon_response.content))
                icon_img = icon_img.resize((70, 70), Image.Resampling.LANCZOS)
                new_icon = ImageTk.PhotoImage(icon_img)
                self.icon_lbl.config(image=new_icon, text="")
                self.icon_lbl.image = new_icon
            except Exception as e:
                print(f"Icon failed: {e}")
                self.icon_lbl.config(image="", text="🌤️")
        threading.Thread(target=load_icon, daemon=True).start()

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
