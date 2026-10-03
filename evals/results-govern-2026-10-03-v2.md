# Assistant eval, 2026-10-03

Model `gemini-2.5-flash`, temperature 0, 8 cases from `evals/govern.yaml`.

- Pass: **5/8**
- Right procedure retrieved: 6/8
- Right procedure cited: 5/8
- Facts correct: 8/12
- Citations to non-existent sources: 0
- Closed-book baseline (same model, no sources), facts correct: 6/12

| case | lang | pass | retrieved | cited | facts | secs |
|---|---|---|---|---|---|---|
| passport-price | en | PASS | True | True | ten_year:ok five_year:ok | 15.3 |
| digital-nomad-residence | en | PASS | True | True | days:ok period:ok | 14.2 |
| passive-residence-income | es | PASS | True | True | income:ok dependant:ok | 18.8 |
| non-resident-tax-rate | fr | FAIL | False | False | rate:MISS | 22.0 |
| customs-allowance | en | FAIL | False | False | cigarettes:MISS industrial:MISS | 19.5 |
| nationality-by-marriage | ca | FAIL | True | False | years:MISS | 18.2 |
| nationality-naturalisation | es | PASS | True | True | years:ok | 11.8 |
| passport-lost-abroad | fr | PASS | True | True | embassy:ok | 15.5 |

## Answers

### passport-price (govern\.ad/.*passaport)

The cost of an Andorran passport is 49.31 euros for passports with a 10-year validity [6]. For passports with a 5-year validity or less, the cost is 32.16 euros [6].

Specifically for renewals:
*   For individuals under 20 years of age, the renewal cost is 32.16€ [1].
*   For individuals over 20 years of age, the renewal cost is 49.31€ [1].

Sources: [1] https://www.e-tramits.ad/tramits/passaports---renovacio/p/GV000462, [2] https://www.e-tramits.ad/tramits/passaports---certificat-de-nacionalitat/p/GV000451, [3] https://www.e-tramits.ad/tramits/passaports---copia-compulsada/p/GV000452, [4] https://www.e-tramits.ad/tramits/passaports---doble-provisional/p/GV000454, [5] https://www.e-tramits.ad/tramits/passaports---duplicat-per-perdua-o-robatori/p/GV000455, [6] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-justicia-i-interior/passaports, [7] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-d-afers-exteriors/el-ministeri/afers-bilaterals-i-consulars/afers-consulars, [8] https://www.govern.ad/ca/tematiques/immigracio/treball/treball-de-fronterer-autoritzacio-de-renovacio

### digital-nomad-residence (govern\.ad/.*nomada-digital)

For Andorra's digital nomad residence, you must establish your main and effective residence in the Principality of Andorra for at least 90 days per natural year [1, 6]. The initial residence authorization is granted for a period of two years [1, 6].

Sources: [1] https://www.e-tramits.ad/tramits/d3-residencia-per-a-nomada-digital/p/GV001311, [2] https://www.e-tramits.ad/tramits/qualificacio-de-persona-fisica-estrangera-que-no-requereix-disposar-duna-ubicacio-geografica-concreta-i-utilitza-les-telecomunicacions-i-la-tecnologia-per-treballar-nomada-digital/p/GV000785, [3] https://www.e-tramits.ad/tramits/b1-residencia-per-raons-de-reagrupament-autoritzacio-inicial/p/GV000489, [4] https://www.e-tramits.ad/tramits/j1-residencia-i-treball-per-compte-propi-autoritzacio-inicial/p/GV000501, [5] https://www.e-tramits.ad/tramits/a1-residencia-i-treball-autoritzacio-inicial/p/GV000484, [6] https://www.govern.ad/ca/tematiques/immigracio/residencia/residencia-per-a-nomada-digital, [7] https://www.govern.ad/ca/tematiques/immigracio/residencia-i-treball, [8] https://www.govern.ad/ca/tematiques/immigracio/residencia-i-treball/residencia-i-treball-autoritzacio-inicial

### passive-residence-income (govern\.ad/.*residencia-sense-treball)

Para la renovación de la autorización de residencia sin trabajo, se debe demostrar que el titular tiene ingresos superiores al 300% del salario mínimo anual vigente, añadiendo el 100% de este indicador por cada persona a cargo [6]. Por ejemplo, para el titular principal, se requiere un salario base multiplicado por 12 meses y por 3 (300%) [6]. Esta información se acredita, entre otros medios, mediante un certificado de pensión de jubilación y/o una declaración de renta del año anterior del último país de residencia y las certificaciones bancarias correspondientes [6].

La información sobre los ingresos anuales específicos para la autorización inicial de residencia sin trabajo no se encuentra detallada en las fuentes proporcionadas [2].

Sources: [1] https://www.e-tramits.ad/tramits/d2-residencia-sense-activitat-lucrativa-renovacio/p/GV001310, [2] https://www.e-tramits.ad/tramits/d1-residencia-sense-treball-autoritzacio-inicial/p/GV001309, [3] https://www.e-tramits.ad/tramits/l-2-certificat-dinscripcio-de-residencia-sense-treball/p/GV000509, [4] https://www.e-tramits.ad/tramits/d14--residencia-sense-treball-autoritzacio-inicial/p/GV000499, [5] https://www.e-tramits.ad/tramits/i1-autoritzacio-de-treball-sense-residencia-autoritzacio-inicial/p/GV000504, [6] https://www.govern.ad/ca/tematiques/immigracio/residencia/residencia-sense-treball-autoritzacio-de-renovacio, [7] https://www.govern.ad/ca/tematiques/immigracio/treball/treball-sense-residencia-autoritzacio-de-renovacio, [8] https://www.govern.ad/ca/tematiques/immigracio/treball/treball-sense-residencia-autoritzacio-inicial

### non-resident-tax-rate (govern\.ad/.*no-residents)

L'information concernant le taux de l'impôt sur le revenu des non-résidents (IRNR) n'a pas été trouvée dans les sources fournies [1, 2, 3, 4, 5, 6, 7, 8].

Pour plus d'informations sur l'IRNR, vous pouvez consulter la page officielle : https://www.e-tramits.ad/tramits/impostos/contingut-irnr [1].

Sources: [1] https://www.e-tramits.ad/tramits/impostos/contingut-irnr, [2] https://www.e-tramits.ad/tramits/impostos/censal, [3] https://www.e-tramits.ad/tramits/irnr-relacio-de-treballadors-que-sacullen-al-regim-especial-de-treballadors-fronterers-i-temporers-representacio-fiscal-formulari-exclusiu-empresaris/p/GV001707, [4] https://www.e-tramits.ad/tramits/impostos/irnr, [5] https://www.e-tramits.ad/tramits/impostos/censal, [6] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-finances/pressupostos-liquidacions, [7] https://www.govern.ad/ca/tematiques/impostos-taxes-i-duana/formularis, [8] https://www.govern.ad/ca/tematiques/impostos-taxes-i-duana/duana/formularis

### customs-allowance (govern\.ad/.*franquicies)

The provided sources do not contain information on the specific quantity of cigarettes or the value limit for other industrial products that can be taken back to the EU from Andorra without paying duty.

The sources mention customs tariffs and franchises in general [6, 7], and that specific tax rates apply to tobacco products when imported into Andorra [6]. However, they do not detail the duty-free allowances for travelers exiting Andorra into the EU.

For more information, you may refer to the "Customs tariffs and franchises" section on the Government of Andorra's website: [6].

Sources: [1] https://www.e-tramits.ad/tramits/autoritzacio-per-a-la-importacio-temporal-de-mitjans-de-transport/p/GV000326, [2] https://www.e-tramits.ad/tramits/llicencia-de-mercaderies-sensibles/p/GV001227, [3] https://www.e-tramits.ad/tramits/autoritzacio-dimportacio-de-substancies-explosives/p/GV000174, [4] https://www.e-tramits.ad/tramits/transport-internacional-de-mercaderies-amb-franca/p/GV001294, [5] https://www.e-tramits.ad/tramits/importacio-exportacio-o-reexportacio-relativa-als-exemplars-productes-de-la-fauna-flora-autoctona-no-autoctona/p/GV000541, [6] https://www.govern.ad/ca/tematiques/impostos-taxes-i-duana/aranzels-duaners-i-granquicies, [7] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-finances/convenis-i-normativa/legislacio-duana, [8] https://www.govern.ad/ca/tematiques/impostos-taxes-i-duana/duana/formularis

### nationality-by-marriage (govern\.ad/.*nacionalitat)

La informació sobre els anys de residència necessaris per demanar la nacionalitat andorrana per estar casat amb una persona andorrana no es troba a les fonts proporcionades.

Podeu trobar informació general sobre la demanda de nacionalitat a l'URL oficial: https://www.e-tramits.ad/tramits/demanda-de-nacionalitat/p/GV100016 [1].

Sources: [1] https://www.e-tramits.ad/tramits/demanda-de-nacionalitat/p/GV100016, [2] https://www.e-tramits.ad/tramits/concessio-de-subvencio-cultural/p/GV000627, [3] https://www.e-tramits.ad/tramits/modificacio-de-nacionalitat/p/GV100017, [4] https://www.e-tramits.ad/tramits/concessio-dun-ajut-a-la-cinematografia/p/GV000704, [5] https://www.e-tramits.ad/tramits/passaports---certificat-de-nacionalitat/p/GV000451, [6] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-justicia-i-interior/nacionalitat/adquisicio-de-la-nacionalitat-andorrana, [7] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-justicia-i-interior/nacionalitat/la-nacionalitat-andorrana-d-origen, [8] https://www.govern.ad/ca/tematiques/habitatge/drets-adquisicio-preferent

### nationality-naturalisation (govern\.ad/.*nacionalitat)

Para obtener la nacionalidad andorrana por naturalización, una persona extranjera que no ha estudiado en Andorra debe acreditar haber tenido la residencia principal y permanente en el Principado de Andorra durante veinte años, de forma ininterrumpida o ininterrumpidamente [6]. Además, debe probar su integración y haber tenido la residencia principal y efectiva en el país en la fecha de presentación de la solicitud [6].

Sources: [1] https://www.e-tramits.ad/tramits/registre-dembarcacions---obtencio-del-titol-per-poder-pilotar-embarcacions-andorranes-desbarjo-i-esportives/p/GV001295, [2] https://www.e-tramits.ad/tramits/demanda-de-nacionalitat/p/GV100016, [3] https://www.e-tramits.ad/tramits/obtencio-del-permis-de-caca/p/GV000571, [4] https://www.e-tramits.ad/tramits/modificacio-de-nacionalitat/p/GV100017, [5] https://www.e-tramits.ad/tramits/obtencio-del-carnet-de-xofer-de-taxi/p/GV001302, [6] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-justicia-i-interior/nacionalitat/adquisicio-de-la-nacionalitat-andorrana, [7] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-justicia-i-interior/nacionalitat/la-nacionalitat-andorrana-d-origen, [8] https://www.govern.ad/ca/tematiques/habitatge/drets-adquisicio-preferent

### passport-lost-abroad (govern\.ad/.*passaport)

Si la perte ou le vol de votre passeport andorran a lieu à l'étranger, vous devez vous adresser à l'Ambassade d'Andorre présente sur place [6]. En l'absence de représentation diplomatique andorrane, vous devrez contacter le Ministère des Affaires Étrangères [6]. Les représentations diplomatiques ont pour rôle d'assister les citoyens andorrans résidant ou voyageant à l'étranger en cas de difficultés, telles que la perte de passeport [7]. Le Service des Affaires Consulaires, centralisé au Ministère des Affaires Étrangères en Andorre, travaille en coordination directe avec les représentations diplomatiques et assiste les citoyens andorrans dans leurs démarches et voyages à l'étranger [7].

Sources: [1] https://www.e-tramits.ad/tramits/passaports---duplicat-per-perdua-o-robatori/p/GV000455, [2] https://www.e-tramits.ad/tramits/passaports---renovacio/p/GV000462, [3] https://www.e-tramits.ad/tramits/duplicat-per-perdua-o-robatori-del-permis-de-conduir/p/GV000281, [4] https://www.e-tramits.ad/tramits/passaports---certificat-de-nacionalitat/p/GV000451, [5] https://www.e-tramits.ad/tramits/passaports---copia-compulsada/p/GV000452, [6] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-justicia-i-interior/passaports, [7] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-d-afers-exteriors/el-ministeri/afers-bilaterals-i-consulars/afers-consulars, [8] https://www.govern.ad/ca/tematiques/immigracio/treball/treball-de-fronterer-autoritzacio-de-renovacio
