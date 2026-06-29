# Data Types Used in the Comparative Legal Analysis

## Scope

The comparative legal analysis examined 48 tax features across five areas of taxation:

* 22 corporate income tax features;
* 13 personal income tax features;
* 5 value-added tax features;
* 1 excise-duty feature, structured through 28 product groups; and
* 7 property and wealth tax features.

The study used three principal variable types:

* **Qualitative and structural variables**, which concern the legal design, scope, or functional structure of a tax rule;
* **Quantitative variables**, which express the level, period, or numerical structure of taxation; and
* **Binomial variables**, which record the presence or absence of a specified legal rule, tax, or regime.

Certain features combined structural and quantitative components. In such cases, the applicable decision rules are specified in `decision_criteria.md`.

## 1. Corporate Income Tax

### 1.1. Tax Liability

| Tag             | Feature                                           | Variable type              |
| --------------- | ------------------------------------------------- | -------------------------- |
| `aaCT_1TLRes`   | Corporate tax residence criteria                  | Qualitative and structural |
| `abCT_2TLBase`  | Scope of the taxable income                 | Qualitative and structural |
| `acCT_3TLGrTre` | Group treatment for corporate income tax purposes | Binomial                   |

### 1.2. Taxable Income

| Tag              | Feature                                                  | Variable type                    |
| ---------------- | -------------------------------------------------------- | -------------------------------- |
| `adCT_4TILos`    | Loss carry-forward                                       | Mixed: binomial and quantitative |
| `aeCT_5TIInc`    | Corporate income tax incentives or preferential regimes  | Qualitative and structural       |
| `afCT_6TIParRel` | Participation relief for dividend income                 | Qualitative and structural       |
| `agCT_7TIUnil`   | Unilateral double-taxation relief for resident companies | Binomial                         |

### 1.3. Tax Rates

| Tag            | Feature                                                    | Variable type                      |
| -------------- | ---------------------------------------------------------- | ---------------------------------- |
| `ahCT_8TRRat`  | Corporate income tax rate applicable to resident companies | Quantitative                       |
| `aiCT_9TRAmt`  | Alternative minimum tax                                    | Binomial                           |
| `ajCT_10TRCap` | Tax treatment of capital gains of resident companies       | Mixed: structural and quantitative |

### 1.4. Non-Residents

| Tag               | Feature                                                                                                            | Variable type                      |
| ----------------- | ------------------------------------------------------------------------------------------------------------------ | ---------------------------------- |
| `akCT_11NRRat`    | Corporate income tax rate applicable to non-resident companies                                                     | Quantitative                       |
| `alCT_12NRCapSha` | Tax treatment of capital gains arising from the disposal of shares in resident companies by non-resident companies | Mixed: structural and quantitative |
| `amCT_13NRCapImm` | Tax treatment of capital gains arising from the disposal of immovable property by non-resident companies           | Mixed: structural and quantitative |
| `anCT_14NRBra`    | Withholding tax rate on branch profits of non-resident companies                                                   | Quantitative                       |
| `aoCT_15NRDiv`    | Withholding tax rate on dividends paid to non-resident companies                                                   | Quantitative                       |
| `apCT_16NRInt`    | Withholding tax rate on interest paid to non-resident companies                                                    | Quantitative                       |
| `arCT_17NRRoy`    | Withholding tax rate on royalties paid to non-resident companies                                                   | Quantitative                       |
| `asCT_18NRFTec`   | Withholding tax rate on technical fees paid to non-resident companies                                              | Quantitative                       |
| `atCT_19NRFMan`   | Withholding tax rate on management fees paid to non-resident companies                                             | Quantitative                       |

### 1.5. Anti-Avoidance

| Tag            | Feature                                      | Variable type |
| -------------- | -------------------------------------------- | ------------- |
| `auCT_20AATP`  | Transfer-pricing legislation                 | Binomial      |
| `axCT_21AALim` | Rules limiting the deductibility of interest | Binomial      |
| `ayCT_22AACFC` | Controlled foreign company legislation       | Binomial      |

## 2. Personal Income Tax

### 2.1. Tax Liability

| Tag            | Feature                                                    | Variable type              |
| -------------- | ---------------------------------------------------------- | -------------------------- |
| `baPT_1TLRes`  | Individual tax residence criteria                          | Qualitative and structural |
| `bbPT_2TLInc`  | Basis of personal income taxation                          | Qualitative and structural |
| `bcPT_3TLUnil` | Unilateral double-taxation relief for resident individuals | Binomial                   |

### 2.2. Taxable Income

| Tag           | Feature                                     | Variable type              |
| ------------- | ------------------------------------------- | -------------------------- |
| `bdPT_4TSTar` | Structure of the personal income tax tariff | Qualitative and structural |
| `bePT_5TSBra` | Number of personal income tax brackets      | Quantitative               |

### 2.3. Tax Rates on Employment Income

| Tag            | Feature                                                                             | Variable type                                        |
| -------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------- |
| `bPT_TRmw`     | Minimum-wage benchmark used in the employment-income effective tax rate calculation | Supporting benchmark; not an independent tax feature |
| `bfPT_6TRTMin` | Effective tax rate on employment income at the minimum-wage benchmark               | Quantitative                                         |
| `bgPT_7TRTTop` | Effective tax rate on employment income at the top-bracket benchmark                | Quantitative                                         |

### 2.4. Non-Residents

| Tag              | Feature                                                                  | Variable type                      |
| ---------------- | ------------------------------------------------------------------------ | ---------------------------------- |
| `bhPT_8NREmp`    | Withholding tax rate on employment income of non-resident individuals    | Mixed: structural and quantitative |
| `biPT_9NR2Div`   | Withholding tax rate on dividends paid to non-resident individuals       | Quantitative                       |
| `bjPT_10NR3Int`  | Withholding tax rate on interest paid to non-resident individuals        | Quantitative                       |
| `bkPT_11NR4Roy`  | Withholding tax rate on royalties paid to non-resident individuals       | Quantitative                       |
| `blPT_12NR5FTec` | Withholding tax rate on technical fees paid to non-resident individuals  | Quantitative                       |
| `bmPT_13NR6FDir` | Withholding tax rate on directors’ fees paid to non-resident individuals | Quantitative                       |

## 3. Value-Added Tax

| Tag          | Feature                                      | Variable type              |
| ------------ | -------------------------------------------- | -------------------------- |
| `caVT_1Rat`  | Standard VAT rate                            | Quantitative               |
| `cbVT_2Red`  | Reduced VAT rate or rates                    | Qualitative and structural |
| `ccVT_3Incr` | Increased VAT rate                           | Qualitative and structural |
| `cdVT_4Reg`  | VAT registration or deregistration threshold | Binomial                   |
| `ceVT_5Gro`  | VAT group regime                             | Binomial                   |

## 4. Excise Duties

| Tag          | Feature                                    | Variable type              |
| ------------ | ------------------------------------------ | -------------------------- |
| `daEX_1Prod` | Selected products subject to excise duties | Qualitative and structural |

## 5. Property and Wealth Taxes

| Tag             | Feature                                  | Variable type |
| --------------- | ---------------------------------------- | ------------- |
| `ebPW_OwnNWIn`  | Net wealth tax applicable to individuals | Binomial      |
| `ecPW_OwnNWCo`  | Net wealth tax applicable to companies   | Binomial      |
| `eaPW_OwnREs`   | Real estate taxes                        | Binomial      |
| `edPW_4TraIGT`  | Inheritance and gift taxes               | Binomial      |
| `efPW_5TraTTax` | Transfer tax                             | Binomial      |
| `egPW_6TranCap` | Capital duty                             | Binomial      |
| `ehPW_7TranSta` | Stamp duty                               | Binomial      |

## Classification note

The mixed variables were assessed sequentially. Loss carry-forward was first assessed according to the existence or absence of a carry-forward provision and, where applicable, according to the period of a finite carry-forward period. Capital-gains variables and the taxation of non-resident employment income were first assessed according to their legal treatment; where a distinct rate applied, the rate was assessed quantitatively.

The minimum-wage benchmark recorded in `bPT_TRmw` was used solely to calculate the effective tax rate recorded in `bfPT_6TRTMin`. It was therefore not counted as a separate feature among the 48 tax features.
