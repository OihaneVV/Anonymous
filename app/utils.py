import math
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, timedelta
from app.models import db, Post

def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia en kilómetros entre dos puntos GPS usando la fórmula de Haversine.
    Parámetros:
        lat1, lon1: latitud y longitud del primer punto en grados decimales
        lat2, lon2: latitud y longitud del segundo punto en grados decimales
    Retorna:
        Distancia en kilómetros (float)
    """
    R = 6371  # Radio de la Tierra en km

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distancia = R * c
    return distancia

def eliminar_posts_viejos():
    limite_tiempo = datetime.now() - timedelta(hours=1)
    posts_viejos = Post.query.filter(Post.timestamp < limite_tiempo).all()
    for post in posts_viejos:
        db.session.delete(post)
    db.session.commit()
