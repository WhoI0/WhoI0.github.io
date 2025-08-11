import webbrowser


def show_smokers_on_map(smokers):
    """
    smokers: список словарей с координатами и именами
    пример: [
        {"name": "Иван", "lat": 55.751244, "lon": 37.618423},
        {"name": "Ольга", "lat": 55.760244, "lon": 37.620423}
    ]
    """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <title>Карта перекуров</title>
        <script src="https://api-maps.yandex.ru/2.1/?lang=ru_RU" type="text/javascript"></script>
        <script type="text/javascript">
            ymaps.ready(init);
            function init() {{
                var map = new ymaps.Map("map", {{
                    center: [{smokers[0]['lat']}, {smokers[0]['lon']}],
                    zoom: 15
                }});

                {"".join([f"map.geoObjects.add(new ymaps.Placemark([{s['lat']}, {s['lon']}], {{balloonContent: '{s['name']} на перекуре'}}));" for s in smokers])}
            }}
        </script>
        <style>
            html, body, #map {{ width: 100%; height: 100%; margin: 0; padding: 0; }}
        </style>
    </head>
    <body>
        <div id="map"></div>
    </body>
    </html>
    """

    with open("smokers_map.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    webbrowser.open("smokers_map.html")


# Пример данных
smokers_data = [
    {"name": "Иван", "lat": 55.751244, "lon": 37.618423},
    {"name": "Ольга", "lat": 55.760244, "lon": 37.620423},
    {"name": "Пётр", "lat": 55.7558, "lon": 37.6173}
]

show_smokers_on_map(smokers_data)
