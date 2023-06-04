# 💊 Medicine and Wellness Sales Dashboard

This project is a Flask application that provides a dashboard for tracking medicine and wellness sales data. It is connected to a MongoDB database and utilizes Grafana for data visualization.

## 🚀 Getting Started

To run the application, follow these steps:

1. Clone the repository:

```bash
 git clone https://github.com/your-username/medicine-sales-dashboard.git
```

2. Navigate to the app directory:

```bash
cd medicine-sales-dashboard/app
```

3. Start the application using Docker Compose:

```bash
docker-compose up
```

This command will start the Flask app along with the MongoDB database. It will launch three instances of the app, one for each container 🐳.

4. Access the application:
   Once the containers are up and running, you can access the application by navigating to `http://localhost:3000` in your web browser.

## ✨ Features

- **Sales Dashboard**: The app provides a graphical dashboard to visualize medicine and wellness sales data. It uses Grafana for data visualization, allowing you to create interactive charts and graphs 📊📈.

- **MongoDB Integration**: The application is connected to a MongoDB database to store and retrieve sales data. It uses an ORM (Object-Relational Mapping) library, such as PyMongo or MongoEngine, to interact with the database 📁💾.

- **Dockerized Environment**: The entire application, including the Flask app and MongoDB, is containerized using Docker. This ensures consistent and reproducible deployments across different environments 🐳🚀.

## 📝 Usage and Configuration

- **Data Collection**: The application collects sales data from various sources, such as point-of-sale systems or online platforms. You can configure the data collection process to import data automatically or manually upload data files 📊📥.

- **Database Configuration**: The connection details for the MongoDB database can be configured in the `server.py` file. Update the `MONGO_URI` variable with the appropriate MongoDB connection string ⚙️🔧.

- **Grafana Integration**: Grafana is configured to connect to the MongoDB database and retrieve sales data for visualization. You may need to configure the data source settings in Grafana to point to the correct MongoDB instance 📈🔌.

## 🤝 Contributing

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request. Make sure to follow the existing coding style and conventions 👥🙌.

```

```
