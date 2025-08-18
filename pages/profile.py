from dash import dcc, html
from utils.users import USERS

def profile_page(current_user):
    if not current_user:
        return html.Div([
            html.H3('Profile'),
            html.P('You must be logged in to view your profile.')
        ])
    user_info = USERS.get(current_user, {})
    return html.Div([
        html.H3('Profile'),
        html.P(f'Username: {current_user}'),
        html.P(f'Role: {user_info.get("role", "user")}'),
        html.H4('Change Password'),
        dcc.Input(id='new-password', type='password', placeholder='New Password', style={'marginBottom':'10px','width':'300px'}),
        html.Button('Update Password', id='update-password-btn', n_clicks=0),
        html.Div(id='profile-msg', style={'color':'green','marginTop':'10px'})
    ])
