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
5. `add_status <status_id>`
6. `swap_status <col_id> <col_id>`
7. `add_assignee <card_id> <name>`
8. `add_reporter <card_id> <name>`
9. `remove_reporter <card_id>`
10. `remove_assignee <card_id>`
11. `add_priority <card_id> <priority>`
12. `save_state`
13. `sort_priority <reverse>`
14. `add_heading <heading>`
15. `load_board <name>`


