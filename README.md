This repository contains three Python scripts that collectively provide a simple software licensing system using Flask and SQLite. Below is a brief overview of each script's functionality, the technologies used, and terminal commands to set up and run the system.

## 1. app.py

### Functionality:
- Implements a Flask web application with RESTful endpoints for managing licenses.
- Requires a token for accessing certain routes.
- Provides endpoints for retrieving all licenses, validating a specific license, adding a new license, and deleting an existing license.
- Includes a login route for obtaining an access token.

### Technologies Used:
- Flask
- SQLAlchemy
- JWT (JSON Web Tokens)

### Setup and Execution:
```bash
pip install flask sqlalchemy
python app.py
