# MySQL Text Search CLI

Another CLI tool by Gabriele Murara, focused on practical database inspection.

A Python command-line tool that performs text search across **all fields of all tables** in a MySQL database.

It is designed to help developers and database administrators quickly locate specific values anywhere inside a database, without manually inspecting schemas or writing repetitive queries.

---

## ✨ Features

- Automatically scans all tables in the selected database
- Searches across every column dynamically
- Simple and intuitive CLI interface
- Lightweight and minimal dependencies
- Compatible with any MySQL-based database

---

## 📦 Installation

### Install in development mode

```bash
git clone https://github.com/your-username/mysql-text-search.git
cd mysql-text-search
pip install -e .
```

### Build a wheel

```bash
python -m build
pip install dist/mysql_text_search-<version>-py3-none-any.whl
```

---

## ⚙️ Configuration

The application supports multiple configuration sources with the following priority order (highest to lowest):

1. Command-line arguments  
2. Values defined in a `.env` file  
3. Environment variables  
4. Built-in default values  

This means that command-line parameters always override everything else.

---

### 🔁 Configuration Priority Example

If `--host` is passed via CLI, it will be used.  
Otherwise:

- If `DB_HOST` exists in `.env`, it will be used.
- Else if `DB_HOST` exists as an environment variable, it will be used.
- Otherwise, the default value will be applied.

---

### 📄 `.env` File

You can create a `.env` file in the project root.

A sample configuration file named `.env.sample` is included in the repository so you can create your own configuration file by copying it:

```bash
cp .env.sample .env
```

Then edit the `.env` file with your database credentials:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=secret
DB_NAME=mydb

CASE_INSENSITIVE_SEARCH=0
MATCH_TYPE=exact

```

---

### 🌍 Environment Variables

The same values can be provided as environment variables:

```bash
export DB_HOST=127.0.0.1
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=secret
export DB_NAME=mydb

export CASE_INSENSITIVE_SEARCH=1
export MATCH_TYPE=contains

```

---

### 🧾 Default Values

| Parameter     | Shortcut | Environment Variable | Default     |
|--------------|----------|--------------|-------------|
| `--host`     | `-h`     | `DB_HOST`           | `127.0.0.1` |
| `--port`     | `-p`     | `DB_PORT`           | `3306`      |
| `--user`     | `-u`     | `DB_USER`           | `root`      |
| `--password` | `-P`     | `DB_PASSWORD`       | *(required)* |
| `--database` | `-n`     | `DB_NAME`           | *(required)* |
| `--case_insensitive` | `-i`     | `CASE_INSENSITIVE_SEARCH`           | `false`     |
| `--match-type` | `-t`     | `MATCH_TYPE`           | `exact`      |

> Parameters marked as *(required)* must be provided through one of the configuration sources.

---

## 🔍 Match Type

The CLI tool supports different match types to control how the search is performed. Use the `--match-type` parameter (or `-t` shortcut) to select the desired behavior.  

| Match Type    | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| `exact`       | Only returns rows where the field exactly matches the query string.        |
| `contains`    | Returns rows where the field contains the query string anywhere.           |
| `starts_with` | Returns rows where the field starts with the query string.               |
| `ends_with`   | Returns rows where the field ends with the query string.                    |

**Example usage:**

```bash
mysql-search --match-type exact "text to search"
mysql-search -u root -P secret -n mydb -t contains "text to search"
```

> Default match type is `exact` if not specified.

---

## 🚀 Usage

Basic example:

```bash
mysql-search "text to search"
```

Full example:

```bash
mysql-search \
    --host localhost \
    --port 3306 \
    --user root \
    --password secret \
    --database mydb \
    --case_insensitive \
    --match-type starts_with \
    "text to search"
```

Or using shortcuts:

```bash
mysql-search \
    -h localhost \
    -p 3306 \
    -u root \
    -P secret \
    -n mydb \
    -t starts_with \
    -i \
    "text to search"
```


---

## 🧾 Example Output

```
[+] Match found
    `{table}`.`{column}` -> number of values
    `{table}`.`{column}` -> number of values
```

---

## 🔎 Version

The CLI version is automatically read from `pyproject.toml`.

Check the installed version:

```bash
mysql-search --version
```

---

## ⚙️ Requirements

- Python 3.12+
- Access to a MySQL database
- Valid database credentials

---

## 📄 License

This project is licensed under the Apache License 2.0.
