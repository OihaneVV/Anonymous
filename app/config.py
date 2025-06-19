import os

class Config:
    DEBUG = True
    # URI de conexión a tu base de datos PostgreSQL (Neon o local)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://Anonymous_owner:npg_KejlPyXs9B4J@ep-twilight-credit-a8vruh70-pooler.eastus2.azure.neon.tech/Anonymous?sslmode=require")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Clave secreta para sesiones y seguridad
    SECRET_KEY = os.getenv("SECRET_KEY", "vnU6lDb4Ufpn2GdMaz2a87CFoX2sJwZoUcco0dCsrj8t_J8m0uw5Jyzj95Ts13DeknkRmqgzAHSebcFksQpdfA")
