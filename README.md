# AKC - Authentik CLI Client

A command-line interface for managing Authentik resources.

## Getting Started

### Prerequisites

- Python 3.10+

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/user/akc.git
    cd akc
    ```

2.  **Create a virtual environment:**

    ```bash
    make venv
    ```

3.  **Activate the virtual environment:**

    ```bash
    source .venv/bin/activate
    ```

4.  **Install dependencies:**

    ```bash
    make deps
    ```

5.  **Install the project in editable mode:**

    ```bash
    make install
    ```

## Initialization

Before using the CLI, you need to initialize it with your Authentik URL and API token.

```bash
akc init --url <your-authentik-url> --token <your-api-token>
```

## Command Options

### User Management (`akc user`)

*   `create <username> <email> [--first-name <first-name>] [--last-name <last-name>] [--is-active] [--is-superuser]`
*   `list [--output <table|json>]`
*   `update <user-id> [--username <username>] [--email <email>] [--first-name <first-name>] [--last-name <last-name>] [--is-active/--not-active] [--is-superuser/--not-superuser]`
*   `delete <user-id>`

### Group Management (`akc group`)

*   `create <name>`
*   `list [--output <table|json>]`
*   `update <group-id> --name <name>`
*   `delete <group-id>`

### Role Management (`akc role`)

*   `create <name>`
*   `list [--output <table|json>]`
*   `update <role-id> --name <name>`
*   `delete <role-id>`

### Application Management (`akc application`)

*   `create <name> <slug> [--type <type>]`
*   `list [--output <table|json>]`
*   `update <app-id> [--name <name>] [--slug <slug>] [--type <type>]`
*   `delete <app-id>`

### User-Group Management (`akc user-group`)

*   `add <user-id> <group-id>`
*   `remove <user-id> <group-id>`

### User-Role Management (`akc user-role`)

*   `add <user-id> <role-id>`
*   `remove <user-id> <role-id>`

### Provider Management (`akc provider`)

*   `create-proxy <name> <authorization-flow> <external-host>`
*   `list [--output <table|json>]`
*   `update <provider-id> --name <name>`
*   `delete <provider-id>`

### Core Management (`akc core`)

*   `get-version`
*   `list-tenants [--output <table|json>]`
*   `create-tenant <schema-name> [--name <name>] [--domain <domain>]`
*   `get-tenant <tenant-uuid>`
*   `delete-tenant <tenant-uuid>`

### Outpost Management (`akc outpost`)

*   `list [--output <table|json>]`
*   `get <uuid>`
*   `delete <uuid>`
*   `health <uuid>`

### Event Management (`akc event`)

*   `list [--output <table|json>]`
*   `get <uuid>`

### Property Mapping Management (`akc propertymapping`)

*   `list [--output <table|json>]`
*   `get <uuid>`
*   `delete <uuid>`

### Policy Management (`akc policy`)

*   `list [--output <table|json>]`
*   `get <uuid>`
*   `delete <uuid>`

### Stage Management (`akc stage`)

*   `list [--output <table|json>]`
*   `get <uuid>`
*   `delete <uuid>`

### Source Management (`akc source`)

*   `list [--output <table|json>]`
*   `get <slug>`
*   `delete <slug>`
