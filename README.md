# Rozwiązanie zadania rekrutacyjnego do KN Solvro (sekcja ML)

## Raport
Raport opisujący przeprowadzone badanie dostępny jest w folderze `latex/` (plik `report.pdf`).

## Reprodukcja
Do zarządzania środowiskiem wirtualnym Pythona użyty został `uv` - package manager od Astral.
Spis użytych bibliotek znajduje się w pliku `pyproject.toml`.
Do odtworzenia środowiska wirtualnego wystarczy uruchomić polecenie:
```
uv sync
```
Wykorzystany zostanie wówczas plik `uv.lock`, który zawiera snapshot środowiska wirtualnego.

Uruchomienie EDA:
```
uv run src/eda.py
```
