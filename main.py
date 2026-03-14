from fastapi import FastAPI
import httpx
from starlette.responses import FileResponse

app = FastAPI()


@app.get("/")
def index():
    return FileResponse("./index.html")


@app.get("/mojeip")
async def sprawdz_ip():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.ipify.org?format=json")
    dane = response.json()
    return {"ip": dane["ip"]}


# ZMIANA: Endpoint teraz wymaga podania lat i lon!
@app.get("/pogoda")
async def pogoda(lat: float, lon: float):
    async with httpx.AsyncClient() as client:
        # 1. Zamieniamy współrzędne GPS na nazwę miasta (Reverse Geocode)
        res_city = await client.get(
            f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lon}"
        )
        city_data = res_city.json()
        # Wyciągamy miasto (lub jeśli brakuje, bierzemy lokalizację ogólną)
        city = city_data.get("city") or city_data.get("locality") or "Nieznane miejsce"

        # 2. Pobieramy pogodę dla konkretnego GPSa z Open-Meteo
        res_pog = await client.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        )
        pog_data = res_pog.json()

    # Zwracamy gotowy wynik
    return {
        "city": city,
        "temp": pog_data['current_weather']['temperature'],
        "wind": pog_data['current_weather']['windspeed']
    }