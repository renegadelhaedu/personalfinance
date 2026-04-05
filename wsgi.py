from app import create_app

#isso é apenas p gunicorn ou outro server de producao
app = create_app()

if __name__ == "__main__":
    app.run()