# Initialize the pages package
from .dashview import dashboard_page
from .transactions import transactions_page, transaction_form, register_callbacks
from .admin import admin_page
from .profile import profile_page

__all__ = ['dashboard_page', 'transactions_page', 'transaction_form', 'register_callbacks', 'admin_page', 'profile_page']
