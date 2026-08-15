# Interne Notiz: Token und Kosten bei Sprachmodellen

**Stand:** 2026-05-04 · **Autor:** Data & AI Team · **Klassifikation:** intern

## Worum es geht

Der geplante Assistent für das SOC schickt Text an ein Sprachmodell. Abgerechnet wird nach Token. Diese Notiz erklärt, was ein Token in diesem Zusammenhang ist, wie viele Token unsere Dokumente erzeugen und wie wir die Kosten schätzen.

## Was ein Token hier bedeutet

Ein Token ist ein Textstück, kein Zugangsmerkmal. Der Tokenizer zerlegt Text in Wortteile: häufige Wörter bleiben ganz, seltene zerfallen in mehrere Token. Deutscher Text erzeugt rund 30 Prozent mehr Token als englischer Text gleicher Länge, weil die Vokabulare überwiegend auf englischem Text entstanden sind.

Als Faustregel rechnen wir mit vier Zeichen je Token für deutschen Fließtext. Tabellen und Kommandozeilen liegen darunter, weil Sonderzeichen einzeln zählen.

## Zahlen aus unserer Wissensbasis

| Dokumentart | Zeichen | Token, geschätzt |
|---|---|---|
| CVE-Advisory | 2.500 | 700 |
| Runbook | 3.500 | 950 |
| Systemdokumentation | 15.000 | 4.100 |

Ein Prompt mit einer Frage und drei Ausschnitten liegt bei rund 1.200 Token. Die Antwort kommt auf 200 bis 400 Token.

## Rotieren im Kontext von Log-Dateien

Ein Wort, das in beiden Welten vorkommt, ist *rotieren*. Bei Log-Dateien bedeutet Rotation, dass eine Datei ab einer bestimmten Größe geschlossen, umbenannt und komprimiert wird, während der Dienst in eine neue Datei schreibt. Unsere Testläufe schreiben ihre Protokolle nach `/var/log/soc-assistent/`, mit täglicher Rotation und 14 Tagen Aufbewahrung. Mit Zugriffstoken hat diese Rotation nichts zu tun.

## Context Window

Das Modell kann nur eine begrenzte Zahl von Token gleichzeitig verarbeiten. Passt der Text nicht hinein, wird er abgeschnitten — ohne Fehlermeldung. Deshalb schicken wir nicht ganze Dokumente, sondern Ausschnitte.

## Nächste Schritte

Messung der tatsächlichen Token-Zahlen auf zehn typischen Fragen, danach eine Hochrechnung für 200 Anfragen am Tag.
