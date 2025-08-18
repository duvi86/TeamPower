from dash import dcc, html

def top_bar(username=None):
    links = [
        dcc.Link('Dashboard', href='/', style={'color':'white','marginRight':'20px'}),
        dcc.Link('Transactions', href='/transactions', style={'color':'white','marginRight':'20px'})
    ]
    if username:
        links.append(dcc.Link('Profile', href='/profile', style={'color':'white'}))
    html_links = html.Div(links + [
        html.Span([
            html.Img(id='user-icon', src='https://img.icons8.com/material-outlined/24/ffffff/user.png', style={'verticalAlign':'middle','marginLeft':'30px','cursor':'pointer'}),
            html.Span(username or '', style={'color':'white','marginLeft':'10px'})
        ])
    ], style={'display':'flex','alignItems':'center'})
    return html.Div([
        html.Div('TeamPower Finance Dashboard', style={'color':'white','fontSize':24,'fontWeight':'bold'}),
        html_links
    ], style={'backgroundColor':'#003366','padding':'10px 20px','display':'flex','alignItems':'center','justifyContent':'space-between'})
