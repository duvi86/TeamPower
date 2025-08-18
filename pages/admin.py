from dash import dcc, html
from utils.users import USERS

def admin_page(current_user):
    if current_user != 'admin':
        return html.Div([
            html.H3('Admin Page'),
            html.P('Access denied. Only admin can manage users.')
        ])
    user_rows = []
    for uname, info in USERS.items():
        user_rows.append(html.Tr([
            html.Td(uname),
            html.Td(info['role']),
            html.Td([
                dcc.Dropdown(
                    id={'type':'access-dropdown','index':uname},
                    options=[{'label':'read','value':'user'},{'label':'read/write','value':'admin'}],
                    value=info['role'],
                    clearable=False,
                    style={'width':'120px'}
                )
            ])
        ]))
    return html.Div([
        html.H3('User Management'),
        html.Table([
            html.Thead(html.Tr([html.Th('Username'),html.Th('Access'),html.Th('Set Access')])),
            html.Tbody(user_rows)
        ], style={'width':'100%','borderCollapse':'collapse'}),
        html.Div(id='admin-msg', style={'color':'green','marginTop':'10px'})
    ])
