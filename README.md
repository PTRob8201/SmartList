# SmartList

A hierarchical note-taking and task management app built with **Streamlit** and **SQLite**.

## Features

✅ **Nested/Hierarchical Lists** - Create tasks with subtasks  
✅ **Check Off Tasks** - Mark items as completed  
✅ **Add/Delete Items** - Simple list management  
✅ **SQLite Database** - Persistent data storage  
✅ **Clean UI** - Minimal and intuitive interface  

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/PTRob8201/SmartList.git
cd SmartList
```

### 2. Create a Virtual Environment
```bash
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use

1. **Add Items**: Use the sidebar to add new items
2. **Parent ID**: 
   - Use `0` or leave empty for root-level items
   - Use an existing item's ID to create nested subtasks
3. **Check Off Tasks**: Click the checkbox to mark items as complete
4. **Delete Items**: Click the trash icon to remove an item
5. **View IDs**: Each item shows its ID for creating nested items

## Example Workflow

```
1. Add "Shopping" (Parent ID: 0)
2. Add "Milk" (Parent ID: 1)
3. Add "Bread" (Parent ID: 1)
4. Add "Eggs" (Parent ID: 1)
```

This creates a hierarchical structure:
```
Shopping
├── Milk
├── Bread
└── Eggs
```

## Database

- **Database File**: `smartlist.db` (created automatically)
- **Database Type**: SQLite
- **Storage**: Local file-based

## Testing on iPad

### Option 1: Deploy to Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub and deploy
4. Access from any device with a browser

### Option 2: Local Network
1. Run the app on your computer
2. Find your computer's IP address
3. On iPad, visit: `http://YOUR_IP:8501`

## Future Enhancements

- [ ] Edit existing items
- [ ] Search functionality
- [ ] Tags and categories
- [ ] Due dates
- [ ] Export to PDF/JSON
- [ ] Dark mode

## License

MIT License

## Contributing

Feel free to fork and submit pull requests!

---

**Built with ❤️ using Streamlit and SQLite**
