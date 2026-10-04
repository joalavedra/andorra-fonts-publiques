# Assistant eval, 2026-10-04

Model `gemini-2.5-flash`, temperature 0, 8 cases from `evals/govern.yaml`.

- Pass: **7/8**
- Right procedure retrieved: 7/8
- Right procedure cited: 7/8
- Facts correct: 10/12
- Citations to non-existent sources: 0

| case | lang | pass | retrieved | cited | facts | secs |
|---|---|---|---|---|---|---|
| passport-price | en | PASS | True | True | ten_year:ok five_year:ok | 17.3 |
| digital-nomad-residence | en | PASS | True | True | days:ok period:ok | 15.4 |
| passive-residence-income | es | PASS | True | True | income:ok dependant:ok | 19.4 |
| non-resident-tax-rate | fr | PASS | True | True | rate:ok | 22.6 |
| customs-allowance | en | FAIL | False | False | cigarettes:MISS industrial:MISS | 23.1 |
| nationality-by-marriage | ca | PASS | True | True | years:ok | 15.7 |
| nationality-naturalisation | es | PASS | True | True | years:ok | 12.0 |
| passport-lost-abroad | fr | PASS | True | True | embassy:ok | 16.4 |

## Answers

### passport-price (govern\.ad/.*passaport)

The cost of an Andorran passport is 49.31 euros for passports with a 10-year validity [6]. For passports with a 5-year validity or less, the cost is 32.16 euros [6].

For renewals, the cost is 32.16€ for individuals under 20 years old and 49.31€ for individuals over 20 years old [1]. A duplicate passport due to loss or theft costs 49.31€ [5]. A provisional double passport costs 32.16€ [4].

Sources: [1] https://www.e-tramits.ad/tramits/passaports---renovacio/p/GV000462, [2] https://www.e-tramits.ad/tramits/passaports---certificat-de-nacionalitat/p/GV000451, [3] https://www.e-tramits.ad/tramits/passaports---copia-compulsada/p/GV000452, [4] https://www.e-tramits.ad/tramits/passaports---doble-provisional/p/GV000454, [5] https://www.e-tramits.ad/tramits/passaports---duplicat-per-perdua-o-robatori/p/GV000455, [6] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-justicia-i-interior/passaports, [7] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-d-afers-exteriors/el-ministeri/afers-bilaterals-i-consulars/afers-consulars, [8] https://www.govern.ad/ca/tematiques/immigracio/treball/treball-de-fronterer-autoritzacio-de-renovacio

### digital-nomad-residence (govern\.ad/.*nomada-digital)

To maintain a digital nomad residence in Andorra, you must establish your main and effective residence in the Principality of Andorra for at least 90 days per natural year [1, 6].

The initial residence authorization for digital nomads is granted for a period of two years [1, 6].

Sources: [1] https://www.e-tramits.ad/tramits/d3-residencia-per-a-nomada-digital/p/GV001311, [2] https://www.e-tramits.ad/tramits/qualificacio-de-persona-fisica-estrangera-que-no-requereix-disposar-duna-ubicacio-geografica-concreta-i-utilitza-les-telecomunicacions-i-la-tecnologia-per-treballar-nomada-digital/p/GV000785, [3] https://www.e-tramits.ad/tramits/b1-residencia-per-raons-de-reagrupament-autoritzacio-inicial/p/GV000489, [4] https://www.e-tramits.ad/tramits/j1-residencia-i-treball-per-compte-propi-autoritzacio-inicial/p/GV000501, [5] https://www.e-tramits.ad/tramits/a1-residencia-i-treball-autoritzacio-inicial/p/GV000484, [6] https://www.govern.ad/ca/tematiques/immigracio/residencia/residencia-per-a-nomada-digital, [7] https://www.govern.ad/ca/tematiques/immigracio/residencia-i-treball, [8] https://www.govern.ad/ca/tematiques/immigracio/residencia-i-treball/residencia-i-treball-autoritzacio-inicial

### passive-residence-income (govern\.ad/.*residencia-sense-treball)

Para la renovación de la autorización de residencia sin trabajo, se debe demostrar que el titular tiene ingresos superiores al 300% del salario mínimo anual vigente, añadiendo el 100% de este indicador por cada persona a cargo [6]. Por ejemplo, para el titular principal, se requiere un salario base multiplicado por 12 meses y por 3 (300%) [6]. Esta información se acredita, entre otros medios, mediante un certificado de pensión de jubilación y/o una declaración de renta del año anterior del último país de residencia y las certificaciones bancarias correspondientes [6].

La información sobre los ingresos anuales específicos para la autorización inicial de residencia sin trabajo no se encuentra detallada en las fuentes proporcionadas [2].

Sources: [1] https://www.e-tramits.ad/tramits/d2-residencia-sense-activitat-lucrativa-renovacio/p/GV001310, [2] https://www.e-tramits.ad/tramits/d1-residencia-sense-treball-autoritzacio-inicial/p/GV001309, [3] https://www.e-tramits.ad/tramits/l-2-certificat-dinscripcio-de-residencia-sense-treball/p/GV000509, [4] https://www.e-tramits.ad/tramits/d14--residencia-sense-treball-autoritzacio-inicial/p/GV000499, [5] https://www.e-tramits.ad/tramits/i1-autoritzacio-de-treball-sense-residencia-autoritzacio-inicial/p/GV000504, [6] https://www.govern.ad/ca/tematiques/immigracio/residencia/residencia-sense-treball-autoritzacio-de-renovacio, [7] https://www.govern.ad/ca/tematiques/immigracio/treball/treball-sense-residencia-autoritzacio-de-renovacio, [8] https://www.govern.ad/ca/tematiques/immigracio/treball/treball-sense-residencia-autoritzacio-inicial

### non-resident-tax-rate (govern\.ad/.*no-residents)

L'impôt sur le revenu des non-résidents (IRNR) est généralement de 10 % du montant de la facture payée [6].

Cependant, il existe des taux spécifiques pour d'autres types de revenus :
*   Pour les revenus payés sous forme de redevances (cànons), l'impôt est de 5 % de la facture payée [6].
*   Pour les réassurances, le taux est de 1,5 % [6].
*   Pour les locations immobilières, une réduction de 20 % est appliquée sur le montant reçu [6].

Un exemple pour un consultant non-résident (assessor no resident) montre une retenue d'IRNR de 10 % [6].

Sources: [1] https://www.e-tramits.ad/tramits/impostos/irnr, [2] https://www.e-tramits.ad/tramits/impostos/irpf, [3] https://www.e-tramits.ad/tramits/impostos/is, [4] https://www.e-tramits.ad/tramits/impostos/ieat, [5] https://www.e-tramits.ad/tramits/devolucio-parcial-de-limpost-especial-sobre-els-hidrocarburs/p/GV000754, [6] https://www.govern.ad/ca/tematiques/impostos-taxes-i-duana/impostos-en-andorra/impost-sobre-la-renda-dels-no-residents-fiscals-a-andorra, [7] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-finances/convenis-i-normativa/impostos, [8] https://www.govern.ad/ca/tematiques/impostos-taxes-i-duana/impostos-en-andorra/sistema-tributari

### customs-allowance (govern\.ad/.*franquicies)

The provided sources do not contain information on how many cigarettes can be taken back to the EU from Andorra without paying duty, nor do they specify the value limit for other industrial products when returning to the EU from Andorra. The sources primarily detail customs procedures, tariffs, and legislation related to importing goods into Andorra or general customs matters within Andorra [1, 2, 3, 4, 5, 6, 7, 8].

For information related to customs tariffs and franchises, you may refer to the official URL: https://www.govern.ad/ca/tematiques/impostos-taxes-i-duana/aranzels-duaners-i-granquicies [6].

Sources: [1] https://www.e-tramits.ad/tramits/autoritzacio-per-a-la-importacio-temporal-de-mitjans-de-transport/p/GV000326, [2] https://www.e-tramits.ad/tramits/llicencia-de-mercaderies-sensibles/p/GV001227, [3] https://www.e-tramits.ad/tramits/autoritzacio-dimportacio-de-substancies-explosives/p/GV000174, [4] https://www.e-tramits.ad/tramits/transport-internacional-de-mercaderies-amb-franca/p/GV001294, [5] https://www.e-tramits.ad/tramits/importacio-exportacio-o-reexportacio-relativa-als-exemplars-productes-de-la-fauna-flora-autoctona-no-autoctona/p/GV000541, [6] https://www.govern.ad/ca/tematiques/impostos-taxes-i-duana/aranzels-duaners-i-granquicies, [7] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-finances/convenis-i-normativa/legislacio-duana, [8] https://www.govern.ad/ca/tematiques/impostos-taxes-i-duana/duana/formularis

### nationality-by-marriage (govern\.ad/.*nacionalitat)

Una persona estrangera que ha contret matrimoni amb una persona de nacionalitat andorrana pot adquirir la nacionalitat andorrana si acredita tenir la residència principal i permanent al Principat d’Andorra ininterrompudament des d’almenys cinc anys, abans o després de la celebració del matrimoni [6].

Sources: [1] https://www.e-tramits.ad/tramits/sorteig-isard-andorrans-residents/p/GV000607, [2] https://www.e-tramits.ad/tramits/sorteig-muflo-en-vedat-andorrans-residents/p/GV000598, [3] https://www.e-tramits.ad/tramits/d3-residencia-per-a-nomada-digital/p/GV001311, [4] https://www.e-tramits.ad/tramits/demanda-de-nacionalitat/p/GV100016, [5] https://www.e-tramits.ad/tramits/modificacio-de-nacionalitat/p/GV100017, [6] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-justicia-i-interior/nacionalitat/adquisicio-de-la-nacionalitat-andorrana, [7] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-justicia-i-interior/nacionalitat/la-nacionalitat-andorrana-d-origen, [8] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-justicia-i-interior/nacionalitat/normativa

### nationality-naturalisation (govern\.ad/.*nacionalitat)

Para obtener la nacionalidad andorrana por naturalización, una persona extranjera debe acreditar haber tenido la residencia principal y permanente en el Principado de Andorra durante veinte años, ya sea de forma interrumpida o ininterrumpida [6]. Además, debe probar su integración y haber tenido la residencia principal y efectiva en el país en la fecha de presentación de la solicitud [6].

Existe otra vía de naturalización que requiere diez años de residencia principal y permanente ininterrumpida en Andorra, pero esta opción también exige haber cursado un mínimo de diez cursos escolares en centros docentes públicos o privados del Principado de Andorra [6]. Dado que no ha estudiado en Andorra, esta última opción no sería aplicable a su caso.

Sources: [1] https://www.e-tramits.ad/tramits/demanda-de-nacionalitat/p/GV100016, [2] https://www.e-tramits.ad/tramits/modificacio-de-nacionalitat/p/GV100017, [3] https://www.e-tramits.ad/tramits/passaports---certificat-de-nacionalitat/p/GV000451, [4] https://www.e-tramits.ad/tramits/certificat-de-societat-mercantil-andorrana/p/GV000900, [5] https://www.e-tramits.ad/tramits/pla-engega---ajut-dadquisicio-de-vehicle-de-mobilitat-electrica/p/GV000314, [6] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-justicia-i-interior/nacionalitat/adquisicio-de-la-nacionalitat-andorrana, [7] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-justicia-i-interior/nacionalitat/la-nacionalitat-andorrana-d-origen, [8] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-justicia-i-interior/nacionalitat/normativa

### passport-lost-abroad (govern\.ad/.*passaport)

Si vous perdez votre passeport andorran à l'étranger, vous devez vous adresser à l'Ambassade d'Andorre présente sur place [6]. En l'absence de représentation diplomatique andorrane, vous devez contacter le Ministère des Affaires Étrangères [6].

Sources: [1] https://www.e-tramits.ad/tramits/passaports---duplicat-per-perdua-o-robatori/p/GV000455, [2] https://www.e-tramits.ad/tramits/primera-matriculacio-dun-vehicle-vehicle-nou-vehicle-ocasio-amb-placa-estrangera-vehicle-amb-placa-mt-i-vehicle-historic/p/GV000365, [3] https://www.e-tramits.ad/tramits/passaports---renovacio/p/GV000462, [4] https://www.e-tramits.ad/tramits/passaports---certificat-de-nacionalitat/p/GV000451, [5] https://www.e-tramits.ad/tramits/passaports---copia-compulsada/p/GV000452, [6] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-justicia-i-interior/passaports, [7] https://www.govern.ad/ca/tematiques/medi-ambient-i-sostenibilitat/pesca/llicencia-de-pesca, [8] https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-d-afers-exteriors/el-ministeri/afers-juridics-internacionals-i-recursos-humans/legalitzacio-de-documents-estrangers
