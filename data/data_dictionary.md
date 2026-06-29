# Data Dictionary for the Tax-Feature XML Template

## Scope

This document defines the tags used in `TaxFeatures_Template.xml`. The template organises the tax features examined in the study across corporate income tax, personal income tax, value-added tax, excise duties, and property and wealth taxes.

## Metadata

| Tag               | Definition                                                                       |
| ----------------- | -------------------------------------------------------------------------------- |
| `A_Country`       | Jurisdiction covered by the tax profile.                                         |
| `B_Currency`      | Currency applicable in the country.                                              |
| `C_RECs`          | Regional Economic Community memberships relevant to the country or jurisdiction. |
| `D_report_source` | Referenced sources.                                                              |

## 1. Corporate Income Tax

  ### 1.1. Tax Liability
  | Tag            | Definition                                                                |
  | -------------- | ------------------------------------------------------------------------- |
  | `aaCT_1TLRes`  | Criteria used to determine corporate tax residence.                       |
  | `abCT_2TLBase` | Territorial, worldwide, or mixed basis of corporate income taxation.      |
  | `acCT_3TLGrTre`| Availability of group treatment for corporate income tax purposes.        |
  
  ### 1.2. Taxable Income
  | Tag            | Definition                                                                |
  | -------------- | ------------------------------------------------------------------------- |
  | `adCT_4TILos`    | Period for carrying tax losses forward.                                   |
  | `aeCT_5TIInc`    | Corporate income tax incentives or preferential regimes.                |
  | `afCT_6TIParRel` | Availability of participation relief for dividend income.               |
  | `agCT_7TIUnil`   | Availability of unilateral double-taxation relief for resident companies. |
  
  ### 1.3. Tax Rates
  | Tag            | Definition                                                                |
  | -------------- | ------------------------------------------------------------------------- |
  | `ahCT_8TRRat`    | Corporate income tax rate applicable to resident companies.               |
  | `aiCT_9TRAmt`    | Alternative minimum tax.                                                  |
  | `ajCT_10TRCap`   | Tax treatment of capital gains of resident companies.                     |
  
  ### 1.4. Non-Residents
  | Tag               | Definition                                                                                                          |
  | ----------------- | ------------------------------------------------------------------------------------------------------------------- |
  | `akCT_11NRRat`    | Corporate income tax rate applicable to non-resident companies.                                                     |
  | `alCT_12NRCapSha` | Tax treatment of capital gains arising from the disposal of shares in resident companies by non-resident companies. |
  | `amCT_13NRCapImm` | Tax treatment of capital gains arising from the disposal of immovable property by non-resident companies.           |
  | `anCT_14NRBra`    | Withholding tax rate on branch profits of non-resident companies.                                                   |
  | `aoCT_15NRDiv`    | Withholding tax rate on dividends paid to non-resident companies.                                                   |
  | `apCT_16NRInt`    | Withholding tax rate on interest paid to non-resident companies.                                                    |
  | `arCT_17NRRoy`    | Withholding tax rate on royalties paid to non-resident companies.                                                   |
  | `asCT_18NRFTec`   | Withholding tax rate on technical fees paid to non-resident companies.                                              |
  | `atCT_19NRFMan`   | Withholding tax rate on management fees paid to non-resident companies.                                             |
  
  ### 1.5. Anti-Avoidance
  
  | Tag              | Definition                                                         |
  | ---------------- | ------------------------------------------------------------------ |
  | `auCT_20AATP`    | Transfer-pricing legislation.                                      |
  | `axCT_21AALim`   | Rules limiting the deductibility of interest.                      |
  | `ayCT_22AACFC`   | Controlled foreign company legislation.                            |

## 2. Personal Income Tax

  ### 2.1. Tax Liability
  | Tag            | Definition                                                                           |
  | -------------- | ------------------------------------------------------------------------------------ |
  | `baPT_1TLRes`  | Criteria used to determine individual tax residence.                                 |
  | `bbPT_2TLInc`  | Territorial, worldwide, or mixed basis of personal income taxation.                  |
  | `bcPT_3TLUnil` | Availability of unilateral double-taxation relief for resident individuals.          |

  ### 2.2. Tax Liability
  | Tag            | Definition                                                                           |
  | -------------- | ------------------------------------------------------------------------------------ |
  | `bdPT_4TSTar`  | Structure of the personal income tax tariff.                                         |
  | `bePT_5TSBra`  | Number of personal income tax brackets.                                              |

  ### 2.3. Tax Rates (on employment)Liability
  | Tag            | Definition                                                                           |
  | -------------- | ------------------------------------------------------------------------------------ |
  | `bPT_TRmw`     | Minimum-wage benchmark used in the employment-income effective tax rate calculation. |
  | `bfPT_6TRTMin` | Effective tax rate on employment income at the minimum-wage benchmark.               |
  | `bgPT_7TRTTop` | Effective tax rate on employment income at the top-bracket benchmark.                |

  ### 2.3. Tax Rates (on employment)Liability
  | Tag            | Definition                                                                           |
  | -------------- | ------------------------------------------------------------------------------------ |
  | `bhPT_8NREmp`    | Withholding tax rate on employment income of non-resident individuals.    |
  | `biPT_9NR2Div`   | Withholding tax rate on dividends paid to non-resident individuals.       |
  | `bjPT_10NR3Int`  | Withholding tax rate on interest paid to non-resident individuals.        |
  | `bkPT_11NR4Roy`  | Withholding tax rate on royalties paid to non-resident individuals.       |
  | `blPT_12NR5FTec` | Withholding tax rate on technical fees paid to non-resident individuals.  |
  | `bmPT_13NR6FDir` | Withholding tax rate on directors’ fees paid to non-resident individuals. |

## 3. Value-added tax
| Tag          | Definition                                    |
| ------------ | --------------------------------------------- |
| `caVT_1Rat`  | Standard VAT rate.                            |
| `cbVT_2Red`  | Reduced VAT rate or rates.                    |
| `ccVT_3Incr` | Increased VAT rate.                           |
| `cdVT_4Reg`  | VAT registration or deregistration threshold. |
| `ceVT_5Gro`  | VAT group regime.                             |

## 4. Excise duties

| Tag          | Definition                                  |
| ------------ | ------------------------------------------- |
| `daEX_1Prod` | Selected products subject to excise duties. |

## 5. Property and wealth taxes

| Tag             | Definition                                |
| --------------- | ----------------------------------------- |
| `ebPW_OwnNWIn`  | Net wealth tax applicable to individuals. |
| `ecPW_OwnNWCo`  | Net wealth tax applicable to companies.   |
| `eaPW_OwnREs`   | Real estate taxes.                        |
| `edPW_4TraIGT`  | Inheritance and gift taxes.               |
| `efPW_5TraTTax` | Transfer tax.                             |
| `egPW_6TranCap` | Capital duty.                             |
| `ehPW_7TranSta` | Stamp duty.                               |

## Data availability and use

The schema is shared without the underlying tax-feature values, which derive from the IBFD and PwC databases and remain subject to the respective providers’ terms of use. It therefore does not reproduce country-level profiles, source texts, or other proprietary materials. Researchers with lawful access to these sources may populate the tagged fields to reproduce, verify, extend, or adapt the dataset.
