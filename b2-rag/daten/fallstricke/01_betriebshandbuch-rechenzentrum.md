# Betriebshandbuch Rechenzentrum Hamburg

**Stand:** 2026-04-30 · **Verantwortlich:** IT-Betrieb Hamburg · **Version:** 12.1 · **Klassifikation:** intern

## 1 Zweck

Dieses Handbuch beschreibt den Regelbetrieb des Rechenzentrums Hamburg der Nordlicht Logistik SE. Es gilt für alle Tätigkeiten im Gebäudeteil C, für die Kälte- und Stromversorgung, für den Zutritt und für die Übergabe zwischen den Schichten. Es ersetzt keine Herstellerdokumentation und keine Sicherheitsunterweisung.

## 2 Gebäude und Flächen

| Fläche | Nutzung | Stellplätze | Anschlussleistung |
|---|---|---|---|
| C1 | Netz und Kern | 24 Racks | 180 kW |
| C2 | Rechenknoten | 96 Racks | 720 kW |
| C3 | Speicher | 48 Racks | 300 kW |
| C4 | Reserve, Aufbau | 32 Racks | 240 kW |
| C0 | Technik, USV, Kälte | — | — |

Die Flächen sind durch Brandabschnitte getrennt. Türen zwischen den Abschnitten sind selbstschließend und dürfen nicht festgestellt werden. Kartonagen, Paletten und Verpackungsmaterial bleiben außerhalb der Flächen; das Auspacken erfolgt im Wareneingang.

## 3 Zutritt

Zutritt zum Gebäudeteil C haben nur Personen mit freigeschaltetem Ausweis und hinterlegtem Fingerabdruck. Die Freischaltung beantragt die Führungskraft; sie ist auf zwölf Monate befristet. Besucher werden am Empfang angemeldet, tragen einen Besucherausweis und werden durchgehend begleitet.

Jeder Zutritt wird protokolliert. Die Protokolle werden 365 Tage aufbewahrt und nur zur Aufklärung eines Vorfalls ausgewertet. Ein Zutritt ohne Ausweis, etwa im Türverbund mit einer anderen Person, ist ein meldepflichtiger Verstoß.

Für Arbeiten außerhalb der Regelarbeitszeit ist eine Anmeldung bis 16:00 Uhr des Vortags nötig. Alleinarbeit in den Technikräumen C0 ist nicht zulässig.

## 4 Stromversorgung

Die Versorgung erfolgt über zwei getrennte Einspeisungen aus verschiedenen Umspannwerken. Jede Einspeisung trägt die volle Last. Dahinter stehen zwei USV-Anlagen mit einer Überbrückungszeit von zwölf Minuten bei Volllast und zwei Netzersatzanlagen mit einer Startzeit von 18 Sekunden.

| Anlage | Typ | Leistung | Prüfung |
|---|---|---|---|
| USV-A | doppelt gewandelt | 800 kVA | monatlich, Kurztest |
| USV-B | doppelt gewandelt | 800 kVA | monatlich, Kurztest |
| NEA-1 | Diesel | 1.000 kVA | monatlich Probelauf, jährlich Lasttest |
| NEA-2 | Diesel | 1.000 kVA | monatlich Probelauf, jährlich Lasttest |

Der Dieselvorrat reicht für 72 Stunden Volllast. Ein Rahmenvertrag sichert die Nachlieferung innerhalb von acht Stunden zu. Der Füllstand wird täglich automatisch gemeldet; unter 60 Prozent wird nachbestellt.

Jedes Rack hat zwei Stromwege. Geräte mit nur einem Netzteil werden über einen automatischen Umschalter angebunden. Die Belegung eines Stromwegs überschreitet nie 40 Prozent der Absicherung, damit der zweite Weg die Last im Fehlerfall vollständig übernehmen kann.

## 5 Kälte

Die Kühlung arbeitet mit Kaltgang-Einhausung und einer Zulufttemperatur von 24 Grad Celsius. Vier Kältemaschinen versorgen die Flächen, drei davon reichen für die Volllast. Die freie Kühlung übernimmt bei Außentemperaturen unter 12 Grad und deckt über das Jahr rund 45 Prozent des Kältebedarfs.

Grenzwerte in den Flächen:

* Zuluft 22 bis 26 Grad, Alarm ab 28 Grad
* relative Feuchte 40 bis 60 Prozent
* Druckdifferenz Kaltgang zu Warmgang mindestens 5 Pascal

Blindplatten sind in allen freien Höheneinheiten Pflicht. Fehlende Blindplatten sind die häufigste Ursache für lokale Warmluftrückführung und werden bei jeder Begehung notiert.

## 6 Netz

Der Kern besteht aus zwei Spine-Switches und je zwei Leaf-Switches pro Reihe. Jedes Rack ist mit zweimal 25 Gigabit angebunden, die Kernstrecken mit 400 Gigabit. Die Anbindung nach Rotterdam läuft über zwei getrennte Trassen verschiedener Anbieter.

Patchungen werden ausschließlich über einen Change durchgeführt und im Kabeldokumentationswerkzeug nachgetragen. Eine Patchung ohne Eintrag gilt als nicht erfolgt. Farbcodierung: gelb für Produktion, blau für Verwaltung, rot für Speichernetz, grau für den Aufbau.

Der Zugriff auf die Verwaltungsoberfläche der Switches erfolgt über das getrennte Verwaltungsnetz. Automatisierte Zugriffe nutzen ein technisches Konto mit einem Token, das im Secret-Store hinterlegt ist. Wie ein solches Token erneuert wird, steht nicht in diesem Handbuch, sondern im zuständigen Runbook.

## 7 Schichtbetrieb

| Schicht | Zeit | Besetzung |
|---|---|---|
| Früh | 06:00 – 14:00 | 2 Personen |
| Spät | 14:00 – 22:00 | 2 Personen |
| Nacht | 22:00 – 06:00 | 1 Person plus Rufbereitschaft |

Die Übergabe dauert 15 Minuten und wird schriftlich festgehalten: offene Störungen, laufende Changes, Auffälligkeiten aus der Begehung, erwartete Anlieferungen. Ohne Übergabeprotokoll endet keine Schicht.

Die Schichtdokumentation läuft über eine Weboberfläche; die Anmeldung daran erfolgt persönlich, der automatische Abgleich mit dem Dienstplan über ein technisches Konto mit einem Token. Die Rufbereitschaft ist innerhalb von 30 Minuten vor Ort. Die Rufbereitschaftsliste liegt beim Empfang aus und im Verzeichnis `betrieb/rufbereitschaft`.

## 8 Begehungen

Zweimal je Schicht wird begangen. Geprüft werden: Anzeigen an USV und Kälteanlage, Temperaturen in den Kaltgängen, freie Fluchtwege, Zustand der Türen, ungewöhnliche Geräusche, Leckagen unter den Kälteverteilern und offene Racktüren. Befunde gehen als Ticket in Helios ITSM.

Die Begehung wird über acht Prüfpunkte quittiert. Der Quittungsvorgang läuft über eine App, die sich am Verwaltungsnetz anmeldet; das dafür verwendete Token wird zentral verwaltet.

## 9 Anlieferung und Einbau

Anlieferungen werden 48 Stunden vorher angekündigt. Der Wareneingang nimmt an Werktagen zwischen 08:00 und 16:00 Uhr an. Geräte werden im Wareneingang ausgepackt, inventarisiert und erst dann in die Fläche gebracht.

Der Wareneingang meldet jede Anlieferung über die Inventar-Schnittstelle. Der Zugriff darauf läuft über ein Token, das der IT-Betrieb verwaltet und turnusmäßig erneuert.

Jeder Einbau braucht: Change-Nummer, zugewiesenen Stellplatz, geprüfte Anschlussleistung, Eintrag im Asset-Inventar und beide Stromwege. Ein Gerät ohne Eintrag im Asset-Inventar wird nicht in Betrieb genommen.

## 10 Ausbau und Entsorgung

Beim Ausbau werden Datenträger vor dem Verlassen der Fläche entnommen. Sie werden entweder mehrfach überschrieben und wiederverwendet oder physisch vernichtet; der Vernichtungsnachweis wird fünf Jahre aufbewahrt. Der Eintrag im Asset-Inventar wird auf `ausgemustert` gesetzt, nicht gelöscht.

## 11 Brandschutz

Die Flächen sind mit einer Sauerstoffreduktionsanlage geschützt, die den Sauerstoffgehalt auf 15,5 Prozent hält. Der Aufenthalt ist damit für gesunde Personen bis zu vier Stunden zulässig. Personen mit Atemwegserkrankungen melden sich vorher beim Betriebsarzt.

Rauchmelder arbeiten als Ansaugsystem mit zwei Auslösestufen. Die erste Stufe meldet an die Leitwarte, die zweite löst den Alarm aus. Eine Auslösung der ersten Stufe wird immer vor Ort geprüft, auch nachts.

## 12 Wartungsfenster

Arbeiten an Strom und Kälte finden sonntags zwischen 02:00 und 06:00 Uhr statt. Arbeiten am Netzkern donnerstags ab 22:00 Uhr. Beide Fenster werden fünf Arbeitstage vorher angekündigt. Außerhalb der Fenster wird nur nach Freigabe des Incident Lead gearbeitet.

### 12.1 Protokolle

Die Anlagen schreiben ihre Meldungen in Dateien, die täglich rotieren und 14 Tage vorgehalten werden. Der Versand an SentinelGrid läuft über einen Agenten, dessen Token im Secret-Store liegt. Läuft das Token ab, bleiben die Meldungen liegen — das ist die häufigste Ursache für eine stille Quelle aus dem Rechenzentrum.

## 13 Kennzahlen

| Kennzahl | Zielwert | Ist 2025 |
|---|---|---|
| Verfügbarkeit Strom | 99,99 Prozent | 100 Prozent |
| Verfügbarkeit Kälte | 99,98 Prozent | 99,99 Prozent |
| PUE im Jahresmittel | unter 1,35 | 1,29 |
| Störungen mit Ausfall | höchstens 2 | 1 |
| Begehungen ohne Befund | über 90 Prozent | 93 Prozent |

## 14 Anhang

Notrufnummern, Ansprechpartner der Anlagenhersteller, Lagepläne der Absperrventile und die Liste der Ersatzteile im Vorrat stehen im Verzeichnis `betrieb/anhang`. Der Anhang wird vierteljährlich geprüft.
