# Stock Scraper

This is a web scraper that retrieves data for over 390 stocks (You can find the stock list in the file [stocks-b3.csv](stocks-b3.csv)) from the website [https://fundamentus.com.br/](https://fundamentus.com.br/) and export it to a csv file in the [`data`](data) directory.

All the logs files are written to [`logs`](logs) directory

## Installation
### Python
To use this scraper, you need to have Python installed on your machine. You can download Python from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/).

### Virtual Environment

It is recommended to create a virtual environment before installing the dependencies. This helps to isolate the project's dependencies from other Python projects on your machine.

To create a virtual environment, run the following command:

```bash
python -m venv .env
```

Activate the virtual environment by running the appropriate command for your operating system:

- For Windows:
```bash
.env\Scripts\activate
```

- For macOS and Linux:
```bash
source .env/bin/activate
```
### Dependencies
Once the virtual environment is activated, you can proceed with installing the required dependencies:

```bash
pip install -r requirements.txt
```

Remember to deactivate the virtual environment when you're done working on the project:

```bash
deactivate
```

## Usage

To run the scraper, navigate to the project directory and execute the following command:

```bash
python main.py
```

The scraper will start fetching data for each stock and at the end save the result with all the data fetched in a CSV file in the [`data`](data) directory.

The output CSV name follows the pattern `output_yyyyMMdd.csv`, considering the execution date.

## Contributing

Contributions are welcome, if you have any suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.


