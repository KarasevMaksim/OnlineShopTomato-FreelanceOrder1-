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

### Installation and Setup

1. **Build Docker Image**:
   ```bash
   docker build -t your_app_name:latest .
   ```
   **If you encounter requirements.txt installation errors**:
   ```bash
   docker build --network=host -t your_app_name:latest .
   ```

2. **Create network for container communication and dir for volume**:
   ```bash
   docker network create your_network_name
   mkdir -p ~/mysql_data
   mkdir -p ~/images
   ```

3. **Launch MySQL Container**:
   ```bash
   docker run --name mysql -d \
     -e MYSQL_RANDOM_ROOT_PASSWORD=yes \
     -e MYSQL_DATABASE=name_db \
     -e MYSQL_USER=name_user_db \
     -e MYSQL_PASSWORD=password_db \
     --network your_network_name \
     -v ~/mysql_data:/var/lib/mysql \
     mysql:latest
   ```

4. **Launch App**:
   ```bash
   docker run --name yoru_app_name -d -p 8000:5000 --rm \
     -e SECRET_KEY=your_secret_key_here \
     -e MAIL_SERVER=smtp.yandex.ru \
     -e MAIL_PORT=587 \
     -e MAIL_USE_TLS=1 \
     -e MAIL_USERNAME=your_email@yandex.ru \
     -e MAIL_PASSWORD=your_smtp_password \
     --network your_network_name \
     -e DATABASE_URL=mysql+pymysql://name_user_db:password_db@mysql/name_db \
     -e NEW_DOMAIN2=https://your_domain.ru \
     -v ~/images:/app/static/img/products \
     your_app_name:latest
   ```

5. **Create admin user**:
   ```bash
   docker exec -it mysql mysql -u name_user_db -p
   ```
   **In MySQL Client, execute:**
   ```sql
   USE name_db;
   INSERT INTO user (name, password, is_admin)
   VALUES ('admin', 'ваш_хешированный_пароль', 1);
   ```

   **To generate the password hash, use Python:**
   ```python
   from werkzeug.security import generate_password_hash
   print(generate_password_hash('your_password'))
   ```

## 🌐 Access

The application will be available at: [http://localhost:8000](http://localhost:8000)

Admin panel: `/admin`

## ⚙️ Configuration

Key environment variables:

| Variable        | Description                     |
| --------------- | ------------------------------- |
| `SECRET_KEY`    | Flask secret key                |
| `DATABASE_URL`  | MySQL connection URL            |
| `MAIL_SERVER`   | SMTP server address             |
| `MAIL_PORT`     | SMTP port number                |
| `MAIL_USE_TLS`  | Use TLS (1/0)                   |
| `MAIL_USERNAME` | SMTP login credentials          |
| `MAIL_PASSWORD` | SMTP password                   |
| `NEW_DOMAIN2`   | Primary website domain          |

### Additional Notes:
- The default port 8000 is mapped to the container's internal port 5000
- Admin routes are protected and require authentication
- SMTP configuration shown is for Yandex Mail (can be adjusted for other providers)
