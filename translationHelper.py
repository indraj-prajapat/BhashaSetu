from dash import html, Input, Output, State, ctx,no_update
import dash_bootstrap_components as dbc
import dash
# Dummy translation function
def dummy_translate(text, target_lang):
    translations = {
        "df": ("Hindi", text, "/assets/hindi.mp3"),
        "ta": ("Tamil", "வணக்கம் உலகம்", "/assets/tamil.mp3"),
        "gu": ("Gujarati", "હેલો વિશ્વ", "/assets/gujarati.mp3"),
    }
    return translations.get(target_lang, ("Unknown", "N/A", ""))

# Dummy audio translation function
def dummy_audio_translate(audio, target_lang):
    translations = {
        "hi": ("Hindi", "/assets/hindi_audio.mp3"),
        "ta": ("Tamil", "/assets/tamil_audio.mp3"),
        "gu": ("Gujarati", "/assets/gujarati_audio.mp3"),
    }
    return translations.get(target_lang, ("Unknown", ""))

def register_callbacks(app):
    @app.callback(
        Output("result-modal-txt", "is_open"),
        Output("translation-table", "children"),
        Input("txt-translation", "n_clicks"),
        Input("close-modal", "n_clicks"),
        State("target-language", "value"),
        State("text-input", "value"),
        State("result-modal-txt", "is_open"),
        prevent_initial_call=True
    )
    def show_translation(btn_click, close_click, lang, text, is_open):
        if not ctx.triggered:
            return is_open, dash.no_update

        trigger = ctx.triggered_id

        if trigger == "txt-translation" and text:
            # Call dummy function
            lang_name, translated_text, audio_file = dummy_translate(text, lang)

            table = dbc.Table([
                html.Thead(html.Tr([
                    html.Th("Language"), html.Th("Translated Text"), html.Th("Audio")
                ])),
                html.Tbody([
                    html.Tr([
                        html.Td(lang_name),
                        html.Td(translated_text),
                        html.Td([
                            html.Audio(src=audio_file, controls=True, style={"width": "200px"}),
                            html.Br(),
                            html.A("Download", href=audio_file, download=True)
                        ])
                    ])
                ])
            ], bordered=True, striped=True, hover=True)

            return True, table

        elif trigger == "close-modal":
            return False, dash.no_update

        return is_open, dash.no_update
    

    @app.callback(
        Output("audio-translate-btn", "style"),
        Output("audio-status", "children"),
        Input("audio-upload", "contents"),
        prevent_initial_call=True,
    )
    def show_audio_button(contents):
        if contents:
            # show the button (inline-block works better than block for small buttons)
            return {"display": "inline-block"}, "✅ Audio uploaded. Click 'Translate Audio' to proceed."
        # if upload removed/cleared - hide again
        return {"display": "none"}, "Upload cleared."

    # Open modal only when the translate button is clicked.
    @app.callback(
        Output("audio-result-modal", "is_open"),
        Output("audio-translation-table", "children"),
        Input("audio-translate-btn", "n_clicks"),
        Input("close-audio-modal", "n_clicks"),
        State("target-language", "value"),
        State("audio-upload", "contents"),
        State("audio-result-modal", "is_open"),
        prevent_initial_call=True,
    )
    def translate_audio(btn_clicks, close_clicks, lang, audio_contents, is_open):
        if not ctx.triggered:
            return is_open, no_update

        trigger = ctx.triggered_id

        # Only open when the translate button is clicked and audio exists
        if trigger == "audio-translate-btn":
            if not audio_contents:
                return is_open, html.Div("⚠️ No audio found. Please upload first.")
            lang_label, translated_audio_path = dummy_audio_translate(audio_contents, lang)

            table = dbc.Table([
                html.Thead(html.Tr([html.Th("Language"), html.Th("Translated Audio")])),
                html.Tbody([
                    html.Tr([
                        html.Td(lang_label),
                        html.Td([
                            html.Audio(src=translated_audio_path, controls=True, style={"width": "200px"}),
                            html.Br(),
                            html.A("Download", href=translated_audio_path, download=True)
                        ])
                    ])
                ])
            ], bordered=True, striped=True, hover=True)

            return True, table

        # Close the modal when close button clicked
        if trigger == "close-audio-modal":
            return False, no_update

        return is_open, no_update