# Runbook Patch-Management

**Gültig ab:** 2025-10-01 · **Verantwortlich:** IT-Betrieb, fachliche Freigabe SOC · **Version:** 3.1

## Zweck

Dieses Runbook regelt, wie Sicherheitsupdates bei der Nordlicht Logistik SE bewertet, freigegeben, eingespielt und nachgewiesen werden. Es beschreibt den Regelweg und den Notfallweg.

## Fristen

Die Frist läuft ab Freigabe durch das SOC, nicht ab Veröffentlichung durch den Hersteller.

| Einstufung | Kriterium | Frist für Server | Frist für Arbeitsplätze |
|---|---|---|---|
| Notfall | CVSS ≥ 9.0 und aktiv ausgenutzt | 72 Stunden | 72 Stunden |
| Kritisch | CVSS ≥ 9.0 | 7 Tage | 14 Tage |
| Hoch | CVSS 7.0 – 8.9 | 30 Tage | 30 Tage |
| Mittel | CVSS 4.0 – 6.9 | 90 Tage | 90 Tage |
| Niedrig | CVSS < 4.0 | nächster Wartungszyklus | nächster Wartungszyklus |

Ist ein System aus dem Internet erreichbar, gilt die nächsthöhere Stufe. Ist ein System nicht erreichbar und durch einen wirksamen Workaround geschützt, kann das SOC die Frist um eine Stufe verlängern und trägt das im Restrisiko-Register ein.

## Regelweg

1. **Erfassung.** Der Schwachstellen-Scanner meldet täglich um 04:00 Uhr an SentinelGrid. Neue Herstelleradvisories werden zusätzlich über die Advisory-Feeds eingelesen.
2. **Bewertung.** Das SOC bewertet innerhalb von zwei Arbeitstagen: Ist ein Asset betroffen? Ist es erreichbar? Gibt es einen Exploit? Grundlage sind CVSS, EPSS und das Asset-Inventar.
3. **Freigabe.** Die Freigabe erfolgt als Change in Helios ITSM mit Präfix `CHG-`. Der Change enthält Fenster, Rückfallplan und den Test, der den Erfolg belegt.
4. **Einspielen.** Zuerst Vorproduktion, dann Produktion. Zwischen beiden liegen mindestens 24 Stunden, in denen die Vorproduktion beobachtet wird.
5. **Nachweis.** Nach dem Einspielen wird die Version im Asset-Inventar aktualisiert und der Scan wiederholt. Erst der wiederholte Scan schließt den Change.

## Notfallweg

Der Notfallweg gilt für die Einstufung Notfall. Er verkürzt die Bewertung auf zwei Stunden und ersetzt die Freigabe im Change-Board durch die Freigabe des Incident Lead. Vorproduktion und Produktion dürfen am selben Tag gepatcht werden.

Der Notfallweg braucht dieselbe Dokumentation wie der Regelweg — sie wird nur nachgereicht, spätestens am folgenden Arbeitstag.

## Wartungsfenster

| Umgebung | Fenster | Vorlauf |
|---|---|---|
| Vorproduktion | dienstags 18:00 – 22:00 | 1 Arbeitstag |
| Produktion Hamburg | donnerstags 22:00 – 02:00 | 5 Arbeitstage |
| Produktion Rotterdam | sonntags 02:00 – 06:00 | 5 Arbeitstage |
| Arbeitsplätze | fortlaufend, Neustart erzwungen nach 7 Tagen | keiner |

Außerhalb der Fenster wird nur im Notfallweg gepatcht.

## Ausnahmen

Ein System, das nicht fristgerecht gepatcht werden kann, braucht einen Eintrag im Restrisiko-Register mit Begründung, kompensierender Maßnahme, Verantwortlichem und Enddatum. Ausnahmen ohne Enddatum werden nicht erteilt. Das Register wird monatlich mit dem CISO durchgesehen.

## Nachweis und Berichterstattung

Der Monatsbericht an die Geschäftsführung enthält: Zahl der offenen Schwachstellen je Einstufung, Zahl der überschrittenen Fristen, älteste offene kritische Schwachstelle und die Liste der aktiven Ausnahmen.
