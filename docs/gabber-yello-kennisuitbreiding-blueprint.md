# Gabber Yello Kennisuitbreiding Blueprint

Versie 1.4 — 29 oktober 2026

## Doel en uitgangspunt
Breid de bestaande goedgekeurde hardcorekennis uit. Maak geen nieuwe basisronde die het eerdere werk herhaalt. Lever volledige themadocumenten aan, met relevante aanvullingen bij het bestaande onderwerp of in een duidelijk aanvullingshoofdstuk. Dennis, Fer en hun medecontroleur lezen de documenten; hun feedback wordt per ronde verwerkt.

## Reviewprotocol
- Bestaande kennis blijft zwart.
- Nieuwe inhoud en nieuwe correcties staan in rode letters, ook als een correctie van de assistent zelf komt.
- Goedgekeurde aanvullingen krijgen zwarte letters met gele markering. Geel betekent inhoudelijk goedgekeurd, niet gedeployed.
- Gebruikerscommentaar en afkeur staan blauw. Behoud die feedback traceerbaar en op de relevante plek.
- Geen bezwaar bij een volledig nagekeken aanvulling mag als akkoord worden verwerkt; ontbrekend commentaar zonder reviewbevestiging niet automatisch.
- Verwerk een afgekeurde claim niet ongemerkt in het kennisbankmateriaal. Leg de reactie blauw vast en leg eventueel een vervangende formulering rood opnieuw voor.
- Bewaar de ontvangen reviewversie en de versiegeschiedenis. In de uiteindelijke kennisbank komt alleen de goedgekeurde inhoud, niet de reviewvragen en commentaren.

## Zeven thema’s
1. Hardcore basis
2. Artiesten dj’s en liveacts
3. Feesten clubs en de geschiedenis van de scene
4. Kleding dansstijl en typische gebruiken
5. Platen labels en bekende tracks
6. Hardcoretermen en gewone Nederlandse betekenissen
7. MHJH smaak eigen mening en persona

## Kennis en bronnen
- Maak onderscheid tussen bevestigd feit, scenegebruik, betwiste geschiedenis, persoonlijke herinnering en mening.
- Verzamel gericht via artiesten, labels, organisatoren, archieven en interviews. Gebruik crawlen alleen als invoer voor controle, nooit als automatische waarheid in de kennisbank.
- Vermeld bron en controledatum bij nieuwe feitelijke kennis. Buitenlandse namen die reviewers niet kennen worden door de assistent geverifieerd.
- Jullie MHJH-ervaringen mogen als toegeschreven interne kennis worden opgenomen; smaak wordt geen objectief feit.
- Privé- en inside-informatie is niet automatisch publiceerbaar. Met name privébezit en archiefopslag van Mirko blijven buiten de publieke kennis zonder toestemming.
- Historische kennis blijft gescheiden van actuele boekingen, releases, line-ups en data. Recente of nieuwste claims vereisen een actuele bron en peildatum; bij ontbreken eerlijk onzeker zijn.
- Nieuwe feiten uit een bezoekerschatsessie worden niet automatisch algemene kennis voor andere gebruikers. Persoonlijk geheugen en goedgekeurde gedeelde kennis blijven gescheiden.
- Haal per vraag alleen relevante kennis op. Een grotere kennisbank betekent niet dat elk gesprek het hele archief meestuurt. Blijf tokengebruik per functie volgen.

## Werkvolgorde
Volledige aanvulling schrijven → broncontrole → Word met rood → menselijke review in blauw → verwerking met geel en eventuele nieuwe rode voorstellen → inhoudelijk akkoord → gecontroleerde selectie voor kennisbank → staging → gerichte tests → expliciete gouden knop voor live.
Tijdens menselijke review kan het volgende document worden voorbereid binnen een actieve werksessie. Er draait niet vanzelf een achtergrondtaak na het afsluiten van een gesprek.

## Bevestigde stand op 29 oktober 2026
- Ronde 1: ontvangen Word met vier blauwe antwoorden. Geen bezwaren bij de aanvulling. Kernpunt over geleidelijke en doorlopende ontwikkeling verwerkt als scenevisie waar het de toekomst betreft. Goedgekeurde aanvullingen geel.
- Ronde 2: ontvangen Word met vier blauwe antwoorden. Dr. Peacock al aanwezig in de basis; verdieping toegevoegd. Ruffians dj-rol en bij MHJH gedraaide set toegevoegd op aanwijzing van Dennis en Fer, met bronattributie.
- Ronde 2: fout in eerdere assistenttekst over herkomst van The Satan gevonden bij eigen broncontrole. Frankrijk vervangen door Rusland. Dennis heeft daarna beide rondes expliciet volledig goedgekeurd, inclusief de twee nog rode passages.
- De aangeleverde blauwe opmerkingen zijn behouden; geen woordelijke feedback gewist.
- De Word-reviewbestanden blijven als reviewhistorie bestaan; hun laatste rode passages zijn door de latere expliciete chatgoedkeuring inhoudelijk afgerond.
- Alleen de goedgekeurde aanvullingen zijn in de bestaande Markdown-kennisbestanden verwerkt. Geen nieuwe blauwe reviewantwoorden of redactionele commentaren naar de runtime gekopieerd.
- Verwijzingen naar de programmering van Den Haag Hakkûh II in ronde 2 zijn gedateerd als historische programmering van 17 oktober 2026; daarmee is geen daadwerkelijk gespeelde set bewezen.
- Ronde 1 en 2 zijn samen met negen offline retrievalcontroles en deze blueprint naar MHJHevents/askyellow-staging op branch main doorgezet. De bestaande kennisselectie, limiet van drie passages en contextbudget zijn ongewijzigd.
- De negen lokale retrievalcontroles slagen. Dit controleert kennisselectie, niet het daadwerkelijke modelantwoord of de Render-deploy.
- Dennis heeft de stagingchat getest met de vraag over The Satan. Het gedeelde antwoord benoemt Rusland, hardcore, drum-and-bass en breakcore correct. Op basis daarvan gaf Dennis op 29 oktober 2026 expliciet de gouden knop voor beide rondes.
- Productierepository askyellow-ai/main is bijgewerkt met uitsluitend beide goedgekeurde kennisbestanden en de bijbehorende offline test. Commit: bea850a5fedb031626fe8942481ea380ce5593b4. Voorgaande livecommit voor een eventuele gerichte rollback: 123fedd7c2265bb815889117d7c2075c620e4dcb.
- De negen retrievalcontroles slagen ook met de bestaande live-kennisloader en de overige live-kennisbestanden. Nieuwe kennisbestanden zijn inhoudelijk identiek aan de geaccepteerde stagingversie. Geen databases, secrets of overige livecode gewijzigd.
- GitHub meldt geen deploystatussen voor deze commit. De productiefunctionaliteit is wel onafhankelijk gecontroleerd: /health geeft HTTP 200, env live en db_ok true. Een nieuwe geïsoleerde gastchat op de live-API geeft The Satan als artiest uit Rusland met hardcore, drum-and-bass en breakcore; knowledge_used=true, web_used=false, memory_used=false. Daarmee is deze nieuwe kennis ook in de draaiende productiechat bevestigd, zonder een volledig modelregressietestpakket te claimen.

## Ronde 3 goedgekeurd en geselecteerd voor staging op 29 oktober 2026
- Dennis heeft de volledige verwerkte review expliciet goedgekeurd, inclusief de rode actualisaties van Mysteryland en Dominator, en opdracht gegeven deze naar staging te zetten. Geen gouden knop voor live ontvangen.
- Goedgekeurde verdieping over Mysteryland-locaties en de tijdlaag 2025/2026/2027, Dominator in Vlietland en als weekendfestival, Decibel-locaties, Ghosttown en Dance 2 Eden, Hellbound versus Hellraiser, Raving Nightmare versus A Nightmare in Rotterdam, Global Hardcore Nation, Operatie Staartjes en het gebruik van flyers en registraties geïntegreerd in ronde 3.
- Voor Mirko Kuit geldt de door Dennis bevestigde correctie: aanwezig bij editie II, maar geen publieke foto's gemaakt. De oude belofte dat hij bij editie II weer fotografeert is ook op de drie relevante plekken in de bestaande persona-kennis van ronde 7 gelijkgetrokken. Dit is geen volledige uitbreiding of herkeuring van ronde 7.
- Reviewvragen, blauwe commentaren en de formulering ter controle zijn niet als kennis naar de runtime gekopieerd. Bronverwijzingen en peildatum zijn behouden. De ontvangen Word blijft de reviewhistorie; de expliciete chatgoedkeuring rondt de laatste rode passages af.
- Alleen ronde 3, de beperkte consistentiecorrectie in ronde 7, de offline retrievaltest en deze statusbeschrijving worden op askyellow-staging/main gewijzigd. De kennisloader, drie-passagelimiet en het contextbudget blijven ongewijzigd.
- De bestaande negen retrievalchecks plus eenentwintig ronde-3-vragen en drie controles op conflicterende Mirko-formuleringen slagen met een verse snapshot van de stagingkennis: 33 checks, verdeeld over drie testmethoden. Dit is geen volledige modelregressietest of bewijs van de Render-deploy.
- Staging /health is vooraf bereikbaar met HTTP 200, env staging en db_ok true. Functionele controle van de nieuwe modelantwoorden volgt na de deploy.
- Productierepository askyellow-ai blijft in deze stap ongemoeid; ronde 3 wacht op stagingacceptatie en een afzonderlijke gouden knop.

## Volgende stappen
1. Ronde 1 en 2 afgerond: inhoud goedgekeurd, staging geaccepteerd, gouden knop ontvangen, livepromotie uitgevoerd en productieantwoord gecontroleerd.
2. Ronde 3 op staging testen; daarna pas met expliciete gouden knop naar live. Rondes 4 tot en met 7 verder uitbreiden op basis van hun bestaande goedgekeurde teksten.
3. De tijdlaag in de overige rondes en operationele kennis nalopen voordat die worden gepubliceerd; deze publicaties corrigeren verwijzingen binnen ronde 2 en 3 en de expliciet bevestigde Mirko-zinnen in ronde 7.
4. Stagingwijzigingen uit de testsessie van september zijn hier niet opnieuw geïnspecteerd. Hun deploystatus en werking moeten vóór nieuwe implementatie worden vastgesteld; eerdere vermoedens over Render zijn geen bevestigde status.
5. Gerichte kennis- en gedragstests na integratie, gevolgd door expliciete livegoedkeuring.
