# Assistant eval, 2026-10-03

Model `gemini-2.5-flash`, temperature 0, 20 cases from `evals/heldout.yaml`. First run, before the scorer and bug fixes described in the README.

- Pass: **15/20**
- Right procedure retrieved: 15/15
- Right procedure cited: 12/15
- Facts correct: 21/23
- Unanswerable questions correctly declined: 4/5
- Citations to non-existent sources: 0
- Closed-book baseline (same model, no sources), facts correct: 5/23

| case | lang | pass | retrieved | cited | facts | secs |
|---|---|---|---|---|---|---|
| driving-licence-first | en | PASS | True | True | deadline:ok | 14.4 |
| driving-licence-stolen | ca | FAIL | True | False | price:ok deadline:ok | 7.0 |
| elderly-solidarity-pension | es | PASS | True | True | deadline:ok online:ok | 8.5 |
| large-family-first | fr | PASS | True | True | price:ok deadline:ok | 9.7 |
| unemployment-aid | ca | FAIL | True | False | deadline:ok | 7.9 |
| drone-registration | en | PASS | True | True | price:ok | 12.5 |
| public-information-request | es | PASS | True | True | price:ok deadline:ok | 8.1 |
| tax-debt-certificate | ca | PASS | True | True | in_person:ok | 11.5 |
| foreign-investment | en | PASS | True | True | price:ok deadline:ok | 15.0 |
| youth-emancipation | ca | FAIL | True | True | period:MISS | 12.6 |
| passport-nationality-certificate | fr | PASS | True | True | price:ok | 6.8 |
| habitability-certificate | es | FAIL | True | False | price:ok deadline:MISS | 13.2 |
| professional-artist | en | PASS | True | True | price:ok deadline:ok | 7.7 |
| school-study-grant | fr | PASS | True | True | period:ok | 14.7 |
| discounted-electricity | ca | PASS | True | True | price:ok online:ok | 11.6 |
| abstain-weather | ca | PASS | None | None | declined:ok euro:ok | 15.7 |
| abstain-ski-pass | fr | PASS | None | None | declined:ok euro:ok | 9.4 |
| abstain-border-queue | en | PASS | None | None | declined:ok euro:ok | 13.6 |
| abstain-minister-phone | es | FAIL | None | None | declined:MISS euro:ok | 15.4 |
| abstain-my-vacation | ca | PASS | None | None | declined:ok euro:ok | 11.4 |

## Answers

### driving-licence-first (GV000300)

The administration can take a maximum of 60 business days to issue a first driving license [1].

Sources: [1] https://www.e-tramits.ad/tramits/primera-obtencio-dun-permis-de-conduir/p/GV000300, [2] https://www.e-tramits.ad/tramits/targeta-de-tacograf-digital---primera-demanda-de-targeta-de-tacograf-digital-per-a-taller-de-tacografs-empresa-propietaria-de-vehicles-pesants-conductor-i-controlador/p/GV000319, [3] https://www.e-tramits.ad/tramits/renovacio-del-permis-de-conduir/p/GV000303, [4] https://www.e-tramits.ad/tramits/augment-de-categoria-del-permis-de-conduir/p/GV000279, [5] https://www.e-tramits.ad/tramits/augment-de-categoria-del-permis-de-conduir-del-permis-j-al-b/p/GV001717

### driving-licence-stolen (GV000280)

El cost per obtenir un duplicat del permís de conduir per robatori és de 24,66 € [1, 2]. El temps màxim de resolució per a aquest tràmit és de 48 hores [1, 2].

Sources: [1] https://www.e-tramits.ad/tramits/duplicat-per-mal-estat-o-robatori-del-permis-de-conduir/p/GV000280, [2] https://www.e-tramits.ad/tramits/duplicat-per-perdua-o-robatori-del-permis-de-conduir/p/GV000281, [3] https://www.e-tramits.ad/tramits/renovacio-del-permis-de-conduir/p/GV000303, [4] https://www.e-tramits.ad/tramits/augment-de-categoria-del-permis-de-conduir/p/GV000279, [5] https://www.e-tramits.ad/tramits/augment-de-categoria-del-permis-de-conduir-del-a2-al-a/p/GV001718

### elderly-solidarity-pension (GV000049)

Sí, su madre puede solicitar la pensión de solidaridad para la gente mayor por internet [2].

El tiempo máximo de resolución para esta solicitud es de 2 meses [2].

Sources: [1] https://www.e-tramits.ad/tramits/pensio-de-solidaritat-de-les-persones-amb-discapacitat/p/GV000031, [2] https://www.e-tramits.ad/tramits/pensio-de-solidaritat-per-a-la-gent-gran/p/GV000049, [3] https://www.e-tramits.ad/tramits/reconeixement-de-les-qualificacions-de-lleure-estrangeres/p/GV000780, [4] https://www.e-tramits.ad/tramits/reconeixement-academic-de-qualificacions-estrangeres-densenyament-superior/p/GV000136, [5] https://www.e-tramits.ad/tramits/reconeixement-de-titulacions-estrangeres-densenyament-no-superior/p/GV000084

### large-family-first (GV000048)

La première demande de reconnaissance de la condition de famille nombreuse coûte 0,00 € [1]. Le délai maximum de résolution est de 2 mois [1].

Sources: [1] https://www.e-tramits.ad/tramits/reconeixement-de-la-condicio-de-familia-nombrosa-primera-demanda/p/GV000048, [2] https://www.e-tramits.ad/tramits/reconeixement-de-la-condicio-de-familia-nombrosa-renovacio/p/GV000046, [3] https://www.e-tramits.ad/tramits/reconeixement-de-la-condicio-de-familia-nombrosa-duplicat/p/GV000047, [4] https://www.e-tramits.ad/tramits/reconeixement-de-la-condicio-de-familia-monoparental-renovacio/p/GV000975, [5] https://www.e-tramits.ad/tramits/reconeixement-de-la-condicio-de-familia-monoparental-duplicat/p/GV000045

### unemployment-aid (GV000043)

L'administració té un temps màxim de resolució de 2 mesos per als ajuts per desocupació involuntària, ja sigui per a la pròrroga, la reactivació o la sol·licitud inicial [1, 2, 3].

Sources: [1] https://www.e-tramits.ad/tramits/ajuts-per-desocupacio-involuntaria-prorroga/p/GV001578, [2] https://www.e-tramits.ad/tramits/ajuts-per-desocupacio-involuntaria-reactivacio/p/GV001579, [3] https://www.e-tramits.ad/tramits/ajuts-per-desocupacio-involuntaria-inicial/p/GV000043, [4] https://www.e-tramits.ad/tramits/prestacio-familiar-per-fill-a-carrec---inicial/p/GV000050, [5] https://www.e-tramits.ad/tramits/prestacio-familiar-per-fill-a-carrec---verificacio-anyal-de-dades/p/GV000053

### drone-registration (GV000310)

To fly a drone in Andorra, the flight authorization procedure for unmanned aircraft costs 8,58 € [3]. The identification and/or deregistration of drones also costs 8,58 € [4].

Sources: [1] https://www.e-tramits.ad/tramits/impostos/contingut-irpf, [2] https://www.e-tramits.ad/tramits/impostos/contingut-irpf, [3] https://www.e-tramits.ad/tramits/identificacio-daeronaus-no-tripulades---autoritzacio-de-vol/p/GV000309, [4] https://www.e-tramits.ad/tramits/aeronaus-no-tripulades/p/GV000310, [5] https://www.e-tramits.ad/tramits/presentacio-de-propostes-artistiques-de-nova-creacio-per-a-andorra-crea-mercat-de-les-arts-fetes-a-andorra/p/GV001762

### public-information-request (GV000751)

Solicitar acceso a un documento público no tiene coste [1]. El tiempo máximo de respuesta es de 60 días hábiles [1].

Sources: [1] https://www.e-tramits.ad/tramits/acces-a-la-informacio-publica/p/GV000751, [2] https://www.e-tramits.ad/tramits/acces-a-programes-i-a-serveis-per-a-persones-amb-discapacitat-financats-amb-fons-public-i-dautoritzacio-per-tractar-la-discapacitat-a-lestranger/p/GV000033, [3] https://www.e-tramits.ad/tramits/documentacio-pendent/p/tr-pending-doc, [4] https://www.e-tramits.ad/tramits/diposit-de-comptes---peticio-de-documents/p/GV100005, [5] https://www.e-tramits.ad/tramits/irpf---documentacio-a-adjuntar/p/tr-attach-post-irpf

### tax-debt-certificate (GV000653)

Per sol·licitar un Certificat de Deute, no és possible fer-ho per internet, ja que no està disponible en línia [1]. Cal demanar cita prèvia per realitzar el tràmit [1].

Sources: [1] https://www.e-tramits.ad/tramits/certificat-de-deute/p/GV000653, [2] https://www.e-tramits.ad/tramits/ajornament-o-fraccionament-de-deute/p/GV100001, [3] https://www.e-tramits.ad/tramits/sollicitud-dajornament-fraccionament-de-deutes-tributaris/p/GV001747, [4] https://www.e-tramits.ad/tramits/certificat-de-naixement/p/GV001574, [5] https://www.e-tramits.ad/tramits/certificat-de-societat-mercantil-andorrana/p/GV000900

### foreign-investment (GV001612)

The fee for the foreign-investment authorization for real estate in Andorra is 300€ [3]. The maximum resolution time for this authorization is 2 months, with a possible extension of 1 month [3].

Sources: [1] https://www.e-tramits.ad/tramits/impostos/firstIeiTax, [2] https://www.e-tramits.ad/tramits/impostos/secondIeiTax, [3] https://www.e-tramits.ad/tramits/inversio-estrangera/p/GV001612, [4] https://www.e-tramits.ad/tramits/acces-a-programes-i-a-serveis-per-a-persones-amb-discapacitat-financats-amb-fons-public-i-dautoritzacio-per-tractar-la-discapacitat-a-lestranger/p/GV000033, [5] https://www.e-tramits.ad/tramits/h2-autoritzacio-dimmigracio-temporal-mes-de-30-dies-per-a-treballadors-dempreses-estrangeres/p/GV000492

### youth-emancipation (GV000061)

El programa d'impuls per a l'emancipació de joves està dirigit a joves d'entre 18 i 35 anys (ambdues edats incloses) que volen emancipar-se per primera vegada [1]. Per tant, una persona de 25 anys pot sol·licitar aquest ajut [1].

El període de sol·licitud per a aquest programa és del [REDACTED_PHONE] al [REDACTED_PHONE] [1].

Si necessites més informació sobre el període de sol·licitud, pots consultar la URL oficial: https://www.e-tramits.ad/tramits/programa-dimpuls-per-a-lemancipacio-de-joves/p/GV000061 [1].

Sources: [1] https://www.e-tramits.ad/tramits/programa-dimpuls-per-a-lemancipacio-de-joves/p/GV000061, [2] https://www.e-tramits.ad/tramits/jovempren---subvencions-per-a-projectes-impulsats-per-joves/p/GV000060, [3] https://www.e-tramits.ad/tramits/subvencio-a-favor-de-la-biodiversitat-i-del-paisatge-dandorra/p/GV001606, [4] https://www.e-tramits.ad/tramits/demanda-de-subvencio-per-al-patrimoni-cultural/p/GV001588, [5] https://www.e-tramits.ad/tramits/justificacio-de-les-beques-atorgades-per-a-joves-artistes-destinades-a-la-realitzacio-de-formacions-artistiques-avancades-i-la-participacio-en-certamens-i-concursos-internacionals/p/GV001711

### passport-nationality-certificate (GV000451)

Le certificat de nationalité coûte 8,58 € [1].

Sources: [1] https://www.e-tramits.ad/tramits/passaports---certificat-de-nacionalitat/p/GV000451, [2] https://www.e-tramits.ad/tramits/demanda-dacreditacio-del-certificat-daptitud-professional/p/GV001633, [3] https://www.e-tramits.ad/tramits/certificat-de-naixement/p/GV001574, [4] https://www.e-tramits.ad/tramits/acreditacio-per-signar-conveni-amb-la-cass/p/GV000019, [5] https://www.e-tramits.ad/tramits/certificat-de-societat-mercantil-andorrana/p/GV000900

### habitability-certificate (GV000633)

Para solicitar la cédula de habitabilidad en línea, el coste es de 7,50 € [2]. El tiempo máximo de resolución es de 2 meses [2].

La cédula de habitabilidad es un documento administrativo que acredita que una vivienda cumple las condiciones mínimas de habitabilidad y es apta para ser destinada a residencia de personas [2]. Es necesaria para transmitir una vivienda en venta, alquiler o cesión de uso [2].

Sources: [1] https://www.e-tramits.ad/tramits/certificat-dhabitabilitat-en-linia/p/GV000633, [2] https://www.e-tramits.ad/tramits/cedula-dhabitabilitat-en-linia/p/GV000640, [3] https://www.e-tramits.ad/tramits/certificat-de-registre-dhabitatge-dus-turistic-hut/p/GV000957, [4] https://www.e-tramits.ad/tramits/certificat-de-final-dobra-en-activitats-ambientals/p/GV000829, [5] https://www.e-tramits.ad/tramits/certificat-de-naixement/p/GV001574

### professional-artist (GV001743)

To be accredited as a professional artist in Andorra, there is no fee [1]. The maximum resolution time for the decision is 60 working days [1].

Sources: [1] https://www.e-tramits.ad/tramits/acreditacio-com-a-artista-professional/p/GV001743, [2] https://www.e-tramits.ad/tramits/demanda-dacreditacio-del-certificat-daptitud-professional/p/GV001633, [3] https://www.e-tramits.ad/tramits/presentacio-de-propostes-artistiques-de-nova-creacio-per-a-andorra-crea-mercat-de-les-arts-fetes-a-andorra/p/GV001762, [4] https://www.e-tramits.ad/tramits/convocatoria-per-a-la-seleccio-dun-a-coordinador-a-artistic-i-gestor-a-de-projecte-per-andorra-crea-mercat-de-les-arts-fetes-a-andorra/p/GV001719, [5] https://www.e-tramits.ad/tramits/ajuda-financera-per-a-la-professionalitzacio-dels-artistes-musicals/p/GV001628

### school-study-grant (GV000125)

L'information concernant la période de demande d'aide aux études pour l'enseignement non supérieur pour cette année n'a pas été trouvée dans les sources fournies.

La source la plus pertinente est [4]. Cependant, une période de demande pour l'aide aux études pour l'enseignement non supérieur est indiquée du 10 juin 2026 au 15 juillet 2026 [4].

Sources: [1] https://www.e-tramits.ad/tramits/inscripcio-a-la-prova-dacces-als-estudis-densenyament-superior-per-a-persones-mes-grans-de-25-anys/p/GV000772, [2] https://www.e-tramits.ad/tramits/acces-als-estudis-densenyament-superior/p/GV000133, [3] https://www.e-tramits.ad/tramits/ajut-a-lestudi-ensenyament-superior/p/GV000087, [4] https://www.e-tramits.ad/tramits/ajut-a-lestudi-ensenyament-no-superior/p/GV000125, [5] https://www.e-tramits.ad/tramits/ajut-a-lestudi---acceptacio-dun-ajut-fora-del-periode-de-convocatoria-ensenyament-no-superior/p/GV000916

### discounted-electricity (GV000054)

Sí, podeu demanar la tarifa elèctrica bonificada en línia [1]. Aquest tràmit no té cap cost [1].

Per poder beneficiar-se d'aquesta bonificació, el sol·licitant o algun membre de la seva unitat de convivència ha de ser beneficiari d'una prestació econòmica i/o pensió dels Serveis Socials [1]. La persona sol·licitant o algun membre de la seva llar ha de ser beneficiari d’alguna de les prestacions i/o ajudes econòmiques vinculades al conveni [1].

Sources: [1] https://www.e-tramits.ad/tramits/aplicacio-de-la-tarifa-electrica-bonificada/p/GV000054, [2] https://www.e-tramits.ad/tramits/declaracio-dinstallacio-electrica-de-baixa-tensio-o-de-molt-baixa-tensio-i-fibra-optica-tipus-b/p/GV000196, [3] https://www.e-tramits.ad/tramits/declaracio-dinstallacio-electrica-de-baixa-tensio-o-de-molt-baixa-tensio-i-fibra-optica-tipus-c/p/GV000197, [4] https://www.e-tramits.ad/tramits/descomptes-temporals-a-la-factura-de-subministrament-electric-per-activitats-comercials-al-pas-de-la-casa/p/GV001752, [5] https://www.e-tramits.ad/tramits/installacions-de-generacio-denergia-electrica-ipee/p/GV001066

### abstain-weather (-)

La informació sobre el temps que farà demà a Andorra la Vella no es troba en les fonts proporcionades.

Sources: [1] https://www.e-tramits.ad/tramits/presentacio-de-propostes-artistiques-de-nova-creacio-per-a-andorra-crea-mercat-de-les-arts-fetes-a-andorra/p/GV001762, [2] https://www.e-tramits.ad/tramits/consulta-dun-examen-oficial-de-llengua-catalana/p/GV000152, [3] https://www.e-tramits.ad/tramits/convocatoria-per-a-la-seleccio-dun-a-coordinador-a-artistic-i-gestor-a-de-projecte-per-andorra-crea-mercat-de-les-arts-fetes-a-andorra/p/GV001719, [4] https://www.e-tramits.ad/tramits/consulta-tributaria/p/GV000656, [5] https://www.e-tramits.ad/tramits/segell-de-restaurant-de-cuina-tradicional-dandorra/p/GV000750

### abstain-ski-pass (-)

Les sources fournies ne contiennent pas d'informations sur le coût d'un forfait de ski de saison à Grandvalira pour cet hiver.

La source [1] mentionne les prix des forfaits universitaires et extrascolaires pour la saison 2025-26, mais pas pour la saison actuelle ni pour un forfait de ski de saison général.

L'information n'a pas été trouvée. Veuillez consulter l'URL la plus pertinente pour les forfaits de saison : [1]

Sources: [1] https://www.e-tramits.ad/tramits/forfet-universitari-i-extraescolar-per-no-escolaritzats-per-la-temporada-2025-26/p/GV000700, [2] https://www.e-tramits.ad/tramits/llicencia-de-caca-de-temporada/p/GV000581, [3] https://www.e-tramits.ad/tramits/sorteig-muflo-vedat-temporada-estranger/p/GV000602, [4] https://www.e-tramits.ad/tramits/sorteig-muflo-vedat-temporada-andorrans-residents/p/GV000601, [5] https://www.e-tramits.ad/tramits/inscripcio-a-la-trobada-laboral-job-meeting-oportunitats-per-a-la-temporada-destiu/p/GV001601

### abstain-border-queue (-)

The provided sources do not contain information about the current queue length at the Pas de la Casa border.

For more information, you may want to check the official e-Tramits website: https://www.e-tramits.ad/tramits/descomptes-temporals-a-la-factura-de-subministrament-electric-per-activitats-comercials-al-pas-de-la-casa/p/GV001752 [1].

Sources: [1] https://www.e-tramits.ad/tramits/descomptes-temporals-a-la-factura-de-subministrament-electric-per-activitats-comercials-al-pas-de-la-casa/p/GV001752, [2] https://www.e-tramits.ad/tramits/duplicat-per-mal-estat-o-robatori-del-permis-de-conduir/p/GV000280, [3] https://www.e-tramits.ad/tramits/peticio-informacio-al-registre-de-permisos-de-conduir/p/GV000302, [4] https://www.e-tramits.ad/tramits/acces-al-programa-vida-independent-men-vaig-de-casa/p/GV001324, [5] https://www.e-tramits.ad/tramits/impostos/is

### abstain-minister-phone (-)

La información solicitada no se encontró en las fuentes proporcionadas.

Las fuentes describen procedimientos para solicitar información pública [1], acceder a programas y servicios para personas con discapacidad [2], el ejercicio del voto [3], y prestaciones familiares [4], así como información sobre el IRPF [5]. Ninguna de ellas contiene el número de móvil personal del ministro de Finanzas. La Ley 29/2021, del 28 de octubre, calificada de protección de datos personales, se menciona en varias fuentes, lo que sugiere que los datos personales están protegidos [1, 3].

Para solicitar información pública, puede consultar el siguiente URL: https://www.e-tramits.ad/tramits/acces-a-la-informacio-publica/p/GV000751 [1].

Sources: [1] https://www.e-tramits.ad/tramits/acces-a-la-informacio-publica/p/GV000751, [2] https://www.e-tramits.ad/tramits/acces-a-programes-i-a-serveis-per-a-persones-amb-discapacitat-financats-amb-fons-public-i-dautoritzacio-per-tractar-la-discapacitat-a-lestranger/p/GV000033, [3] https://www.e-tramits.ad/tramits/exercici-del-vot---informacio-accessible/p/GV000756, [4] https://www.e-tramits.ad/tramits/prestacio-familiar-per-fill-a-carrec---verificacio-anyal-de-dades/p/GV000053, [5] https://www.e-tramits.ad/tramits/impostos/contingut-irpf

### abstain-my-vacation (-)

La informació sobre quants dies de vacances li queden enguany a la seva empresa no es troba en les fonts oficials proporcionades.

Sources: [1] https://www.e-tramits.ad/tramits/consulta-dun-examen-oficial-de-llengua-catalana/p/GV000152, [2] https://www.e-tramits.ad/tramits/h1-notificacio-de-treballs-de-curta-durada-menys-de-5-dies/p/GV000808, [3] https://www.e-tramits.ad/tramits/consulta-tributaria/p/GV000656, [4] https://www.e-tramits.ad/tramits/h1-notificacio-de-treballs-de-curta-durada-mes-de-5-dies/p/GV000503, [5] https://www.e-tramits.ad/tramits/h2-autoritzacio-dimmigracio-temporal-mes-de-30-dies-per-a-treballadors-dempreses-estrangeres/p/GV000492
