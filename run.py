from base import create_app,db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        from base import db  # Import db within the app context
        db.create_all()
    app.run(debug=True)
