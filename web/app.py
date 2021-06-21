# dash libs
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

app = dash.Dash(
    # external_scripts= external_scripts,
    external_stylesheets= [
            # {
            #     'href': 'bootstrap.min.css',
            #     'rel': 'stylesheet',
            # },
            # {
            #     'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css',
            #     'rel': 'stylesheet',
            # },
            dbc.themes.BOOTSTRAP,
        ]
)


text_input = html.Div(
	[
		dbc.Input(id="input", placeholder="Type something...", type="text"),
		html.Br(),
		html.P(id="output"),
	]
)


@app.callback(Output("output", "children"), [Input("input", "value")])
def output_text(value):
	return value

app.layout = html.Div(
    [
        autoplot_layout,
        area_equipments_layout,
        chart,
    ],
)


if __name__ == '__main__':
	app.run_server(debug=True, port=3700)