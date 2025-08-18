import dash
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
from utils.db import get_transactions_df
from dash.dependencies import Input, Output

def dashboard_page():
    """Main dashboard page function that renders the dashboard layout"""
    # Color sche                    style={'height': '450px'}
                )
            ], style={
                'flex': 1,
                'background': 'white',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'height': '550px',
                'overflow': 'hidden'
            }),lors = {
        'Budget': '#2E86C1',      # Strong blue
        'Planned': '#F1C40F',     # Warm yellow
        'Consumed': '#E74C3C',    # Bright red
        'OPEX': '#27AE60',        # Rich green
        'CAPEX': '#8E44AD',       # Deep purple
        'background': '#F8F9F9',  # Light gray
        'text': '#2C3E50'         # Dark blue-gray
    }
    
    df = get_transactions_df()
    # Ensure all expected columns exist
    expected_cols = ['Date','Cost Center Project','Cost Center SOW','SOW Number','PO','Amount','Category','Type']
    for col in expected_cols:
        if col not in df.columns:
            df[col] = None
    
    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Create full year date range
    year_start = pd.Timestamp('2025-01-01')
    year_end = pd.Timestamp('2025-12-31')
    
    total_budget = df[df['Category']=='Budget']['Amount'].sum() if not df.empty else 0
    total_planned = df[df['Category']=='Planned']['Amount'].sum() if not df.empty else 0
    total_consumed = df[df['Category']=='Consumed']['Amount'].sum() if not df.empty else 0
    funding_gap = total_consumed - total_budget
    
    if not df.empty:
        # Create full year date range with all dates
        date_range = pd.date_range(start=year_start, end=year_end, freq='D')
        
        # Create cumulative sums for each category
        categories = ['Budget', 'Planned', 'Consumed']
        ytd_data = []
        
        for category in categories:
            cat_data = df[df['Category'] == category].copy()
            if not cat_data.empty:
                daily_sums = cat_data.groupby('Date')['Amount'].sum()
                cumsum = daily_sums.reindex(date_range, fill_value=0).cumsum()
                ytd_data.append(pd.DataFrame({category: cumsum}))
        
        ytd = pd.concat(ytd_data, axis=1).fillna(method='ffill').fillna(0)
        
        # Create full year monthly range including December
        all_months = pd.date_range(start=year_start, end=pd.Timestamp('2025-12-01'), freq='MS')
        
        # Monthly aggregation by type with all months
        monthly_data = df.groupby([df['Date'].dt.strftime('%Y-%m'), 'Type'])['Amount'].sum().unstack(fill_value=0)
        
        # Reindex to include all months with proper month names
        month_index = [d.strftime('%Y-%m') for d in all_months]
        monthly = pd.DataFrame(index=month_index, columns=['OPEX', 'CAPEX']).fillna(0)
        if not monthly_data.empty:
            monthly.update(monthly_data)
    else:
        ytd = pd.DataFrame(index=pd.date_range(start=year_start, end=year_end, freq='D'))
        month_index = [d.strftime('%Y-%m') for d in pd.date_range(start=year_start, end=pd.Timestamp('2025-12-01'), freq='MS')]
        monthly = pd.DataFrame(index=month_index, columns=['OPEX', 'CAPEX']).fillna(0)
        
    layout = html.Div([
        html.H2('Key Performance Indicators', 
                style={'color': colors['text'], 
                       'textAlign': 'center',
                       'marginBottom': '30px',
                       'fontSize': '32px',
                       'fontWeight': '600'}),
        
        # KPI Cards Row
        html.Div([
            html.Div([
                html.H4('Total Yearly Budget', style={'color': colors['text'], 'marginBottom': '10px'}),
                html.H3(f"${total_budget:,.0f}", 
                       style={'color': colors['Budget'], 
                             'fontSize': '28px',
                             'fontWeight': 'bold'})
            ], style={'background': 'white', 
                     'padding': '20px', 
                     'borderRadius': '10px',
                     'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                     'flex': 1,
                     'margin': '0 10px',
                     'textAlign': 'center'}),
            html.Div([
                html.H4('Total Planned Consumption', style={'color': colors['text'], 'marginBottom': '10px'}),
                html.H3(f"${total_planned:,.0f}", 
                       style={'color': colors['Planned'],
                             'fontSize': '28px',
                             'fontWeight': 'bold'})
            ], style={'background': 'white', 
                     'padding': '20px', 
                     'borderRadius': '10px',
                     'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                     'flex': 1,
                     'margin': '0 10px',
                     'textAlign': 'center'}),
            html.Div([
                html.H4('Total Actual Consumed', style={'color': colors['text'], 'marginBottom': '10px'}),
                html.H3(f"${total_consumed:,.0f}", 
                       style={'color': colors['Consumed'],
                             'fontSize': '28px',
                             'fontWeight': 'bold'})
            ], style={'background': 'white', 
                     'padding': '20px', 
                     'borderRadius': '10px',
                     'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                     'flex': 1,
                     'margin': '0 10px',
                     'textAlign': 'center'}),
            html.Div([
                html.H4('Funding Gap', style={'color': colors['text'], 'marginBottom': '10px'}),
                html.H3(f"${funding_gap:,.0f}", 
                       style={'color': '#E74C3C' if funding_gap > 0 else '#27AE60',
                             'fontSize': '28px',
                             'fontWeight': 'bold'})
            ], style={'background': 'white', 
                     'padding': '20px', 
                     'borderRadius': '10px',
                     'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                     'flex': 1,
                     'margin': '0 10px',
                     'textAlign': 'center'})
        ], style={'display': 'flex',
                  'flexDirection': 'row',
                  'margin': '20px 0 40px 0',
                  'gap': '20px'}),

        # Graphs Container - Both in Same Row
        html.Div([
            # Left Graph - Year-to-Date
            html.Div([
                html.H2('Year-to-Date Overview', 
                    style={'color': colors['text'], 
                           'textAlign': 'center',
                           'marginBottom': '20px',
                           'fontSize': '24px',
                           'fontWeight': '600'}),
                dcc.Graph(
                    figure=px.line(
                        ytd,
                        title='Year-to-Date Financial Tracking',
                        labels={'value': 'Amount ($)', 'index': 'Date', 'variable': 'Category'}
                    ).update_layout(
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        title={
                            'y': 0.95,
                            'x': 0.5,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            'font': {'size': 20, 'color': colors['text']}
                        },
                        legend=dict(
                            bgcolor='rgba(255,255,255,0.8)',
                            bordercolor='rgba(0,0,0,0.1)',
                            borderwidth=1,
                            font={'size': 12, 'color': colors['text']}
                        ),
                        xaxis=dict(
                            showgrid=True,
                            gridcolor='rgba(220,220,220,0.5)',
                            showline=True,
                            linewidth=2,
                            linecolor='rgba(0,0,0,0.2)',
                            title_font={'size': 14, 'color': colors['text']},
                            tickfont={'size': 12, 'color': colors['text']}
                        ),
                        yaxis=dict(
                            showgrid=True,
                            gridcolor='rgba(220,220,220,0.5)',
                            showline=True,
                            linewidth=2,
                            linecolor='rgba(0,0,0,0.2)',
                            title_font={'size': 14, 'color': colors['text']},
                            tickfont={'size': 12, 'color': colors['text']},
                            tickformat='$,.0f'
                        ),
                        hovermode='x unified',
                        hoverlabel=dict(
                            bgcolor='white',
                            font_size=14,
                            font_family="Arial"
                        ),
                        height=450,
                        margin={'t': 60, 'b': 40, 'l': 40, 'r': 40}
                    ),
                    style={'height': '450px'}
                )
            ], style={
                'flex': 1,
                'marginRight': '20px',
                'background': 'white',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
            }),
            
            # Right Graph - Monthly Analysis
            html.Div([
   
                dcc.Graph(
                    figure=px.bar(
                        monthly,
                        x=monthly.index,
                        y=monthly.columns,
                        title='Monthly Financial Distribution',
                        labels={'value': 'Amount ($)', 'x': 'Month', 'variable': 'Type'},
                        barmode='stack',
                        color_discrete_map={
                            'OPEX': colors['OPEX'],
                            'CAPEX': colors['CAPEX']
                        }
                    ).update_layout(
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        title={
                            'y':0.95,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            'font': {'size': 20, 'color': colors['text']}
                        },
                        xaxis=dict(
                            ticktext=['Q1 - Jan', 'Feb', 'Mar', 
                                    'Q2 - Apr', 'May', 'Jun', 
                                    'Q3 - Jul', 'Aug', 'Sep', 
                                    'Q4 - Oct', 'Nov', 'Dec'],
                            tickvals=monthly.index,
                            tickmode='array',
                            tickangle=45,
                            showgrid=True,
                            gridcolor='rgba(220,220,220,0.5)',
                            showline=True,
                            linewidth=2,
                            linecolor='rgba(0,0,0,0.2)',
                            title_font={'size': 14, 'color': colors['text']},
                            tickfont={'size': 12, 'color': colors['text']}
                        ),
                        yaxis=dict(
                            showgrid=True,
                            gridcolor='rgba(220,220,220,0.5)',
                            showline=True,
                            linewidth=2,
                            linecolor='rgba(0,0,0,0.2)',
                            title_font={'size': 14, 'color': colors['text']},
                            tickfont={'size': 12, 'color': colors['text']},
                            tickformat='$,.0f'
                        ),
                        legend=dict(
                            bgcolor='rgba(255,255,255,0.8)',
                            bordercolor='rgba(0,0,0,0.1)',
                            borderwidth=1,
                            font={'size': 12, 'color': colors['text']}
                        ),
                        hovermode='x unified',
                        hoverlabel=dict(
                            bgcolor='white',
                            font_size=14,
                            font_family="Arial"
                        ),
                        height=450,
                        margin={'t': 60, 'b': 40, 'l': 40, 'r': 40},
                        bargap=0.15,
                        bargroupgap=0.1,
                        shapes=[
                            # Quarters separator lines
                            dict(type='line', x0='2025-03', x1='2025-03', y0=0, y1=1.02, yref='paper',
                                 line=dict(color='rgba(44, 62, 80, 0.5)', width=2, dash='dot')),
                            dict(type='line', x0='2025-06', x1='2025-06', y0=0, y1=1.02, yref='paper',
                                 line=dict(color='rgba(44, 62, 80, 0.5)', width=2, dash='dot')),
                            dict(type='line', x0='2025-09', x1='2025-09', y0=0, y1=1.02, yref='paper',
                                 line=dict(color='rgba(44, 62, 80, 0.5)', width=2, dash='dot')),
                            # Quarter background shading
                            dict(type='rect', x0='2025-01', x1='2025-03', y0=0, y1=1, yref='paper',
                                 fillcolor='rgba(220,220,220,0.2)', layer='below', line_width=0),
                            dict(type='rect', x0='2025-07', x1='2025-09', y0=0, y1=1, yref='paper',
                                 fillcolor='rgba(220,220,220,0.2)', layer='below', line_width=0)
                        ]
                    ),
                    style={'height': '100%'}
                )
            ], style={
                'flex': 1,
                'background': 'white',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'height': '550px',
                'overflow': 'hidden'
            })
        ], style={
            'display': 'flex',
            'gap': '24px',
            'marginBottom': '40px',
            'height': '550px'
        }),

        # Transaction Summary Section
        html.H2('Detailed Transaction Summary', 
                style={'color': colors['text'], 
                       'textAlign': 'center',
                       'marginBottom': '20px',
                       'fontSize': '28px',
                       'fontWeight': '600'}),
        html.Div([
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in expected_cols],
                page_size=10,
                style_header={
                    'backgroundColor': colors['text'],
                    'color': 'white',
                    'fontWeight': 'bold',
                    'textAlign': 'center',
                    'fontSize': '14px',
                    'padding': '12px'
                },
                style_cell={
                    'textAlign': 'left',
                    'padding': '12px',
                    'fontSize': '13px'
                },
                style_data={
                    'backgroundColor': 'white',
                    'color': colors['text']
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 249, 250)'
                    }
                ],
                style_table={
                    'border': f'1px solid {colors["text"]}',
                    'borderRadius': '10px',
                    'overflow': 'hidden'
                }
            )
        ], style={
            'background': 'white',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            'marginBottom': '40px'
        })
    ], style={
        'padding': '20px',
        'backgroundColor': colors['background'],
        'minHeight': '100vh'
    })
    
    return layout


