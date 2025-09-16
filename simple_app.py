import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import base64

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "AI Translation Hub"

# Indian languages for the dropdown
INDIAN_LANGUAGES = [
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
] + INDIAN_LANGUAGES

# Custom CSS styles
custom_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;500;600&display=swap');

:root {
    --primary-bg: #0a0e1a;
    --secondary-bg: #1a1f2e;
    --accent-blue: #00d4ff;
    --accent-purple: #8b5cf6;
    --accent-cyan: #06ffa5;
    --text-primary: #ffffff;
    --text-secondary: #a0aec0;
    --glass-bg: rgba(26, 31, 46, 0.7);
    --glass-border: rgba(0, 212, 255, 0.3);
    --shadow-glow: 0 0 20px rgba(0, 212, 255, 0.3);
}

body {
    font-family: 'Exo 2', sans-serif !important;
    background: var(--primary-bg) !important;
    color: var(--text-primary) !important;
    margin: 0;
    padding: 0;
}

body::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(circle at 20% 80%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
    z-index: -1;
}

.main-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    position: relative;
    z-index: 1;
}

.header-section {
    text-align: center;
    margin-bottom: 40px;
    padding: 20px 0;
}

.main-title {
    font-family: 'Orbitron', monospace !important;
    font-size: 3.5rem !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #00d4ff 0%, #8b5cf6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
    letter-spacing: 3px;
    margin-bottom: 20px;
}

.glass-panel {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 20px !important;
    padding: 25px !important;
    backdrop-filter: blur(15px) !important;
    box-shadow: var(--shadow-glow) !important;
    margin-bottom: 20px !important;
}

.section-title {
    font-family: 'Orbitron', monospace !important;
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    color: var(--accent-cyan) !important;
    margin-bottom: 15px !important;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.futuristic-textarea {
    background: rgba(10, 14, 26, 0.8) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 15px !important;
    color: var(--text-primary) !important;
    font-size: 1rem !important;
    padding: 15px !important;
    width: 100% !important;
    min-height: 150px !important;
}

.futuristic-textarea:focus {
    outline: none !important;
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.3) !important;
}

.output-area {
    background: rgba(26, 31, 46, 0.9) !important;
    border: 1px solid var(--accent-purple) !important;
    border-radius: 15px !important;
    padding: 20px !important;
    min-height: 150px !important;
    color: var(--text-primary) !important;
    font-size: 1.1rem !important;
    line-height: 1.7;
}

.action-button {
    background: linear-gradient(135deg, #00d4ff 0%, #8b5cf6 100%) !important;
    border: none !important;
    border-radius: 25px !important;
    color: white !important;
    padding: 12px 25px !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    margin: 10px 5px !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.action-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 25px rgba(0, 212, 255, 0.4) !important;
}

.upload-area {
    border: 2px dashed var(--glass-border) !important;
    border-radius: 15px !important;
    padding: 20px !important;
    text-align: center !important;
    background: var(--glass-bg) !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    margin: 10px 0 !important;
}

.upload-area:hover {
    border-color: var(--accent-blue) !important;
    background: rgba(0, 212, 255, 0.1) !important;
}

.language-dropdown .Select-control {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 15px !important;
    color: var(--text-primary) !important;
}

@media (max-width: 768px) {
    .main-title {
        font-size: 2.5rem !important;
    }
    
    .main-container {
        padding: 15px !important;
    }
}
</style>
"""

# Define the layout
app.layout = html.Div([
    # Custom CSS
    html.Div([
        html.Script(src="https://cdn.tailwindcss.com"),
        dcc.Markdown(custom_style, dangerously_allow_html=True)
    ]),
    
    # Main container
    html.Div([
        # Header
        html.Div([
            html.H1("AI TRANSLATION", className="main-title"),
            html.P("Translate text, audio, and video into Indian languages", 
                   style={'color': 'var(--text-secondary)', 'fontSize': '1.2rem', 'marginTop': '10px'})
        ], className="header-section"),
        
        # Language selection
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Label("From:", style={'color': 'var(--text-secondary)', 'marginBottom': '8px'}),
                    dcc.Dropdown(
                        id='source-language',
                        options=SOURCE_LANGUAGES,
                        value='en',
                        className='language-dropdown',
                        clearable=False,
                        style={'marginBottom': '20px'}
                    ),
                ], md=5),
                dbc.Col([
                    html.Button("⇄", id='swap-languages', 
                               style={
                                   'background': 'linear-gradient(135deg, #00d4ff 0%, #8b5cf6 100%)',
                                   'border': 'none',
                                   'borderRadius': '50%',
                                   'width': '50px',
                                   'height': '50px',
                                   'color': 'white',
                                   'fontSize': '1.5rem',
                                   'cursor': 'pointer',
                                   'marginTop': '25px'
                               }),
                ], md=2, style={'textAlign': 'center'}),
                dbc.Col([
                    html.Label("To:", style={'color': 'var(--text-secondary)', 'marginBottom': '8px'}),
                    dcc.Dropdown(
                        id='target-language',
                        options=INDIAN_LANGUAGES,
                        value='hi',
                        className='language-dropdown',
                        clearable=False,
                        style={'marginBottom': '20px'}
                    ),
                ], md=5),
            ])
        ], className="glass-panel"),
        
        # Text translation section
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.H3("Text Input", className="section-title"),
                    dcc.Textarea(
                        id='text-input',
                        placeholder='Enter text to translate...',
                        className='futuristic-textarea'
                    ),
                    dcc.Upload(
                        id='text-file-upload',
                        children=html.Div([
                            html.I(className="fas fa-upload", style={'marginRight': '8px'}),
                            'Upload Text File'
                        ]),
                        className='upload-area',
                        multiple=False
                    ),
                ], md=6),
                dbc.Col([
                    html.H3("Translation", className="section-title"),
                    html.Div(
                        id='translation-output',
                        className='output-area',
                        children="Translation will appear here..."
                    ),
                    html.Div([
                        html.Button([
                            html.I(className="fas fa-language", style={'marginRight': '8px'}),
                            'Translate'
                        ], id='translate-button', className='action-button'),
                        html.Button([
                            html.I(className="fas fa-copy", style={'marginRight': '8px'}),
                            'Copy'
                        ], id='copy-button', className='action-button'),
                    ], style={'textAlign': 'center', 'marginTop': '15px'}),
                ], md=6),
            ])
        ], className="glass-panel"),
        
        # Media upload section
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.H3("Audio Translation", className="section-title"),
                    html.Button([
                        html.I(className="fas fa-microphone", style={'marginRight': '8px'}),
                        'Record Audio'
                    ], id='record-button', className='action-button', 
                    style={'width': '100%', 'marginBottom': '10px'}),
                    dcc.Upload(
                        id='audio-upload',
                        children=html.Div([
                            html.I(className="fas fa-file-audio", style={'marginRight': '8px'}),
                            'Upload Audio File'
                        ]),
                        className='upload-area',
                        multiple=False
                    ),
                    html.Div(id='audio-status', style={'marginTop': '10px'}),
                ], md=6),
                dbc.Col([
                    html.H3("Video Translation", className="section-title"),
                    dcc.Upload(
                        id='video-upload',
                        children=html.Div([
                            html.I(className="fas fa-file-video", style={'marginRight': '8px'}),
                            'Upload Video File'
                        ]),
                        className='upload-area',
                        multiple=False
                    ),
                    html.Div(id='video-status', style={'marginTop': '10px'}),
                ], md=6),
            ])
        ], className="glass-panel"),
        
        # Progress indicator
        dcc.Loading(
            id="loading",
            type="default",
            children=html.Div(id="loading-output")
        ),
        
    ], className="main-container"),
    
    # Font Awesome for icons
    html.Link(
        rel='stylesheet',
        href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
    ),
], style={'minHeight': '100vh'})

# Callbacks
@app.callback(
    Output('translation-output', 'children'),
    Output('loading-output', 'children'),
    Input('translate-button', 'n_clicks'),
    State('text-input', 'value'),
    State('source-language', 'value'),
    State('target-language', 'value'),
    prevent_initial_call=True
)
def translate_text(n_clicks, text_input, source_lang, target_lang):
    if n_clicks and text_input:
        # Placeholder for actual translation logic
        source_name = next((lang['label'] for lang in SOURCE_LANGUAGES if lang['value'] == source_lang), source_lang)
        target_name = next((lang['label'] for lang in INDIAN_LANGUAGES if lang['value'] == target_lang), target_lang)
        translated_text = f"[Demo Translation from {source_name} to {target_name}]\n\n{text_input}\n\n→ This is where your Python backend would process the translation using your AI models."
        return translated_text, ""
    return "Translation will appear here...", ""

@app.callback(
    Output('text-input', 'value'),
    Input('text-file-upload', 'contents'),
    State('text-file-upload', 'filename'),
    prevent_initial_call=True
)
def handle_text_file_upload(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if filename and 'txt' in filename.lower():
                text_content = decoded.decode('utf-8')
                return text_content
        except Exception as e:
            return f"Error reading file: {str(e)}"
    return ""

@app.callback(
    Output('audio-status', 'children'),
    Input('audio-upload', 'contents'),
    State('audio-upload', 'filename'),
    prevent_initial_call=True
)
def handle_audio_upload(contents, filename):
    if contents is not None:
        return html.Div([
            html.I(className="fas fa-check-circle", style={'color': 'var(--accent-cyan)', 'marginRight': '8px'}),
            f"Audio file '{filename}' uploaded successfully! Ready for translation."
        ], style={'color': 'var(--accent-cyan)', 'fontWeight': '500'})
    return ""

@app.callback(
    Output('video-status', 'children'),
    Input('video-upload', 'contents'),
    State('video-upload', 'filename'),
    prevent_initial_call=True
)
def handle_video_upload(contents, filename):
    if contents is not None:
        return html.Div([
            html.I(className="fas fa-check-circle", style={'color': 'var(--accent-cyan)', 'marginRight': '8px'}),
            f"Video file '{filename}' uploaded successfully! Ready for translation."
        ], style={'color': 'var(--accent-cyan)', 'fontWeight': '500'})
    return ""

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
    app.run(debug=False, host='0.0.0.0', port=8053)

