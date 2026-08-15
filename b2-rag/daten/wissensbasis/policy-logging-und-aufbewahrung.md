# Richtlinie Logging und Aufbewahrung

**Gültig ab:** 2025-09-01 · **Verantwortlich:** CISO, abgestimmt mit dem Betriebsrat · **Version:** 3.4

## Zweck

Diese Richtlinie legt fest, welche Ereignisse protokolliert werden, wie lange die Protokolle aufbewahrt werden und wer sie einsehen darf. Sie schafft die Grundlage für Erkennung, Nachvollziehbarkeit und Beweissicherung.

## Was protokolliert wird

Verpflichtend für jedes System im Asset-Inventar:

* Anmeldungen, erfolgreich und fehlgeschlagen, mit Konto, Quelle und Zeitstempel
* Änderungen an Berechtigungen und Gruppenmitgliedschaften
* Start, Stopp und Konfigurationsänderungen sicherheitsrelevanter Dienste
* administrative Kommandos auf Servern
* Zugriffe auf personenbezogene Daten in den dafür gekennzeichneten Anwendungen

Nicht protokolliert werden Inhalte privater Kommunikation, Tastatureingaben und der Inhalt aufgerufener Webseiten jenseits des Domänennamens.

## Aufbewahrungsfristen

| Datenart | Aufbewahrung im schnellen Zugriff | Archiv | Summe |
|---|---|---|---|
| Firewall-Logs | 90 Tage | 275 Tage | 365 Tage |
| VPN- und Fernzugriffs-Logs | 90 Tage | 275 Tage | 365 Tage |
| Anmeldungen Verzeichnisdienst | 180 Tage | 545 Tage | 730 Tage |
| Systemprotokolle Server | 30 Tage | 335 Tage | 365 Tage |
| Anwendungsprotokolle | 30 Tage | 155 Tage | 185 Tage |
| Proxy- und DNS-Logs | 30 Tage | 60 Tage | 90 Tage |
| Beweissicherungen aus Vorfällen | dauerhaft bis Abschluss | 10 Jahre | — |

Der schnelle Zugriff bedeutet: durchsuchbar in SentinelGrid, Antwortzeit unter zehn Sekunden. Das Archiv liegt auf Objektspeicher, ist unveränderlich abgelegt und wird auf Anforderung innerhalb von vier Stunden bereitgestellt.

## Zeitsynchronisation

Alle Systeme synchronisieren ihre Uhr gegen `ntp1.nordlicht.internal` und `ntp2.nordlicht.internal`. Eine Abweichung von mehr als zwei Sekunden erzeugt eine Meldung. Ohne gemeinsame Zeitbasis ist eine Auswertung über mehrere Systeme hinweg wertlos.

## Zugriff auf Protokolle

Lesenden Zugriff auf Rohdaten hat ausschließlich das SOC. Auswertungen mit Personenbezug sind nur zur Aufklärung eines konkreten Vorfalls zulässig und werden im Vier-Augen-Prinzip durchgeführt: eine Person aus dem SOC, eine Person aus dem Datenschutz. Jede solche Auswertung wird selbst protokolliert.

Führungskräfte erhalten keine personenbezogenen Auswertungen. Eine Verhaltens- oder Leistungskontrolle findet nicht statt; das ist mit dem Betriebsrat in der Betriebsvereinbarung BV-2025-07 festgehalten.

## Schutz der Protokolle

Protokolle werden innerhalb von 60 Sekunden nach ihrer Entstehung an SentinelGrid weitergeleitet. Lokale Kopien dürfen gelöscht werden, sobald die Weiterleitung bestätigt ist. Im Archiv sind die Daten schreibgeschützt abgelegt; auch das SOC kann sie nicht ändern oder vorzeitig löschen.

## Prüfung

Der Nachweis vollständiger Protokollierung ist Teil der jährlichen Prüfung. Systeme, die keine Ereignisse liefern, erscheinen im Bericht `Stille Quellen` und werden innerhalb von 30 Tagen angebunden oder außer Betrieb genommen.
