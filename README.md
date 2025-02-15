# RepoRocket

RepoRocket is a universal launcher for GitHub applications with Steam Cloud integration. It allows users to search, download, and manage GitHub repositories, providing a seamless experience for running and maintaining applications. RepoRocket also supports Steam Cloud-compatible save file management, ensuring your data is always backed up and synchronized across devices.

## Features
- **Search GitHub Repositories**: Easily search for GitHub repositories directly from the application.
- **Download and Manage Apps**: Download and manage GitHub applications with a user-friendly interface.
- **Steam Cloud Integration**: Sync save files with Steam Cloud for seamless data backup and synchronization.
- **Cross-Platform Support**: Available for both Windows and Linux.

## Setup

### Prerequisites
- Python 3.6 or higher
- Pip (Python package installer)

### Installation
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/reporocket.git
    cd reporocket
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application
To run the application, execute the following command:
```bash
python RepoRocket.py
```

## Building the Application

### Windows
1. **Navigate to the Scripts Directory**:
    ```bash
    cd scripts
    ```

2. **Run the Build Script**:
    ```bat
    build_windows.bat
    ```

### Linux
1. **Navigate to the Scripts Directory**:
    ```bash
    cd scripts
    ```

2. **Run the Build Script**:
    ```bash
    ./build_linux.sh
    ```

## Directory Structure
- `applications/`: Stores downloaded GitHub applications.
- `saves/`: Stores save files for applications, synced with Steam Cloud.
- `img/`: Images for the launcher UI.
- `scripts/`: Build scripts for Windows and Linux.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

![logo](https://github.com/user-attachments/assets/beea4963-f851-4f3f-999f-12923c76f625)
