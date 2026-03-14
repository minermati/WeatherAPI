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
    # Zwracamy słownik, żeby JS był szczęśliwy
    return {"ip": dane["ip"]}


@app.get("/pogoda")
async def pogoda():
    async with httpx.AsyncClient() as client:
        # Pobieramy lokalizację
        res_loc = await client.get("http://ip-api.com/json")
        loc_data = res_loc.json()

        lat = loc_data['lat']
        lon = loc_data['lon']
        city = loc_data['city']

        # Pobieramy pogodę
        res_pog = await client.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true")
        pog_data = res_pog.json()
    # Zwracamy kompletny obiekt
    return {
        "city": city,
        "temp": pog_data['current_weather']['temperature'],
        "wind": pog_data['current_weather']['windspeed']
    }
