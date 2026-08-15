# Post-Mortem INC-2026-0311 — Kompromittierung des VPN-Gateways

**Vorfall:** INC-2026-0311 · **Schweregrad:** SEV-1 · **Zeitraum:** 2026-03-11 bis 2026-03-14 · **Autor:** Incident Lead der Spätschicht · **Freigegeben:** 2026-03-24

## Zusammenfassung

Ein Angreifer hat über CVE-2026-3224 eine Administrator-Session auf dem VPN-Gateway `vpn-gw-ham-01` erlangt, ein zusätzliches lokales Konto angelegt und über drei Tage hinweg Verbindungen in das interne Netz aufgebaut. Der Zugriff wurde am 14.03.2026 um 02:41 Uhr erkannt und innerhalb von 38 Minuten unterbunden. Kundendaten sind nach heutigem Stand nicht abgeflossen. Der Ausfall des Fernzugriffs betrug vier Stunden.

## Zeitleiste

| Zeitpunkt | Ereignis |
|---|---|
| 11.03. 09:00 | NorthPeak veröffentlicht Advisory NP-SA-2026-014 zu CVE-2026-3224 |
| 11.03. 11:20 | Advisory-Feed legt Ticket VUL-2026-0442 an, Einstufung zunächst Kritisch |
| 11.03. 23:14 | erster erfolgreicher Zugriff auf `/api/v2/session/resume` von 198.51.100.77 |
| 12.03. 00:02 | Angreifer legt das lokale Konto `svc-backup2` an |
| 12.03. 08:30 | Bewertung im SOC, Einstufung auf Notfall, Change CHG-2026-0771 erstellt |
| 13.03. 22:00 | Wartungsfenster verstreicht, Patch wird auf das nächste Fenster verschoben |
| 14.03. 02:41 | SentinelGrid meldet Anmeldung von `svc-backup2` außerhalb der Geschäftszeit |
| 14.03. 02:55 | Incident Lead stuft auf SEV-1, Krisenstab wird einberufen |
| 14.03. 03:19 | Endpunkt im Reverse Proxy blockiert, alle Sessions verworfen |
| 14.03. 04:10 | Forensische Sicherung abgeschlossen, Patch 8.1.2 eingespielt |
| 14.03. 07:05 | Fernzugriff wieder verfügbar |
| 18.03. | Abschluss der Nacharbeiten, Rezertifizierung aller VPN-Konten |

## Grundursache

Die Grundursache ist ein nicht fristgerecht eingespielter Notfall-Patch. Die Schwachstelle war seit dem 11.03. bekannt, das Advisory lag vor, das Asset war im Inventar korrekt erfasst und die Einstufung Notfall war am 12.03. um 08:30 Uhr gesetzt. Der Patch wurde trotzdem in das reguläre Wartungsfenster gelegt, das am 13.03. um 22:00 Uhr ohne Umsetzung verstrich, weil der zuständige Administrator im Urlaub war und die Vertretung den Change nicht kannte.

Der Notfallweg im Runbook Patch-Management hätte den Patch innerhalb von 72 Stunden verlangt und das Wartungsfenster übergangen. Er wurde nicht ausgelöst, weil der Change bereits im Regelweg lief und niemand ihn umgehängt hat.

## Beitragende Faktoren

* Die Vertretungsregelung für Changes war nicht dokumentiert. Ein Change ohne aktiven Bearbeiter erzeugte keine Meldung.
* Die Erkennungsregel `SG-VPN-0042` für Anfragen an den betroffenen Endpunkt wurde erst am 13.03. um 16:00 Uhr aktiviert, 29 Stunden nach dem ersten Zugriff.
* Das Anlegen eines lokalen Kontos auf der Appliance erzeugte keine Meldung. Die Appliance protokollierte das Ereignis, die Regel dafür fehlte.
* Die Zeitleiste ließ sich nur deshalb lückenlos rekonstruieren, weil die VPN-Logs 365 Tage aufbewahrt werden.

## Was gut lief

Die Erkennung am 14.03. war eine Regel, kein Zufall. Vom ersten Alarm bis zur Eindämmung vergingen 38 Minuten, die Vorgabe für SEV-1 liegt bei 60 Minuten. Die forensische Sicherung erfolgte vor dem Patch, damit blieben alle Spuren erhalten. Der Krisenstab war um 03:15 Uhr vollständig erreichbar.

## Maßnahmen

| Nr. | Maßnahme | Verantwortlich | Frist | Status |
|---|---|---|---|---|
| 1 | Changes mit Einstufung Notfall erzeugen bei Fristüberschreitung eine Meldung an die SOC-Leitung | IT-Betrieb | 2026-04-15 | umgesetzt |
| 2 | Vertretungsregelung für Changes dokumentieren und im Werkzeug hinterlegen | IT-Betrieb | 2026-04-30 | umgesetzt |
| 3 | Erkennungsregeln für neue kritische CVEs innerhalb von 24 Stunden nach Advisory aktivieren | SOC | 2026-05-31 | in Arbeit |
| 4 | Kontenanlage auf allen Netzkomponenten als Ereignis anbinden | SOC | 2026-06-30 | in Arbeit |
| 5 | Lokale Administratorkonten auf allen Appliances inventarisieren | IT-Betrieb | 2026-05-15 | umgesetzt |

## Bewertung des Datenabflusses

Der Angreifer hatte über den VPN-Zugang Netzzugriff auf die Segmente `dmz-ham` und `office-ham`. Die Auswertung der Firewall-Logs zeigt 41 Verbindungen zum Dateiserver `fs-ham-02` mit insgesamt 3,2 Megabyte übertragener Daten. Die abgerufenen Dateien liegen im Ordner `IT/Netzplaene` und enthalten keine personenbezogenen Daten. Eine Meldung an die Aufsichtsbehörde war damit nicht erforderlich; die Prüfung dieser Frage ist im Ticket dokumentiert.

## Lehre

Eine Frist ist erst dann eine Frist, wenn ihre Überschreitung jemanden erreicht. Der Notfallweg existierte, war beschrieben und war allen bekannt — er wurde nur nicht ausgelöst, weil kein Mechanismus den Regelweg unterbrochen hat.
