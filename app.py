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

# Sidebar for actions
with st.sidebar:
    st.header("Add New Item")
    parent_id = st.number_input("Parent Item ID (0 for root)", min_value=0, step=1)
    title = st.text_input("Item Title")
    
    if st.button("Add Item", key="add_btn"):
        if title.strip():
            add_item(title, parent_id if parent_id > 0 else None)
            st.success("Item added!")
            st.rerun()
        else:
            st.error("Please enter a title")

# Main content
st.subheader("Your List")

# Get all items
items = get_items()

if not items:
    st.info("No items yet. Add one from the sidebar!")
else:
    # Display items in a hierarchical structure
    def display_items(items, parent_id=None, level=0):
        """Recursively display items in a tree structure"""
        children = [item for item in items if item['parent_id'] == parent_id]
        
        for item in children:
            col1, col2, col3 = st.columns([0.5, 6, 1.5])
            
            with col1:
                # Checkbox for completion
                if st.checkbox("✓", value=item['completed'], key=f"check_{item['id']}"):
                    toggle_item(item['id'], not item['completed'])
                    st.rerun()
            
            with col2:
                # Item title with indentation
                indent = "  " * level
                if item['completed']:
                    st.markdown(f"{indent}~~{item['title']}~~")
                else:
                    st.markdown(f"{indent}**{item['title']}** (ID: {item['id']})")
            
            with col3:
                if st.button("🗑️", key=f"del_{item['id']}", help="Delete item"):
                    delete_item(item['id'])
                    st.rerun()
            
            # Recursively display children
            display_items(items, item['id'], level + 1)
    
    display_items(items)

# Footer
st.divider()
st.markdown("---")
st.caption("💡 Tip: Use the Parent Item ID to create nested lists. Root items have ID > 0.")
