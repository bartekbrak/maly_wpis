Aplikacja "mały wpis", nakodowałem minimalistyczne rozwiązanie zero-code prawie.

Prototyp rozwiązania oparty o google forms.
wypełnianie w przeglądarce: https://forms.gle/KqxBHWMx35c5F2uK8
id_formularza: 1FAIpQLSfuOs_WeY34JfOC210Q9IdsKXtyTe4qOxWrmxPBLRsfJCMIHw
id pytań: 20524943 1700693865 248453629 754572586 2074737791 283448663 499044367
arkusz odpowiedzi: https://docs.google.com/spreadsheets/d/14XO0oEPp1qA7nLS1yLoBlLznKWOYw9oobnWSDtvXuZQ/edit?resourcekey=&gid=807424543#gid=807424543

wypełnienie w konsoli:

    curl -X POST "https://docs.google.com/forms/d/e/1FAIpQLSfuOs_WeY34JfOC210Q9IdsKXtyTe4qOxWrmxPBLRsfJCMIHw/formResponse" \
        --data-urlencode "entry.20524943=Jakaś tam odpowiedź" \
        --data-urlencode "entry.1700693865=Jakaś tam odpowiedź" \
        --data-urlencode "entry.248453629=Jakaś tam odpowiedź" \
        --data-urlencode "entry.754572586=Jakaś tam odpowiedź" \
        --data-urlencode "entry.2074737791=Jakaś tam odpowiedź" \
        --data-urlencode "entry.283448663=Jakaś tam odpowiedź" \
        --data-urlencode "entry.499044367=Jakaś tam odpowiedź" \
        --data-urlencode "submit=Submit"

wypełnianie TUI:
    1. w oparciu o textual i uv run
    2. w oparciu o https://github.com/charmbracelet/gum
