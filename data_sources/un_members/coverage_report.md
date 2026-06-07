# Couverture des États membres de l'ONU

Croise la liste canonique des 193 États membres de l'ONU avec les quatre sources qui alimentent la carte civilisationnelle. Régénéré par `civvec basis coverage-report`.

## Synthèse

- Total États ONU : **193**
- Couverture intégrale (géométrie + Hofstede + IW + taxonomie) : **59**
- Géométrie absente : **0**
- Hofstede manquant : **132**
- Inglehart-Welzel manquant : **103**
- Civilisation curatée manquante : **6**

## Provenance des coordonnées (cascade d'imputation)

- États avec `x_viz` ET `x_score` non-nuls dans `state_coordinates.json` : **193 / 193**

Provenance de `x_viz` :
- `imputed_pew` : 103
- `imputed_wvs_items` : 30
- `observed` : 60

Provenance de `x_score` :
- `imputed_governance` : 132
- `observed` : 52
- `observed_with_dim_imputation` : 9

Cf. `docs/16_imputation_cascade.md` pour la définition de chaque tier (`observed` > `imputed_pew` / `imputed_governance` > `centroid_prior`).

## États sans polygone (à charger depuis NE 50m ou source équivalente)

_(aucun)_

## États sans données Hofstede

- `AFG` — Afghanistan
- `AGO` — Angola
- `ALB` — Albanie
- `AND` — Andorre
- `ARE` — Émirats arabes unis
- `ARM` — Arménie
- `ATG` — Antigua-et-Barbuda
- `AUT` — Autriche
- `AZE` — Azerbaïdjan
- `BDI` — Burundi
- `BEL` — Belgique
- `BEN` — Bénin
- `BFA` — Burkina Faso
- `BHR` — Bahreïn
- `BHS` — Bahamas
- `BIH` — Bosnie-Herzégovine
- `BLZ` — Belize
- `BRB` — Barbade
- `BRN` — Brunéi Darussalam
- `BTN` — Bhoutan
- `BWA` — Botswana
- `CAF` — République centrafricaine
- `CHE` — Suisse
- `CIV` — Côte d'Ivoire
- `CMR` — Cameroun
- `COD` — République démocratique du Congo
- `COG` — Congo
- `COM` — Comores
- `CPV` — Cabo Verde
- `CRI` — Costa Rica
- `CUB` — Cuba
- `CYP` — Chypre
- `CZE` — Tchéquie
- `DJI` — Djibouti
- `DMA` — Dominique
- `DOM` — République dominicaine
- `DZA` — Algérie
- `ERI` — Érythrée
- `EST` — Estonie
- `FSM` — Micronésie
- `GAB` — Gabon
- `GEO` — Géorgie
- `GIN` — Guinée
- `GMB` — Gambie
- `GNB` — Guinée-Bissau
- `GNQ` — Guinée équatoriale
- `GRD` — Grenade
- `GUY` — Guyana
- `HND` — Honduras
- `HRV` — Croatie
- `HTI` — Haïti
- `HUN` — Hongrie
- `ISL` — Islande
- `ISR` — Israël
- `JAM` — Jamaïque
- `KAZ` — Kazakhstan
- `KGZ` — Kirghizistan
- `KHM` — Cambodge
- `KIR` — Kiribati
- `KNA` — Saint-Kitts-et-Nevis
- `KWT` — Koweït
- `LAO` — Laos
- `LBN` — Liban
- `LBR` — Libéria
- `LBY` — Libye
- `LCA` — Sainte-Lucie
- `LIE` — Liechtenstein
- `LKA` — Sri Lanka
- `LSO` — Lesotho
- `LTU` — Lituanie
- `LUX` — Luxembourg
- `LVA` — Lettonie
- `MCO` — Monaco
- `MDA` — Moldova
- `MDG` — Madagascar
- `MDV` — Maldives
- `MHL` — Îles Marshall
- `MKD` — Macédoine du Nord
- `MLI` — Mali
- `MLT` — Malte
- `MNE` — Monténégro
- `MOZ` — Mozambique
- `MRT` — Mauritanie
- `MUS` — Maurice
- `MWI` — Malawi
- `NAM` — Namibie
- `NER` — Niger
- `NIC` — Nicaragua
- `NPL` — Népal
- `NRU` — Nauru
- `OMN` — Oman
- `PAN` — Panama
- `PHL` — Philippines
- `PLW` — Palaos
- `PNG` — Papouasie-Nouvelle-Guinée
- `POL` — Pologne
- `PRK` — Corée du Nord
- `PRT` — Portugal
- `PRY` — Paraguay
- `QAT` — Qatar
- `RWA` — Rwanda
- `SDN` — Soudan
- `SEN` — Sénégal
- `SLB` — Îles Salomon
- `SLE` — Sierra Leone
- `SLV` — El Salvador
- `SMR` — Saint-Marin
- `SOM` — Somalie
- `SSD` — Soudan du Sud
- `STP` — Sao Tomé-et-Principe
- `SUR` — Suriname
- `SVK` — Slovaquie
- `SVN` — Slovénie
- `SWZ` — Eswatini
- `SYC` — Seychelles
- `SYR` — Syrie
- `TCD` — Tchad
- `TGO` — Togo
- `TJK` — Tadjikistan
- `TKM` — Turkménistan
- `TLS` — Timor-Leste
- `TON` — Tonga
- `TTO` — Trinité-et-Tobago
- `TUN` — Tunisie
- `TUV` — Tuvalu
- `TZA` — Tanzanie
- `UGA` — Ouganda
- `UZB` — Ouzbékistan
- `VCT` — Saint-Vincent-et-les Grenadines
- `VUT` — Vanuatu
- `WSM` — Samoa
- `YEM` — Yémen

## États sans coordonnées Inglehart-Welzel

- `AFG` — Afghanistan
- `AGO` — Angola
- `ALB` — Albanie
- `ARE` — Émirats arabes unis
- `ATG` — Antigua-et-Barbuda
- `AUT` — Autriche
- `BDI` — Burundi
- `BEL` — Belgique
- `BEN` — Bénin
- `BHR` — Bahreïn
- `BHS` — Bahamas
- `BIH` — Bosnie-Herzégovine
- `BLZ` — Belize
- `BRB` — Barbade
- `BRN` — Brunéi Darussalam
- `BTN` — Bhoutan
- `BWA` — Botswana
- `CAF` — République centrafricaine
- `CIV` — Côte d'Ivoire
- `CMR` — Cameroun
- `COD` — République démocratique du Congo
- `COG` — Congo
- `COM` — Comores
- `CPV` — Cabo Verde
- `CRI` — Costa Rica
- `CUB` — Cuba
- `DJI` — Djibouti
- `DMA` — Dominique
- `DOM` — République dominicaine
- `ERI` — Érythrée
- `FSM` — Micronésie
- `GAB` — Gabon
- `GIN` — Guinée
- `GMB` — Gambie
- `GNB` — Guinée-Bissau
- `GNQ` — Guinée équatoriale
- `GRD` — Grenade
- `GUY` — Guyana
- `HND` — Honduras
- `HRV` — Croatie
- `HTI` — Haïti
- `ISL` — Islande
- `ISR` — Israël
- `JAM` — Jamaïque
- `KHM` — Cambodge
- `KIR` — Kiribati
- `KNA` — Saint-Kitts-et-Nevis
- `LAO` — Laos
- `LBR` — Libéria
- `LCA` — Sainte-Lucie
- `LIE` — Liechtenstein
- `LKA` — Sri Lanka
- `LSO` — Lesotho
- `LTU` — Lituanie
- `LUX` — Luxembourg
- `LVA` — Lettonie
- `MCO` — Monaco
- `MDA` — Moldova
- `MDV` — Maldives
- `MHL` — Îles Marshall
- `MKD` — Macédoine du Nord
- `MLT` — Malte
- `MNE` — Monténégro
- `MOZ` — Mozambique
- `MRT` — Mauritanie
- `MUS` — Maurice
- `MWI` — Malawi
- `NAM` — Namibie
- `NER` — Niger
- `NPL` — Népal
- `NRU` — Nauru
- `OMN` — Oman
- `PAN` — Panama
- `PLW` — Palaos
- `PNG` — Papouasie-Nouvelle-Guinée
- `PRK` — Corée du Nord
- `PRT` — Portugal
- `PRY` — Paraguay
- `SAU` — Arabie saoudite
- `SDN` — Soudan
- `SEN` — Sénégal
- `SLB` — Îles Salomon
- `SLE` — Sierra Leone
- `SLV` — El Salvador
- `SMR` — Saint-Marin
- `SOM` — Somalie
- `SSD` — Soudan du Sud
- `STP` — Sao Tomé-et-Principe
- `SUR` — Suriname
- `SWZ` — Eswatini
- `SYC` — Seychelles
- `SYR` — Syrie
- `TCD` — Tchad
- `TGO` — Togo
- `TKM` — Turkménistan
- `TLS` — Timor-Leste
- `TON` — Tonga
- `TUV` — Tuvalu
- `TZA` — Tanzanie
- `UGA` — Ouganda
- `VCT` — Saint-Vincent-et-les Grenadines
- `VUT` — Vanuatu
- `WSM` — Samoa

## États sans rattachement curaté dans la taxonomie

- `BIH` — Bosnie-Herzégovine
- `CIV` — Côte d'Ivoire
- `ISR` — Israël
- `KOR` — Corée du Sud
- `LBN` — Liban
- `TCD` — Tchad

## Tableau détaillé

| ISO3 | Nom (fr) | Géo | Hofstede | IW | Civ. curatée | Sous-ensemble | x_viz prov. | x_score prov. |
|------|----------|-----|----------|----|--------------|---------------|-------------|---------------|
| `AFG` | Afghanistan | ✓ | missing | missing | islamic | — | imputed_pew | imputed_governance |
| `AGO` | Angola | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `ALB` | Albanie | ✓ | missing | missing | islamic | — | imputed_pew | imputed_governance |
| `AND` | Andorre | ✓ | missing | present | western | — | imputed_wvs_items | imputed_governance |
| `ARE` | Émirats arabes unis | ✓ | missing | missing | islamic | — | imputed_pew | imputed_governance |
| `ARG` | Argentine | ✓ | present | present | latin_american | southern_cone | observed | observed |
| `ARM` | Arménie | ✓ | missing | present | orthodox | — | imputed_wvs_items | imputed_governance |
| `ATG` | Antigua-et-Barbuda | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `AUS` | Australie | ✓ | present | present | western | english_speaking | observed | observed |
| `AUT` | Autriche | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `AZE` | Azerbaïdjan | ✓ | missing | present | islamic | — | imputed_wvs_items | imputed_governance |
| `BDI` | Burundi | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `BEL` | Belgique | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `BEN` | Bénin | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `BFA` | Burkina Faso | ✓ | missing | present | islamic | — | imputed_wvs_items | imputed_governance |
| `BGD` | Bangladesh | ✓ | present | present | islamic | south_asian_islamic | observed | observed |
| `BGR` | Bulgarie | ✓ | present | present | orthodox | balkan_orthodox | observed | observed |
| `BHR` | Bahreïn | ✓ | missing | missing | islamic | — | imputed_pew | imputed_governance |
| `BHS` | Bahamas | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `BIH` | Bosnie-Herzégovine | ✓ | missing | missing | — | — | imputed_pew | imputed_governance |
| `BLR` | Bélarus | ✓ | present | present | orthodox | slavic_orthodox | observed | observed |
| `BLZ` | Belize | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `BOL` | Bolivie | ✓ | imputed | present | indigenous | andean | observed | observed_with_dim_imputation |
| `BRA` | Brésil | ✓ | present | present | latin_american | brazil_caribbean | observed | observed |
| `BRB` | Barbade | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `BRN` | Brunéi Darussalam | ✓ | missing | missing | islamic | — | imputed_pew | imputed_governance |
| `BTN` | Bhoutan | ✓ | missing | missing | buddhist | mahayana | imputed_pew | imputed_governance |
| `BWA` | Botswana | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `CAF` | République centrafricaine | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `CAN` | Canada | ✓ | present | present | western | english_speaking | observed | observed |
| `CHE` | Suisse | ✓ | missing | present | western | — | imputed_wvs_items | imputed_governance |
| `CHL` | Chili | ✓ | present | present | latin_american | southern_cone | observed | observed |
| `CHN` | Chine | ✓ | present | present | sinic | mainland_sinic | observed | observed |
| `CIV` | Côte d'Ivoire | ✓ | missing | missing | — | — | imputed_pew | imputed_governance |
| `CMR` | Cameroun | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `COD` | République démocratique du Congo | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `COG` | Congo | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `COL` | Colombie | ✓ | present | present | latin_american | andean | observed | observed |
| `COM` | Comores | ✓ | missing | missing | islamic | — | imputed_pew | imputed_governance |
| `CPV` | Cabo Verde | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `CRI` | Costa Rica | ✓ | missing | missing | latin_american | — | imputed_pew | imputed_governance |
| `CUB` | Cuba | ✓ | missing | missing | latin_american | — | imputed_pew | imputed_governance |
| `CYP` | Chypre | ✓ | missing | present | orthodox | — | imputed_wvs_items | imputed_governance |
| `CZE` | Tchéquie | ✓ | missing | present | western | — | imputed_wvs_items | imputed_governance |
| `DEU` | Allemagne | ✓ | present | present | western | protestant_europe | observed | observed |
| `DJI` | Djibouti | ✓ | missing | missing | islamic | — | imputed_pew | imputed_governance |
| `DMA` | Dominique | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `DNK` | Danemark | ✓ | present | present | western | protestant_europe | observed | observed |
| `DOM` | République dominicaine | ✓ | missing | missing | latin_american | — | imputed_pew | imputed_governance |
| `DZA` | Algérie | ✓ | missing | present | islamic | — | imputed_wvs_items | imputed_governance |
| `ECU` | Équateur | ✓ | imputed | present | indigenous | andean | observed | observed_with_dim_imputation |
| `EGY` | Égypte | ✓ | present | present | islamic | arab_islamic | observed | observed |
| `ERI` | Érythrée | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `ESP` | Espagne | ✓ | present | present | western | catholic_europe | observed | observed |
| `EST` | Estonie | ✓ | missing | present | western | — | imputed_wvs_items | imputed_governance |
| `ETH` | Éthiopie | ✓ | imputed | present | african | east_africa | observed | observed_with_dim_imputation |
| `FIN` | Finlande | ✓ | present | present | western | protestant_europe | observed | observed |
| `FJI` | Fidji | ✓ | imputed | present | oceanian | melanesia | observed | observed_with_dim_imputation |
| `FRA` | France | ✓ | present | present | western | catholic_europe | observed | observed |
| `FSM` | Micronésie | ✓ | missing | missing | oceanian | — | imputed_pew | imputed_governance |
| `GAB` | Gabon | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `GBR` | Royaume-Uni | ✓ | present | present | western | english_speaking | observed | observed |
| `GEO` | Géorgie | ✓ | missing | present | orthodox | — | imputed_wvs_items | imputed_governance |
| `GHA` | Ghana | ✓ | present | present | african | west_africa | observed | observed |
| `GIN` | Guinée | ✓ | missing | missing | islamic | — | imputed_pew | imputed_governance |
| `GMB` | Gambie | ✓ | missing | missing | islamic | — | imputed_pew | imputed_governance |
| `GNB` | Guinée-Bissau | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `GNQ` | Guinée équatoriale | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `GRC` | Grèce | ✓ | present | present | orthodox | balkan_orthodox | observed | observed |
| `GRD` | Grenade | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `GTM` | Guatemala | ✓ | imputed | present | latin_american | mexican_central_american | observed | observed_with_dim_imputation |
| `GUY` | Guyana | ✓ | missing | missing | latin_american | — | imputed_pew | imputed_governance |
| `HND` | Honduras | ✓ | missing | missing | latin_american | — | imputed_pew | imputed_governance |
| `HRV` | Croatie | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `HTI` | Haïti | ✓ | missing | missing | latin_american | — | imputed_pew | imputed_governance |
| `HUN` | Hongrie | ✓ | missing | present | western | — | imputed_wvs_items | imputed_governance |
| `IDN` | Indonésie | ✓ | present | present | islamic | southeast_asian_islamic | observed | observed |
| `IND` | Inde | ✓ | present | present | hindic | indian_subcontinent_hindu | observed | observed |
| `IRL` | Irlande | ✓ | present | present | western | english_speaking | observed | observed |
| `IRN` | Iran | ✓ | present | present | islamic | turco_iranian | observed | observed |
| `IRQ` | Iraq | ✓ | present | present | islamic | arab_islamic | observed | observed |
| `ISL` | Islande | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `ISR` | Israël | ✓ | missing | missing | — | — | imputed_pew | imputed_governance |
| `ITA` | Italie | ✓ | present | present | western | catholic_europe | observed | observed |
| `JAM` | Jamaïque | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `JOR` | Jordanie | ✓ | present | present | islamic | arab_islamic | observed | observed |
| `JPN` | Japon | ✓ | present | present | japanese | — | observed | observed |
| `KAZ` | Kazakhstan | ✓ | missing | present | islamic | — | imputed_wvs_items | imputed_governance |
| `KEN` | Kenya | ✓ | imputed | present | african | east_africa | observed | observed_with_dim_imputation |
| `KGZ` | Kirghizistan | ✓ | missing | present | islamic | — | imputed_wvs_items | imputed_governance |
| `KHM` | Cambodge | ✓ | missing | missing | buddhist | theravada | imputed_pew | imputed_governance |
| `KIR` | Kiribati | ✓ | missing | missing | oceanian | — | imputed_pew | imputed_governance |
| `KNA` | Saint-Kitts-et-Nevis | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `KOR` | Corée du Sud | ✓ | present | present | — | mahayana | observed | observed |
| `KWT` | Koweït | ✓ | missing | present | islamic | — | imputed_wvs_items | imputed_governance |
| `LAO` | Laos | ✓ | missing | missing | buddhist | theravada | imputed_pew | imputed_governance |
| `LBN` | Liban | ✓ | missing | present | — | — | imputed_wvs_items | imputed_governance |
| `LBR` | Libéria | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `LBY` | Libye | ✓ | missing | present | islamic | — | imputed_wvs_items | imputed_governance |
| `LCA` | Sainte-Lucie | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `LIE` | Liechtenstein | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `LKA` | Sri Lanka | ✓ | missing | missing | hindic | indian_subcontinent_hindu | imputed_pew | imputed_governance |
| `LSO` | Lesotho | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `LTU` | Lituanie | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `LUX` | Luxembourg | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `LVA` | Lettonie | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `MAR` | Maroc | ✓ | present | present | islamic | arab_islamic | observed | observed |
| `MCO` | Monaco | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `MDA` | Moldova | ✓ | missing | missing | orthodox | — | imputed_pew | imputed_governance |
| `MDG` | Madagascar | ✓ | missing | present | african | — | imputed_wvs_items | imputed_governance |
| `MDV` | Maldives | ✓ | missing | missing | islamic | — | imputed_pew | imputed_governance |
| `MEX` | Mexique | ✓ | present | present | latin_american | mexican_central_american | observed | observed |
| `MHL` | Îles Marshall | ✓ | missing | missing | oceanian | — | imputed_pew | imputed_governance |
| `MKD` | Macédoine du Nord | ✓ | missing | missing | orthodox | — | imputed_pew | imputed_governance |
| `MLI` | Mali | ✓ | missing | present | islamic | — | imputed_wvs_items | imputed_governance |
| `MLT` | Malte | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `MMR` | Myanmar | ✓ | imputed | present | buddhist | theravada | observed | observed_with_dim_imputation |
| `MNE` | Monténégro | ✓ | missing | missing | orthodox | — | imputed_pew | imputed_governance |
| `MNG` | Mongolie | ✓ | present | present | buddhist | mahayana | observed | observed |
| `MOZ` | Mozambique | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `MRT` | Mauritanie | ✓ | missing | missing | islamic | — | imputed_pew | imputed_governance |
| `MUS` | Maurice | ✓ | missing | missing | hindic | — | imputed_pew | imputed_governance |
| `MWI` | Malawi | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `MYS` | Malaisie | ✓ | present | present | islamic | southeast_asian_islamic | observed | observed |
| `NAM` | Namibie | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `NER` | Niger | ✓ | missing | missing | islamic | — | imputed_pew | imputed_governance |
| `NGA` | Nigéria | ✓ | present | present | african | west_africa | observed | observed |
| `NIC` | Nicaragua | ✓ | missing | present | latin_american | — | imputed_wvs_items | imputed_governance |
| `NLD` | Pays-Bas | ✓ | present | present | western | protestant_europe | observed | observed |
| `NOR` | Norvège | ✓ | present | present | western | protestant_europe | observed | observed |
| `NPL` | Népal | ✓ | missing | missing | hindic | indian_subcontinent_hindu | imputed_pew | imputed_governance |
| `NRU` | Nauru | ✓ | missing | missing | oceanian | — | imputed_pew | imputed_governance |
| `NZL` | Nouvelle-Zélande | ✓ | present | present | oceanian | english_speaking | observed | observed |
| `OMN` | Oman | ✓ | missing | missing | islamic | — | imputed_pew | imputed_governance |
| `PAK` | Pakistan | ✓ | present | present | islamic | south_asian_islamic | observed | observed |
| `PAN` | Panama | ✓ | missing | missing | latin_american | — | imputed_pew | imputed_governance |
| `PER` | Pérou | ✓ | present | present | latin_american | andean | observed | observed |
| `PHL` | Philippines | ✓ | missing | present | latin_american | — | imputed_wvs_items | imputed_governance |
| `PLW` | Palaos | ✓ | missing | missing | oceanian | — | imputed_pew | imputed_governance |
| `PNG` | Papouasie-Nouvelle-Guinée | ✓ | missing | missing | oceanian | — | imputed_pew | imputed_governance |
| `POL` | Pologne | ✓ | missing | present | western | — | imputed_wvs_items | imputed_governance |
| `PRK` | Corée du Nord | ✓ | missing | missing | sinic | — | imputed_pew | imputed_governance |
| `PRT` | Portugal | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `PRY` | Paraguay | ✓ | missing | missing | latin_american | — | imputed_pew | imputed_governance |
| `QAT` | Qatar | ✓ | missing | present | islamic | — | imputed_wvs_items | imputed_governance |
| `ROU` | Roumanie | ✓ | present | present | orthodox | balkan_orthodox | observed | observed |
| `RUS` | Russie | ✓ | present | present | orthodox | slavic_orthodox | observed | observed |
| `RWA` | Rwanda | ✓ | missing | present | african | — | imputed_wvs_items | imputed_governance |
| `SAU` | Arabie saoudite | ✓ | present | missing | islamic | arab_islamic | imputed_pew | observed |
| `SDN` | Soudan | ✓ | missing | missing | islamic | — | imputed_pew | imputed_governance |
| `SEN` | Sénégal | ✓ | missing | missing | islamic | — | imputed_pew | imputed_governance |
| `SGP` | Singapour | ✓ | present | present | sinic | insular_sinic | observed | observed |
| `SLB` | Îles Salomon | ✓ | missing | missing | oceanian | — | imputed_pew | imputed_governance |
| `SLE` | Sierra Leone | ✓ | missing | missing | islamic | — | imputed_pew | imputed_governance |
| `SLV` | El Salvador | ✓ | missing | missing | latin_american | — | imputed_pew | imputed_governance |
| `SMR` | Saint-Marin | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `SOM` | Somalie | ✓ | missing | missing | islamic | — | imputed_pew | imputed_governance |
| `SRB` | Serbie | ✓ | present | present | orthodox | slavic_orthodox | observed | observed |
| `SSD` | Soudan du Sud | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `STP` | Sao Tomé-et-Principe | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `SUR` | Suriname | ✓ | missing | missing | latin_american | — | imputed_pew | imputed_governance |
| `SVK` | Slovaquie | ✓ | missing | present | western | — | imputed_wvs_items | imputed_governance |
| `SVN` | Slovénie | ✓ | missing | present | western | — | imputed_wvs_items | imputed_governance |
| `SWE` | Suède | ✓ | present | present | western | protestant_europe | observed | observed |
| `SWZ` | Eswatini | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `SYC` | Seychelles | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `SYR` | Syrie | ✓ | missing | missing | islamic | — | imputed_pew | imputed_governance |
| `TCD` | Tchad | ✓ | missing | missing | — | — | imputed_pew | imputed_governance |
| `TGO` | Togo | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `THA` | Thaïlande | ✓ | present | present | buddhist | theravada | observed | observed |
| `TJK` | Tadjikistan | ✓ | missing | present | islamic | — | imputed_wvs_items | imputed_governance |
| `TKM` | Turkménistan | ✓ | missing | missing | islamic | — | imputed_pew | imputed_governance |
| `TLS` | Timor-Leste | ✓ | missing | missing | latin_american | — | imputed_pew | imputed_governance |
| `TON` | Tonga | ✓ | missing | missing | oceanian | — | imputed_pew | imputed_governance |
| `TTO` | Trinité-et-Tobago | ✓ | missing | present | western | — | imputed_wvs_items | imputed_governance |
| `TUN` | Tunisie | ✓ | missing | present | islamic | — | imputed_wvs_items | imputed_governance |
| `TUR` | Turquie | ✓ | present | present | islamic | turco_iranian | observed | observed |
| `TUV` | Tuvalu | ✓ | missing | missing | oceanian | — | imputed_pew | imputed_governance |
| `TZA` | Tanzanie | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `UGA` | Ouganda | ✓ | missing | missing | african | — | imputed_pew | imputed_governance |
| `UKR` | Ukraine | ✓ | present | present | orthodox | slavic_orthodox | observed | observed |
| `URY` | Uruguay | ✓ | present | present | latin_american | southern_cone | observed | observed |
| `USA` | États-Unis | ✓ | present | present | western | english_speaking | observed | observed |
| `UZB` | Ouzbékistan | ✓ | missing | present | islamic | — | imputed_wvs_items | imputed_governance |
| `VCT` | Saint-Vincent-et-les Grenadines | ✓ | missing | missing | western | — | imputed_pew | imputed_governance |
| `VEN` | Venezuela | ✓ | present | present | latin_american | brazil_caribbean | observed | observed |
| `VNM` | Viet Nam | ✓ | present | present | sinic | mainland_sinic | observed | observed |
| `VUT` | Vanuatu | ✓ | missing | missing | oceanian | — | imputed_pew | imputed_governance |
| `WSM` | Samoa | ✓ | missing | missing | oceanian | — | imputed_pew | imputed_governance |
| `YEM` | Yémen | ✓ | missing | present | islamic | — | imputed_wvs_items | imputed_governance |
| `ZAF` | Afrique du Sud | ✓ | present | present | african | southern_africa | observed | observed |
| `ZMB` | Zambie | ✓ | imputed | present | african | southern_africa | observed | observed_with_dim_imputation |
| `ZWE` | Zimbabwe | ✓ | imputed | present | african | southern_africa | observed | observed_with_dim_imputation |
