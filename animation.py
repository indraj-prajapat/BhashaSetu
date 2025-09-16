from dash import Dash, html, Output, Input, State
from dash_extensions import Lottie

app = Dash(__name__)
server = app.server  # For deployment

app.layout = html.Div([
    html.H2("Click to Start Futuristic AI Animation"),
    html.Button("Translate", id="translate-btn", n_clicks=0),

    html.Div(id="popup", className="popup hidden", children=[
        html.Div(className="popup-content", children=[
            html.Div(className="animation-row", children=[
                html.Div(id="lottie-container-left", className="hidden", children=[
                    html.Div(className="lottie-animation1 slide-in-left", children=[
                        Lottie(
                            id="lottie-left",
                            options={"loop": True, "autoplay": False},
                            url="/assets/MXcxdY0Q8P.json"
                        )
                    ])
                ]),
                html.Div(id="lottie-container-right", className="hidden", children=[
                    html.Div(className="lottie-animation2 slide-in-right", children=[
                        Lottie(
                            id="lottie-right",
                            options={"loop": True, "autoplay": False},
                            url="/assets/ani2.json"
                        )
                    ])
                ])
            ])
        ])
    ])
])




@app.callback(
    Output("popup", "className"),
    Output("lottie-container-left", "className"),
    Output("lottie-container-right", "className"),
    Output("lottie-left", "options"),
    Output("lottie-right", "options"),
    Input("translate-btn", "n_clicks"),
    State("lottie-left", "options"),
    State("lottie-right", "options"),
)
def show_popup(n, left_opts, right_opts):
    if n > 0:
        left_opts["autoplay"] = True
        right_opts["autoplay"] = True
        return "popup popup-show", "lottie-container-active", "lottie-container-active", left_opts, right_opts
    return "popup hidden", "hidden", "hidden", left_opts, right_opts



if __name__ == "__main__":
    app.run(debug=True)
