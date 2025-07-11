
# Tomato Online Shop 🍅
## 🌐 [tomato-online-shop.ru](https://tomato-online-shop.ru)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.3+-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=flat&logo=mysql&logoColor=white)](https://www.mysql.com)
[![Docker](https://img.shields.io/badge/Docker-20.10+-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Node.js](https://img.shields.io/badge/Node.js-14+-339933?style=flat&logo=node.js&logoColor=white)](https://nodejs.org/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
An e-commerce platform for selling fresh vegetables, developed with Python Flask, MySQL database, and SMTP for email notifications.

## 🔥 Key Features

- User-friendly vegetable catalog with filtering
- News feed
- Contact information
- Informational blocks
- Shopping cart
- Order processing
- Admin panel:
    
    - Create product categories and subcategories
    - Add, modify, and delete product categories
    - Add, modify, and delete products
    - Enable/disable shopping cart functionality
    - View order list        
    - Filter order list
    - Export order list
- Email notifications via SMTP
- Docker containerization

## 🛠 Technologies

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Email**: SMTP (поддержка Yandex)
- **Deployment**: Docker
## 🚀 Quick Start

### 📦 Installation via Docker Compose
Project Setup with Docker Compose and Environment Variables
This project uses Docker Compose to manage multi-container Docker applications. Follow the instructions below to set up and run the project.

### Prerequisites
Ensure you have the following tools installed:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setting Up Environment Variables

1. Create a `.env` file in the root directory of the project.
2. Add the following environment variables to the `.env` file, replacing the values with your own:

### ⚙️ Environment Variables Configuration

| Variable         | Default Value            | Description                       |
| ---------------- | ------------------------ | --------------------------------- |
| `MYSQL_DATABASE` | `your_db_name`           | MySQL database name               |
| `MYSQL_USER`     | `your_db_user_name`      | MySQL username                    |
| `MYSQL_PASSWORD` | `your_password`          | MySQL password                    |
| `SECRET_KEY`     | `your_secret_key`        | Flask application secret key      |
| `MAIL_SERVER`    | `smtp.yandex.ru`         | Yandex SMTP server address        |
| `MAIL_PORT`      | `587`                    | Yandex SMTP port                  |
| `MAIL_USE_TLS`   | `1`                      | Enable TLS encryption             |
| `MAIL_USERNAME`  | `your_email_login`       | Yandex email login                |
| `MAIL_PASSWORD`  | `your_smtp_password`     | Yandex smtp password/app password |
| `DOMAIN`         | `https://your_domain.ru` | Primary domain for URL generation |
| `NEW_DOMAIN2`    | `https://your_domain.ru` | Primary domain for URL generation |

### Additional Notes:
- The default port 8000 is mapped to the container's internal port 5000
- Admin routes are protected and require authentication
- SMTP configuration shown is for Yandex Mail (can be adjusted for other providers)

### Running the Project with Docker Compose
1. Open a terminal and navigate to the root directory of the project.
2. Start the project using Docker Compose:
```bash
docker-compose up -d
```
This command will start all the services defined in the `docker-compose.yml` file in the background.

### Description of the docker-compose.yml File
The `docker-compose.yml` file defines two services:

- `db`: A MySQL database service.
- `app`: Your application service.

Both services are configured to operate on the same network and have dependencies set so that the application starts only after the database is ready.

### **Create admin user**:
   ```bash
   docker exec -it mysql_container mysql -u name_user_db -p
   ```
   **In MySQL Client, execute:**
   ```sql
   USE name_db;
   INSERT INTO user (name, password, is_admin)
   VALUES ('admin', 'your_hashed_password', 1);
   ```

   **To generate the password hash, use Python:**
   ```python
   from werkzeug.security import generate_password_hash
   print(generate_password_hash('your_password'))
   ```

## 🌐 Access

The application will be available at: [http://localhost:8000](http://localhost:8000)

Admin panel: `/admin`


