# Proyecto de Migración de Datos - PoC

Este repositorio contiene el código desarrollado por Sebastián Franco como parte de un desafío técnico para la posición de Ingeniero de Datos en Globant.

## Descripción del Proyecto

El proyecto tiene como objetivo principal realizar la migración de datos de 3 diferentes archivos de excel a una nueva base de datos utilizando diferentes herramientas y tecnologías. El alcance del proyecto incluye:

1. **Migración de Datos Históricos:** Se debe mover datos históricos desde archivos en formato xlsx a la nueva base de datos.

2. **Creación de un Servicio de API Rest:** Se debe desarrollar un servicio de API Rest para recibir nuevos datos. Este servicio debe cumplir con las siguientes características:
   - Cada nueva transacción debe cumplir con las reglas del diccionario de datos.
   - Capacidad para insertar transacciones por lotes (de 1 a 1000 filas) con una sola solicitud.
   - Recepción de datos para cada tabla en el mismo servicio.
   - Consideración de las reglas de datos para cada tabla.

3. **Backup de Datos:** Se debe implementar una funcionalidad para realizar copias de seguridad de cada tabla y guardarlas en el sistema de archivos en formato AVRO.

4. **Restauración de Datos:** Se debe crear una funcionalidad para restaurar una tabla específica con su copia de seguridad correspondiente.

5. **Exploración de Datos y Métricas:** Se debe crear un punto final para cada una de las siguientes métricas solicitadas por los interesados:

    - Número de empleados contratados por cada puesto y departamento en 2021 dividido por trimestre.
    - Lista de IDs, nombres y número de empleados contratados de cada departamento que contrató más empleados que el promedio de empleados contratados en 2021 para todos los departamentos, ordenados por el número de empleados contratados (descendente).

## Arquitectura del Proyecto

El proyecto se desarrolló localmente utilizando Visual Studio Code como entorno de desarrollo integrado (IDE) y MySQL como base de datos relacional. Aunque se sugiere una arquitectura en la nube para un entorno de producción, en este caso se optó por una implementación local debido a la simplicidad del proyecto y los recursos disponibles.

## Estructura del Repositorio

- **flask_app:** Contiene el código fuente del servicio de API Rest desarrollado con Flask.
- **README.md:** Documentación principal del proyecto.
- **departments_backup.avro:** Archivo de copia de seguridad de la tabla de departamentos en formato AVRO.
- **dim_department.ipynb:** Cuaderno de Jupyter con el proceso ETL para la dimensión de departamentos.
- **dim_job.ipynb:** Cuaderno de Jupyter con el proceso ETL para la dimensión de puestos de trabajo.
- **fct_hired_empleyee.ipynb:** Cuaderno de Jupyter con el proceso ETL para la tabla de empleados contratados.
- **hired_employees_backup.avro:** Archivo de copia de seguridad de la tabla de empleados contratados en formato AVRO.
- **jobs_backup.avro:** Archivo de copia de seguridad de la tabla de puestos de trabajo en formato AVRO.

## Consideraciones Adicionales

- **Markdown para README:** Se incluyó un archivo README.md detallado que proporciona información sobre el proyecto, su estructura y cómo ejecutarlo.
- **Seguridad de la API:** Aunque no se implementó en este PoC, se recomienda encarecidamente considerar aspectos de seguridad, como la autenticación y la autorización, al desarrollar servicios de API Rest en un entorno de producción. También se hace la claridad de que no están anonimizadas las contraseñas de la base de datos. 

## Tecnologías Utilizadas

- Python
- Flask
- MySQL
- Jupyter Notebook
- AVRO