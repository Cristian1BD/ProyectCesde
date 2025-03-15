from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Crear instancia de la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agenda.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Crear una instancia de SQLAlchemy
db = SQLAlchemy(app)

# Definir el modelo de la base de datos
class ImportantDate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    #hola

    def __repr__(self):
        return f'<ImportantDate {self.name} on {self.date}>'

# Crear la base de datos si no existe
with app.app_context():
    db.create_all()

# Ruta para ver todas las fechas importantes
@app.route('/dates', methods=['GET'])
def get_dates():
    dates = ImportantDate.query.all()
    return jsonify([
        {'id': date.id, 'name': date.name, 'date': date.date.strftime('%Y-%m-%d')}
        for date in dates
    ])

# Ruta para agregar una nueva fecha importante
@app.route('/dates', methods=['POST'])
def add_date():
    data = request.get_json()
    name = data.get('name')
    date_str = data.get('date')
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'La fecha debe estar en formato YYYY-MM-DD'}), 400
   
    new_date = ImportantDate(name=name, date=date)
    db.session.add(new_date)
    db.session.commit()
    return jsonify({'id': new_date.id, 'name': new_date.name, 'date': new_date.date.strftime('%Y-%m-%d')}), 201

# Ruta para actualizar una fecha importante
@app.route('/dates/<int:id>', methods=['PUT'])
def update_date(id):
    date = ImportantDate.query.get(id)
    if not date:
        return jsonify({'error': 'Fecha no encontrada'}), 404
   
    data = request.get_json()
    date.name = data.get('name', date.name)
    date_str = data.get('date', str(date.date))
   
    try:
        date.date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'La fecha debe estar en formato YYYY-MM-DD'}), 400
   
    db.session.commit()
    return jsonify({'id': date.id, 'name': date.name, 'date': date.date.strftime('%Y-%m-%d')})

# Ruta para eliminar una fecha importante
@app.route('/dates/<int:id>', methods=['DELETE'])
def delete_date(id):
    date = ImportantDate.query.get(id)
    if not date:
        return jsonify({'error': 'Fecha no encontrada'}), 404
   
    db.session.delete(date)
    db.session.commit()
    return jsonify({'message': 'Fecha eliminada exitosamente'})

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
