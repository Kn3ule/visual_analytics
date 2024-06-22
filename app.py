import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from PIL import Image
import base64
import os
import json



# Initialisiere das Dash-Board
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Lade die Daten aus dem JSON-File
with open('data/classification_data.json') as f:
    classification_data = json.load(f)

# Funktion zum Laden und Kodieren von Bildern
def encode_image(image_file):
    with open(image_file, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode('utf-8')

# Liste der Bilder im Ordner 'images'
image_folder = 'images/original'
images = [os.path.join(image_folder, image) for image in os.listdir(image_folder) if image.endswith(('.png', '.JPG', '.jpeg', '.jpg'))]
cem_folder = 'images/cem'
cem = [os.path.join(cem_folder, image) for image in os.listdir(cem_folder) if image.endswith(('.png', '.JPG', '.jpeg'))]
lime_folder = 'images/lime'
lime = [os.path.join(lime_folder, image) for image in os.listdir(lime_folder) if image.endswith(('.png', '.JPG', '.jpeg'))]


def find_matching_image_in_array(img_name, image_array):
    for image in image_array:
        if os.path.basename(image).startswith(img_name):
            return image
    return None

#Load Data for 

# Navbar
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("XAI Fruit Classification", className="ms-2")
        ]
    ),
    color= "red",
    dark=True,
    className="mb-4"
)

# Layout des Dashboards
app.layout = html.Div([
    navbar,
    dbc.Row([
        html.Div(
            [
                html.H5("Please select a picture, which should be classified", style={'text-align': 'center', 'margin-bottom': '20px'}),
                html.Div(
                        [
                                html.Img(
                                    src=encode_image(image),
                                    id={'type': 'image', 'index': i},
                                    style={
                                        #'width': '80px',
                                        #'height': '80px',
                                    }
                                )
                            for i, image in enumerate(images)
                        ],
                        style={
                            #'flexDirection': 'column',
                            #'overflowY': 'auto',
                            'text-align': 'center',
                            #'padding': '20px',
                        }
                )
            ]
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.Div(
                [
                    html.H4("LIME-Explanation:", style={'text-align': 'center', 'margin-bottom': '20px'}, id="lime-heading"),
                    dbc.Tooltip(
                        "LIME (Local Interpretable Model-agnostic Explanations) helps explain complex AI models by approximating them locally with simpler models. Green areas show features pushing predictions towards the positive class, while red areas indicate features pushing towards the negative class. ",
                        target="lime-heading",
                        placement="top"
                    ),
                    html.Div(id="left-container", style={'padding': '10px'})
                ],
                style={'height': '100%', 'margin-top': '5%'}
            ), width=4
        ),
        dbc.Col(
            html.Div(
                [
                    html.H4("Model Results:", style={'text-align': 'center', 'margin-bottom': '20px'}),
                    html.Div(id='middle-container', style={'padding': '10px'})
                ],
                style={'height': '100%', 'margin-top': '5%'}
            ),
            width=4
        ),
        dbc.Col(
            html.Div(
                [
                    html.H4("CEM Explanation:", style={'text-align': 'center', 'margin-bottom': '20px'}, id="cem-heading"),
                    dbc.Tooltip(
                        "CEM (Contrastive Explanation Method) explains AI model predictions by identifying key features that both support (pertinent positives) and contradict (pertinent negatives) a decision. Green areas highlight features reinforcing the prediction, while red areas show features that, if absent or different, would change the prediction.",
                        target="cem-heading",
                        placement="bottom"
                    ),
                    html.Div(id='right-container', style={'padding': '10px'})
                ],
                style={'height': '100%', 'margin-top': '5%'}
            ),
            width=4
        )
    ], className="g-0")
], style={'height': '100%'})

# Callback für die Bildauswahl und Anzeige von Informationen
@app.callback(
    [Output('left-container', 'children'),
     Output('middle-container', 'children'),
     Output('right-container', 'children'),
     Output({'type': 'image', 'index': dash.dependencies.ALL}, 'style')],
    [Input({'type': 'image', 'index': dash.dependencies.ALL}, 'n_clicks')],
    [State({'type': 'image', 'index': dash.dependencies.ALL}, 'id'),
     State({'type': 'image', 'index': dash.dependencies.ALL}, 'n_clicks')]
)
def display_info(n_clicks, ids, all_n_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return [
            html.P('LIME Information will be shown here', style={'text-align': 'center'}),
            html.P('Please select an image!', style={'text-align': 'center'}),
            html.P('CEM Information will be shown here', style={'text-align': 'center'}),
            [{'filter': 'none', 'height': '175px', 'padding': '10px'} for _ in images]
        ]

    clicked_id = ctx.triggered[0]['prop_id'].split('.')[0]
    clicked_index = eval(clicked_id)['index']


    # Überprüfen, ob das angeklickte Bild bereits ausgewählt ist
    if all_n_clicks[clicked_index] % 2 == 1:
        # Ein anderes Bild wurde angeklickt
        clicked_image = os.path.basename(images[clicked_index])
        image_info = f"Bild: {clicked_image}"
        image_description = f"Das ist die Beschreibung für das Bild {clicked_image}."
        styles = [{'filter': 'grayscale(100%)', 'height': '175px', 'padding': '10px'} if i != clicked_index else {'filter': 'none', 'height': '175px', 'padding': '10px'} for i in range(len(images))]

        # Daten aus der JSON-Datei für das ausgewählte Bild abrufen
        selected_image_name = clicked_image
        selected_image_data = next((item for item in classification_data if item["image_name"] == selected_image_name), None)
        if selected_image_data:
            predicted_value = selected_image_data["predicted_value"]
            actual_value = selected_image_data["actual_value"]
            labels = selected_image_data["distributions"]["labels"]
            sizes = selected_image_data["distributions"]["values"]

            classification_info = html.Div([
                html.P(f"Actual Label: {actual_value}"),
                html.P(f"Predicted Value: {predicted_value}"),
                html.Img(src=encode_image(images[clicked_index]),style={'width': '50%', 'text-align': 'center'}),
                html.Details([
                    html.Summary("Click here for prediction details"),
                    dcc.Graph(
                        id='pie-chart',
                        figure={
                            'data': [
                                go.Pie(
                                    labels=labels,
                                    values=sizes,
                                    marker=dict(colors=['#A76C25', '#FF2A00', '#714B17', '#FFE800'])
                                )
                            ],
                            'layout': go.Layout(
                                title=f"Distributions of Classification:",
                                showlegend=True
                            )
                        }
                    )
                ], style={"margin-top": "20px"})
            ], style={'padding': '10px', 'text-align': 'center'})
            #classification_info = html.Div([html.Img(src=encode_image(images[clicked_index]),style={'width': '30%', 'text-align': 'center'}), json_info],style={'text-align': 'center'})

            left_container_info = html.Div([
                html.Div([
                    #html.P(f"LIME Explanation to {clicked_image}."),
                    html.Img(src=encode_image(find_matching_image_in_array(clicked_image.replace('.jpg', ''), lime)),style={'width': '50%', 'text-align': 'center', 'margin-top': '75px'})
                ], style={'padding': '10px', 'text-align': 'center'})
            ])

            # Informationen für den rechten Container (Explainer)
            right_container_info = html.Div([
                html.Div([
                    #html.P(f"CEM Explanation to {clicked_image}."),
                    html.Img(src=encode_image(find_matching_image_in_array(clicked_image.replace('.jpg', ''), cem)),style={'width': '50%', 'text-align': 'center', 'margin-top': '15px'})
                ], style={'padding': '10px', 'text-align': 'center'})
            ])
        else:
            classification_info = html.P("Keine Daten für dieses Bild gefunden.")

    else:
        # Das gleiche Bild wurde erneut angeklickt
        image_info = 'Wählen Sie ein Bild aus.'
        image_description = 'Informationen werden hier angezeigt.'
        styles = [{'filter': 'none', 'height': '175px', 'padding': '10px'} for _ in images]
        classification_info = html.P('Please select an image!', style={'text-align': 'center'})
        left_container_info = html.P('LIME Information will be shown here', style={'text-align': 'center'})
        right_container_info = html.P('CEM Information will be shown here', style={'text-align': 'center'})


    return [left_container_info, classification_info, right_container_info, styles]



# Starte die App
if __name__ == '__main__':
    app.run(debug=True)