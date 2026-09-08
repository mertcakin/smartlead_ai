from app import create_app


# Flask uygulamasını başlattım.
app = create_app()


if __name__ == "__main__":
    # Uygulamayı geliştirme modunda çalıştırdım.
    app.run(debug=True)