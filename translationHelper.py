from dash import html, Input, Output, State, ctx,no_update
import dash_bootstrap_components as dbc
import dash
import requests

# Dummy translation function
# def dummy_translate(text, target_lang):
#     translations = {
#         "df": ("Hindi", text, "/assets/hindi.mp3"),
#         "ta": ("Tamil", "வணக்கம் உலகம்", "/assets/tamil.mp3"),
#         "gu": ("Gujarati", "હેલો વિશ્વ", "/assets/gujarati.mp3"),
#     }
#     return translations.get(target_lang, ("Unknown", "N/A", ""))

def dummy_translate(text, target_lang, use_backend=True):
    """
    Wrapper for translation.
    If use_backend=True -> Calls FastAPI backend
    If use_backend=False -> Uses dummy translations
    """

    if not use_backend:
        # Local dummy fallback
        translations = {
            "hi": ("Hindi", "हैलो, आप कैसे हैं?", "/assets/hindi.mp3"),
            "ta": ("Tamil", "வணக்கம் உலகம்", "/assets/tamil.mp3"),
            "gu": ("Gujarati", "હેલો વિશ્વ", "/assets/gujarati.mp3"),
        }
        lang, translated, audio = translations.get(target_lang, ("Unknown", "N/A", ""))
        return [{
            "language": target_lang,
            "translation": translated,
            "audio_file": audio
        }]

    # Call FastAPI backend
    try:
        response = requests.post(
            "http://localhost:8000/text-to-speech",   # FastAPI endpoint
            json={"source_text": text, "target_languages": target_lang}
        )
        if response.status_code == 200:
            return response.json()  # Already in expected format (list of dicts)
        else:
            return [{
                "language": target_lang,
                "translation": "Error from backend",
                "audio_file": ""
            }]
    except Exception as e:
        return [{
            "language": target_lang,
            "translation": f"Exception: {str(e)}",
            "audio_file": ""
        }]

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
            results = dummy_translate(text, lang)  # list of dicts from backend

            # Build rows dynamically for each translation
            rows = []
            for translation in results:
                lang_name = translation.get("language", "Unknown")
                translated_text = translation.get("translation", "N/A")
                audio_file = translation.get("audio_file", "")

                download_name = f"tts_{lang_name}.wav"

                rows.append(
                    html.Tr([
                        html.Td(lang_name),
                        html.Td(translated_text),
                        html.Td([
                            html.Audio(src=audio_file, controls=True,
                                       style={"width": "200px"}) if audio_file else "N/A",
                            html.Br(),
                            html.A(
                                "Download",
                                href=audio_file,
                                download=download_name
                            ) if audio_file else ""
                        ])
                    ])
                )

            table = dbc.Table([
                html.Thead(html.Tr([
                    html.Th("Language"),
                    html.Th("Translated Text"),
                    html.Th("Audio")
                ])),
                html.Tbody(rows)
            ], bordered=True, striped=True, hover=True)

            return True, table

        elif trigger == "close-modal":
            return False, dash.no_update

        return is_open, dash.no_update
