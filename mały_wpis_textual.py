# /// script
# dependencies = [
#   "textual",
#   "httpx",
# ]
# ///

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Label, Button, TextArea
from textual.containers import ScrollableContainer, Vertical
import httpx

# --- CONFIGURATION ---
URL = "https://docs.google.com/forms/d/e/1FAIpQLSfuOs_WeY34JfOC210Q9IdsKXtyTe4qOxWrmxPBLRsfJCMIHw/formResponse"

# Map: (Label, Google ID, WidgetType)
# Using TextArea for thoughts (long text), Input for short facts.
QUESTIONS = [
    ("Jakie pozytywne myśli?", "20524943", "long"),
    ("Jakie negatywne myśli?", "1700693865", "long"),
    ("Jak możesz sobie pomóc?", "248453629", "long"),
    ("Ruszałeś się dzisiaj/wczoraj?", "754572586", "short"),
    ("O której poszedłeś spać?", "2074737791", "short"),
    ("Czego się boisz?", "283448663", "long"),
    ("Jak fizycznie się czujesz?", "499044367", "long"),
]

class GoogleFormTUI(App):
    TITLE = "Dziennik Samopoczucia"
    BINDINGS = [("q", "quit", "Wyjdź"), ("ctrl+s", "submit", "Wyślij")]

    CSS = """
    ScrollableContainer { padding: 1 2; }
    Label { margin-top: 1; color: $accent; text-style: bold; }
    Input, TextArea { margin-bottom: 1; border: tall $primary; }
    TextArea { height: 5; }
    Input:focus, TextArea:focus { border: tall $secondary; background: $boost; }
    #status { margin-top: 2; text-align: center; background: $surface; padding: 1; min-height: 3; }
    Button { margin-top: 2; width: 100%; height: 3; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with ScrollableContainer():
            for label, gid, qtype in QUESTIONS:
                yield Label(label)
                if qtype == "long":
                    # TextArea for paragraphs
                    yield TextArea(id=f"f_{gid}")
                else:
                    # Input for single line
                    yield Input(placeholder="Wpisz tutaj...", id=f"f_{gid}")
            yield Button("WYŚLIJ FORMULARZ (Ctrl+S)", variant="primary", id="submit_btn")
            yield Label("Gotowy", id="status")
        yield Footer()

    def on_mount(self) -> None:
        # Focus the first question immediately
        first_input = self.query_one("#f_20524943")
        first_input.focus()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit_btn":
            await self.action_submit()

    async def action_submit(self) -> None:
        status = self.query_one("#status", Label)
        status.update("Wysyłanie...")

        # Collect data
        form_data = {}
        # Get data from both Inputs and TextAreas
        for widget in self.query("Input, TextArea"):
            google_id = f"entry.{widget.id[2:]}" # Strips 'f_'
            form_data[google_id] = widget.text if hasattr(widget, 'text') else widget.value
        
        form_data["submit"] = "Submit"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(URL, data=form_data)
                if response.status_code == 200:
                    status.update("✅ Sukces! Formularz wysłany do Google.")
                    # Clear all fields
                    for widget in self.query("Input, TextArea"):
                        if hasattr(widget, 'text'): widget.text = ""
                        else: widget.value = ""
                else:
                    status.update(f"❌ Błąd: {response.status_code}")
        except Exception as e:
            status.update(f"❌ Błąd połączenia: {str(e)}")

if __name__ == "__main__":
    app = GoogleFormTUI()
    app.run()