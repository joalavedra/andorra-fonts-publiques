# Assistant eval, 2026-10-03

Model `gemini-2.5-flash`, temperature 0, 8 cases from `evals/govern.yaml`.

- Pass: **4/8**
- Right procedure retrieved: 6/8
- Right procedure cited: 5/8
- Facts correct: 5/12
- Citations to non-existent sources: 0
- Closed-book baseline (same model, no sources), facts correct: 5/12

| case | lang | pass | retrieved | cited | facts | secs |
|---|---|---|---|---|---|---|
| passport-price | en | FAIL | False | False | ten_year:MISS five_year:MISS | 17.5 |
| digital-nomad-residence | en | PASS | True | True | days:ok period:ok | 15.8 |
| passive-residence-income | es | FAIL | True | True | income:MISS dependant:MISS | 16.5 |
| non-resident-tax-rate | fr | PASS | True | True | rate:ok | 24.7 |
| customs-allowance | en | FAIL | False | False | cigarettes:MISS industrial:MISS | 21.3 |
| nationality-by-marriage | ca | PASS | True | True | years:ok | 14.5 |
| nationality-naturalisation | es | PASS | True | True | years:ok | 12.6 |
| passport-lost-abroad | fr | FAIL | True | False | embassy:MISS | 24.7 |

## Answers

### passport-price (govern\.ad/.*passaport)

The information regarding the cost of an Andorran passport was not found in the provided sources.

The most relevant official URL is: https://www.e-tramits.ad/tramits/passaports---copia-compulsada/p/GV000452 [4].

Sources: [1] https://www.e-tramits.ad/tramits/expedicio-de-titols-densenyament-superior-de-caracter-estatal---certificat-del-titol/p/GV000134, [2] https://www.e-tramits.ad/tramits/primera-obtencio-dun-permis-de-conduir/p/GV000300, [3] https://www.e-tramits.ad/tramits/expedicio-de-qualificacions-densenyament-no-superior-del-sistema-educatiu-andorra/p/GV000070, [4] https://www.e-tramits.ad/tramits/passaports---copia-compulsada/p/GV000452, [5] https://www.e-tramits.ad/tramits/expedicio-del-diploma-de-llengua-catalana-de-ciencies-humanes-i-socials-dandorra-chsa-i-de-competencia-digital-ciutadana-cdc/p/GV000902, [6] https://www.govern.ad/ca/tematiques/registre-civil/matrimonis-civils/expedient-previ-a-la-celebracio-del-matrimoni-civil, [7] https://www.govern.ad/ca/tematiques/registre-civil/unions-estables-de-parella/expedient-previ-al-registre-d-unions-estables-de-parella

### digital-nomad-residence (govern\.ad/.*nomada-digital)

For Andorra's digital nomad residence (D.3. Residència per a nòmada digital), you must establish your main and effective residence in the Principality of Andorra for at least 90 days per natural year [1, 6]. The initial residence authorization is granted for a period of two years [1, 6].

Sources: [1] https://www.e-tramits.ad/tramits/d3-residencia-per-a-nomada-digital/p/GV001311, [2] https://www.e-tramits.ad/tramits/j2-residencia-i-treball-per-compte-propi-autoritzacio-de-renovacio/p/GV000502, [3] https://www.e-tramits.ad/tramits/b2-residencia-per-raons-de-reagrupament-autoritzacio-de-renovacio/p/GV000490, [4] https://www.e-tramits.ad/tramits/j1-residencia-i-treball-per-compte-propi-autoritzacio-inicial/p/GV000501, [5] https://www.e-tramits.ad/tramits/b1-residencia-per-raons-de-reagrupament-autoritzacio-inicial/p/GV000489, [6] https://www.govern.ad/ca/tematiques/immigracio/residencia/residencia-per-a-nomada-digital, [7] https://www.govern.ad/ca/tematiques/immigracio/residencia-i-treball

### passive-residence-income (govern\.ad/.*residencia-sense-treball)

La información sobre los ingresos anuales específicos requeridos para la residencia sin trabajo en Andorra no se encuentra en las fuentes proporcionadas [1, 2, 3, 4, 5, 6, 7].

Para obtener más detalles sobre la autorización inicial de residencia sin trabajo, puede consultar la siguiente URL oficial: https://www.e-tramits.ad/tramits/d1-residencia-sense-treball-autoritzacio-inicial/p/GV001309 [2].

Sources: [1] https://www.e-tramits.ad/tramits/d2-residencia-sense-activitat-lucrativa-renovacio/p/GV001310, [2] https://www.e-tramits.ad/tramits/d1-residencia-sense-treball-autoritzacio-inicial/p/GV001309, [3] https://www.e-tramits.ad/tramits/i2-autoritzacio-de-treball-sense-residencia-autoritzacio-de-renovacio/p/GV000505, [4] https://www.e-tramits.ad/tramits/i1-autoritzacio-de-treball-sense-residencia-autoritzacio-inicial/p/GV000504, [5] https://www.e-tramits.ad/tramits/l-2-certificat-dinscripcio-de-residencia-sense-treball/p/GV000509, [6] https://www.govern.ad/ca/tematiques/immigracio/residencia/residencia-sense-treball-autoritzacio-inicial, [7] https://www.govern.ad/ca/tematiques/immigracio/residencia/residencia-sense-treball-autoritzacio-de-renovacio

### non-resident-tax-rate (govern\.ad/.*no-residents)

L'impôt sur le revenu des non-résidents fiscaux (IRNR) est généralement de 10 % du montant de la facture payée pour les services [6]. Cela inclut les services de conseil, les études, les projets, l'assistance technique et le soutien à la gestion, si les services sont consommés en Andorre [6].

Il existe des taux spécifiques pour d'autres types de revenus :
*   Pour les redevances (cànons), l'impôt est de 5 % de la facture payée [6].
*   Pour les réassurances, il est de 1,5 % [6].
*   Pour les locations de biens immobiliers, une réduction de 20 % est appliquée sur le montant reçu [6].

Sources: [1] https://www.e-tramits.ad/tramits/impostos/irnr, [2] https://www.e-tramits.ad/tramits/impostos/irpf, [3] https://www.e-tramits.ad/tramits/impostos/is, [4] https://www.e-tramits.ad/tramits/impostos/ieat, [5] https://www.e-tramits.ad/tramits/devolucio-parcial-de-limpost-especial-sobre-els-hidrocarburs/p/GV000754, [6] https://www.govern.ad/ca/tematiques/impostos-taxes-i-duana/impostos-en-andorra/impost-sobre-la-renda-dels-no-residents-fiscals-a-andorra, [7] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-finances/convenis-i-normativa/impostos

### customs-allowance (govern\.ad/.*franquicies)

The information regarding the number of cigarettes you can take back to the EU from Andorra without paying duty, and the value limit for other industrial products, was not found in the provided sources. The sources primarily discuss import authorizations into Andorra, international transport of goods, or customs duties applied to goods entering Andorra [1, 2, 3, 4, 5, 6, 7].

For more information, you may refer to the general customs and franchises page: https://www.govern.ad/ca/tematiques/impostos-taxes-i-duana/aranzels-duaners-i-granquicies [7].

Sources: [1] https://www.e-tramits.ad/tramits/autoritzacio-per-a-la-importacio-temporal-de-mitjans-de-transport/p/GV000326, [2] https://www.e-tramits.ad/tramits/transport-internacional-de-mercaderies-amb-italia/p/GV001298, [3] https://www.e-tramits.ad/tramits/autoritzacio-dimportacio-de-substancies-explosives/p/GV000174, [4] https://www.e-tramits.ad/tramits/transport-internacional-de-mercaderies-amb-franca/p/GV001294, [5] https://www.e-tramits.ad/tramits/transport-internacional-public-de-mercaderies-amb-portugal/p/GV001292, [6] https://www.govern.ad/ca/tematiques/impostos-taxes-i-duana/duana/formularis, [7] https://www.govern.ad/ca/tematiques/impostos-taxes-i-duana/aranzels-duaners-i-granquicies

### nationality-by-marriage (govern\.ad/.*nacionalitat)

Per demanar la nacionalitat andorrana estant casat amb una persona de nacionalitat andorrana, cal acreditar una residència principal i permanent al Principat d’Andorra de manera ininterrompuda des d’almenys cinc anys, abans o després de la celebració del matrimoni, i provar la integració al Principat d’Andorra [6].

Sources: [1] https://www.e-tramits.ad/tramits/passaports---certificat-de-nacionalitat/p/GV000451, [2] https://www.e-tramits.ad/tramits/ajuts-per-assistir-a-la-universitat-catalana-destiu-i-a-la-diada-andorrana/p/GV001623, [3] https://www.e-tramits.ad/tramits/demanda-de-nacionalitat/p/GV100016, [4] https://www.e-tramits.ad/tramits/modificacio-de-nacionalitat/p/GV100017, [5] https://www.e-tramits.ad/tramits/certificat-de-societat-mercantil-andorrana/p/GV000900, [6] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-justicia-i-interior/nacionalitat/adquisicio-de-la-nacionalitat-andorrana, [7] https://www.govern.ad/ca/tematiques/cultura-i-esports/fundacions/escena-nacional-d-andorra

### nationality-naturalisation (govern\.ad/.*nacionalitat)

Para obtener la nacionalidad andorrana por naturalización, una persona extranjera debe acreditar haber tenido la residencia principal y permanente en el Principado de Andorra durante veinte años, ya sea de forma interrumpida o ininterrumpida [6]. Además, a la fecha de presentación de la solicitud, debe haber tenido la residencia principal y efectiva en el país durante, como mínimo, los cinco años anteriores a dicha fecha [6].

Sources: [1] https://www.e-tramits.ad/tramits/registre-dembarcacions---obtencio-del-titol-per-poder-pilotar-embarcacions-andorranes-desbarjo-i-esportives/p/GV001295, [2] https://www.e-tramits.ad/tramits/ajuts-per-assistir-a-la-universitat-catalana-destiu-i-a-la-diada-andorrana/p/GV001623, [3] https://www.e-tramits.ad/tramits/inscripcio-a-la-prova-oficial-per-a-lobtencio-del-diploma-de-competencies-digitals-ciutadanes/p/GV001643, [4] https://www.e-tramits.ad/tramits/subvencio-per-a-ladquisicio-i-implementacio-delements-de-prevencio-dels-danys-i-perjudicis-que-les-especies-de-fauna-protegides-en-perill-dextincio-o-en-un-grau-damenaca-superior-puguin-causar-a-lagricultura-la-ramaderia-i-lapicultura/p/GV001759, [5] https://www.e-tramits.ad/tramits/convocatoria-per-a-la-seleccio-dun-a-coordinador-a-artistic-i-gestor-a-de-projecte-per-andorra-crea-mercat-de-les-arts-fetes-a-andorra/p/GV001719, [6] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-justicia-i-interior/nacionalitat/adquisicio-de-la-nacionalitat-andorrana, [7] https://www.govern.ad/ca/tematiques/habitatge/drets-adquisicio-preferent

### passport-lost-abroad (govern\.ad/.*passaport)

Pour demander un duplicata de votre passeport andorran suite à une perte, vous devez vous adresser aux bureaux des procédures (oficines de Tràmits) [1]. Cette démarche doit être effectuée en personne et de manière personnelle [1]. Un rendez-vous est nécessaire [1].

En cas de perte, il est requis de présenter la dénonciation (plainte) délivrée par la Police Andorrane [1].

Les sources fournies n'indiquent pas comment obtenir cette dénonciation de la Police Andorrane si la perte du passeport est survenue à l'étranger. Pour plus d'informations, veuillez consulter l'URL officielle : https://www.e-tramits.ad/tramits/passaports---duplicat-per-perdua-o-robatori/p/GV000455 [1].

Sources: [1] https://www.e-tramits.ad/tramits/passaports---duplicat-per-perdua-o-robatori/p/GV000455, [2] https://www.e-tramits.ad/tramits/duplicat-per-perdua-o-robatori-del-permis-de-conduir/p/GV000281, [3] https://www.e-tramits.ad/tramits/primera-matriculacio-dun-vehicle-vehicle-nou-vehicle-ocasio-amb-placa-estrangera-vehicle-amb-placa-mt-i-vehicle-historic/p/GV000365, [4] https://www.e-tramits.ad/tramits/demanda-de-beca-per-a-estades-de-creacio-i-formacio-a-lestranger-2026/p/GV001758, [5] https://www.e-tramits.ad/tramits/targeta-blava---duplicat-per-perdua-o-per-robatori/p/GV000036, [6] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-justicia-i-interior/passaports, [7] https://www.govern.ad/ca/tematiques/registre-civil/matrimonis-civils/expedient-previ-a-la-celebracio-del-matrimoni-civil
