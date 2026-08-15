# Richtlinie Passwörter und Multi-Faktor-Authentisierung

**Gültig ab:** 2026-02-01 · **Verantwortlich:** CISO · **Version:** 5.0 · **Ersetzt:** Version 4.3 vom 2024-05-01

## Geltungsbereich

Diese Richtlinie gilt für alle Konten der Nordlicht Logistik SE: persönliche Konten, administrative Konten, technische Konten und Zugänge von Dienstleistern.

## Passwörter

| Kontoart | Mindestlänge | Ablauf | Sperre nach Fehlversuchen |
|---|---|---|---|
| persönliches Konto | 12 Zeichen | kein Ablauf | 10 Versuche, 15 Minuten |
| administratives Konto (`adm-`) | 16 Zeichen | kein Ablauf | 5 Versuche, 30 Minuten |
| technisches Konto | 32 Zeichen, zufällig | 365 Tage | keine Sperre, Meldung an das SOC |
| Dienstleisterzugang | 16 Zeichen | 90 Tage | 5 Versuche, 30 Minuten |

Ein regelmäßiger Passwortwechsel ohne Anlass ist mit Version 5.0 entfallen. Er führte zu vorhersehbaren Mustern und häufigeren Zurücksetzungen. Gewechselt wird bei Verdacht auf Kompromittierung, nach einem Vorfall auf dem betroffenen System und bei jedem Treffer im Abgleich mit veröffentlichten Datensammlungen.

Verboten sind: Wiederverwendung eines Passworts aus einem anderen Dienst, Weitergabe an Dritte, Ablage in unverschlüsselten Dateien. Der Passwortmanager `Vaultbird` ist für alle Mitarbeitenden bereitgestellt und für dienstliche Zugangsdaten verpflichtend.

## Multi-Faktor-Authentisierung

MFA ist für alle Konten verpflichtend, die von außerhalb des internen Netzes erreichbar sind, und für alle administrativen Konten.

**Phishing-resistente Verfahren** sind für die folgenden Konten zwingend: administrative Konten (`adm-`), Konten mit Zugriff auf das Finanzsystem, Konten der Geschäftsführung sowie alle Zugänge zum VPN-Gateway und zur Verwaltungsoberfläche von SentinelGrid. Zugelassen sind ausschließlich FIDO2-Sicherheitsschlüssel und Passkeys, die an das Gerät gebunden sind.

Für alle übrigen Konten sind zusätzlich zugelassen: Einmalpasswörter aus einer Authentisierungs-App (TOTP) und Push-Bestätigungen mit Nummernabgleich.

Nicht mehr zugelassen sind seit dem 01.02.2026: SMS, Sprachanruf und einfache Push-Bestätigung ohne Nummernabgleich.

## Ausnahmen

Wo ein System kein MFA unterstützt, ist der Zugang auf das interne Netz zu beschränken und im Restrisiko-Register zu führen. Die Ausnahme wird jährlich überprüft.

## Technische Konten

Technische Konten nutzen bevorzugt zertifikatsbasierte Anmeldung oder kurzlebige Token. Wo ein Passwort nötig ist, wird es im Secret-Store `Vaultbird Machine` erzeugt und abgelegt; niemand kennt es im Klartext. Der Verantwortliche prüft jährlich, ob das Konto noch benötigt wird.

## Durchsetzung

Der Verzeichnisdienst setzt Länge, Sperre und MFA-Pflicht technisch durch. Konten, die eine Vorgabe nicht erfüllen, erscheinen im wöchentlichen Abweichungsbericht an das SOC und werden nach 14 Tagen ohne Nachbesserung gesperrt.
