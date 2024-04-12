# Python Kanban Board

This is a simple Kanban board implemented in Python. It allows users to manage tasks across different stages of completion using a command-line interface.

![image](https://github.com/polyesterswing/kanban/assets/67583328/8d3fde5d-9363-4765-9aad-0a879e0ee503)

## Requirements
- Textual
```
pip install textual
```

## Usage

1. Run the application using `python main.py`.
2. Follow the on-screen instructions to manage tasks on the board.
3. Use the commands provided to add, move, list, or delete tasks.

## Commands
1. `delete_card <card_id>`
2. `add_card <col_id> <text>`
3. `modify_card <card_id> <text>`
4. `add_status <name>`
5. `swap_status <col_id> <col_id>`
6. `add_assignee <card_id> <name>`
7. `add_reporter <card_id> <name>`
8. `remove_reporter <card_id>`
9. `remove_assignee <card_id>`
10. `add_priority <card_id> <priority>`
11. `save_state`
12. `sort_priority <reverse>`
13. `add_heading <heading>`
14. `load_board <name>`

## To-Do
1. Indication when command is incorrect
2. Help Menu, with information about all commands

