# Gabber Yello Kennisuitbreiding Blueprint

Versie 1.6 — 30 oktober 2026

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

## Reparatie vervolgvragen en bronselectie op staging
- Aanleiding: bij de vervolgvraag 'jo dus het is er nog steeds?' ging de oude code zonder Mysteryland zoeken en voegde ongerelateerde zoekresultaten automatisch als bronnen toe. Op 'dus dit jaar ook?' werd vervolgens onterecht een editie in 2026 bevestigd. Dennis gaf expliciet toestemming deze reparatie op staging uit te voeren; geen livegoedkeuring.
- Een begrensde onderwerpresolver gebruikt recente gesprekscontext en namen uit de goedgekeurde kennis. Historie bepaalt alleen waarnaar de vraag verwijst, nooit of een bewering waar is. Bij een onduidelijke of dubbele verwijzing volgt één gerichte vraag.
- De kennis wordt opnieuw geselecteerd met het opgeloste onderwerp; relatieve jaartallen volgen Europe/Amsterdam. Een onderwerpwissel mag geen oud jaar meenemen. De eerdere zwakke tekstmatch blokkeert deze herselectie niet meer.
- Algemene webresultaten krijgen een relevantiecontrole op titel en snippet, onderwerp, gevraagd jaar en waar relevant campinginformatie. Dit is een controle op zoekmetadata, geen volledige pagina- of entailmentverificatie. Een onderwerp alleen in een URL is onvoldoende. Ook een op datum passend resultaat over een ander genoemd festival wordt geweigerd.
- Alleen vooraf gefilterde bronnen waarnaar het model daadwerkelijk inline verwijst komen in de uiteindelijke bronnenlijst, met hernummering. Ontbrekende of ongeldige bronverwijzingen bij een webantwoord geven een eerlijke terugvaltekst; er wordt geen decoratieve bronnenlijst aangeplakt. Als een geselecteerde kennispassage het genoemde onderwerp en gevraagde jaar expliciet als overgeslagen benoemt, mag de terugval die gecontroleerde zin letterlijk gebruiken zonder webbronclaim. Deze terugval leidt geen positieve editie af en gebruikt geen chatbewering als bron.
- Bij een mislukte of lege webcheck mogen concrete gedateerde feiten uit de gecontroleerde kennis nog worden benoemd, maar niet als zojuist online bevestigd.
- Bestaande lokale agenda-zoekvragen en plaatscorrecties blijven ondersteund. Een genoemd festival blijft in een weekendzoekopdracht behouden; vandaag en morgen krijgen een concrete datum voor de bestaande datumfilter.
- Onderwerpselectie en bronfiltering zijn lokaal en vereisen geen extra modelaanroep. De bestaande kennisloader, maximaal drie kennispassages, het kennisbudget en de tokenlogging blijven behouden. Alleen bij een tijdgebonden vraag of vervolgvraag komt een korte extra onderwerpinstructie mee; algemene webcontext blijft op maximaal vier resultaten begrensd.
- 60 offline testmethoden slagen, inclusief de bestaande 33 kennischecks, de volledige gemelde gespreksketen met een vooraf fout assistentantwoord, onderwerpwissels, onbekende namen, dubbelzinnigheid, bronafwijzing, bronnummering, provideruitval, agenda-regressies, de expliciet gedateerde kennisterugval en overdracht van het onderwerp aan de modelprompt. Geen echte model- of provideraanroepen in deze offline tests.
- De eerste echte stagingproef vond nog onnodige dubbelzinnigheid: de intro Mysteryland in de jaren negentig maakte van de periode een tweede onderwerp. Periodes, kale jaartallen, getallen en stijlnamen zijn daarom als concurrerende namen uitgesloten. Twee extra regressietests dekken dit geval. De artiestenvervolgvraag over The Satan bleef in die praktijktest correct bij Rusland. De herhaalde volledige festivalproef volgt na deze naverbetering.
- De tweede praktijkproef hield het onderwerp vast en toonde geen ongerelateerde bronnen, maar de strenge citatiecontrole gaf een algemene terugvalzin ondanks de expliciete pauze in de kennis. De hierboven beschreven beperkte kennisterugval is daarom toegevoegd; de strenge broncontrole wordt niet losgelaten. De herhaalde praktijkproef moet ook bevestigen dat het antwoord over 2026 weer inhoudelijk bruikbaar is.
- Deze reparatie wordt uitsluitend op askyellow-staging/main gepubliceerd. Praktijktest na de Render-deploy volgt afzonderlijk; offline tests zijn geen garantie dat ieder modelantwoord correct is. Live blijft op bea850a5fedb031626fe8942481ea380ce5593b4 totdat Dennis afzonderlijk de gouden knop geeft.


## Gouden knop en kennisrelease ronde 3 op 30 oktober 2026
- Dennis heeft de stagingchat zelf gecontroleerd, is tevreden en heeft expliciet toestemming gegeven deel 3 naar main door te zetten.
- Productierepository askyellow-ai/main is bijgewerkt met de geaccepteerde ronde-3-kennis, de drie Mirko-consistentiecorrecties in ronde 7 en de bestaande offline retrievaltest. Releasecommit: 6a9a7ff9bb3b5c69d54d89f6e20f2d2797548e07. Vorige productiecommit: bea850a5fedb031626fe8942481ea380ce5593b4.
- De drie productieblobs zijn identiek aan stagingcommit 9181e234ebaed7db7ffd4fb24c8142490896425f. De vergelijking met de vorige productiecommit toont uitsluitend deze drie bestanden; main is na de overdracht opnieuw gecontroleerd.
- De kennisloader is op beide omgevingen identiek. De bestaande stagingtests zijn bij deze kennisoverdracht niet opnieuw uitgevoerd; dit verslag claimt geen nieuwe testuitslag.
- De latere wijzigingen aan chat.py, gabber_context.py, gabber_web.py en llm.py zijn niet onderdeel van deze beperkte kennisrelease en blijven op staging.
- De Render-deploy en een nieuw antwoord van de draaiende productiechat zijn vanuit deze sessie nog niet bevestigd.
- Deel 4 is als volgende kennisuitbreiding gestart vanuit de bestaande ronde-4-tekst. Nieuwe voorstellen en correcties blijven ter review; nog geen runtimepublicatie van deel 4.

## Volgende stappen
1. Ronde 1 en 2 afgerond: inhoud goedgekeurd, staging geaccepteerd, gouden knop ontvangen, livepromotie uitgevoerd en productieantwoord gecontroleerd.
2. Ronde 3 staat na de gouden knop op askyellow-ai/main; de draaiende productie nog onafhankelijk controleren. Ronde 4 uitbreiden op basis van de bestaande tekst en voorleggen ter review.
3. De tijdlaag in de overige rondes en operationele kennis nalopen voordat die worden gepubliceerd; deze publicaties corrigeren verwijzingen binnen ronde 2 en 3 en de expliciet bevestigde Mirko-zinnen in ronde 7.
4. Stagingwijzigingen uit de testsessie van september zijn hier niet opnieuw geïnspecteerd. Hun deploystatus en werking moeten vóór nieuwe implementatie worden vastgesteld; eerdere vermoedens over Render zijn geen bevestigde status.
5. Gerichte kennis- en gedragstests na integratie, gevolgd door expliciete livegoedkeuring.

