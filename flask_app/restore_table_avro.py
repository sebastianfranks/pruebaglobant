# restore_avro.py
from fastavro import reader
from app import app, db
from models import Department, Job, HiredEmployee

def restore_table_from_avro(table_model, schema, file_name):
    """Restore a database table from an AVRO file."""
    with app.app_context():
        with open(file_name, 'rb') as avro_file:
            avro_reader = reader(avro_file, schema)
            records = [record for record in avro_reader]
            
            for record in records:
                # Check if the record already exists
                existing_record = table_model.query.get(record['id'])
                if existing_record:
                    print(f"Skipping insertion of record with id {record['id']}. Record already exists.")
                else:
                    # Insert the record if it doesn't already exist
                    item = table_model(**record)
                    db.session.add(item)
            
            db.session.commit()

if __name__ == "__main__":
    departments_schema = {
        'type': 'record',
        'name': 'department',
        'fields': [
            {'name': 'id', 'type': 'int'},
            {'name': 'department', 'type': 'string'},
        ]
    }
    
    jobs_schema = {
        'type': 'record',
        'name': 'job',
        'fields': [
            {'name': 'id', 'type': 'int'},
            {'name': 'job', 'type': 'string'},
        ]
    }

    hired_employees_schema = {
        'type': 'record',
        'name': 'hired_employee',
        'fields': [
            {'name': 'id', 'type': 'int'},
            {'name': 'name', 'type': 'string'},
            {'name': 'datetime', 'type': {'type': 'string', 'logicalType': 'timestamp-millis'}},
            {'name': 'department_id', 'type': 'int'},
            {'name': 'job_id', 'type': 'int'},
        ]
    }

    restore_table_from_avro(Department, departments_schema, 'departments_backup.avro')
    restore_table_from_avro(Job, jobs_schema, 'jobs_backup.avro')
    restore_table_from_avro(HiredEmployee, hired_employees_schema, 'hired_employees_backup.avro')

    print("Restore completed successfully.")
