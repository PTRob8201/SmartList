# SmartList Documentation

**SmartList** is a hierarchical note-taking and task management application built with Streamlit and SQLite. It features Dynalist-style inline editing, nested lists, and a clean tree-based interface.

---

## Table of Contents

1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Features](#features)
4. [Usage Guide](#usage-guide)
5. [Keyboard Shortcuts](#keyboard-shortcuts)
6. [Database](#database)
7. [Troubleshooting](#troubleshooting)
8. [Architecture](#architecture)

---

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/PTRob8201/SmartList.git
   cd SmartList
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the app**
   - Open your browser to `http://localhost:8501`

---

## Getting Started

### First Time Setup

1. Click **"➕ Add New Item"** at the top
2. Enter your first item title
3. Click **"✅ Add Item"**
4. Your item now appears in the list!

### Adding Sub-items

1. Click the **"➕"** button next to any item
2. Type your sub-item title
3. Click **"✓"** to add or **"✕"** to cancel
4. The sub-item appears indented under the parent item

### Example Structure

```
🏠 Home
├─ 🧹 Cleaning
│  ├─ Vacuum living room
│  ├─ Wash dishes
│  └─ Take out trash
├─ 🛒 Shopping
│  ├─ Milk
│  ├─ Bread
│  └─ Eggs
└─ 📝 Work
   ├─ Email client
   └─ Review PR
```

---

## Features

### ✏️ Inline Editing (Dynalist-style)

- **Click on any item** to enter edit mode
- **Type** to modify the text
- **Click 💾** to save your changes
- Changes persist to the database immediately

### 📋 Hierarchical Lists

- Create unlimited nesting levels
- Visual tree structure with `├─` and `└─` connectors
- Easy parent-child relationships

### ✅ Task Completion

- Check the **✓** checkbox to mark items as complete
- Completed items show with ~~strikethrough~~ text
- Completion status is saved automatically

### ➕ Quick Add Sub-items

- Click **"➕"** next to any item to add a child
- Type the sub-item title directly
- Saves instantly to the database

### 🗑️ Delete Items

- Click **"🗑️"** to remove an item
- Cascading delete removes all sub-items
- Action is immediate and permanent

---

## Usage Guide

### Main Interface

```
📝 SmartList
├─ ➕ Add New Item (button)
├─ Your List
│  ├─ Item 1          [✓] [Item Text] [➕] [🗑️]
│  │  ├─ Sub-item 1
│  │  └─ Sub-item 2
│  └─ Item 2
└─ Quick Guide (footer)
```

### Step-by-Step Workflow

#### Adding a Root Item

1. Click **"➕ Add New Item"** at the top
2. A form appears with an input field
3. Type your item title
4. Click **"✅ Add Item"** to create
5. Item appears in the list

#### Adding a Sub-item

1. Locate the parent item
2. Click the **"➕"** button on the right
3. An inline form appears below the parent
4. Type the sub-item title
5. Click **"✓"** to confirm
6. Cancel with **"✕"** if needed

#### Editing an Item

1. Click on the item text (or click the hidden edit button)
2. The item becomes an editable text field
3. Modify the text as needed
4. Click **"💾"** to save
5. Changes appear immediately

#### Completing a Task

1. Click the **"✓"** checkbox next to the item
2. The item text shows with ~~strikethrough~~
3. The checkbox remains checked
4. Click again to mark as incomplete

#### Deleting an Item

1. Click the **"🗑️"** button
2. The item is immediately deleted
3. All sub-items are also removed
4. ⚠️ This action cannot be undone

### Example: Building a Project Plan

```
1. Click "➕ Add New Item"
2. Type "Website Redesign" → Add Item
3. Click "➕" next to "Website Redesign"
4. Type "Design mockups" → Click ✓
5. Click "➕" next to "Design mockups"
6. Type "Desktop layout" → Click ✓
7. Add more sub-items as needed
8. Check off items as you complete them
```

Result:
```
Website Redesign
└─ Design mockups
   └─ Desktop layout
```

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Edit item | Click on item text |
| Save edit | Click 💾 button |
| Add sub-item | Click ➕ button |
| Delete item | Click 🗑️ button |
| Toggle complete | Click ✓ checkbox |
| Cancel edit | Refresh page or navigate away |

---

## Database

### SQLite Schema

SmartList uses SQLite with the following table structure:

```sql
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    parent_id INTEGER,
    completed BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES items(id)
);
```

### Database Location

- **File**: `smartlist.db` (created in the app directory)
- **Auto-created**: On first run
- **Persistent**: Data survives app restarts

### Backing Up Your Data

```bash
# Copy the database file for backup
cp smartlist.db smartlist_backup.db

# Or export to CSV (using sqlite3)
sqlite3 smartlist.db ".mode csv" ".output backup.csv" "SELECT * FROM items;"
```

---

## Troubleshooting

### App won't start

**Problem**: `ModuleNotFoundError: No module named 'streamlit'`

**Solution**:
```bash
pip install -r requirements.txt
```

### Items not saving

**Problem**: Items disappear after refresh

**Solution**:
- Check that `smartlist.db` exists in the app directory
- Ensure database permissions are correct
- Restart the app: `streamlit run app.py`

### Editing not working

**Problem**: Can't enter edit mode

**Solution**:
- Refresh the page (Ctrl+R or Cmd+R)
- Clear browser cache
- Restart Streamlit

### Sub-items not appearing

**Problem**: Added sub-items but don't see them

**Solution**:
- Refresh the page
- Check parent item has correct ID
- Ensure database query is working

### Database locked

**Problem**: `database is locked` error

**Solution**:
- Close all other connections to `smartlist.db`
- Restart the Streamlit app
- Check file permissions

---

## Architecture

### File Structure

```
SmartList/
├── app.py                 # Main Streamlit application
├── database.py            # SQLite database functions
├── requirements.txt       # Python dependencies
├── smartlist.db          # SQLite database (auto-created)
└── README.md             # Project documentation
```

### Key Components

#### `app.py` - Main Application

- **Page Config**: Streamlit setup and styling
- **Session State**: Manages editing and adding modes
- **Display Logic**: Recursive tree rendering
- **User Interaction**: Buttons, checkboxes, text inputs

#### `database.py` - Database Layer

Key functions:
- `init_db()` - Initialize database on startup
- `add_item(title, parent_id)` - Create new item
- `get_items()` - Fetch all items (used for tree rendering)
- `update_item(id, title)` - Edit item text
- `delete_item(id)` - Remove item (cascading)
- `toggle_item(id, completed)` - Mark complete/incomplete

### Data Flow

```
User clicks item
    ↓
Streamlit captures event
    ↓
Session state updates
    ↓
Database function called
    ↓
Database modified
    ↓
Page rerenders with `st.rerun()`
    ↓
User sees changes
```

### Session State Management

```python
st.session_state = {
    'editing_id': None,          # Which item is being edited
    'adding_nested_id': None,    # Which item's sub-form is open
    'show_add_form': False,      # Top-level add form visibility
    'edited_text': {}            # Stores edited text during edit mode
}
```

---

## Development

### Adding New Features

1. **Edit `database.py`** for data layer changes
2. **Edit `app.py`** for UI changes
3. **Test locally**: `streamlit run app.py`
4. **Commit changes**: `git add . && git commit -m "description"`

### Example: Add Due Dates

1. Modify database schema:
   ```sql
   ALTER TABLE items ADD COLUMN due_date DATE;
   ```

2. Update `database.py` functions to handle `due_date`

3. Update `app.py` to display and edit due dates

### Dependencies

- **streamlit** - Web UI framework
- **sqlite3** - Database (built-in)

---

## Performance Tips

- For 1,000+ items, tree rendering may slow down
- Consider adding search/filter features for large lists
- Archive completed items to improve performance
- Use nested items liberally to keep top-level lists short

---

## Future Enhancements

- [ ] Search functionality
- [ ] Drag-and-drop reordering
- [ ] Due dates and priorities
- [ ] Tags and categories
- [ ] Export to PDF/Markdown
- [ ] Collaborative editing
- [ ] Dark mode
- [ ] Keyboard shortcuts (Tab to indent, etc.)

---

## Support

For issues or questions:
1. Check the **Troubleshooting** section above
2. Review the code comments in `app.py` and `database.py`
3. Open an issue on GitHub

---

## License

SmartList is open source. See LICENSE file for details.

---

## Credits

Built with:
- **Streamlit** - Interactive web apps
- **SQLite** - Lightweight database
- **Python** - Programming language

Inspired by **Dynalist** - powerful outliner application

---

**Last Updated**: October 2026  
**Version**: 1.0.0
