import numpy as np
from plutus_backtest.backtest import _security_list, _consolidated_table_detailed, _portfolio_construction, _stats
from plutus_backtest.plots import _accumulated_return, _monthly_return, _drawdown, _plotting
from plutus_backtest.benchmark import _benchmark_construction
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, html, dcc, dash_table
import visdcc

def _report_generator (asset, o_day, c_day, weights_factor=None,
                       take_profit=None,
                       stop_loss=None,
                       benchmark=None,
                       price_period_relation=None):
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Structuring input

    weights_factor = weights_factor if weights_factor is not None else np.ones(len(asset))
    take_profit = take_profit if take_profit is not None else len(asset) * [np.inf]
    stop_loss = stop_loss if stop_loss is not None else len(asset) * [-np.inf]

    if price_period_relation is None:
        p_p_p = "Open"
        p_p_n = "Adj Close"
    else:
        if price_period_relation == 'O-C':
            p_p_p = "Open"
            p_p_n = "Adj Close"
        elif price_period_relation == 'C-O':
            p_p_p = "Adj Close"
            p_p_n = "Open"
        elif price_period_relation == 'C-C':
            p_p_p = "Adj Close"
            p_p_n = "Adj Close"
        else:
            p_p_p = "Open"
            p_p_n = "Open"

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Calling _security_list

    security_list = _security_list(asset=asset,
                                   o_day=o_day,
                                   c_day=c_day,
                                   weights_factor=weights_factor,
                                   take_profit=take_profit,
                                   stop_loss=stop_loss)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Calling _benchmark_construction
    if benchmark == None:
        benchmark_construction = None
    else:
        benchmark_construction = _benchmark_construction(security_list = security_list,
                                                         benchmark = benchmark,
                                                         p_p_n = p_p_n,
                                                         p_p_p = p_p_p)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Calling _consolidated_table_detailed

    consolidated_table_detailed, auxiliar_df = _consolidated_table_detailed(security_list = security_list,
                                                               asset = asset,
                                                               o_day=o_day,
                                                               p_p_n = p_p_n,
                                                               p_p_p = p_p_p)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Calling _portfolio_construction
    final_portfolio, portfolio_weights = _portfolio_construction(detailed_return = consolidated_table_detailed,
                                                     security_list = security_list,
                                                     auxiliar_df = auxiliar_df,
                                                     weights_factor=weights_factor)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Calling _stats
    stats = _stats(final_portfolio)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Plotting
    accumulated_return = _accumulated_return(final_portfolio=final_portfolio)
    monthly_return = _monthly_return(final_portfolio=final_portfolio)
    drawdown = _drawdown(final_portfolio=final_portfolio)
    plots = _plotting(accumulated_return=accumulated_return,
                                                          monthly_return=monthly_return,
                                                          drawdown=drawdown,
                                                          portfolio_weights=portfolio_weights,
                                                          benchmark_performance=benchmark_construction,
                                                          benchmark_ticker=benchmark)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Building app

    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])



    sidebar = dbc.Card(
        [
            html.Div(
                [
                    dash_table.DataTable(
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                        },
                        data = stats.to_dict('records'),
                        columns = [{"name": i, "id": i} for i in stats.columns]
                    )
                ]
            ),
            html.Hr(),
            html.Div(
                [
                    dash_table.DataTable(
                        style_data={
                                'whiteSpace': 'normal',
                                'height': 'auto',
                        },
                        data = security_list.to_dict('records'),
                        columns = [{"name": i, "id": i} for i in security_list.columns]
                    )
                ]
            )
        ]
    )

    graphs = dbc.Card(
        [
            html.Div(
                [
                    dcc.Graph(figure=plots)
                ]
            )
        ]
    )

    button = dbc.Card(
        [
            html.Div(
                [
                    html.Button("Download", id="click1"),
                    visdcc.Run_js(id="javascript")
                ]
            )
        ]
    )


    app.layout = dbc.Container(
        [
            html.H1("Backtest results"),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(sidebar, md=4),
                    dbc.Col(graphs),
                ],
                align="top",
            ),
            dbc.Row(
                [
                    dbc.Col(button),
                ],
                align="left",
            ),
        ],
        fluid=True,
    )

    app.title = "Plutus Backtest App!"


    @app.callback(
        Output("javascript", "run"),
        [Input("click1", "n_clicks")])
    def myfun(x):
        if x:
            return "window.print()"
            return ""

    app.run_server(debug=True, port=8888)
