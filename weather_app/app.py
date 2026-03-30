from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    lat = None
    lon = None

    if request.method == "POST":
        try:
            lat = request.form.get("lat")
            lon = request.form.get("lon")

            if not lat or not lon:
                raise ValueError("緯度・経度が入力されていません")

            url = (
                "https://api.open-meteo.com/v1/forecast"
                f"?latitude={lat}&longitude={lon}"
                "&current_weather=true"
            )

            r = requests.get(url, timeout=10)
            data = r.json()

            if "current_weather" not in data:
                raise ValueError("天気データが取得できませんでした")

            weather = data["current_weather"]

        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        weather=weather,
        lat=lat,
        lon=lon,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=False)
