# Digital Key Tracker

A command-line application for managing lost and found items.

## Features

*   **User Registration:** Register new users with different roles (finder, claimer, admin).
*   **Item Logging:** Log new found items with descriptions and locations.
*   **Item Claiming:** Allow users to claim found items.
*   **History Tracking:** View claim history for users.
*   **Admin Controls:** Admins can delete items.
*   **Listing:** List all registered users and all found items.

## Installation

This project requires **Python 3.9** and uses `pipenv` for dependency management.

1.  **Clone the repository:**

    ```bash
    git clone git@github.com:Rubil-Mogere-94/lost_and_found_system.git
    cd lost-and-found-system
    ```

2.  **Install dependencies:**

    Ensure you have `pipenv` installed (`pip install pipenv`). Then, install the project dependencies:

    ```bash
    pipenv install
    ```

    This command will create a virtual environment (using Python 3.9 as specified in `Pipfile`) and install all necessary packages. If you encounter issues with the Python version, you might need to specify it during virtual environment creation (e.g., `pipenv --python 3.9`).

3.  **Initialize the database:**

    The application uses a SQLite database (`key_tracker.db`) which needs to be initialized. Run the main application once to create the database schema. Use `python3` as shown, or `python` if `python3` is not available on your system:

    ```bash
    pipenv run python3 run.py
    ```

    You should see the application's help message, indicating the database has been created.

## Usage

To run the application, use `pipenv run python3 run.py` followed by the desired command and its options. (Note: On some systems, `python` might be used instead of `python3`.)

For example, to list all registered users:

```bash
pipenv run python run.py list-users
```

### Example Usage

To register a new user named "Alice Smith" with the email "alice@example.com" and the role "finder":

```bash
pipenv run python run.py register --name "Alice Smith" --email "alice@example.com" --role finder
```

### End-to-End Workflow Example

This example demonstrates a typical flow: registering a user, logging a found item, and then listing all items.

1.  **Register a new user (e.g., a finder):**

    ```bash
    pipenv run python run.py register --name "apex moghe" --email "
apex.moghe@gmail.com" --role finder
    ```

2.  **Log a new found item (using the user ID from the previous step):**

    (Note: Replace `[USER_ID]` with the actual ID returned after registering the user.)

    ```bash
pipenv run python run.py log-item --user-id [USER_ID] --description "Blue backpack" --location "Library"
    ```

3.  **List all items to verify the logged item:**

    ```bash
pipenv run python run.py list-items
    ```

4.  **List all users to verify the registered user:**

    ```bash
pipenv run python run.py list-users
    ```

## Commands

*   `register`: Registers a new user in the system. This command is used to create accounts for individuals who will either find items (`finder`), claim items (`claimer`), or manage the system (`admin`).
    *   `--name`: (Required) The full name of the user.
    *   `--email`: (Required) The unique email address of the user.
    *   `--role`: (Required) The role of the user. Must be one of: `finder`, `claimer`, or `admin`.

*   `log-item`: Logs a newly found item into the system. This command records details about an item that has been discovered.
    *   `--user-id`: (Required) The ID of the user who found the item. This user must already be registered in the system.
    *   `--description`: (Required) A brief description of the found item (e.g., "Blue backpack", "Silver watch").
    *   `--location`: (Required) The location where the item was found (e.g., "Library", "Cafeteria").

*   `claim`: Allows a user to claim a previously logged item. Once an item is claimed, its status is updated in the system.
    *   `--item-id`: (Required) The ID of the item to be claimed.
    *   `--user-id`: (Required) The ID of the user who is claiming the item. This user must already be registered in the system.

*   `history`: Displays the history of items claimed by a specific user. This helps track what items a user has successfully claimed.
    *   `--user-id`: (Required) The ID of the user whose claim history you want to view.

*   `delete`: Deletes an item from the system. This action can only be performed by users with the `admin` role, ensuring data integrity and control.
    *   `--item-id`: (Required) The ID of the item to be deleted.
    *   `--user-id`: (Required) The ID of an admin user who is performing the deletion.

*   `list-users`: Lists all registered users in the system, displaying their ID, name, email, and assigned role.

*   `list-items`: Lists all items currently logged in the system, including their description, location, and current status (claimed or unclaimed).

## Database

The application uses a SQLite database named `key_tracker.db`, which is created in the root directory of the project upon first run or database initialization.

## Seed the database

To populate the database with initial sample data for testing or demonstration purposes, you can run the `seed.py` script:

```bash
pipenv run python seed.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.