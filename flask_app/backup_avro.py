# backup_avro.py
from fastavro import writer, parse_schema
from app import app
from models import db, Department, Job, HiredEmployee

def backup_table_to_avro(table_model, schema, file_name):
    """Backup a database table to an AVRO file."""
    with app.app_context():
        items = table_model.query.all()
        records = [item.to_dict() for item in items]
        
        with open(file_name, 'wb') as out:
            writer(out, schema, records)

if __name__ == "__main__":
    departments_schema = parse_schema({
        'type': 'record',
        'name': 'department',
        'fields': [
            {'name': 'id', 'type': 'int'},
            {'name': 'department', 'type': 'string'},
        ]
    })
    
    jobs_schema = parse_schema({
        'type': 'record',
        'name': 'job',
        'fields': [
            {'name': 'id', 'type': 'int'},
            {'name': 'job', 'type': 'string'},
        ]
    })

    hired_employees_schema = parse_schema({
        'type': 'record',
        'name': 'hired_employee',
        'fields': [
            {'name': 'id', 'type': 'int'},
            {'name': 'name', 'type': 'string'},
            {'name': 'datetime', 'type': {'type': 'string', 'logicalType': 'timestamp-millis'}},
            {'name': 'department_id', 'type': 'int'},
            {'name': 'job_id', 'type': 'int'},
        ]
    })

    backup_table_to_avro(Department, departments_schema, 'departments_backup.avro')
    backup_table_to_avro(Job, jobs_schema, 'jobs_backup.avro')
    backup_table_to_avro(HiredEmployee, hired_employees_schema, 'hired_employees_backup.avro')

    print("Backup completed successfully.")
