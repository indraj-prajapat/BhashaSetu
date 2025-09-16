from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import dash

# Sample cleaned text lines
raw_text = """
🔹 Preprocessing Stage
Input Video Ingestion
Acquire and load the source video for processing.

Frame Rate & Resolution Analysis
Analyze technical properties to ensure format compatibility.

Scene Detection and Segmentation
Identify transitions and divide the video into logical scenes.



🔹 Audio Processing Stage
Audio Extraction from Video
Isolate the audio stream from the video.

Audio Format Normalization
Convert audio to a standard format and bitrate.

Noise Reduction and Denoising
Filter background noise and enhance speech clarity.

Silence and Pause Detection
Mark natural breaks for alignment and synthesis planning.

Speaker Diarization and Identification
Detect who is speaking and segment by speaker identity.

Gender and Age Estimation (Optional)
Estimate speaker demographics for voice modeling.

Dialect and Accent Detection
Classify speaker's regional speech patterns.

Emotion Detection from Audio
Classify voice-based emotional tone (happy, sad, angry, etc.).

Prosodic Feature Extraction
Analyze pitch, loudness, and rhythm from voice signal.

🔹 Speech-to-Text & Language Processing
Automatic Speech Recognition (ASR)
Convert spoken audio to raw transcribed text.

Punctuation and Capitalization Restoration
Reformat ASR output for grammatical correctness.



Idioms and Phrases Detection
Identify culturally-bound expressions requiring contextual translation.

Text-based Emotion Analysis
Detect sentiment and tone in transcribed content.

Context-Aware Text Segmentation
Break text into logical, contextually accurate segments.

Disfluency and Filler Removal
Clean up “um,” “uh,” and repetitions from raw text.

🔹 Translation & Enrichment
Source Text Quality Assessment
Evaluate transcription reliability before translation.

Machine Translation to Target Language
Translate segmented content using neural translation models.

Cultural Localization
Adapt translation to fit cultural and contextual relevance.

Keyword Highlighting and Tagging
Emphasize important terms for emphasis in synthesis.

Prosody Alignment with Translation
Match prosody of source speech to translated text flow.

Emotional Conflict Resolution
Adjust emotion in translation to reflect original tone faithfully.

🔹 Voice Synthesis & Alignment
Phoneme and Prosody Mapping
Map translated words to target-language phoneme patterns.

Speaker Voice Cloning or Matching
Generate or select voice that mimics original speaker’s tone and style.

Text-to-Speech Synthesis (TTS)
Generate target language speech using prosody-aware TTS.

Time Stretching and Duration Control
Adjust speech speed to fit scene timing and lip sync needs.

Pause and Segment-Based Audio Merging
Merge synthesized audio clips aligned to original pause structure.

🔹 Video Recomposition
Video-Audio Synchronization
Integrate new audio while preserving original video timing.

Lip Synchronization Adjustment
Align synthesized speech with speaker’s lip movements.


Subtitle Generation and Alignment
Create subtitles in target language, synced with audio.

Style and Font Consistency
Apply consistent subtitle formatting (font, size, positioning).

Subtitle Burn-in or Export
Either hardcode subtitles into the video or provide as a separate file.

🔹 Postprocessing & Delivery
Video Encoding and Compression
Encode final output with optimal size and quality.

Quality Assurance Review
Review the final video for sync, translation, and audio quality.

Final Export and Delivery
Output the fully processed translated video for end-use.
"""

lines = [
    ' '.join(line.replace(',', ' ').replace(';', ' ').split())
    for line in raw_text.strip().split('\n')
    if line.strip()
]

TOTAL_DURATION_MS = 60000
INTERVAL_MS = TOTAL_DURATION_MS // len(lines)

def get_line_processor_layout():
    """
    Generates the layout for the line processor display.
    Includes a title, a div for displaying lines, and dcc.Interval components
    for timing the display.
    """
    return html.Div([
      
        html.Div(id='line-display-div', className='media-section1'),
        # Main interval for updating lines, initially disabled
        dcc.Interval(id='line-interval', interval=INTERVAL_MS, n_intervals=0, disabled=True),
        # Delay interval: fires once after 2 seconds to enable the main interval
        dcc.Interval(id='start-delay', interval=22000, n_intervals=0, max_intervals=1),
        # dcc.Store to keep track of the current line index
        dcc.Store(id='line-current-index', data=0),
    ], style={'maxWidth': '600px', 'margin': '50px auto', 'fontFamily': 'Arial, sans-serif'})

# ------------- Callback Registration ------------------
def register_line_processor_callbacks(app: dash.Dash):
    """
    Registers the callbacks for the line processor.

    Args:
        app (dash.Dash): The Dash application instance.
    """

    # Callback to enable the main line interval after the 2-second delay
    @app.callback(
        Output('line-interval', 'disabled'),
        Input('start-delay', 'n_intervals'),
        prevent_initial_call=True # Prevent this callback from firing on initial load
    )
    def start_after_delay(n):
        """
        Enables the 'line-interval' after the 'start-delay' interval fires once.
        """
        # Once start-delay fires (n_intervals becomes 1), disable becomes False
        return False

    # Main callback to update the displayed lines
    @app.callback(
        Output('line-display-div', 'children'), # Updates the content of the display div
        Output('line-current-index', 'data'),  # Updates the stored current index
        Output('line-interval', 'disabled', allow_duplicate=True), # Disables the interval when all lines are processed
        Input('line-interval', 'n_intervals'), # Triggered by the main interval
        State('line-current-index', 'data'),   # Get the current index from dcc.Store
        prevent_initial_call=True # Prevent this callback from firing on initial load
    )
    def update_display(n_intervals, current_index):
        """
        Updates the display of lines, showing completed, processing, and pending states.
        It also manages the scrolling window of visible lines.
        """
        # Determine the current step (line being processed)
        step = min(n_intervals, len(lines))
        max_visible = 5  # Number of lines visible at any given time
        total = len(lines) # Total number of lines

        # Calculate the start and end indices for the visible window
        if step <= 2:
            start_index = 0
        elif step >= total - 2:
            start_index = max(0, total - max_visible)
        else:
            start_index = step - 2

        end_index = min(start_index + max_visible, total)
        visible_lines = lines[start_index:end_index]

        display_lines = []

        # Helper function to style each line based on its state
        def styled_div(content, icon='', bg='#f0f0f0', color='black', bold=False, className='output-area'):
            return html.Div([
                html.Span(icon, style={'marginRight': '8px'}),
                html.Span(content, style={'fontWeight': 'bold' if bold else 'normal'})
            ], className=className, style={
                'padding': '10px',
                'borderRadius': '8px',
                'marginBottom': '6px',
                'boxShadow': '0 1px 3px rgba(0,0,0,0.1)',
                # 'backgroundColor': bg,
                'color': color,
                'display': 'flex',
                'alignItems': 'center',
                'minHeight': '40px',
                'transition': 'all 0.3s ease-in-out' # Smooth transitions for styling changes
            })

        # Populate display_lines with styled divs
        for idx in range(start_index, end_index):
            if idx < step:
                # Line is completed
                display_lines.append(styled_div(lines[idx], icon='✅', bg='#e8f5e9', color='green', className='line-completed'))
            elif idx == step:
                # Line is currently processing
                display_lines.append(styled_div(
                    html.Span([
                        dbc.Spinner(size="sm", color="primary", type="border", spinner_style={"marginRight": "8px"}),
                        html.Span(lines[idx], style={'fontWeight': 'bold'})
                    ]),
                    bg='#e3f2fd', color='#0d47a1', className='line-processing'
                ))
            else:
                # Line is pending
                display_lines.append(styled_div(lines[idx], icon='⏳', bg='#f5f5f5', color='gray', className='line-pending'))

        # Fill remaining visible slots with empty divs if fewer than max_visible lines are left
        while len(display_lines) < max_visible:
            display_lines.append(styled_div('', icon='', bg='#f5f5f5', color='gray'))

        # Check if all lines have been processed
        is_disabled = step >= len(lines)
        return display_lines, step, is_disabled