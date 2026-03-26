# Statistical-Tests-Analyzer
Statistical Testing Tool
A Python function that automatically selects and performs the appropriate statistical hypothesis tests based on your data characteristics. No more manually checking assumptions or deciding which test to use.

Features
Automatic Normality Checking – Determines if data is parametric or non-parametric

Automatic Variance Testing – Checks equality of variances for parametric tests

Multiple Test Support – Handles 2+ groups for both independent and dependent designs

Post-Hoc Analysis – Automatically runs appropriate post-hoc tests when significant differences are found

Human-Readable Output – Clear conclusions without digging through complex statistics

Statistical Tests Included
Design	Parametric	Non-Parametric
2 Independent Groups	Independent T-Test	Mann-Whitney U
2+ Independent Groups	One-Way ANOVA / Welch's ANOVA	Kruskal-Wallis
2 Dependent Groups	Dependent T-Test	Wilcoxon Signed-Rank
2+ Dependent Groups	Repeated Measures ANOVA	Friedman Test
Post-Hoc Tests
Tukey HSD – Parametric, independent groups

Dunn's Test – Non-parametric, independent groups (with Bonferroni correction)

Nemenyi Test – Non-parametric, dependent groups

Requirements
text
pandas
scipy
numpy
statsmodels
pingouin
scikit-posthocs
Installation
bash
pip install pandas scipy numpy statsmodels pingouin scikit-posthocs
Usage
Basic Syntax
python
from stat_test import stat_test

result = stat_test(
    path_of_csv='your_data.csv',
    list_of_groups=['group1', 'group2', 'group3'],
    subjects='Independent'  # Or 'Dependent'
)
Examples
Example 1: Independent Groups (Treatment Vs Control)

python
stat_test('clinical_data.csv', ['treatment', 'placebo'])
Example 2: Multiple Independent Groups

python
stat_test('product_data.csv', ['low_price', 'medium_price', 'high_price'])
Example 3: Dependent Groups (Repeated Measures)

python
stat_test('patient_data.csv', ['before', 'after', 'followup'], subjects='Dependent')
Input Requirements
CSV File – First row must contain column headers

Group Columns – Must contain numerical continuous data

No Missing Values – Data should be cleaned before input

Sample Size – For small datasets (<5000), Shapiro-Wilk is used; for larger datasets, D'Agostino-Pearson test is recommended

Output
The function returns:

Statistical test result (p-value or post-hoc table)

Human-readable conclusion printed to console

Limitations
Data must be cleaned with no missing values

User must specify whether groups are independent or dependent (requires domain knowledge)

Only continuous data types are supported

Future Updates
Bonferroni correction for Nemenyi post-hoc test

Built-in data cleaning functionality

Visualization outputs (boxplots, Q-Q plots)

Effect size calculations

Support for categorical data

License
MIT

Author
Yohannes Shiferaw

https://github.com/johnshiferaw

Feel free to use, modify, and contribute!

