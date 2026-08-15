# Runbook Zugriffstoken technischer Konten erneuern

**Gültig ab:** 2026-01-10 · **Verantwortlich:** Identity & Access Management · **Version:** 1.4

## Zweck

Dieses Runbook beschreibt, wie das Zugriffstoken eines technischen Kontos im Secret-Store Vaultbird Machine erneuert wird, ohne dass die anbindende Anwendung ausfällt. Beispiel ist das Konto `svc-assethub`, das SentinelGrid für die stündliche Abfrage des Asset-Inventars nutzt.

## Voraussetzungen

* Rolle `secrets.operator` im Secret-Store
* Change in Helios ITSM, außer im Notfallweg
* Kenntnis der Anwendungen, die das Token verwenden — sichtbar unter `vaultbird secret consumers <pfad>`

## Ablauf

1. **Zweites Token ausstellen.** Ein technisches Konto kann zwei gültige Token gleichzeitig haben. Das neue Token wird ausgestellt, ohne das alte zu widerrufen:

   ```
   vaultbird token issue --account svc-assethub --ttl 365d --label rotation-2026-06
   ```

2. **Neues Token verteilen.** Der Wert wird unter demselben Pfad als neue Version abgelegt: `vaultbird secret put kv/sentinelgrid/assethub token=@neu.txt`. Anwendungen, die den Pfad lesen, bekommen ab der nächsten Aktualisierung die neue Version.

3. **Anwendung nachladen lassen.** SentinelGrid liest Secrets alle 15 Minuten neu. Ein sofortiges Nachladen erzwingt `sg-cli secrets reload`. Andere Anwendungen brauchen einen Neustart; das steht im jeweiligen Betriebsteil.

4. **Wirksamkeit prüfen.** Im Zugriffsprotokoll des Secret-Stores muss die neue Token-Kennung erscheinen: `vaultbird token usage --account svc-assethub --since 1h`. Solange dort noch die alte Kennung auftaucht, ist mindestens eine Anwendung nicht umgestellt.

5. **Altes Token widerrufen.** Erst wenn die alte Kennung eine Stunde lang nicht mehr benutzt wurde:

   ```
   vaultbird token revoke --account svc-assethub --id <alte-kennung>
   ```

6. **Nachweis.** Change schließen, Datum der Erneuerung im Konteneintrag hinterlegen. Der nächste Termin wird automatisch elf Monate später eingeplant.

## Fristen

| Anlass | Frist |
|---|---|
| Regelerneuerung | jährlich, spätestens 365 Tage nach Ausstellung |
| Verdacht auf Kompromittierung | sofort, ohne Change |
| Austritt des Verantwortlichen | 5 Arbeitstage |
| Nach einem Vorfall auf dem System | vor dem Wiederanlauf |

## Notfallweg

Bei Verdacht auf Kompromittierung wird das alte Token zuerst widerrufen und danach ein neues ausgestellt. Der Ausfall der Anwendung wird in Kauf genommen. Der Incident Lead entscheidet, das Vorgehen wird im Vorfallsticket dokumentiert.

## Häufige Fehler

* Das alte Token wird widerrufen, bevor alle Anwendungen umgestellt sind. Die Prüfung in Schritt 4 verhindert das.
* Das Token wird zusätzlich in einer Konfigurationsdatei abgelegt. Dann liest die Anwendung weiter den alten Wert; die Datei wird beim nächsten Ausrollen überschrieben und der Ausfall tritt verzögert auf.
* Die Laufzeit wird auf `never` gesetzt. Token ohne Ablauf sind nicht zulässig.
