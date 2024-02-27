from flask import Flask, jsonify
from datetime import datetime
from models import Department, Job, HiredEmployee
from database import db
from sqlalchemy import func

app = Flask(__name__)

# Configura tu cadena de conexión aquí usando tus credenciales
username = 'root'
password = 'MySQL'
database_name = 'prueba_globant'
host = 'localhost'  # o la IP si es remoto
port = '3306'  # Puerto por defecto de MySQL

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


def validate_data(table, data):
    if table == 'departments':
        required_fields = ['department']
    elif table == 'jobs':
        required_fields = ['job']
    elif table == 'hired_employees':
        required_fields = ['name', 'datetime', 'department_id', 'job_id']
    else:
        return False, "Invalid table name"
    
    # Verificar campos obligatorios
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validaciones adicionales (ejemplo para hired_employees)
    if table == 'hired_employees':
        try:
            datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return False, "Invalid datetime format for datetime, should be YYYY-MM-DD HH:MM:SS"
        
        # Asegúrate de que el job_id exista
        if not Job.query.get(data['job_id']):
            return False, "job_id does not exist"
    
    return True, ""

# Endpoint para inserción en lote
@app.route('/batch_insert', methods=['POST'])
def batch_insert():
    data = request.json
    table_name = data.get('table')
    rows = data.get('rows', [])
    
    if not rows or not table_name or len(rows) > 1000:
        return jsonify({'error': 'Invalid request'}), 400
    
    model = {'departments': Department, 'jobs': Job, 'hired_employees': HiredEmployee}.get(table_name)
    if not model:
        return jsonify({'error': 'Invalid table name'}), 400
    
    for row in rows:
        is_valid, message = validate_data(table_name, row)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        new_record = model(**row)
        db.session.add(new_record)
    
    try:
        db.session.commit()  # Aquí se realiza el commit para confirmar todas las inserciones.
        return jsonify({'message': 'Batch insert successful'}), 201
    except Exception as e:
        db.session.rollback()  # En caso de error, se hace rollback para mantener la consistencia.
        return jsonify({'error': str(e)}), 400
    
# Ruta del endpoint para obtener métricas de empleados contratados en 2021
@app.route('/metrics/employees_hired_2021')
def employees_hired_2021():
    # Obtener las métricas de empleados contratados en 2021
    metrics = db.session.query(
        Department.department,
        Job.job,
        func.count(func.distinct(HiredEmployee.id)).label('total_hired')
    ).join(
        HiredEmployee, Department.id == HiredEmployee.department_id
    ).join(
        Job, Job.id == HiredEmployee.job_id
    ).filter(
        func.year(HiredEmployee.datetime) == 2021
    ).group_by(
        Department.department, Job.job
    ).order_by(
        Department.department, Job.job
    ).all()

    # Formatear los resultados en un diccionario
    formatted_metrics = []
    for metric in metrics:
        formatted_metrics.append({
            'department': metric[0],
            'job': metric[1],
            'total_hired': metric[2]
        })

    # Devolver los resultados en formato JSON
    return jsonify(formatted_metrics)

@app.route('/metrics/departments_hired_above_mean')
def departments_hired_above_mean():
    # Subconsulta para calcular el recuento de empleados contratados por departamento en 2021
    subquery = db.session.query(
        Department.id,
        func.count(HiredEmployee.id).label('total_hired')
    ).join(
        HiredEmployee, Department.id == HiredEmployee.department_id
    ).filter(
        func.extract('year', HiredEmployee.datetime) == 2021
    ).group_by(
        Department.id
    ).subquery()

    # Calcular la media del recuento de empleados contratados en 2021 para todos los departamentos
    mean_hired_employees = db.session.query(func.avg(subquery.c.total_hired)).scalar()

    # Obtener los departamentos que contrataron más empleados que la media en 2021
    departments_above_mean = db.session.query(
        Department.id,
        Department.department,
        subquery.c.total_hired
    ).join(
        subquery, Department.id == subquery.c.id
    ).filter(
        subquery.c.total_hired > mean_hired_employees
    ).order_by(
        subquery.c.total_hired.desc()
    ).all()

    # Formatear los resultados en un diccionario
    formatted_departments = []
    for department in departments_above_mean:
        formatted_departments.append({
            'id': department[0],
            'name': department[1],
            'total_hired': department[2]
        })

    # Devolver los resultados en formato JSON
    return jsonify(formatted_departments)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)