from dash import dcc, html

def login_modal(show, error_msg=None):
    style = {'position':'fixed','top':0,'left':0,'width':'100vw','height':'100vh','zIndex':1001}
    if not show:
        style['display'] = 'none'
        style['pointerEvents'] = 'none'
    else:
        style['pointerEvents'] = 'auto'
    return html.Div([
        html.Div([
            html.H3('Login'),
            dcc.Input(id='login-username', type='text', placeholder='Username', style={'marginBottom':'10px','width':'100%'}),
            dcc.Input(id='login-password', type='password', placeholder='Password', style={'marginBottom':'10px','width':'100%'}),
            html.Button('Login', id='login-btn', n_clicks=0, style={'width':'100%'}),
            html.Button('Cancel', id='cancel-login-btn', n_clicks=0, style={'width':'100%','marginTop':'10px'}),
            html.Div(error_msg or '', style={'color':'red','marginTop':'10px'})
        ], style={'background':'white','padding':'30px','borderRadius':'8px','width':'300px','margin':'auto','marginTop':'100px','boxShadow':'0 2px 8px rgba(0,0,0,0.2)'}),
        html.Div(style={'position':'fixed','top':0,'left':0,'width':'100vw','height':'100vh','background':'rgba(0,0,0,0.3)','zIndex':1000,'pointerEvents':'none'})
    ], style=style)
