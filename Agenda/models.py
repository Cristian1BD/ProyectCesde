from app import db

# Definir el modelo de la base de datos
class ImportantDate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<ImportantDate {self.name} on {self.date}>'