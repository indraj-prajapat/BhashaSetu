import dash
from dash import dcc, html, Input, Output, State, callback,ctx
import dash_bootstrap_components as dbc
import base64
import io
import os
from dash_extensions import Lottie
from line_processor_component import get_line_processor_layout, register_line_processor_callbacks
from translationHelper import register_callbacks
import tempfile
from moviepy import VideoFileClip
# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Subhashit - an AiTransmute solution"

# Indian languages for the dropdown
INDIAN_LANGUAGES = [
    {'label': 'Default', 'value': 'df'},
    {'label': 'Hindi (हिन्दी)', 'value': 'hi'},
    {'label': 'Tamil (தமிழ்)', 'value': 'ta'},
    {'label': 'Bengali (বাংলা)', 'value': 'bn'},
    {'label': 'Telugu (తెలుగు)', 'value': 'te'},
    {'label': 'Marathi (मराठी)', 'value': 'mr'},
    {'label': 'Gujarati (ગુજરાતી)', 'value': 'gu'},
    {'label': 'Kannada (ಕನ್ನಡ)', 'value': 'kn'},
    {'label': 'Malayalam (മലയാളം)', 'value': 'ml'},
    {'label': 'Punjabi (ਪੰਜਾਬੀ)', 'value': 'pa'},
    {'label': 'Urdu (اردو)', 'value': 'ur'},
]

SOURCE_LANGUAGES = [
    {'label': 'English', 'value': 'en'},
    {'label': 'Spanish', 'value': 'es'},
    {'label': 'French', 'value': 'fr'},
    {'label': 'German', 'value': 'de'},
    {'label': 'Chinese', 'value': 'zh'},
    {'label': 'Japanese', 'value': 'ja'},
    {'label': 'Korean', 'value': 'ko'},
    {'label': 'Russian', 'value': 'ru'},
    {'label': 'Arabic', 'value': 'ar'},
] + INDIAN_LANGUAGES

# Define the layout
app.layout = html.Div([
    # Custom CSS
    html.Link(
        rel='stylesheet',
        href='/assets/app_style.css'
    ),
    
    # Main container
    html.Div([
        # Header
        html.Div([
            html.Div([
                # html.Img(src='/assets/logo.png', className='logo'),
                html.H1('सु',className='main-title1'),
                html.H1("Bhashit", className='main-title'),
            ], className='header-content'),
        ], className='header'),
        
        # Language selection
        html.Div([
            html.Div([
                html.Label("From:", className='language-label'),
                dcc.Dropdown(
                    id='source-language',
                    options=SOURCE_LANGUAGES,
                    value='en',
                    className='language-dropdown',
                    clearable=False
                ),
            ], className='language-selector'),
            
            html.Div([
                html.Button("⇄", className='swap-button', id='swap-languages'),
            ], className='swap-container'),
            
            html.Div([
                html.Label("To:", className='language-label'),
                dcc.Dropdown(
                    id='target-language',
                    options=INDIAN_LANGUAGES,
                    value='df',
                    className='language-dropdown',
                    clearable=False
                ),
            ], className='language-selector'),
        ], className='language-selection'),
        
        # Main content area
        html.Div([
            # Text input/output section
            html.Div([
                html.Div([
                    html.H3("Text Input", className='section-title'),
                    dcc.Textarea(
                        id='text-input',
                        placeholder='Enter text to translate...',
                        className='text-area input-area',
                        rows=6
                    ),
             
                    html.Button([
                            html.Span('Click here for translation')
                        ], id='txt-translation', className='media-button')
                ], className='input-section-txt'),
      
            ], className='text-section'),
            dbc.Modal([
                dbc.ModalHeader("Translation Result"),
                dbc.ModalBody(id="translation-table"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-modal", className="ms-auto", n_clicks=0)
                ),
            ], id="result-modal-txt", is_open=False),
            
            # Media input section
            html.Div([
                # Audio section
                html.Div([
                    html.H3("Audio Translation", className='section-title'),
                    
                    html.Div([
                        
                        dcc.Upload(
                            id='audio-upload',
                            children=html.Div([
                                html.I(className='audio-icon'),
                                html.Span('Upload Audio')
                            ]),
                            className='media-button upload',
                            multiple=False
                        ),
                    ], className='media-controls'),

                    html.Div(id='audio-status', className='status-display'),
                    # BUTTON IS PART OF INITIAL LAYOUT BUT HIDDEN
                    html.Button(
                        "Translate Audio",
                        id="audio-translate-btn",
                        n_clicks=0,
                        className="media-button",
                        style={"display": "none"}  # hidden initially
                    ),
                    
                ], className='media-section'),
                # ---- MODAL ----
                dbc.Modal([
                    dbc.ModalHeader("Audio Translation Result"),
                    dbc.ModalBody(id="audio-translation-table"),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close-audio-modal", className="ms-auto", n_clicks=0)
                    ),
                ], id="audio-result-modal", is_open=False),
                
                # Video section
                html.Div([
                    html.H3("Video Translation", className='section-title'),
                    html.Div([
                        dcc.Upload(
                            id='video-upload',
                            children=html.Div([
                                html.I(className='video-icon'),
                                html.Span('Upload Video')
                            ]),
                            className='media-button upload',
                            multiple=False
                        ),
                    ], className='media-controls'),

                    html.Div(id='video-status', className='status-display'),

                    html.Div(id='translate-container', className='hidden', children=[
                        html.Button("Translate", id="translate-btn", className='media-button upload', n_clicks=0)
                    ])
                ], className='media-section')

            ], className='media-sections'),
        ], className='main-content'),
        
        # Progress indicator
        html.Div([
            dcc.Loading(
                id="loading",
                type="default",
                children=html.Div(id="loading-output")
            )
        ], className='loading-container'),
        html.Div(id="popup", className="popup hidden", children=[
            html.Button("✖", id="close-btn", className="close-btn"),
            dcc.Interval(
                id="progress-interval",
                interval=1000,        # 1 second
                n_intervals=0,
                max_intervals=70,
                disabled=True         # Start as disabled
            ),
            
            html.Div(className="popup-content", children=[
                html.Div(id="status-bar-container", className="status-bar", children=[
                    html.Div(id="status-bar-fill", className="status-fill"),
                    html.Div("Processing video translation...", className="status-text")
                ]),
                get_line_processor_layout(),
                html.Div(className="animation-row", children=[
                    # Left Lottie Animation with Status Bar
                    html.Div(id="lottie-container-left", className="hidden", children=[
                        
                        html.Div(className="lottie-animation1 slide-in-left", children=[
                            Lottie(
                                id="lottie-left",
                                options={"loop": True, "autoplay": False},
                                url="/assets/Scanning.json"
                            )
                        ])
                    ]),

                    # Right Lottie Animation
                    html.Div(id="lottie-container-right", className="hidden", children=[
                        html.Div(className="lottie-animation2 slide-in-right", children=[
                            Lottie(
                                id="lottie-right",
                                options={"loop": True, "autoplay": False},
                                url="/assets/video.json"
                            )
                        ])
                    ])
                ]),

                # Cancel button below the animation row
                html.Div(className="cancel-btn-container", children=[
                    html.Button("Cancel Process", id="cancel-btn", className="cancel-btn"),
                    html.A("Download Video", id="download-btn", className="download-btn hidden", href="/assets/translated_video.mp4", download="translated_video.mp4"),
                    # Invisible button to detect click
                    html.Button(id="download-btn-helper", n_clicks=0, style={"display": "none"})
                ])
            ])
        ])

        
    ], className='app-container'),
    
    # Hidden divs to store data
    html.Div(id='audio-data', style={'display': 'none'}),
    html.Div(id='video-data', style={'display': 'none'}),
    html.Div(id='text-file-data', style={'display': 'none'}),
], className='app-wrapper')

# Callbacks

register_callbacks(app)
register_line_processor_callbacks(app)
@app.callback(
    Output("translate-container", "className"),
    Input("video-upload", "contents"),
    prevent_initial_call=True
)
def show_translate_button(uploaded_file):
    if uploaded_file:
        return ""  # Show the div (no class)
    return "hidden"

@app.callback(
    Output("cancel-btn", "className"),
    Output("download-btn", "className"),
    Input("progress-interval", "n_intervals"),
    prevent_initial_call=True
)
def toggle_buttons(n_intervals):
    if n_intervals >= 70:
        return "hidden", "download-btn"
    return "cancel-btn", "hidden"


@app.callback(
    Output("status-bar-fill", "style"),
    Input("progress-interval", "n_intervals"),
    prevent_initial_call=True
)
def update_progress_bar(n_intervals):
    progress_percent = min(100, int((n_intervals / 70) * 100))
    return {"width": f"{progress_percent}%", "backgroundColor": "#00ffff"}





@app.callback(
    Output("popup", "className"),
    Output("lottie-container-left", "className"),
    Output("lottie-container-right", "className"),
    Output("lottie-left", "options"),
    Output("lottie-right", "options"),
    Output("progress-interval", "disabled"),
    Input("translate-btn", "n_clicks"),
    Input("cancel-btn", "n_clicks"),
    Input("download-btn-helper", "n_clicks"),
    Input("close-btn", "n_clicks"),  # 👈 new close button
    State("lottie-left", "options"),
    State("lottie-right", "options"),
    prevent_initial_call=True
)
def handle_all_actions(n_translate, n_cancel, n_download, n_close, left_opts, right_opts):
    trigger = ctx.triggered_id

    if trigger == "translate-btn":
        left_opts["autoplay"] = True
        right_opts["autoplay"] = True
        return (
            "popup popup-show",
            "lottie-container-active",
            "lottie-container-active",
            left_opts,
            right_opts,
            False
        )

    elif trigger in ["cancel-btn", "download-btn-helper", "close-btn"]:
        return (
            "popup hidden",
            "hidden",
            "hidden",
            left_opts,
            right_opts,
            True
        )

    return "popup hidden", "hidden", "hidden", left_opts, right_opts, True



# @app.callback(
#     Output('translation-output', 'children'),
#     Output('loading-output', 'children'),
#     Input('translate-button', 'n_clicks'),
#     State('text-input', 'value'),
#     State('source-language', 'value'),
#     State('target-language', 'value'),
#     prevent_initial_call=True
# )
# def translate_text(n_clicks, text_input, source_lang, target_lang):
#     if n_clicks and text_input:
#         # Placeholder for actual translation logic
#         # In a real implementation, you would call your Python backend here
#         translated_text = f"[Translated from {source_lang} to {target_lang}] {text_input}"
#         return translated_text, ""
#     return "Translation will appear here...", ""

# @app.callback(
#     Output('text-input', 'value'),
#     Input('text-file-upload', 'contents'),
#     State('text-file-upload', 'filename'),
#     prevent_initial_call=True
# )
# def handle_text_file_upload(contents, filename):
#     if contents is not None:
#         content_type, content_string = contents.split(',')
#         decoded = base64.b64decode(content_string)
#         try:
#             if 'txt' in filename.lower():
#                 text_content = decoded.decode('utf-8')
#                 return text_content
#         except Exception as e:
#             return f"Error reading file: {str(e)}"
#     return ""

# @app.callback(
#     Output('audio-status', 'children'),
#     Input('audio-upload', 'contents'),
#     State('audio-upload', 'filename'),
#     prevent_initial_call=True
# )
# def handle_audio_upload(contents, filename):
#     if contents is not None:
#         return html.Div([
#             html.I(className='success-icon'),
#             html.Span(f"Audio file '{filename}' uploaded successfully!")
#         ], className='success-message')
#     return ""

@app.callback(
    Output('video-status', 'children'),
    Input('video-upload', 'contents'),
    State('video-upload', 'filename'),
    prevent_initial_call=True
)
def handle_video_upload(contents, filename):
    if contents is None:
        return ""

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    with tempfile.NamedTemporaryFile(delete=False, suffix=filename) as tmp:
        tmp.write(decoded)
        temp_path = tmp.name

    try:
        clip = VideoFileClip(temp_path)
        duration = clip.duration  # in seconds
        clip.close()

        file_size = os.path.getsize(temp_path)  # in bytes
        file_size_mb = round(file_size / (1024 * 1024), 2)

        return html.Div([
            html.I(className='success-icon'),
            html.Span(f"Video file '{filename}' uploaded successfully!"),
            html.Br(),
            html.Span(f"📏 Duration: {round(duration, 2)} seconds"),
            html.Br(),
            html.Span(f"📦 Size: {file_size_mb} MB")
        ], className='success-message')

    except Exception as e:
        return html.Div([
            html.I(className='error-icon'),
            html.Span(f"⚠️ Error processing video: {str(e)}")
        ], className='error-message')
    finally:
        os.remove(temp_path)

@app.callback(
    [Output('source-language', 'value'), Output('target-language', 'value')],
    Input('swap-languages', 'n_clicks'),
    [State('source-language', 'value'), State('target-language', 'value')],
    prevent_initial_call=True
)
def swap_languages(n_clicks, source, target):
    if n_clicks:
        return target, source
    return source, target

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)

