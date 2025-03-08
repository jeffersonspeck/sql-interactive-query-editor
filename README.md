# SQL Interactive Query Editor

**A simple yet powerful graphical SQL query editor built with Python, Tkinter, and PostgreSQL.**

This project provides a graphical user interface (GUI) for executing SQL queries directly or from files, displaying results interactively in a clear, tabular format. It's perfect for quick database inspections and simple query executions.

## Features

- Execute SQL queries directly from a graphical interface.
- Load and execute SQL queries from files.
- Export results to XLSX 
- Interactive, resizable result tables with auto-sized columns.
- Copy row data easily to the clipboard.
- User-friendly error handling and clear feedback.

## Tech Stack

- **Python**
- **Tkinter** (GUI interface)
- **PostgreSQL** (Database)
- **psycopg2** (Database connection)
- **python-dotenv** (Environment variable management)
- **pandas** (DataSet)
- **openpyxl** (XLSX)

## Prerequisites

- Python 3.x
- PostgreSQL database
- If you're using **WSL** (Windows Subsystem for Linux), you'll also need an X Server like [VcXsrv](https://sourceforge.net/projects/vcxsrv/) or [Xming](https://sourceforge.net/projects/xming/).

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/jeffersonspeck/sql-interactive-query-editor.git
cd sql-interactive-query-editor
```

### 2. Create and Configure `.env` File

Create a `.env` file at the root of your project directory with the following configuration:

```env
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

Replace these values with your actual PostgreSQL connection details.

### 3. Install Dependencies

Run the following command to install necessary Python packages:

```bash
pip install psycopg2-binary python-dotenv tabulate pandas openpyxl
```

### 4. Install Tkinter

Tkinter usually comes pre-installed with Python, but if it's missing:

- **Ubuntu/Debian (including WSL):**

```bash
sudo apt update
sudo apt install python3-tk
```

- **Fedora:**

```bash
sudo dnf install python3-tkinter
```

- **Arch Linux:**

```bash
sudo pacman -S tk
```

### 5. (WSL Users Only) X Server Setup

If using WSL, ensure your graphical environment is properly configured:

- Install [VcXsrv](https://sourceforge.net/projects/vcxsrv/) or [Xming](https://sourceforge.net/projects/xming/).
- Start your X server.
- Configure WSL by adding the following lines to `~/.bashrc`:

```bash
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0
export LIBGL_ALWAYS_INDIRECT=1
export XMODIFIERS=@im=none
export GTK_IM_MODULE=xim
export QT_IM_MODULE=xim
```

Then reload bash:

```bash
source ~/.bashrc
```

## Running the Application

Launch the SQL editor GUI with:

```bash
python editor_sql.py
```

## How to Use

- Enter SQL queries directly into the provided text box.
- Alternatively, use the "Load SQL File" button to execute queries from a file.
- Click **"Execute SQL"** to run your queries.
- Results will appear clearly formatted in an interactive table.
- Select a row and use **"Copy Selected Row"** to copy its data to your clipboard.

## Contribution

Feel free to open an issue or pull request to enhance the functionality or interface.

---

Happy querying!

