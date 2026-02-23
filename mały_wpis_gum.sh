#!/bin/bash

# --- CONFIGURATION ---
URL="https://docs.google.com/forms/d/e/1FAIpQLSfuOs_WeY34JfOC210Q9IdsKXtyTe4qOxWrmxPBLRsfJCMIHw/formResponse"

# Initialize variables
Q1=""; Q2=""; Q3=""; Q4=""; Q5=""; Q6=""; Q7=""

while true; do
  clear
  gum style --foreground 212 --border double --padding "0 1" "Dziennik Samopoczucia"
  
  # Prepare previews: replace newlines with spaces so the menu doesn't break
  P1=$(echo "$Q1" | tr '\n' ' '); P2=$(echo "$Q2" | tr '\n' ' ')
  P3=$(echo "$Q3" | tr '\n' ' '); P6=$(echo "$Q6" | tr '\n' ' ')
  P7=$(echo "$Q7" | tr '\n' ' ')

  # Menu with full questions and non-truncated answers
  CHOICE=$(gum choose --header "Wybierz pole do edycji:" -- \
    "Jakie pozytywne myśli? -> $P1" \
    "Jakie negatywne myśli? -> $P2" \
    "Jak możesz sobie pomóc? -> $P3" \
    "Ruszałeś się dzisiaj/wczoraj? -> $Q4" \
    "O której poszedłeś spać? -> $Q5" \
    "Czego się boisz? -> $P6" \
    "Jak fizycznie się czujesz? -> $P7" \
    "---" \
    "WYŚLIJ (Submit)" \
    "WYJDŹ (Exit)")

  case "$CHOICE" in
    "Jakie pozytywne"*) Q1=$(gum write --value "$Q1" --placeholder "Jakie pozytywne myśli?") ;;
    "Jakie negatywne"*) Q2=$(gum write --value "$Q2" --placeholder "Jakie negatywne myśli?") ;;
    "Jak możesz"*)      Q3=$(gum write --value "$Q3" --placeholder "Jak możesz sobie pomóc?") ;;
    "Ruszałeś się"*)    Q4=$(gum input --value "$Q4" --placeholder "Ruszałeś się dzisiaj/wczoraj?") ;;
    "O której"*)        Q5=$(gum input --value "$Q5" --placeholder "O której poszedłeś spać?") ;;
    "Czego się boisz"*) Q6=$(gum write --value "$Q6" --placeholder "Czego się boisz?") ;;
    "Jak fizycznie"*)   Q7=$(gum write --value "$Q7" --placeholder "Jak fizycznie się czujesz?") ;;
    "WYŚLIJ"*) break ;;
    "WYJDŹ"*) exit 0 ;;
  esac
done

# Final Verification
echo -e "\nTwoje odpowiedzi:"
gum style --foreground 212 "1. $Q1" "2. $Q2" "3. $Q3" "4. $Q4" "5. $Q5" "6. $Q6" "7. $Q7"

if gum confirm "Czy chcesz wysłać te dane?"; then
    gum spin --title "Trwa wysyłanie do Google..." -- \
    curl -s -o /dev/null -w "%{http_code}" -X POST "$URL" \
        --data-urlencode "entry.20524943=$Q1" \
        --data-urlencode "entry.1700693865=$Q2" \
        --data-urlencode "entry.248453629=$Q3" \
        --data-urlencode "entry.754572586=$Q4" \
        --data-urlencode "entry.2074737791=$Q5" \
        --data-urlencode "entry.283448663=$Q6" \
        --data-urlencode "entry.499044367=$Q7" \
        --data-urlencode "submit=Submit"
    
    echo -e "\n✅ Wysłano pomyślnie!"
else
    echo "Anulowano."
fi