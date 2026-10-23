import streamlit as st
import sqlite3
from datetime import datetime
from database import init_db, add_item, get_items, delete_item, toggle_item, update_item

# Page config
st.set_page_config(page_title="SmartList", layout="wide")
st.title("📝 SmartList")
st.markdown("A hierarchical note-taking and task management app")

# Initialize database
init_db()

# Initialize session state for editing
if "editing_id" not in st.session_state:
    st.session_state.editing_id = None

# Top section with add button
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("➕ Add New Item", use_container_width=True):
        st.session_state.show_add_form = not st.session_state.get("show_add_form", False)

# Show add form if button is clicked
if st.session_state.get("show_add_form", False):
    st.divider()
    st.subheader("Add New Item")
    
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("Item Title", key="new_title")
    
    with col2:
        parent_id = st.number_input("Parent Item ID (0 for root)", min_value=0, step=1, key="new_parent_id")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Add Item", use_container_width=True):
            if title.strip():
                add_item(title, parent_id if parent_id > 0 else None)
                st.success("Item added!")
                st.session_state.show_add_form = False
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
    # Display items in a hierarchical structure
    def display_items(items, parent_id=None, level=0):
        """Recursively display items in a tree structure"""
        children = [item for item in items if item['parent_id'] == parent_id]
        
        for item in children:
            col1, col2, col3, col4 = st.columns([0.5, 5, 1, 1.5])
            
            with col1:
                # Checkbox for completion
                if st.checkbox("✓", value=item['completed'], key=f"check_{item['id']}"):
                    toggle_item(item['id'], not item['completed'])
                    st.rerun()
            
            with col2:
                # Item title with indentation and inline editing
                indent = "  " * level
                
                # Check if we're in edit mode for this item
                if st.session_state.editing_id == item['id']:
                    # Edit mode: show text input
                    edited_title = st.text_input(
                        "Edit title",
                        value=item['title'],
                        key=f"edit_input_{item['id']}",
                        label_visibility="collapsed"
                    )
                else:
                    # Display mode
                    if item['completed']:
                        st.markdown(f"{indent}~~{item['title']}~~")
                    else:
                        st.markdown(f"{indent}**{item['title']}** (ID: {item['id']})")
            
            with col3:
                # Edit button
                if st.session_state.editing_id == item['id']:
                    # Save button when editing
                    if st.button("💾", key=f"save_{item['id']}", help="Save changes"):
                        edited_title = st.session_state.get(f"edit_input_{item['id']}", item['title'])
                        if edited_title.strip():
                            update_item(item['id'], edited_title)
                            st.session_state.editing_id = None
                            st.rerun()
                else:
                    # Edit button
                    if st.button("✏️", key=f"edit_{item['id']}", help="Edit item"):
                        st.session_state.editing_id = item['id']
                        st.rerun()
            
            with col4:
                col_delete, col_cancel = st.columns(2)
                
                with col_delete:
                    if st.button("🗑️", key=f"del_{item['id']}", help="Delete item"):
                        delete_item(item['id'])
                        st.rerun()
                
                with col_cancel:
                    if st.session_state.editing_id == item['id']:
                        if st.button("✕", key=f"cancel_{item['id']}", help="Cancel editing"):
                            st.session_state.editing_id = None
                            st.rerun()
            
            # Recursively display children
            display_items(items, item['id'], level + 1)
    
    display_items(items)

# Footer
st.divider()
st.caption("💡 Tip: Click ✏️ to edit items inline, click 💾 to save. Use the Parent Item ID to create nested lists.")
