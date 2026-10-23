import streamlit as st
import sqlite3
from datetime import datetime
from database import init_db, add_item, get_items, delete_item, toggle_item, update_item

# Page config
st.set_page_config(page_title="SmartList", layout="wide")
st.title("📝 SmartList")
st.markdown("A hierarchical note-taking and task management app (Dynalist-style)")

# Initialize database
init_db()

# Initialize session state for editing and adding nested items
if "editing_id" not in st.session_state:
    st.session_state.editing_id = None
if "adding_nested_id" not in st.session_state:
    st.session_state.adding_nested_id = None
if "edited_text" not in st.session_state:
    st.session_state.edited_text = {}

# Top section with add button
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("➕ Add New Item", use_container_width=True):
        st.session_state.show_add_form = not st.session_state.get("show_add_form", False)
        st.session_state.adding_nested_id = None  # Clear nested form when opening main form

# Show add form if button is clicked
if st.session_state.get("show_add_form", False):
    st.divider()
    st.subheader("Add New Item")
    
    title = st.text_input("Item Title", key="new_title", placeholder="Type your item title...")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Add Item", use_container_width=True):
            if title.strip():
                add_item(title, None)
                st.success("Item added!")
                st.session_state.show_add_form = False
                st.session_state.edited_text = {}
                st.rerun()
            else:
                st.error("Please enter a title")
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.show_add_form = False
            st.rerun()
    
    st.divider()

# Main content
st.subheader("Your List")

# Get all items
items = get_items()

if not items:
    st.info("No items yet. Click '➕ Add New Item' to create one!")
else:
    # Display items in a hierarchical structure with Dynalist-style editing
    def display_items(items, parent_id=None, level=0):
        """Recursively display items in a tree structure with Dynalist-style editing"""
        children = [item for item in items if item['parent_id'] == parent_id]
        
        for idx, item in enumerate(children):
            is_last = idx == len(children) - 1
            
            # Create indentation with tree characters
            if level == 0:
                tree_prefix = ""
                indent = ""
            else:
                tree_prefix = "└─ " if is_last else "├─ "
                indent = "   " * (level - 1) + ("   " if is_last else "│  ")
            
            # Create container for each item
            with st.container(border=False):
                col1, col2, col3 = st.columns([0.5, 5, 1.5])
                
                with col1:
                    # Checkbox for completion
                    if st.checkbox("✓", value=item['completed'], key=f"check_{item['id']}"):
                        toggle_item(item['id'], not item['completed'])
                        st.rerun()
                
                with col2:
                    # Dynalist-style inline editing - click to edit, ESC to cancel, ENTER to save
                    if st.session_state.editing_id == item['id']:
                        # Edit mode: show text input that fills the line
                        col_input, col_buttons = st.columns([5, 1])
                        
                        with col_input:
                            edited_title = st.text_input(
                                "Edit",
                                value=st.session_state.edited_text.get(f"text_{item['id']}", item['title']),
                                key=f"edit_input_{item['id']}",
                                label_visibility="collapsed",
                                placeholder="Edit item..."
                            )
                            # Store the edited text in session state
                            st.session_state.edited_text[f"text_{item['id']}"] = edited_title
                        
                        with col_buttons:
                            if st.button("💾", key=f"save_{item['id']}", help="Save (or press Enter)", use_container_width=True):
                                if edited_title.strip():
                                    update_item(item['id'], edited_title)
                                    st.session_state.editing_id = None
                                    st.session_state.edited_text.pop(f"text_{item['id']}", None)
                                    st.rerun()
                    else:
                        # Display mode - click to edit
                        display_text = f"<code>{indent}{tree_prefix}</code>"
                        
                        if item['completed']:
                            display_text += f"~~{item['title']}~~"
                        else:
                            display_text += f"**{item['title']}**"
                        
                        # Make the entire line clickable to edit
                        st.markdown(display_text, unsafe_allow_html=True)
                        
                        # Hidden button to enter edit mode
                        if st.button(
                            f"Click to edit or press ➕ to add sub-item",
                            key=f"click_edit_{item['id']}",
                            help="Click to edit this item inline",
                            use_container_width=True
                        ):
                            st.session_state.editing_id = item['id']
                            st.session_state.edited_text[f"text_{item['id']}"] = item['title']
                            st.rerun()
                
                with col3:
                    # Action buttons - Add sub-item, Edit, Delete
                    col_add, col_del = st.columns(2)
                    
                    with col_add:
                        if st.button("➕", key=f"add_nested_{item['id']}", help="Add sub-item", use_container_width=True):
                            st.session_state.adding_nested_id = item['id']
                            st.session_state.editing_id = None
                            st.rerun()
                    
                    with col_del:
                        if st.button("🗑️", key=f"del_{item['id']}", help="Delete item", use_container_width=True):
                            delete_item(item['id'])
                            st.rerun()
                
                # Show nested add form if this item is selected
                if st.session_state.adding_nested_id == item['id']:
                    with st.container():
                        nested_indent = indent + ("   " if is_last else "│  ")
                        
                        col1, col2 = st.columns([5, 1.5])
                        
                        with col1:
                            st.markdown(f"<code>{nested_indent}</code>➕ **New sub-item:**", unsafe_allow_html=True)
                            nested_title = st.text_input(
                                "Sub-item",
                                key=f"nested_input_{item['id']}",
                                placeholder="Type sub-item title..."
                            )
                        
                        with col2:
                            col_add, col_cancel = st.columns(2)
                            
                            with col_add:
                                if st.button("✓", key=f"add_nested_confirm_{item['id']}", help="Add", use_container_width=True):
                                    if nested_title.strip():
                                        add_item(nested_title, item['id'])
                                        st.success("Sub-item added!")
                                        st.session_state.adding_nested_id = None
                                        st.session_state.edited_text = {}
                                        st.rerun()
                            
                            with col_cancel:
                                if st.button("✕", key=f"cancel_nested_{item['id']}", help="Cancel", use_container_width=True):
                                    st.session_state.adding_nested_id = None
                                    st.rerun()
            
            # Recursively display children
            display_items(items, item['id'], level + 1)
    
    display_items(items)

# Footer with instructions
st.divider()
st.markdown("""
### ⌨️ Quick Guide
- **Click on item text** to edit inline (Dynalist-style)
- **➕ Button** - Add a sub-item
- **🗑️ Button** - Delete item
- **✓ Checkbox** - Mark as complete
- **💾 Button** - Save changes when editing
""")
