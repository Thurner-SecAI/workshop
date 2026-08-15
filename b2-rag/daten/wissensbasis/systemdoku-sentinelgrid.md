# Systemdokumentation SentinelGrid

**Stand:** 2026-05-20 · **Verantwortlich:** Plattformteam SOC · **Version:** 9.3 · **Klassifikation:** intern

## 1 Überblick

SentinelGrid ist die zentrale Plattform für Ereignisdaten der Nordlicht Logistik SE. Sie nimmt Protokolle aus rund 4.100 Quellen entgegen, normalisiert sie auf ein gemeinsames Schema, wertet sie gegen Erkennungsregeln aus und stellt sie dem Security Operations Center zur Suche bereit. Die Plattform ist selbst betrieben und läuft auf eigener Hardware in den Rechenzentren Hamburg und Rotterdam.

Diese Dokumentation beschreibt Aufbau, Betrieb und Grenzen der Plattform. Sie richtet sich an das Plattformteam, an die Analysten im SOC und an System Owner, die eine neue Quelle anbinden wollen.

Was SentinelGrid **nicht** ist: kein Werkzeug für Anwendungs-Monitoring, keine Ablage für Geschäftsdaten und kein Ersatz für die Protokollierung auf den Quellsystemen selbst. Anwendungsmetriken laufen über eine getrennte Zeitreihendatenbank; SentinelGrid sieht davon nur die sicherheitsrelevanten Ereignisse.

## 2 Architektur

Die Plattform besteht aus fünf Schichten. Jede Schicht ist unabhängig skalierbar und hat einen eigenen Ausfallpfad.

| Schicht | Aufgabe | Komponenten | Standort |
|---|---|---|---|
| Erfassung | Ereignisse entgegennehmen | 8 Collector-Knoten | Hamburg, Rotterdam |
| Aufbereitung | Normalisieren, Anreichern | 6 Prozessor-Knoten | Hamburg |
| Speicherung | Indexieren, Vorhalten | 12 Index-Knoten, Objektspeicher | Hamburg, Rotterdam |
| Auswertung | Regeln, Korrelation | 4 Regel-Knoten | Hamburg |
| Zugriff | Suche, Dashboards, API | 3 Frontend-Knoten | Hamburg |

### 2.1 Erfassung

Die Collector-Knoten nehmen Daten über vier Wege entgegen: Syslog über TCP mit TLS auf Port 6514, den SentinelGrid-Agenten auf Port 9443, HTTP-Einlieferung über die API `/ingest/v1/events` und Abholung aus Warteschlangen für Cloud-Dienste. Jeder Weg schreibt in denselben Puffer.

Der Puffer ist eine verteilte Warteschlange mit einer Vorhaltezeit von sechs Stunden. Fällt die Aufbereitung aus, laufen die Daten nicht verloren, sondern stauen sich. Sechs Stunden sind so bemessen, dass ein ungeplanter Ausfall über Nacht ohne Datenverlust überstanden wird.

Quellen liefern nicht direkt an einen Knoten, sondern an den Namen `ingest.nordlicht.internal`. Dahinter steht ein Load Balancer, der auf beide Standorte verteilt. Fällt ein Standort aus, übernimmt der andere die volle Last; dafür ist jeder Standort auf 60 Prozent der Gesamtlast ausgelegt.

### 2.2 Aufbereitung

Die Prozessor-Knoten bringen jedes Ereignis auf das gemeinsame Schema. Das Schema folgt dem Elastic Common Schema in der Fassung 8.11 und ist um sieben eigene Felder erweitert, darunter `nl.asset_id`, `nl.standort` und `nl.kritikalitaet`.

Die Anreicherung ergänzt jedes Ereignis um:

* die Asset-Kennung aus dem Asset-Inventar, ermittelt über IP-Adresse und Zeitpunkt
* den Standort und die Kritikalität des Assets
* den Namen des System Owners
* geografische Angaben zu öffentlichen IP-Adressen
* Treffer aus den Threat-Intelligence-Listen

Ereignisse, die sich keiner Asset-Kennung zuordnen lassen, bekommen den Wert `unbekannt` und erscheinen im täglichen Bericht `Unbekannte Quellen`. Ein hoher Anteil unbekannter Ereignisse ist fast immer ein Hinweis auf ein Asset, das im Inventar fehlt.

### 2.3 Speicherung

Die Index-Knoten halten die Daten für den schnellen Zugriff. Die Vorhaltezeit im schnellen Zugriff richtet sich nach der Datenart und ist in der Richtlinie Logging und Aufbewahrung festgelegt. Nach Ablauf wird ein Index in den Objektspeicher verschoben, dort unveränderlich abgelegt und aus dem schnellen Zugriff entfernt.

Jeder Index existiert zweimal: einmal in Hamburg, einmal in Rotterdam. Der Abgleich läuft asynchron mit einem Rückstand von typischerweise unter zwei Minuten. Bei einem Ausfall in Hamburg ist die Suche in Rotterdam sofort möglich, es können aber die letzten Minuten fehlen.

### 2.4 Auswertung

Die Regel-Knoten werten den Datenstrom gegen die Erkennungsregeln aus. Regeln sind in Sigma geschrieben und liegen im Git-Repository `soc/detections`. Jede Regel hat eine Kennung nach dem Muster `SG-<Bereich>-<Nummer>`, eine Beschreibung, eine Einstufung, einen Verweis auf die Gegenmaßnahme und mindestens einen Test.

Eine Regel geht erst in den Betrieb, wenn sie gegen die Ereignisse der letzten 30 Tage geprüft wurde. Erzeugt sie dabei mehr als 50 Treffer pro Tag, gilt sie als zu unscharf und wird überarbeitet.

Die Korrelation fasst zusammengehörende Treffer zu einem Fall zusammen. Grundlage ist ein Zeitfenster von 30 Minuten und mindestens ein gemeinsames Feld — üblicherweise Asset, Konto oder Quell-IP. Aus einem Fall entsteht automatisch ein Ticket in Helios ITSM.

### 2.5 Zugriff

Analysten arbeiten über die Weboberfläche unter `https://sentinelgrid.nordlicht.internal`. Der Zugang erfordert ein persönliches Konto, MFA mit FIDO2 und die Rolle `soc.analyst` oder `soc.lead`. Die Suchsprache ist SGQL, eine Teilmenge von KQL mit eigenen Erweiterungen für Zeitfenster.

Die API unter `/api/v3` liefert dieselben Daten für Automatisierung und Berichte. Zugriff über die API erfolgt mit kurzlebigen Token, die höchstens acht Stunden gültig sind.

## 3 Kapazität und Leistung

Im Normalbetrieb verarbeitet SentinelGrid rund 42.000 Ereignisse pro Sekunde. Die Spitzenlast liegt bei 78.000 Ereignissen pro Sekunde und tritt werktags zwischen 07:30 und 08:30 Uhr auf, wenn sich die Belegschaft anmeldet. Die Auslegungsgrenze der aktuellen Hardware liegt bei 110.000 Ereignissen pro Sekunde.

| Kennzahl | Wert |
|---|---|
| Ereignisse pro Tag | rund 3,6 Milliarden |
| Datenvolumen pro Tag nach Komprimierung | 2,1 Terabyte |
| Speicher im schnellen Zugriff | 340 Terabyte |
| Speicher im Archiv | 4,8 Petabyte |
| Angebundene Quellen | 4.100 |
| Aktive Erkennungsregeln | 612 |
| Fälle pro Tag im Mittel | 34 |

Die Antwortzeit einer Suche über 24 Stunden liegt im Mittel bei 1,8 Sekunden, über 30 Tage bei 11 Sekunden. Suchen über das Archiv dauern länger, weil die Daten zuerst zurückgeholt werden; die Bereitstellung ist innerhalb von vier Stunden zugesagt.

Die Verzögerung zwischen dem Entstehen eines Ereignisses und seiner Sichtbarkeit in der Suche beträgt im Mittel 24 Sekunden. Der vereinbarte Wert liegt bei 60 Sekunden und wird als Kennzahl `ingest_lag_p95` überwacht.

## 4 Anbindung einer neuen Quelle

Eine neue Quelle wird über das Formular `Quelle anbinden` in Helios ITSM beantragt. Der Antrag enthält Asset-Kennung, Art der Quelle, erwartetes Volumen und den fachlichen Grund. Das Plattformteam prüft, ob ein Parser vorhanden ist.

1. **Parser prüfen.** Für 140 Produkte liegt ein Parser bereit. Fehlt einer, wird er geschrieben; der Aufwand liegt bei ein bis drei Tagen.
2. **Testeinlieferung.** Die Quelle liefert zunächst in den Index `staging-*`. Dort wird geprüft, ob Felder korrekt belegt sind und die Zeitstempel stimmen.
3. **Volumenabschätzung.** Liegt das erwartete Volumen über 500 Ereignissen pro Sekunde, wird die Kapazitätsplanung angepasst.
4. **Freigabe.** Nach erfolgreicher Testeinlieferung wird die Quelle auf den produktiven Index umgestellt und im Quellenverzeichnis eingetragen.
5. **Regeln.** Der Antragsteller benennt, welche Ereignisse sicherheitsrelevant sind. Daraus entstehen Regeln oder Ergänzungen bestehender Regeln.

Eine Quelle ohne Eintrag im Quellenverzeichnis wird nach 14 Tagen verworfen. Das verhindert, dass Testsysteme dauerhaft Volumen erzeugen.

### 4.1 Parser

Ein Parser besteht aus einer Erkennungsbedingung, einer Zerlegungsvorschrift und einer Abbildung auf das gemeinsame Schema. Die Erkennungsbedingung entscheidet, welcher Parser für ein Rohereignis zuständig ist; sie prüft üblicherweise Programmname und Format der ersten Zeichen. Die Zerlegung arbeitet mit Grok-Mustern für Textformate und direkt mit Feldern für JSON-Quellen.

Jeder Parser liegt im Repository `soc/parsers` und braucht mindestens fünf Testereignisse mit erwartetem Ergebnis. Die Tests laufen bei jeder Änderung; ein Parser ohne grüne Tests wird nicht ausgeliefert. Änderungen an einem Parser wirken nur auf neu eintreffende Ereignisse, nicht rückwirkend auf bereits indexierte Daten.

Fällt ein Parser aus, weil eine Quelle ihr Format geändert hat, landet das Ereignis mit dem Feld `nl.parse_error` im Index und bleibt durchsuchbar. Diese Ereignisse erscheinen im Bericht `Parse-Fehler` und werden innerhalb von fünf Arbeitstagen bearbeitet.

## 5 Betrieb

### 5.1 Überwachung der Plattform

SentinelGrid überwacht sich selbst. Die wichtigsten Kennzahlen und ihre Schwellen:

| Kennzahl | Warnung | Alarm |
|---|---|---|
| `ingest_lag_p95` | 60 Sekunden | 300 Sekunden |
| Puffer-Füllstand | 40 Prozent | 70 Prozent |
| Ausgefallene Quellen | 5 | 20 |
| Freier Speicher schneller Zugriff | 20 Prozent | 10 Prozent |
| Abgleichsrückstand Rotterdam | 5 Minuten | 30 Minuten |

Alarme gehen an die Rufbereitschaft des Plattformteams. Der Ausfall einer einzelnen Quelle ist kein Alarm, sondern erscheint im Bericht `Stille Quellen`.

### 5.2 Wartung

Updates der Plattform laufen im Wartungsfenster der Produktion Hamburg, donnerstags ab 22:00 Uhr. Die Knoten werden nacheinander aktualisiert; die Erfassung läuft dabei weiter, weil der Puffer die Lücke überbrückt. Ein Update dauert je nach Umfang zwei bis vier Stunden.

Größere Versionssprünge werden zuerst in der Umgebung `sg-stage` geprüft, die einen Zehntel der Produktionslast aus gespiegelten Daten erhält.

### 5.3 Sicherung

Gesichert werden Konfiguration, Regelwerk, Dashboards und die Zuordnungstabellen — nicht die Ereignisdaten selbst, die durch die Spiegelung nach Rotterdam und das Archiv abgedeckt sind. Die Sicherung läuft täglich um 01:00 Uhr, wird 90 Tage aufbewahrt und vierteljährlich durch eine Rücksicherung in `sg-stage` geprüft.

### 5.4 Wiederanlauf

Für den vollständigen Verlust des Standorts Hamburg ist ein Wiederanlauf in Rotterdam vorgesehen. Die Zielvorgaben lauten: Wiederherstellungszeit vier Stunden, maximaler Datenverlust fünf Minuten. Der Wiederanlauf wird jährlich geprobt, zuletzt am 08.02.2026 mit einer gemessenen Wiederherstellungszeit von drei Stunden und zehn Minuten.

## 6 Schnittstellen

| Gegenstelle | Richtung | Zweck | Technik |
|---|---|---|---|
| Asset-Inventar AssetHub | lesend | Anreicherung, Kritikalität | REST, stündlich |
| Helios ITSM | schreibend | Tickets aus Fällen | REST, ereignisgesteuert |
| Verzeichnisdienst | lesend | Kontodaten, Gruppen | LDAP, stündlich |
| Threat-Intelligence-Feeds | lesend | Indikatoren | STIX/TAXII, alle 30 Minuten |
| Schwachstellen-Scanner | lesend | Scanergebnisse | REST, täglich 04:00 |
| Beweisspeicher | schreibend | Exporte für Vorfälle | S3-kompatibel |

Alle Schnittstellen nutzen technische Konten mit kurzlebigen Token. Die Konten sind im Secret-Store hinterlegt und haben einen benannten Verantwortlichen im Plattformteam.

## 7 Bekannte Grenzen

* **Zeitstempel aus der Zukunft.** Ereignisse mit einem Zeitstempel mehr als fünf Minuten in der Zukunft werden auf die Empfangszeit gesetzt und markiert. Ursache ist fast immer eine falsch gesetzte Zeitzone auf der Quelle.
* **Sehr lange Einzelereignisse.** Ereignisse über 32 Kilobyte werden abgeschnitten. Betroffen sind vor allem Prozessaufrufe mit sehr langen Kommandozeilen; das relevante Feld bleibt in der Regel erhalten, der Rest nicht.
* **Suche über mehr als 90 Tage.** Solche Suchen greifen auf das Archiv zu und laufen asynchron. Das Ergebnis kommt als Benachrichtigung, nicht als direkte Antwort in der Oberfläche.
* **Keine Volltextsuche über Anhänge.** Dateien aus Tickets oder E-Mails werden nicht indexiert, nur ihre Prüfsummen.
* **Regeln über mehrere Standorte.** Korrelationen, die Ereignisse aus Hamburg und Rotterdam verbinden, greifen erst nach Abschluss des Abgleichs. Bei erhöhtem Rückstand verzögern sich diese Regeln entsprechend.

## 8 Zuständigkeiten

| Bereich | Zuständig | Vertretung |
|---|---|---|
| Plattform, Knoten, Speicher | Plattformteam SOC | IT-Betrieb Hamburg |
| Regelwerk und Korrelation | Detection Engineering | SOC-Leitung |
| Anbindung neuer Quellen | Plattformteam SOC | — |
| Zugriffsrechte auf die Oberfläche | Identity & Access Management | SOC-Leitung |
| Verträge und Lizenzen | Einkauf IT | CISO |

## 9 Häufige Störungen und ihre Behandlung

### 9.1 Der Puffer läuft voll

Ein steigender Puffer-Füllstand bedeutet, dass die Aufbereitung langsamer arbeitet als die Erfassung liefert. Übliche Ursachen sind ein Prozessor-Knoten, der nach einem Update nicht wieder in die Gruppe zurückgekehrt ist, ein neuer Parser mit einem teuren regulären Ausdruck oder eine Quelle, die plötzlich das Zehnfache ihres üblichen Volumens sendet.

Vorgehen: zuerst die Zahl der aktiven Prozessor-Knoten prüfen, dann die Rangliste der Quellen nach Volumen der letzten Stunde. Eine einzelne entgleiste Quelle wird über die Sperrliste am Collector angehalten; das ist eine bewusste Entscheidung des Incident Lead und wird im Ticket festgehalten. Der Puffer leert sich danach mit etwa dem Doppelten der Zulaufrate.

### 9.2 Eine Quelle liefert nicht mehr

Der Bericht `Stille Quellen` erscheint werktags um 09:00 Uhr und listet jede Quelle, die in den letzten 24 Stunden weniger als zehn Prozent ihres üblichen Volumens geliefert hat. Häufigste Ursachen sind ein abgelaufenes Zertifikat auf der Quelle, eine geänderte Firewall-Regel und ein Neustart des Quellsystems ohne Start des Agenten.

Der Bericht geht an das Plattformteam und an den jeweiligen System Owner. Bleibt eine Quelle länger als 30 Tage still, wird sie aus dem Quellenverzeichnis entfernt und das Asset im Inventar als nicht angebunden markiert.

### 9.3 Suchen sind langsam

Langsame Suchen haben fast immer eine der drei Ursachen: ein zu großes Zeitfenster, eine Suche mit führendem Platzhalter oder eine gleichzeitige Archivrückholung, die Speicherbandbreite belegt. Führende Platzhalter lassen sich meist durch ein Feldkriterium ersetzen; die Oberfläche weist beim Absenden darauf hin.

Für wiederkehrende Auswertungen über große Zeiträume gibt es gespeicherte Suchen, die nachts laufen und ihr Ergebnis als Tabelle ablegen.

### 9.4 Doppelte Ereignisse

Doppelte Ereignisse entstehen, wenn eine Quelle sowohl über Syslog als auch über den Agenten liefert. Das kommt bei Umstellungen vor. Die Aufbereitung erkennt Duplikate über eine Prüfsumme aus Zeitstempel, Quelle und Rohtext innerhalb eines Fensters von fünf Minuten und verwirft sie. Über das Fenster hinaus bleiben Duplikate bestehen und müssen an der Quelle abgestellt werden.

### 9.5 Abgleich nach Rotterdam hängt

Ein Rückstand über 30 Minuten ist ein Alarm. Ursache ist meistens die Netzstrecke zwischen den Standorten, seltener ein voller Index-Knoten in Rotterdam. Solange der Rückstand besteht, sind Suchen in Rotterdam unvollständig und standortübergreifende Korrelationsregeln verzögert. Die Erfassung ist davon nicht betroffen.

## 10 Rollen in der Oberfläche

| Rolle | Rechte | Vergabe |
|---|---|---|
| `soc.analyst` | Suche über alle Indizes, Fälle bearbeiten | IAM, nach Freigabe der SOC-Leitung |
| `soc.lead` | zusätzlich Regeln ändern, Quellen sperren | IAM, nach Freigabe des CISO |
| `soc.plattform` | zusätzlich Knoten und Konfiguration verwalten | IAM, nach Freigabe des CISO |
| `owner.readonly` | Suche nur über die eigenen Assets | IAM, nach Freigabe des Plattformteams |
| `audit.readonly` | Suche über Metadaten, keine Rohdaten | IAM, befristet auf die Prüfung |

Die Rolle `owner.readonly` filtert über das Feld `nl.asset_id`. Ein System Owner sieht damit die Ereignisse seiner eigenen Systeme, aber keine Ereignisse anderer Bereiche. Diese Trennung ist mit dem Betriebsrat abgestimmt und Voraussetzung dafür, dass Fachbereiche überhaupt Zugriff bekommen.

Jede Suche wird protokolliert: Konto, Zeitpunkt, Suchausdruck, Zahl der Treffer. Diese Protokolle liegen in einem eigenen Index, auf den nur die Rolle `audit.readonly` und der Datenschutz Zugriff haben.

## 11 Datenschutz

Die Plattform verarbeitet personenbezogene Daten, weil Anmeldungen und administrative Kommandos einem Konto zugeordnet sind. Grundlage ist die Betriebsvereinbarung BV-2025-07. Die Verarbeitung ist auf den Zweck der Erkennung und Aufklärung von Sicherheitsvorfällen beschränkt.

Drei Vorkehrungen setzen das technisch um: die Filterung nach Asset für Fachbereiche, das Vier-Augen-Prinzip bei personenbezogenen Auswertungen und die Protokollierung jeder Suche. Auswertungen zur Verhaltens- oder Leistungskontrolle finden nicht statt.

Anfragen betroffener Personen nach Auskunft beantwortet der Datenschutz mit Unterstützung des Plattformteams. Die Auskunft umfasst die zu einer Person gespeicherten Ereignisse im schnellen Zugriff; Archivdaten werden auf ausdrückliche Anforderung zurückgeholt.

## 12 Glossar

| Begriff | Bedeutung |
|---|---|
| Quelle | ein System, das Ereignisse an SentinelGrid liefert |
| Ereignis | eine einzelne Zeile im gemeinsamen Schema |
| Treffer | ein Ereignis, auf das eine Erkennungsregel zutrifft |
| Fall | mehrere zusammengehörende Treffer, aus denen ein Ticket entsteht |
| Parser | die Vorschrift, die aus einem Rohtext Felder macht |
| Index | die Einheit, in der Ereignisse gespeichert und gealtert werden |
| Rückstand | die Verzögerung des Abgleichs zwischen den Standorten |

## 13 Änderungsverzeichnis

| Version | Datum | Änderung |
|---|---|---|
| 9.3 | 2026-05-20 | Kapazitätszahlen aktualisiert, Abschnitt Grenzen ergänzt |
| 9.2 | 2026-02-11 | Wiederanlauf-Probe dokumentiert, Schwellen angepasst |
| 9.1 | 2025-11-30 | Schema auf ECS 8.11 gehoben |
| 9.0 | 2025-09-15 | Zweiter Standort Rotterdam in Betrieb genommen |
