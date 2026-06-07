# États publiés

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

Liste des **193 États** dont les coordonnées `x_viz` et `x_score` ont
été calculées dans la base vectorielle. Pour la méthodologie,
voir [`08_civilizational_basis.md`](../methodology/08_civilizational_basis.md) et
[`16_imputation_cascade.md`](../methodology/16_imputation_cascade.md) pour la
cascade d'imputation qui garantit la couverture des 193 États ONU.

La colonne **Provenance** indique le tier de la cascade ayant produit chaque
coordonnée. Tiers (par qualité décroissante) :

- `observed` — sondage canonique direct (WVS wave 7 / Hofstede 2010)
- `observed_with_dim_imputation` — Hofstede présent mais dimensions partielles
- `imputed_wvs_items` — WVS waves 5-6 prédites par ridge sur les 10 items IW
- `imputed_pew` — régression Pew + UNDP + UN voting + V-Dem → IW
- `imputed_governance` — régression WGI + FSI + UNDP + UN voting + V-Dem → Hofstede
- `centroid_prior` — barycentre civilisationnel (cas-limite ; 0 État actuellement)

| État | ISO3 | `x_viz` (TS, SE) | Prov. `x_viz` | Prov. `x_score` | Géométrie |
|---|---|---|---|---|---|

| [Afghanistan](AFG.md) | `AFG` | `[-1.95, -1.18]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Angola](AGO.md) | `AGO` | `[-1.27, -0.49]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Albanie](ALB.md) | `ALB` | `[0.08, 0.12]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Andorre](AND.md) | `AND` | `[0.80, 1.65]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Émirats arabes unis](ARE.md) | `ARE` | `[-0.37, -0.17]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Argentine](ARG.md) | `ARG` | `[-0.60, 0.65]` | `observed` | `observed` | ✓ |

| [Arménie](ARM.md) | `ARM` | `[-1.21, -0.91]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Antigua-et-Barbuda](ATG.md) | `ATG` | `[-0.48, 0.13]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Australie](AUS.md) | `AUS` | `[0.50, 1.65]` | `observed` | `observed` | ✓ |

| [Autriche](AUT.md) | `AUT` | `[0.46, 0.97]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Azerbaïdjan](AZE.md) | `AZE` | `[-0.75, -0.63]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Burundi](BDI.md) | `BDI` | `[-1.57, -0.79]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Belgique](BEL.md) | `BEL` | `[0.82, 1.08]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Bénin](BEN.md) | `BEN` | `[-1.29, -0.46]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Burkina Faso](BFA.md) | `BFA` | `[-1.21, -0.78]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Bangladesh](BGD.md) | `BGD` | `[-1.05, -0.65]` | `observed` | `observed` | ✓ |

| [Bulgarie](BGR.md) | `BGR` | `[-0.25, -0.95]` | `observed` | `observed` | ✓ |

| [Bahreïn](BHR.md) | `BHR` | `[-0.68, -0.36]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Bahamas](BHS.md) | `BHS` | `[-0.80, 0.08]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Bosnie-Herzégovine](BIH.md) | `BIH` | `[-0.29, -0.10]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Bélarus](BLR.md) | `BLR` | `[0.45, -1.20]` | `observed` | `observed` | ✓ |

| [Belize](BLZ.md) | `BLZ` | `[-0.82, -0.03]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Bolivie](BOL.md) | `BOL` | `[-1.10, 0.05]` | `observed` | `observed_with_dim_imputation` | ✓ |

| [Brésil](BRA.md) | `BRA` | `[-1.05, 0.85]` | `observed` | `observed` | ✓ |

| [Barbade](BRB.md) | `BRB` | `[-0.40, 0.59]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Brunéi Darussalam](BRN.md) | `BRN` | `[-0.57, 0.10]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Bhoutan](BTN.md) | `BTN` | `[-0.47, -0.35]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Botswana](BWA.md) | `BWA` | `[-0.88, 0.24]` | `imputed_pew` | `imputed_governance` | ✓ |

| [République centrafricaine](CAF.md) | `CAF` | `[-1.34, -0.83]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Canada](CAN.md) | `CAN` | `[0.55, 1.70]` | `observed` | `observed` | ✓ |

| [Suisse](CHE.md) | `CHE` | `[0.53, 1.99]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Chili](CHL.md) | `CHL` | `[-0.20, 0.85]` | `observed` | `observed` | ✓ |

| [Chine](CHN.md) | `CHN` | `[0.75, -0.95]` | `observed` | `observed` | ✓ |

| [Côte d'Ivoire](CIV.md) | `CIV` | `[-1.19, -0.39]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Cameroun](CMR.md) | `CMR` | `[-1.14, -0.49]` | `imputed_pew` | `imputed_governance` | ✓ |

| [République démocratique du Congo](COD.md) | `COD` | `[-1.68, -0.83]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Congo](COG.md) | `COG` | `[-1.26, -0.23]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Colombie](COL.md) | `COL` | `[-0.90, 1.10]` | `observed` | `observed` | ✓ |

| [Comores](COM.md) | `COM` | `[-1.49, -0.84]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Cabo Verde](CPV.md) | `CPV` | `[-0.64, 0.25]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Costa Rica](CRI.md) | `CRI` | `[-0.36, 0.71]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Cuba](CUB.md) | `CUB` | `[-0.89, -0.60]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Chypre](CYP.md) | `CYP` | `[-0.46, 0.28]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Tchéquie](CZE.md) | `CZE` | `[1.17, 0.77]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Allemagne](DEU.md) | `DEU` | `[1.40, 1.15]` | `observed` | `observed` | ✓ |

| [Djibouti](DJI.md) | `DJI` | `[-1.30, -0.80]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Dominique](DMA.md) | `DMA` | `[-0.44, 0.05]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Danemark](DNK.md) | `DNK` | `[1.50, 2.20]` | `observed` | `observed` | ✓ |

| [République dominicaine](DOM.md) | `DOM` | `[-0.59, 0.21]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Algérie](DZA.md) | `DZA` | `[-1.14, -0.52]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Équateur](ECU.md) | `ECU` | `[-1.05, 0.30]` | `observed` | `observed_with_dim_imputation` | ✓ |

| [Égypte](EGY.md) | `EGY` | `[-1.55, -1.20]` | `observed` | `observed` | ✓ |

| [Érythrée](ERI.md) | `ERI` | `[-1.67, -1.07]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Espagne](ESP.md) | `ESP` | `[0.65, 0.95]` | `observed` | `observed` | ✓ |

| [Estonie](EST.md) | `EST` | `[1.13, -0.34]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Éthiopie](ETH.md) | `ETH` | `[-1.10, -0.65]` | `observed` | `observed_with_dim_imputation` | ✓ |

| [Finlande](FIN.md) | `FIN` | `[0.90, 1.50]` | `observed` | `observed` | ✓ |

| [Fidji](FJI.md) | `FJI` | `[-0.80, 0.40]` | `observed` | `observed_with_dim_imputation` | ✓ |

| [France](FRA.md) | `FRA` | `[1.20, 1.45]` | `observed` | `observed` | ✓ |

| [Micronésie](FSM.md) | `FSM` | `[-0.69, -0.15]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Gabon](GAB.md) | `GAB` | `[-1.12, -0.35]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Royaume-Uni](GBR.md) | `GBR` | `[0.85, 1.50]` | `observed` | `observed` | ✓ |

| [Géorgie](GEO.md) | `GEO` | `[-1.25, -1.00]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Ghana](GHA.md) | `GHA` | `[-1.45, 0.20]` | `observed` | `observed` | ✓ |

| [Guinée](GIN.md) | `GIN` | `[-1.36, -0.49]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Gambie](GMB.md) | `GMB` | `[-1.34, -0.37]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Guinée-Bissau](GNB.md) | `GNB` | `[-1.34, -0.52]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Guinée équatoriale](GNQ.md) | `GNQ` | `[-1.06, -0.23]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Grèce](GRC.md) | `GRC` | `[-0.10, 0.05]` | `observed` | `observed` | ✓ |

| [Grenade](GRD.md) | `GRD` | `[-0.85, 0.02]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Guatemala](GTM.md) | `GTM` | `[-1.25, 0.30]` | `observed` | `observed_with_dim_imputation` | ✓ |

| [Guyana](GUY.md) | `GUY` | `[-0.75, 0.04]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Honduras](HND.md) | `HND` | `[-1.05, -0.19]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Croatie](HRV.md) | `HRV` | `[0.03, 0.44]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Haïti](HTI.md) | `HTI` | `[-1.56, -0.55]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Hongrie](HUN.md) | `HUN` | `[0.43, 0.05]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Indonésie](IDN.md) | `IDN` | `[-1.10, -0.30]` | `observed` | `observed` | ✓ |

| [Inde](IND.md) | `IND` | `[-0.60, -0.20]` | `observed` | `observed` | ✓ |

| [Irlande](IRL.md) | `IRL` | `[0.10, 1.10]` | `observed` | `observed` | ✓ |

| [Iran](IRN.md) | `IRN` | `[-1.10, -0.40]` | `observed` | `observed` | ✓ |

| [Iraq](IRQ.md) | `IRQ` | `[-1.45, -1.15]` | `observed` | `observed` | ✓ |

| [Islande](ISL.md) | `ISL` | `[0.46, 0.99]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Israël](ISR.md) | `ISR` | `[1.17, 0.82]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Italie](ITA.md) | `ITA` | `[0.40, 0.85]` | `observed` | `observed` | ✓ |

| [Jamaïque](JAM.md) | `JAM` | `[-0.48, 0.39]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Jordanie](JOR.md) | `JOR` | `[-1.30, -1.05]` | `observed` | `observed` | ✓ |

| [Japon](JPN.md) | `JPN` | `[1.95, 0.45]` | `observed` | `observed` | ✓ |

| [Kazakhstan](KAZ.md) | `KAZ` | `[-0.11, -0.54]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Kenya](KEN.md) | `KEN` | `[-1.55, -0.65]` | `observed` | `observed_with_dim_imputation` | ✓ |

| [Kirghizistan](KGZ.md) | `KGZ` | `[-1.01, -0.55]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Cambodge](KHM.md) | `KHM` | `[-0.66, -0.61]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Kiribati](KIR.md) | `KIR` | `[-1.20, -0.29]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Saint-Kitts-et-Nevis](KNA.md) | `KNA` | `[-0.53, 0.18]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Corée du Sud](KOR.md) | `KOR` | `[1.65, 0.55]` | `observed` | `observed` | ✓ |

| [Koweït](KWT.md) | `KWT` | `[-1.04, 0.06]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Laos](LAO.md) | `LAO` | `[-0.60, -0.46]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Liban](LBN.md) | `LBN` | `[-1.07, -0.45]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Libéria](LBR.md) | `LBR` | `[-1.59, -0.55]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Libye](LBY.md) | `LBY` | `[-1.59, -0.79]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Sainte-Lucie](LCA.md) | `LCA` | `[-0.92, 0.01]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Liechtenstein](LIE.md) | `LIE` | `[0.18, 0.56]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Sri Lanka](LKA.md) | `LKA` | `[-0.50, 0.07]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Lesotho](LSO.md) | `LSO` | `[-1.40, -0.17]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Lituanie](LTU.md) | `LTU` | `[0.16, 0.70]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Luxembourg](LUX.md) | `LUX` | `[0.61, 1.00]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Lettonie](LVA.md) | `LVA` | `[0.36, 0.86]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Maroc](MAR.md) | `MAR` | `[-1.15, -0.95]` | `observed` | `observed` | ✓ |

| [Monaco](MCO.md) | `MCO` | `[-0.06, 0.34]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Moldova](MDA.md) | `MDA` | `[-0.36, 0.20]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Madagascar](MDG.md) | `MDG` | `[-1.35, -0.62]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Maldives](MDV.md) | `MDV` | `[-1.26, -0.77]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Mexique](MEX.md) | `MEX` | `[-0.80, 0.70]` | `observed` | `observed` | ✓ |

| [Îles Marshall](MHL.md) | `MHL` | `[-0.36, 0.02]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Macédoine du Nord](MKD.md) | `MKD` | `[-0.15, 0.13]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Mali](MLI.md) | `MLI` | `[-1.25, -0.27]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Malte](MLT.md) | `MLT` | `[-0.03, 0.64]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Myanmar](MMR.md) | `MMR` | `[-0.50, -0.05]` | `observed` | `observed_with_dim_imputation` | ✓ |

| [Monténégro](MNE.md) | `MNE` | `[-0.17, 0.22]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Mongolie](MNG.md) | `MNG` | `[-0.20, -0.65]` | `observed` | `observed` | ✓ |

| [Mozambique](MOZ.md) | `MOZ` | `[-1.26, -0.59]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Mauritanie](MRT.md) | `MRT` | `[-1.61, -1.06]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Maurice](MUS.md) | `MUS` | `[-0.62, 0.39]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Malawi](MWI.md) | `MWI` | `[-1.49, -0.34]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Malaisie](MYS.md) | `MYS` | `[-0.95, -0.20]` | `observed` | `observed` | ✓ |

| [Namibie](NAM.md) | `NAM` | `[-0.87, 0.18]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Niger](NER.md) | `NER` | `[-1.62, -0.86]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Nigéria](NGA.md) | `NGA` | `[-1.45, -0.90]` | `observed` | `observed` | ✓ |

| [Nicaragua](NIC.md) | `NIC` | `[-1.28, 0.11]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Pays-Bas](NLD.md) | `NLD` | `[1.45, 1.65]` | `observed` | `observed` | ✓ |

| [Norvège](NOR.md) | `NOR` | `[1.55, 2.30]` | `observed` | `observed` | ✓ |

| [Népal](NPL.md) | `NPL` | `[-0.99, -0.20]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Nauru](NRU.md) | `NRU` | `[-0.26, 0.10]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Nouvelle-Zélande](NZL.md) | `NZL` | `[0.65, 1.85]` | `observed` | `observed` | ✓ |

| [Oman](OMN.md) | `OMN` | `[-0.91, -0.25]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Pakistan](PAK.md) | `PAK` | `[-1.30, -0.95]` | `observed` | `observed` | ✓ |

| [Panama](PAN.md) | `PAN` | `[-0.57, 0.52]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Pérou](PER.md) | `PER` | `[-0.85, 0.40]` | `observed` | `observed` | ✓ |

| [Philippines](PHL.md) | `PHL` | `[-1.34, 0.69]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Palaos](PLW.md) | `PLW` | `[-0.24, 0.11]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Papouasie-Nouvelle-Guinée](PNG.md) | `PNG` | `[-1.33, -0.10]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Pologne](POL.md) | `POL` | `[-0.48, 0.08]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Corée du Nord](PRK.md) | `PRK` | `[0.38, -0.34]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Portugal](PRT.md) | `PRT` | `[0.10, 0.71]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Paraguay](PRY.md) | `PRY` | `[-0.49, 0.32]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Qatar](QAT.md) | `QAT` | `[-1.62, -0.50]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Roumanie](ROU.md) | `ROU` | `[-0.35, -0.40]` | `observed` | `observed` | ✓ |

| [Russie](RUS.md) | `RUS` | `[0.05, -1.05]` | `observed` | `observed` | ✓ |

| [Rwanda](RWA.md) | `RWA` | `[-0.56, -0.43]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Arabie saoudite](SAU.md) | `SAU` | `[-0.73, -0.36]` | `imputed_pew` | `observed` | ✓ |

| [Soudan](SDN.md) | `SDN` | `[-1.71, -0.92]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Sénégal](SEN.md) | `SEN` | `[-1.23, -0.42]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Singapour](SGP.md) | `SGP` | `[0.30, -0.40]` | `observed` | `observed` | ✓ |

| [Îles Salomon](SLB.md) | `SLB` | `[-1.40, -0.09]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Sierra Leone](SLE.md) | `SLE` | `[-1.42, -0.63]` | `imputed_pew` | `imputed_governance` | ✓ |

| [El Salvador](SLV.md) | `SLV` | `[-0.74, -0.06]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Saint-Marin](SMR.md) | `SMR` | `[0.04, 0.39]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Somalie](SOM.md) | `SOM` | `[-1.95, -1.21]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Serbie](SRB.md) | `SRB` | `[0.15, -0.65]` | `observed` | `observed` | ✓ |

| [Soudan du Sud](SSD.md) | `SSD` | `[-0.82, -0.70]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Sao Tomé-et-Principe](STP.md) | `STP` | `[-0.94, 0.05]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Suriname](SUR.md) | `SUR` | `[-0.62, 0.34]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Slovaquie](SVK.md) | `SVK` | `[0.27, 0.09]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Slovénie](SVN.md) | `SVN` | `[0.92, 0.67]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Suède](SWE.md) | `SWE` | `[1.78, 2.35]` | `observed` | `observed` | ✓ |

| [Eswatini](SWZ.md) | `SWZ` | `[-1.18, -0.05]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Seychelles](SYC.md) | `SYC` | `[-0.65, 0.58]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Syrie](SYR.md) | `SYR` | `[-1.67, -1.01]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Tchad](TCD.md) | `TCD` | `[-1.61, -0.87]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Togo](TGO.md) | `TGO` | `[-1.15, -0.47]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Thaïlande](THA.md) | `THA` | `[-0.20, 0.20]` | `observed` | `observed` | ✓ |

| [Tadjikistan](TJK.md) | `TJK` | `[-1.07, 0.31]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Turkménistan](TKM.md) | `TKM` | `[-1.18, -0.85]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Timor-Leste](TLS.md) | `TLS` | `[-1.26, -0.03]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Tonga](TON.md) | `TON` | `[-0.98, 0.01]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Trinité-et-Tobago](TTO.md) | `TTO` | `[-1.40, -0.46]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Tunisie](TUN.md) | `TUN` | `[-1.00, -1.18]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Turquie](TUR.md) | `TUR` | `[-0.85, -0.65]` | `observed` | `observed` | ✓ |

| [Tuvalu](TUV.md) | `TUV` | `[-0.60, -0.13]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Tanzanie](TZA.md) | `TZA` | `[-1.30, -0.58]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Ouganda](UGA.md) | `UGA` | `[-1.52, -0.54]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Ukraine](UKR.md) | `UKR` | `[0.20, -0.85]` | `observed` | `observed` | ✓ |

| [Uruguay](URY.md) | `URY` | `[-0.05, 1.10]` | `observed` | `observed` | ✓ |

| [États-Unis](USA.md) | `USA` | `[-0.10, 1.55]` | `observed` | `observed` | ✓ |

| [Ouzbékistan](UZB.md) | `UZB` | `[-0.80, 0.39]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Saint-Vincent-et-les Grenadines](VCT.md) | `VCT` | `[-0.73, 0.08]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Venezuela](VEN.md) | `VEN` | `[-1.10, 0.70]` | `observed` | `observed` | ✓ |

| [Viet Nam](VNM.md) | `VNM` | `[0.05, -0.20]` | `observed` | `observed` | ✓ |

| [Vanuatu](VUT.md) | `VUT` | `[-1.23, 0.10]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Samoa](WSM.md) | `WSM` | `[-1.04, -0.15]` | `imputed_pew` | `imputed_governance` | ✓ |

| [Yémen](YEM.md) | `YEM` | `[-1.48, -0.77]` | `imputed_wvs_items` | `imputed_governance` | ✓ |

| [Afrique du Sud](ZAF.md) | `ZAF` | `[-0.60, 0.00]` | `observed` | `observed` | ✓ |

| [Zambie](ZMB.md) | `ZMB` | `[-1.20, -0.30]` | `observed` | `observed_with_dim_imputation` | ✓ |

| [Zimbabwe](ZWE.md) | `ZWE` | `[-1.15, -0.40]` | `observed` | `observed_with_dim_imputation` | ✓ |


## Téléchargements en bloc

- [Coordonnées États (`state_coordinates.json`)](../assets/data/state_coordinates.json)
- [Centroïdes civilisationnels (`civilization_centroids.json`)](../assets/data/civilization_centroids.json)
- [Seconds moments (`state_moments.json`)](../assets/data/state_moments.json)
- [Géométries ADM0 110m (`global_state_baseline.geojson`)](../assets/data/global_state_baseline.geojson)

---

[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Second moment M(s)](../moments/index.md) ·
[Distances](../distances/index.md)
