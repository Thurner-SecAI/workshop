# Runbook Incident Response

**Gültig ab:** 2026-01-15 · **Verantwortlich:** SOC-Leitung · **Version:** 4.2 · **Prüfzyklus:** halbjährlich

## Zweck und Geltungsbereich

Dieses Runbook beschreibt, wie das Security Operations Center der Nordlicht Logistik SE einen Sicherheitsvorfall aufnimmt, bewertet, eindämmt und abschließt. Es gilt für alle Systeme im Asset-Inventar, für alle Standorte und für alle Vorfälle, die über SentinelGrid, den Service Desk oder eine externe Meldung eingehen.

## Rollen

| Rolle | Besetzung | Aufgabe |
|---|---|---|
| Incident Lead | Schichtführung SOC | führt den Vorfall, entscheidet über Maßnahmen |
| Analyst | SOC-Schicht | untersucht, dokumentiert, sammelt Beweise |
| System Owner | laut Asset-Inventar | setzt Maßnahmen auf dem betroffenen System um |
| Kommunikation | Unternehmenskommunikation | jede Aussage nach außen |
| Krisenstab | CISO, CIO, Rechtsabteilung | ab Stufe SEV-1 |

Der Incident Lead ist nicht zwingend die fachlich erfahrenste Person. Die Rolle ist eine Führungsrolle: Sie hält den Überblick, verteilt Aufgaben und trifft Entscheidungen.

## Schweregrade

| Stufe | Kriterium | Reaktionszeit | Eskalation |
|---|---|---|---|
| SEV-1 | Produktionsausfall, Datenabfluss oder aktiv ausgenutzte kritische Schwachstelle | 15 Minuten, rund um die Uhr | CISO sofort, Krisenstab innerhalb von 60 Minuten |
| SEV-2 | Einzelnes System kompromittiert, keine Kundendaten betroffen | 1 Stunde während der Geschäftszeit | SOC-Leitung |
| SEV-3 | Verdacht ohne Bestätigung, Richtlinienverstoß | 1 Arbeitstag | keine |
| SEV-4 | Beobachtung ohne unmittelbaren Handlungsbedarf | 5 Arbeitstage | keine |

Über die Einstufung auf SEV-1 entscheidet der Incident Lead. Die Entscheidung wird nicht verhandelt, sondern im Ticket begründet. Eine spätere Herabstufung ist möglich und wird ebenfalls begründet.

## Ablauf

### 1. Aufnahme

Jeder Vorfall bekommt ein Ticket in Helios ITSM mit dem Präfix `INC-`. Pflichtfelder sind Zeitpunkt der Erkennung, Quelle der Meldung, betroffene Assets und die erste Einschätzung. Ohne Ticket keine Maßnahme — auch nicht bei offensichtlichen Fällen.

### 2. Triage

Der Analyst prüft innerhalb der Reaktionszeit: Ist die Meldung echt? Welche Systeme sind betroffen? Läuft der Angriff noch? Grundlage sind die Ereignisse in SentinelGrid, das Asset-Inventar und die Kontaktliste der System Owner.

### 3. Eindämmung

Vor der Bereinigung steht die Eindämmung. Übliche Maßnahmen in der Reihenfolge ihrer Schwere:

* Netzsegment des betroffenen Systems isolieren
* betroffene Konten sperren und Sessions verwerfen
* eingehenden Zugriff aus dem Internet auf den betroffenen Dienst blockieren
* System vom Netz nehmen, nur nach Rücksprache mit dem System Owner

Ein System wird **nicht** neu gestartet und **nicht** neu installiert, bevor eine forensische Sicherung vorliegt. Der Arbeitsspeicher ist nach einem Neustart verloren.

### 4. Beweissicherung

Gesichert werden mindestens: Systemabbild oder Snapshot, relevante Logdateien, Netzwerkmitschnitt der letzten Stunde, Liste der laufenden Prozesse und offenen Verbindungen. Alle Artefakte werden im Beweisspeicher `evidence.nordlicht.internal` abgelegt, mit Prüfsumme und Zeitstempel. Zugriff darauf hat nur das SOC.

### 5. Bereinigung und Wiederanlauf

Die Bereinigung folgt der Ursache, nicht dem Symptom. Ein System geht erst zurück in den Betrieb, wenn die ausgenutzte Schwachstelle geschlossen ist, alle Zugangsdaten des Systems erneuert sind und die Überwachung eine Woche lang unauffällig bleibt.

### 6. Abschluss

Ein Vorfall gilt als abgeschlossen, wenn das Ticket alle Maßnahmen dokumentiert, der System Owner den Wiederanlauf bestätigt hat und die Nacharbeiten als eigene Tickets erfasst sind. Für SEV-1 und SEV-2 ist innerhalb von zehn Arbeitstagen ein Post-Mortem zu erstellen.

## Meldepflichten

Bei Verdacht auf einen Abfluss personenbezogener Daten informiert der Incident Lead unverzüglich die Rechtsabteilung. Die Frist gegenüber der Aufsichtsbehörde beträgt 72 Stunden ab Kenntnis. Die Frist läuft ab dem Zeitpunkt, an dem der Verdacht begründet ist, nicht ab der Bestätigung.

## Was nicht getan wird

Keine Kommunikation an Kunden, Presse oder Sozialkanäle ohne die Unternehmenskommunikation. Kein Kontakt zu einem Angreifer. Keine Gegenangriffe. Keine Analyse von Schadsoftware auf einem Arbeitsplatzrechner — dafür gibt es die abgeschottete Analyseumgebung `lab-sandbox-01`.
