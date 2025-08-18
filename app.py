

# --- Dash (Plotly) Webapp ---
import dash
from dash import dcc, html, Input, Output, State
from dash.dependencies import ALL
from dash import ctx
import dash.exceptions

from components.top_bar import top_bar
from components.login_modal import login_modal
from pages.dashview import dashboard_page
from pages.transactions import transactions_page, transaction_form, register_callbacks
from pages.admin import admin_page
from pages.profile import profile_page
from utils.users import USERS


app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = 'TeamPower Finance Dashboard'
register_callbacks(app)

# --- Store login state ---
app._user = None
app._show_login = False
app._login_error = None

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(top_bar(), id='top-bar'),
    html.Div(id='page-content'),
    html.Div(login_modal(False), id='login-modal-container'),
    dcc.Download(id='download-dataframe-csv')
])

# --- Top Bar and Login Modal Callback ---
@app.callback(
    Output('top-bar', 'children'),
    Output('login-modal-container', 'children'),
    Input('user-icon', 'n_clicks'),
    Input('login-btn', 'n_clicks'),
    Input('cancel-login-btn', 'n_clicks'),
    Input('url', 'pathname'),
    State('login-username', 'value'),
    State('login-password', 'value'),
)
def handle_login(user_icon_click=None, login_click=None, cancel_click=None, pathname=None, username=None, password=None):
    trigger = ctx.triggered_id if ctx.triggered_id else None
    # Always allow login modal to open
    if trigger == 'user-icon':
        app._show_login = True
        app._login_error = None
    elif trigger == 'login-btn':
        user = USERS.get(username)
        if user and user['password'] == password:
            app._user = username
            app._show_login = False
            app._login_error = None
        else:
            app._login_error = 'Invalid credentials.'
            app._show_login = True
    elif trigger == 'cancel-login-btn':
        app._show_login = False
        app._login_error = None
    return top_bar(app._user), login_modal(app._show_login, app._login_error)

# --- Unified Page Content Callback ---
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
)
def display_page(pathname):
    user = app._user
    # Handle routing
    if pathname == '/profile':
        return profile_page(user)
    elif pathname == '/admin':
        return admin_page(user)
    elif pathname == '/transactions':
        return transactions_page()
    else:
        return dashboard_page()

# --- Admin Access Change Callback ---
@app.callback(
    Output('admin-msg', 'children'),
    Input({'type':'access-dropdown','index':ALL}, 'value'),
    State({'type':'access-dropdown','index':ALL}, 'id'),
)
def update_access(values, ids):
    msg = ''
    for v, i in zip(values, ids):
        uname = i['index']
        if uname in USERS:
            USERS[uname]['role'] = v
            msg += f"Updated {uname} to {v}. "
    return msg

# --- Profile Password Update Callback ---
@app.callback(
    Output('profile-msg', 'children'),
    Input('update-password-btn', 'n_clicks'),
    State('new-password', 'value'),
)
def update_password(n_clicks, new_password):
    if n_clicks and new_password:
        if app._user and app._user in USERS:
            USERS[app._user]['password'] = new_password
            return 'Password updated!'
    return ''

# --- CSV Download Callbacks ---
@app.callback(
    Output('download-dataframe-csv', 'data'),
    Input('download-button', 'n_clicks'),
    Input('url', 'pathname'),
    prevent_initial_call=True
)
def download_csv(n_clicks, pathname):
    if pathname == '/transactions' and n_clicks:
        from utils.db import get_transactions_df
        df = get_transactions_df()
        return dcc.send_data_frame(df.to_csv, 'transactions.csv', index=False)
    return None

if __name__ == '__main__':
    app.run(debug=False, port=8051)
