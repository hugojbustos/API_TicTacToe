# Django Tic Tac Toe Game

This project implements a Tic Tac Toe game using Django and Django Rest Framework.

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/hugojbustos/API_TicTacToe.git
    cd your-repo
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Apply migrations:

    ```bash
    python manage.py migrate
    ```

4. Run the development server:

    ```bash
    python manage.py runserver
    ```

Visit default [http://localhost:8000] to check API doc.
Visit default [http://localhost:8000/admin] to admin the tables/models.
Visit default [http://localhost:8000/api] to check all the endpoints to manage the game.For this point you can user Postman

5. Run the API using Docker:

    docker-compose build
    docker-compose up

## Contributing

Feel free to contribute to this project by opening issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
