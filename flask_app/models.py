from database import db

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'department': self.department
        }
    

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'job': self.job
        }

class HiredEmployee(db.Model):
    __tablename__ = 'hired_employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)  # Cambio de Date a DateTime
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'datetime': self.datetime.isoformat() if self.datetime else None,  # Convertir a cadena si no es None
            'department_id': self.department_id if isinstance(self.department_id, int) else 99,
            'job_id': self.job_id if isinstance(self.job_id, int) else 999,  # Asegurar que job_id sea entero o 999
        }