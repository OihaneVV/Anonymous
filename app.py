from app import create_app, db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    print("Tablas creadas correctamente.")
    app.run(debug=True)