# Assistant eval, 2026-10-03

Model `gemini-2.5-flash`, temperature 0, 20 cases from `evals/heldout.yaml`.

- Pass: **20/20**
- Right procedure retrieved: 15/15
- Right procedure cited: 15/15
- Facts correct: 23/23
- Unanswerable questions correctly declined: 5/5
- Citations to non-existent sources: 0
- Closed-book baseline (same model, no sources), facts correct: 6/23

| case | lang | pass | retrieved | cited | facts | secs |
|---|---|---|---|---|---|---|
| driving-licence-first | en | PASS | True | True | deadline:ok | 14.1 |
| driving-licence-stolen | ca | PASS | True | True | price:ok deadline:ok | 9.8 |
| elderly-solidarity-pension | es | PASS | True | True | deadline:ok online:ok | 9.5 |
| large-family-first | fr | PASS | True | True | price:ok deadline:ok | 10.8 |
| unemployment-aid | ca | PASS | True | True | deadline:ok | 9.6 |
| drone-registration | en | PASS | True | True | price:ok | 13.1 |
| public-information-request | es | PASS | True | True | price:ok deadline:ok | 8.5 |
| tax-debt-certificate | ca | PASS | True | True | in_person:ok | 10.0 |
| foreign-investment | en | PASS | True | True | price:ok deadline:ok | 15.2 |
| youth-emancipation | ca | PASS | True | True | period:ok | 13.2 |
| passport-nationality-certificate | fr | PASS | True | True | price:ok | 16.7 |
| habitability-certificate | es | PASS | True | True | price:ok deadline:ok | 8.7 |
| professional-artist | en | PASS | True | True | price:ok deadline:ok | 13.8 |
| school-study-grant | fr | PASS | True | True | period:ok | 10.1 |
| discounted-electricity | ca | PASS | True | True | price:ok online:ok | 11.0 |
| abstain-weather | ca | PASS | None | None | declined:ok euro:ok | 19.0 |
| abstain-ski-pass | fr | PASS | None | None | declined:ok euro:ok | 11.2 |
| abstain-border-queue | en | PASS | None | None | declined:ok euro:ok | 14.0 |
| abstain-minister-phone | es | PASS | None | None | declined:ok euro:ok | 25.3 |
| abstain-my-vacation | ca | PASS | None | None | declined:ok euro:ok | 11.3 |

## Answers

### driving-licence-first (GV000300)

The administration can take a maximum of 60 business days to issue a first driving license [1].

Sources: [1] https://www.e-tramits.ad/tramits/primera-obtencio-dun-permis-de-conduir/p/GV000300, [2] https://www.e-tramits.ad/tramits/targeta-de-tacograf-digital---primera-demanda-de-targeta-de-tacograf-digital-per-a-taller-de-tacografs-empresa-propietaria-de-vehicles-pesants-conductor-i-controlador/p/GV000319, [3] https://www.e-tramits.ad/tramits/renovacio-del-permis-de-conduir/p/GV000303, [4] https://www.e-tramits.ad/tramits/augment-de-categoria-del-permis-de-conduir/p/GV000279, [5] https://www.e-tramits.ad/tramits/augment-de-categoria-del-permis-de-conduir-del-permis-j-al-b/p/GV001717

### driving-licence-stolen (GV000280)

El cost per obtenir un duplicat del permís de conduir per robatori és de 24,66 € [1, 2]. El temps màxim de resolució per a aquest tràmit és de 48 hores [1, 2].

Sources: [1] https://www.e-tramits.ad/tramits/duplicat-per-mal-estat-o-robatori-del-permis-de-conduir/p/GV000280, [2] https://www.e-tramits.ad/tramits/duplicat-per-perdua-o-robatori-del-permis-de-conduir/p/GV000281, [3] https://www.e-tramits.ad/tramits/expedicio-de-titols-densenyament-superior-de-caracter-estatal---duplicat-del-titol/p/GV000135, [4] https://www.e-tramits.ad/tramits/carnet-professional---capa-ozo---duplicat/p/GV000538, [5] https://www.e-tramits.ad/tramits/targeta-de-tacograf-digital---duplicat-de-targeta-de-tacograf-digital-per-a-taller-de-tacografs-empresa-propietaria-de-vehicles-pesants-conductor-i-controlador/p/GV000321

### elderly-solidarity-pension (GV000049)

Sí, su madre puede solicitar la pensión de solidaridad para la gente mayor por internet [2].

El tiempo máximo de resolución para esta solicitud es de 2 meses [2].

Sources: [1] https://www.e-tramits.ad/tramits/pensio-de-solidaritat-de-les-persones-amb-discapacitat/p/GV000031, [2] https://www.e-tramits.ad/tramits/pensio-de-solidaritat-per-a-la-gent-gran/p/GV000049, [3] https://www.e-tramits.ad/tramits/reconeixement-de-les-qualificacions-de-lleure-estrangeres/p/GV000780, [4] https://www.e-tramits.ad/tramits/reconeixement-academic-de-qualificacions-estrangeres-densenyament-superior/p/GV000136, [5] https://www.e-tramits.ad/tramits/reconeixement-de-titulacions-estrangeres-densenyament-no-superior/p/GV000084

### large-family-first (GV000048)

La première demande de reconnaissance de la condition de famille nombreuse coûte 0,00 € [1]. Le délai maximum de résolution est de 2 mois [1].

Sources: [1] https://www.e-tramits.ad/tramits/reconeixement-de-la-condicio-de-familia-nombrosa-primera-demanda/p/GV000048, [2] https://www.e-tramits.ad/tramits/reconeixement-de-la-condicio-de-familia-nombrosa-renovacio/p/GV000046, [3] https://www.e-tramits.ad/tramits/reconeixement-de-la-condicio-de-familia-nombrosa-duplicat/p/GV000047, [4] https://www.e-tramits.ad/tramits/reconeixement-de-la-condicio-de-familia-monoparental-renovacio/p/GV000975, [5] https://www.e-tramits.ad/tramits/reconeixement-de-la-condicio-de-familia-monoparental-duplicat/p/GV000045

### unemployment-aid (GV000043)

L'administració té un termini màxim de 2 mesos per resoldre l'ajut per desocupació involuntària [1, 2, 3].

Sources: [1] https://www.e-tramits.ad/tramits/ajuts-per-desocupacio-involuntaria-prorroga/p/GV001578, [2] https://www.e-tramits.ad/tramits/ajuts-per-desocupacio-involuntaria-reactivacio/p/GV001579, [3] https://www.e-tramits.ad/tramits/ajuts-per-desocupacio-involuntaria-inicial/p/GV000043, [4] https://www.e-tramits.ad/tramits/prestacio-familiar-per-fill-a-carrec---inicial/p/GV000050, [5] https://www.e-tramits.ad/tramits/prestacio-familiar-per-fill-a-carrec---verificacio-anyal-de-dades/p/GV000053

### drone-registration (GV000310)

The cost for the identification of unmanned aircraft and flight authorization in Andorra is 8.58 € [3]. The identification and/or deregistration of drones also costs 8.58 € [4].

Sources: [1] https://www.e-tramits.ad/tramits/impostos/contingut-irpf, [2] https://www.e-tramits.ad/tramits/impostos/contingut-irpf, [3] https://www.e-tramits.ad/tramits/identificacio-daeronaus-no-tripulades---autoritzacio-de-vol/p/GV000309, [4] https://www.e-tramits.ad/tramits/aeronaus-no-tripulades/p/GV000310, [5] https://www.e-tramits.ad/tramits/presentacio-de-propostes-artistiques-de-nova-creacio-per-a-andorra-crea-mercat-de-les-arts-fetes-a-andorra/p/GV001762

### public-information-request (GV000751)

Solicitar acceso a un documento público no tiene coste [1]. El tiempo máximo de respuesta es de 60 días hábiles [1].

Sources: [1] https://www.e-tramits.ad/tramits/acces-a-la-informacio-publica/p/GV000751, [2] https://www.e-tramits.ad/tramits/acces-a-programes-i-a-serveis-per-a-persones-amb-discapacitat-financats-amb-fons-public-i-dautoritzacio-per-tractar-la-discapacitat-a-lestranger/p/GV000033, [3] https://www.e-tramits.ad/tramits/demanda-de-treballadors-publics-interins-de-personal-de-refugis/p/GV001231, [4] https://www.e-tramits.ad/tramits/exercici-del-vot---informacio-accessible/p/GV000756, [5] https://www.e-tramits.ad/tramits/demanda-de-treballadors-publics-interins-de-personal-de-medi-natural/p/GV001285

### tax-debt-certificate (GV000653)

Per sol·licitar un Certificat de Deute, no està disponible la tramitació en línia [1]. Cal demanar cita prèvia per realitzar el tràmit [1].

Sources: [1] https://www.e-tramits.ad/tramits/certificat-de-deute/p/GV000653, [2] https://www.e-tramits.ad/tramits/expedicio-de-titols-densenyament-superior-de-caracter-estatal---certificat-del-titol/p/GV000134, [3] https://www.e-tramits.ad/tramits/certificat-de-naixement/p/GV001574, [4] https://www.e-tramits.ad/tramits/certificat-de-societat-mercantil-andorrana/p/GV000900, [5] https://www.e-tramits.ad/tramits/expedicio-de-qualificacions-densenyament-no-superior-del-sistema-educatiu-andorra/p/GV000070

### foreign-investment (GV001612)

The fee for the foreign investment authorization for real estate in Andorra is 300€ [3]. The maximum resolution time for this authorization is 2 months, with a possible extension of 1 month [3].

Sources: [1] https://www.e-tramits.ad/tramits/impostos/firstIeiTax, [2] https://www.e-tramits.ad/tramits/impostos/secondIeiTax, [3] https://www.e-tramits.ad/tramits/inversio-estrangera/p/GV001612, [4] https://www.e-tramits.ad/tramits/acces-a-programes-i-a-serveis-per-a-persones-amb-discapacitat-financats-amb-fons-public-i-dautoritzacio-per-tractar-la-discapacitat-a-lestranger/p/GV000033, [5] https://www.e-tramits.ad/tramits/h2-autoritzacio-dimmigracio-temporal-mes-de-30-dies-per-a-treballadors-dempreses-estrangeres/p/GV000492

### youth-emancipation (GV000061)

Hi ha dos programes relacionats amb l'emancipació de joves que podrien ser d'interès per a una persona de 25 anys:

1.  **Programa d’impuls per a l’emancipació de joves**: Aquest programa està dirigit a joves d'entre 18 i 35 anys (ambdós inclosos) que volen emancipar-se per primera vegada [1]. La subvenció està destinada a cobrir el dipòsit del contracte d’arrendament d’habitatge i la primera mensualitat de renda [1]. El període de sol·licitud per a aquest programa és del 23 de setembre de 2026 al 5 d'octubre de 2026 [1]. Per tant, pots demanar aquest ajut fins al 5 d'octubre de 2026 [1].

2.  **Accés al programa Vida independent “Vull emancipar-me”**: Aquest programa promou l’aprenentatge d’habilitats per a una vida autònoma i està dirigit a persones d'entre 17 i 30 anys [2]. No obstant això, un requisit previ és tenir reconegut un grau de menyscabament del 33% o superior amb un diagnòstic de discapacitat intel·lectual i/o trastorn del neurodesenvolupament [2]. El període de sol·licitud per a aquest programa és "Tot l’any" [2].

Sources: [1] https://www.e-tramits.ad/tramits/programa-dimpuls-per-a-lemancipacio-de-joves/p/GV000061, [2] https://www.e-tramits.ad/tramits/acces-al-programa-vida-independent-vull-emancipar-me/p/GV000041, [3] https://www.e-tramits.ad/tramits/programa-de-beques-per-a-joves-artistes-destinades-a-la-realitzacio-de-formacions-artistiques-avancades-i-la-participacio-en-certamens-i-concursos-internacionals/p/GV001631, [4] https://www.e-tramits.ad/tramits/jovempren---subvencions-per-a-projectes-impulsats-per-joves/p/GV000060, [5] https://www.e-tramits.ad/tramits/programa-alternatiu-de-rehabilitacio-per-a-persones-menors-dedat/p/GV000881

### passport-nationality-certificate (GV000451)

Le certificat de nationalité coûte 8,58 € [1].

Sources: [1] https://www.e-tramits.ad/tramits/passaports---certificat-de-nacionalitat/p/GV000451, [2] https://www.e-tramits.ad/tramits/demanda-dacreditacio-del-certificat-daptitud-professional/p/GV001633, [3] https://www.e-tramits.ad/tramits/certificat-de-naixement/p/GV001574, [4] https://www.e-tramits.ad/tramits/acreditacio-per-signar-conveni-amb-la-cass/p/GV000019, [5] https://www.e-tramits.ad/tramits/certificat-de-societat-mercantil-andorrana/p/GV000900

### habitability-certificate (GV000633)

El coste para solicitar el certificado de habitabilidad en línea es de 7,50 € [2]. El tiempo máximo de resolución es de 72 horas [2].

Sources: [1] https://www.e-tramits.ad/tramits/expedicio-de-titols-densenyament-superior-de-caracter-estatal---certificat-del-titol/p/GV000134, [2] https://www.e-tramits.ad/tramits/certificat-dhabitabilitat-en-linia/p/GV000633, [3] https://www.e-tramits.ad/tramits/certificat-de-registre-dhabitatge-dus-turistic-hut/p/GV000957, [4] https://www.e-tramits.ad/tramits/certificat-de-final-dobra-en-activitats-ambientals/p/GV000829, [5] https://www.e-tramits.ad/tramits/certificat-de-naixement/p/GV001574

### professional-artist (GV001743)

There is no fee to be accredited as a professional artist in Andorra [1]. The maximum resolution time for the decision is 60 business days [1].

Sources: [1] https://www.e-tramits.ad/tramits/acreditacio-com-a-artista-professional/p/GV001743, [2] https://www.e-tramits.ad/tramits/demanda-dacreditacio-del-certificat-daptitud-professional/p/GV001633, [3] https://www.e-tramits.ad/tramits/presentacio-de-propostes-artistiques-de-nova-creacio-per-a-andorra-crea-mercat-de-les-arts-fetes-a-andorra/p/GV001762, [4] https://www.e-tramits.ad/tramits/convocatoria-per-a-la-seleccio-dun-a-coordinador-a-artistic-i-gestor-a-de-projecte-per-andorra-crea-mercat-de-les-arts-fetes-a-andorra/p/GV001719, [5] https://www.e-tramits.ad/tramits/ajuda-financera-per-a-la-professionalitzacio-dels-artistes-musicals/p/GV001628

### school-study-grant (GV000125)

L'information concernant la période de demande d'aide aux études pour l'enseignement non supérieur cette année n'a pas été trouvée dans les sources fournies. Les sources indiquent une période de demande du 10 juin 2026 au 15 juillet 2026 [4].

Pour plus d'informations, vous pouvez consulter l'URL suivante : https://www.e-tramits.ad/tramits/ajut-a-lestudi-ensenyament-no-superior/p/GV000125.

Sources: [1] https://www.e-tramits.ad/tramits/inscripcio-a-la-prova-dacces-als-estudis-densenyament-superior-per-a-persones-mes-grans-de-25-anys/p/GV000772, [2] https://www.e-tramits.ad/tramits/acces-als-estudis-densenyament-superior/p/GV000133, [3] https://www.e-tramits.ad/tramits/ajut-a-lestudi-ensenyament-superior/p/GV000087, [4] https://www.e-tramits.ad/tramits/ajut-a-lestudi-ensenyament-no-superior/p/GV000125, [5] https://www.e-tramits.ad/tramits/ajut-a-lestudi---acceptacio-dun-ajut-fora-del-periode-de-convocatoria-ensenyament-no-superior/p/GV000916

### discounted-electricity (GV000054)

Sí, pots demanar la tarifa elèctrica bonificada en línia [1]. Aquest tràmit està disponible en línia [1]. L'aplicació de la tarifa elèctrica bonificada no té cap cost [1].

Per poder beneficiar-te d'aquesta bonificació, el sol·licitant o algun membre de la unitat de convivència ha de ser beneficiari d'alguna prestació econòmica o pensió dels Serveis Socials [1].

Sources: [1] https://www.e-tramits.ad/tramits/aplicacio-de-la-tarifa-electrica-bonificada/p/GV000054, [2] https://www.e-tramits.ad/tramits/declaracio-dinstallacio-electrica-de-baixa-tensio-o-de-molt-baixa-tensio-i-fibra-optica-tipus-b/p/GV000196, [3] https://www.e-tramits.ad/tramits/declaracio-dinstallacio-electrica-de-baixa-tensio-o-de-molt-baixa-tensio-i-fibra-optica-tipus-c/p/GV000197, [4] https://www.e-tramits.ad/tramits/descomptes-temporals-a-la-factura-de-subministrament-electric-per-activitats-comercials-al-pas-de-la-casa/p/GV001752, [5] https://www.e-tramits.ad/tramits/installacions-de-generacio-denergia-electrica-ipee/p/GV001066

### abstain-weather (-)

La informació sobre el temps que farà demà a Andorra la Vella no es troba a les fonts proporcionades.

Sources: [1] https://www.e-tramits.ad/tramits/impostos/contingut-irpf, [2] https://www.e-tramits.ad/tramits/presentacio-de-propostes-artistiques-de-nova-creacio-per-a-andorra-crea-mercat-de-les-arts-fetes-a-andorra/p/GV001762, [3] https://www.e-tramits.ad/tramits/peticio-informacio-al-registre-de-permisos-de-conduir/p/GV000302, [4] https://www.e-tramits.ad/tramits/convocatoria-per-a-la-seleccio-dun-a-coordinador-a-artistic-i-gestor-a-de-projecte-per-andorra-crea-mercat-de-les-arts-fetes-a-andorra/p/GV001719, [5] https://www.e-tramits.ad/tramits/segell-de-restaurant-de-cuina-tradicional-dandorra/p/GV000750

### abstain-ski-pass (-)

Les sources fournies ne contiennent pas d'informations sur le coût d'un forfait de ski de saison général à Grandvalira pour cet hiver. Les prix mentionnés concernent des forfaits universitaires et extra-scolaires pour la saison 2025-2026 [1].

L'information n'a pas été trouvée. Le lien le plus pertinent est le suivant : [https://www.e-tramits.ad/tramits/forfet-universitari-i-extraescolar-per-no-escolaritzats-per-la-temporada-2025-26/p/GV000700](https://www.e-tramits.ad/tramits/forfet-universitari-i-extraescolar-per-no-escolaritzats-per-la-temporada-2025-26/p/GV000700)

Sources: [1] https://www.e-tramits.ad/tramits/forfet-universitari-i-extraescolar-per-no-escolaritzats-per-la-temporada-2025-26/p/GV000700, [2] https://www.e-tramits.ad/tramits/inscripcio-a-notificacions-sms-sobre-lesqui-escolar/p/GV000702, [3] https://www.e-tramits.ad/tramits/llicencia-de-caca-de-temporada/p/GV000581, [4] https://www.e-tramits.ad/tramits/sorteig-muflo-vedat-temporada-estranger/p/GV000602, [5] https://www.e-tramits.ad/tramits/sorteig-muflo-vedat-temporada-andorrans-residents/p/GV000601

### abstain-border-queue (-)

The information about the current queue length at the Pas de la Casa border was not found in the provided sources.
The most relevant official URL, although not containing the answer, is related to Pas de la Casa: https://www.e-tramits.ad/tramits/descomptes-temporals-a-la-factura-de-subministrament-electric-per-activitats-comercials-al-pas-de-la-casa/p/GV001752 [1].

Sources: [1] https://www.e-tramits.ad/tramits/descomptes-temporals-a-la-factura-de-subministrament-electric-per-activitats-comercials-al-pas-de-la-casa/p/GV001752, [2] https://www.e-tramits.ad/tramits/duplicat-per-mal-estat-o-robatori-del-permis-de-conduir/p/GV000280, [3] https://www.e-tramits.ad/tramits/peticio-informacio-al-registre-de-permisos-de-conduir/p/GV000302, [4] https://www.e-tramits.ad/tramits/acces-al-programa-vida-independent-men-vaig-de-casa/p/GV001324, [5] https://www.e-tramits.ad/tramits/impostos/is

### abstain-minister-phone (-)

La información sobre el número de móvil personal del ministro de Finanzas no se encuentra en las fuentes proporcionadas.
Para obtener información relevante, puede consultar el siguiente URL oficial: https://www.e-tramits.ad/ [1, 2, 3, 4, 5].

Sources: [1] https://www.e-tramits.ad/tramits/acces-a-programes-i-a-serveis-per-a-persones-amb-discapacitat-financats-amb-fons-public-i-dautoritzacio-per-tractar-la-discapacitat-a-lestranger/p/GV000033, [2] https://www.e-tramits.ad/tramits/acces-al-servei-dassistencia-personal-persona-beneficiaria/p/GV000891, [3] https://www.e-tramits.ad/tramits/inscripcio-a-la-prova-dacces-als-estudis-densenyament-superior-per-a-persones-mes-grans-de-25-anys/p/GV000772, [4] https://www.e-tramits.ad/tramits/numero-didentificacio-administrativa-nia---atorgament/p/GV000419, [5] https://www.e-tramits.ad/tramits/numero-didentificacio-administrativa-nia---modificacio-de-dades/p/GV000420

### abstain-my-vacation (-)

La informació sobre quants dies de vacances li queden enguany a la seva empresa no es troba a les fonts proporcionades.

Sources: [1] https://www.e-tramits.ad/tramits/consulta-dun-examen-oficial-de-llengua-catalana/p/GV000152, [2] https://www.e-tramits.ad/tramits/h1-notificacio-de-treballs-de-curta-durada-menys-de-5-dies/p/GV000808, [3] https://www.e-tramits.ad/tramits/consulta-tributaria/p/GV000656, [4] https://www.e-tramits.ad/tramits/h1-notificacio-de-treballs-de-curta-durada-mes-de-5-dies/p/GV000503, [5] https://www.e-tramits.ad/tramits/h2-autoritzacio-dimmigracio-temporal-mes-de-30-dies-per-a-treballadors-dempreses-estrangeres/p/GV000492
