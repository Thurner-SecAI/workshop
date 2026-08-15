# Runbook Zugriffskontrolle

**Gültig ab:** 2025-07-01 · **Verantwortlich:** Identity & Access Management · **Version:** 2.6

## Zweck

Dieses Runbook beschreibt, wie Zugänge bei Eintritt, Wechsel und Austritt einer Person angelegt, geändert und entzogen werden, und wie Berechtigungen regelmäßig überprüft werden.

## Grundsätze

* Jeder Zugang gehört zu genau einer Person. Gemeinsam genutzte Konten sind nicht zulässig.
* Rechte werden über Rollen vergeben, nicht einzeln. Eine Rolle bündelt die Rechte einer Tätigkeit.
* Es gilt das Prinzip der geringsten Rechte. Erweiterte Rechte sind befristet.
* Technische Konten haben einen benannten menschlichen Verantwortlichen.

## Eintritt

Die Personalabteilung legt die Person im HR-System an. Der nächtliche Abgleich erzeugt daraus das Konto im Verzeichnisdienst und die Basisrolle des Standorts. Fachliche Rollen beantragt die Führungskraft über Helios ITSM mit dem Formular `Zugang beantragen`. Der Antrag braucht die Freigabe des Rollenverantwortlichen.

Der Zugang wird frühestens am Tag vor dem Eintritt aktiv. Zugangsdaten werden über zwei Wege übergeben: der Benutzername per E-Mail an die Führungskraft, das Einmalpasswort per SMS an die Person.

## Wechsel

Bei einem Wechsel der Tätigkeit werden alle bisherigen fachlichen Rollen entzogen und die neuen beantragt. Das Ansammeln von Rechten über mehrere Stationen hinweg ist der häufigste Befund der internen Revision. Der Entzug geschieht automatisch mit dem Wirksamwerden der neuen Stelle im HR-System; er wird nicht beantragt.

## Austritt

| Schritt | Zeitpunkt | Verantwortlich |
|---|---|---|
| Konto im Verzeichnisdienst deaktivieren | letzter Arbeitstag, 18:00 | automatisch aus HR |
| Alle Sessions und Token verwerfen | letzter Arbeitstag, 18:05 | automatisch |
| VPN-Zertifikat sperren | letzter Arbeitstag, 18:05 | automatisch |
| Hardware-Token einziehen | letzter Arbeitstag | Führungskraft |
| Postfach auf Vertretung umleiten | letzter Arbeitstag | IT-Betrieb |
| Konto löschen | nach 90 Tagen | automatisch |

Bei einer fristlosen Trennung meldet die Personalabteilung den Fall telefonisch an den Service Desk. Die Deaktivierung erfolgt dann sofort und nicht zum Feierabend. Das SOC prüft im Anschluss die Zugriffe der letzten 30 Tage.

## Erweiterte Rechte

Administrative Rechte werden über getrennte Konten mit dem Präfix `adm-` vergeben. Diese Konten sind nicht für E-Mail, Internet oder Büroanwendungen zugelassen und werden nur von einem privilegierten Arbeitsplatz aus benutzt. Anmeldungen mit `adm-`-Konten von einem regulären Arbeitsplatz erzeugen eine Meldung in SentinelGrid.

Rechte für einen einzelnen Einsatz werden befristet über die Notfallfreigabe vergeben. Die Freigabe läuft nach acht Stunden automatisch ab und wird protokolliert.

## Rezertifizierung

Jede Führungskraft bestätigt vierteljährlich die Rollen ihrer Mitarbeitenden. Rollenverantwortliche bestätigen halbjährlich die Rechte, die in ihrer Rolle stecken. Wird eine Rezertifizierung nach zwei Erinnerungen nicht abgeschlossen, werden die betroffenen Rollen entzogen.

Technische Konten werden jährlich überprüft. Ein technisches Konto ohne Anmeldung in den letzten 180 Tagen wird deaktiviert.
