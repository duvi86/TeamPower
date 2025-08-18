

from dash import dcc, html, Input, Output, State
from dash import dash_table
from datetime import datetime
from utils.db import get_transactions_df, add_transaction
import pandas as pd

# Color scheme
COLORS = {
    'primary': '#2E86C1',      # Blue
    'secondary': '#2C3E50',    # Dark blue-gray
    'success': '#27AE60',      # Green
    'warning': '#F1C40F',      # Yellow
    'danger': '#E74C3C',       # Red
    'light': '#F8F9F9',       # Light gray
    'white': '#FFFFFF',
    'border': '#E0E0E0',
    'text': '#2C3E50',
    'textLight': '#7F8C8D'
}

# Shared styles
CARD_STYLE = {
    'background': COLORS['white'],
    'borderRadius': '12px',
    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
    'padding': '24px',
    'marginBottom': '24px'
}

INPUT_STYLE = {
    'width': '100%',
    'padding': '12px',
    'borderRadius': '6px',
    'border': f'1px solid {COLORS["border"]}',
    'fontSize': '14px',
    'marginTop': '5px',
    'backgroundColor': COLORS['white']
}

LABEL_STYLE = {
    'color': COLORS['text'],
    'fontSize': '14px',
    'fontWeight': '500',
    'marginBottom': '4px'
}

BUTTON_STYLE = {
    'backgroundColor': COLORS['primary'],
    'color': COLORS['white'],
    'padding': '12px 24px',
    'borderRadius': '6px',
    'border': 'none',
    'fontSize': '14px',
    'fontWeight': '600',
    'cursor': 'pointer',
    'transition': 'all 0.3s ease',
    'outline': 'none',
    'hover': {
        'backgroundColor': '#2874A6',
        'transform': 'translateY(-1px)',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
    }
}


def transactions_page():
    df = get_transactions_df()
    
    # Calculate stats
    total_transactions = len(df) if not df.empty else 0
    total_amount = df['Amount'].sum() if not df.empty else 0
    latest_date = df['Date'].max() if not df.empty else 'No transactions'
    
    return html.Div([
        # Header with Stats
        html.Div([
            html.H1('Finance Transaction Center', style={
                'color': COLORS['text'],
                'fontSize': '32px',
                'fontWeight': '600',
                'textAlign': 'center',
                'marginBottom': '32px',
                'letterSpacing': '-0.5px'
            }),
            
            # Stats Cards Row
            html.Div([
                html.Div([
                    html.Div([
                        html.H4('Total Transactions', style={
                            'color': COLORS['text'],
                            'marginBottom': '8px',
                            'fontSize': '16px'
                        }),
                        html.H2(f"{total_transactions:,}", style={
                            'color': COLORS['primary'],
                            'margin': '0',
                            'fontSize': '28px',
                            'fontWeight': '600'
                        })
                    ], style=CARD_STYLE),
                    
                    html.Div([
                        html.H4('Total Amount', style={
                            'color': COLORS['text'],
                            'marginBottom': '8px',
                            'fontSize': '16px'
                        }),
                        html.H2(f"${total_amount:,.2f}", style={
                            'color': COLORS['success'],
                            'margin': '0',
                            'fontSize': '28px',
                            'fontWeight': '600'
                        })
                    ], style=CARD_STYLE),
                    
                    html.Div([
                        html.H4('Latest Entry', style={
                            'color': COLORS['text'],
                            'marginBottom': '8px',
                            'fontSize': '16px'
                        }),
                        html.H2(str(latest_date).split()[0], style={
                            'color': COLORS['warning'],
                            'margin': '0',
                            'fontSize': '28px',
                            'fontWeight': '600'
                        })
                    ], style=CARD_STYLE)
                ], style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(3, 1fr)',
                    'gap': '24px',
                    'marginBottom': '32px'
                })
            ]),
            
            # Main Content Grid
            html.Div([
                # Left Column - Form
                html.Div([
                    transaction_form()
                ], style={'flex': '1'}),
                
                # Right Column - Table
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3('Transaction History', style={
                                'color': COLORS['text'],
                                'margin': '0',
                                'fontSize': '20px',
                                'fontWeight': '600'
                            }),
                            html.Button(
                                '⬇ Export CSV',
                                id='download-button',
                                style=BUTTON_STYLE
                            )
                        ], style={
                            'display': 'flex',
                            'justifyContent': 'space-between',
                            'alignItems': 'center',
                            'marginBottom': '16px'
                        }),
                        
                        dash_table.DataTable(
                            id='transactions-table',
                            data=df.to_dict('records'),
                            columns=[{'name': i, 'id': i} for i in df.columns],
                            page_size=10,
                            style_header={
                                'backgroundColor': COLORS['secondary'],
                                'color': COLORS['white'],
                                'fontWeight': '600',
                                'textAlign': 'left',
                                'padding': '12px',
                                'fontSize': '14px'
                            },
                            style_cell={
                                'textAlign': 'left',
                                'padding': '12px',
                                'fontSize': '13px',
                                'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
                            },
                            style_data={
                                'backgroundColor': COLORS['white'],
                                'color': COLORS['text']
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': COLORS['light']
                                }
                            ],
                            sort_action='native',
                            filter_action='native',
                            row_selectable='multi',
                            selected_rows=[],
                            page_action='native',
                            style_table={
                                'overflowX': 'auto',
                                'border': f'1px solid {COLORS["border"]}',
                                'borderRadius': '6px'
                            }
                        ),
                        
                        html.Div(id='transaction-msg', style={
                            'marginTop': '16px',
                            'padding': '12px',
                            'borderRadius': '6px',
                            'backgroundColor': f'{COLORS["success"]}20',
                            'color': COLORS['success'],
                            'fontWeight': '500',
                            'display': 'none'
                        })
                    ], style=CARD_STYLE)
                ], style={'flex': '2'})
            ], style={
                'display': 'flex',
                'gap': '24px',
                'alignItems': 'flex-start'
            })
        ])
    ], style={
        'padding': '32px',
        'maxWidth': '1600px',
        'margin': '0 auto',
        'backgroundColor': COLORS['light'],
        'minHeight': '100vh'
    })

# Transaction form layout
def transaction_form():
    return html.Div([
        html.H3('New Transaction Entry', style={
            'color': COLORS['text'],
            'marginTop': '0',
            'marginBottom': '24px',
            'textAlign': 'center',
            'fontSize': '24px',
            'fontWeight': '600'
        }),
        
        # Two-column Form Layout
        html.Div([
            # Left Column
            html.Div([
                html.Div([
                    html.Label('Transaction Date *', style=LABEL_STYLE),
                    dcc.DatePickerSingle(
                        id='date',
                        date=datetime.today().strftime('%Y-%m-%d'),
                        min_date_allowed='2025-01-01',
                        max_date_allowed='2025-12-31',
                        style={'width': '100%'},
                        calendar_orientation='horizontal',
                        display_format='YYYY-MM-DD',
                        placeholder='Select date'
                    )
                ], style={'marginBottom': '16px'}),
                
                *[html.Div([
                    html.Label(f'{label} *', style=LABEL_STYLE),
                    dcc.Input(
                        id=id_,
                        type=type_,
                        placeholder=f'Enter {label}',
                        style=INPUT_STYLE,
                        **extra_props
                    )
                ], style={'marginBottom': '16px'}) for label, id_, type_, extra_props in [
                    ('Cost Center Project', 'ccp', 'text', {}),
                    ('Cost Center SOW', 'ccs', 'text', {}),
                ]]
            ], style={'flex': '1', 'marginRight': '20px'}),
            
            # Right Column
            html.Div([
                *[html.Div([
                    html.Label(f'{label} *', style=LABEL_STYLE),
                    dcc.Input(
                        id=id_,
                        type=type_,
                        placeholder=f'Enter {label}',
                        style=INPUT_STYLE,
                        **extra_props
                    )
                ], style={'marginBottom': '16px'}) for label, id_, type_, extra_props in [
                    ('SOW Number', 'sow', 'text', {}),
                    ('PO Number', 'po', 'text', {}),
                    ('Amount ($)', 'amount', 'number', {'min': 0, 'step': '0.01'})
                ]]
            ], style={'flex': '1'})
        ], style={
            'display': 'flex',
            'gap': '24px',
            'marginBottom': '24px'
        }),
        
        html.Div([
            html.Label('Category *', style=LABEL_STYLE),
            dcc.Dropdown(
                id='category',
                options=[{'label': c, 'value': c} for c in ['Budget', 'Planned', 'Consumed']],
                value='Budget',
                style={
                    'borderRadius': '6px',
                    'marginTop': '5px',
                    'border': f'1px solid {COLORS["border"]}'
                }
            )
        ], style={'marginBottom': '16px'}),
        
        html.Div([
            html.Label('Type *', style=LABEL_STYLE),
            dcc.Dropdown(
                id='type',
                options=[{'label': t, 'value': t} for t in ['OPEX', 'CAPEX']],
                value='OPEX',
                style={
                    'borderRadius': '6px',
                    'marginTop': '5px',
                    'border': f'1px solid {COLORS["border"]}'
                }
            )
        ], style={'marginBottom': '24px'}),
        
        html.Button(
            'Add Transaction',
            id='add-btn',
            n_clicks=0,
            style=BUTTON_STYLE
        ),
        
        html.Div(
            '* Required fields',
            style={
                'color': COLORS['textLight'],
                'fontSize': '12px',
                'marginTop': '16px',
                'textAlign': 'center'
            }
        )
    ], style=CARD_STYLE)

# Callback for form and table update
def register_callbacks(app):
    @app.callback(
        Output('transactions-table', 'data'),
        Output('transaction-msg', 'children'),
        Output('transaction-msg', 'style'),
        Output('url', 'pathname'),
        Input('add-btn', 'n_clicks'),
        State('date', 'date'),
        State('ccp', 'value'),
        State('ccs', 'value'),
        State('sow', 'value'),
        State('po', 'value'),
        State('amount', 'value'),
        State('category', 'value'),
        State('type', 'value'),
        prevent_initial_call=True
    )
    def add_transaction_callback(n_clicks, date, ccp, ccs, sow, po, amount, category, type_):
        msg = ''
        msg_style = {
            'marginTop': '16px',
            'padding': '12px',
            'borderRadius': '6px',
            'fontWeight': '500',
            'display': 'block'
        }
        
        if n_clicks:
            if all([date, ccp, ccs, sow, po, amount, category, type_]):
                try:
                    add_transaction(date, ccp, ccs, sow, po, amount, category, type_)
                    msg = '✓ Transaction added successfully!'
                    msg_style.update({
                        'backgroundColor': f'{COLORS["success"]}20',
                        'color': COLORS['success']
                    })
                    df = get_transactions_df()
                    return df.to_dict('records'), msg, msg_style, '/'
                except Exception as e:
                    msg = f'⚠ Error: {str(e)}'
                    msg_style.update({
                        'backgroundColor': f'{COLORS["danger"]}20',
                        'color': COLORS['danger']
                    })
            else:
                msg = '⚠ Please fill all required fields'
                msg_style.update({
                    'backgroundColor': f'{COLORS["warning"]}20',
                    'color': COLORS['warning']
                })
        
        df = get_transactions_df()
        return df.to_dict('records'), msg, msg_style, '/transactions'
