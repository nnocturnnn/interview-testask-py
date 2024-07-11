# Test Task: Web Service for Working with a Dataset

This is a test project that demonstrates the development of a service for working with a dataset in CSV format. The project allows you to read a CSV file, write the data to a database, display the data as a table with pagination, apply filters based on category, gender, Date of Birth, age, and age range, and export data in CSV format according to the specified filters.

## Table of Contents
- [Project Requirements](#project-requirements)
- [Getting Started](#getting-started)
  - [Running the Project with Docker](#running-the-project-with-docker)
- [Usage](#usage)
- [TODO](#TODO)

## Project Requirements

### Dataset
The dataset is provided in CSV format and contains the following columns:
- 'category' (client's favorite category)
- 'firstname'
- 'lastname'
- 'email'
- 'gender'
- 'birthDate'

### Functionality
The project is required to:
1. Read the CSV file.
2. Write the received data to a database.
3. Display data as a table with pagination (or provide a simple JSON API).
4. Implement filters for the following values:
   - Category
   - Gender
   - Date of Birth
   - Age
   - Age range (e.g., 25 - 30 years).
5. Implement data export in CSV format according to the specified filters.

## Getting Started

To get started with the project, follow the instructions below.

### Running the Project with Docker

1. Clone this GitLab repository:
   ```bash
   git clone https://github.com/nnocturnnn/TestTaskRexIT.git
   cd TestTaskRexIT
   ```
2. Build the Docker Image:
    ```
    docker build -t dataset-service .
    ```
3. Run the Docker Container:
    ```
    docker run -p 5000:5000 dataset-service
    ```
4. Access the Project:

Once the container is running, you can access the project at http://localhost:5000.

## Usage

After running the project, you can access it through a web browser. The web interface provides options to upload a CSV file, filter data based on category, gender, Date of Birth, age, and age range, and export data in CSV format. You can interact with the service to explore and filter the dataset as needed.

## TODO

- Write comprehensive tests for the web application to ensure it functions correctly.
- Create unit tests for miscellaneous functions to validate their behavior.
- Enhance the category filtering functionality to provide a better user experience.
- Improve the appearance and styling of the web application by upgrading the CSS.
