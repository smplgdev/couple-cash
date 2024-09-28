from notion.api import get_buttons, get_db_props

if __name__ == '__main__':
    get_buttons('Category') # "Type of expenses" || "Category" || "Subcategory" (if Category is Food)
