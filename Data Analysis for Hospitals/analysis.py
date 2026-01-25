import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV files
general_df = pd.read_csv('test/general.csv')
prenatal_df = pd.read_csv('test/prenatal.csv')
sports_df = pd.read_csv('test/sports.csv')

# Rename columns
prenatal_df.columns = general_df.columns
sports_df.columns = general_df.columns

# Merge DataFrames
df = pd.concat(
    [general_df, prenatal_df, sports_df],
    ignore_index=True
)

# Data cleaning (from previous stages)
df.drop(columns=['Unnamed: 0'], inplace=True)
df.dropna(how='all', inplace=True)

df['gender'] = df['gender'].replace({
    'female': 'f', 'woman': 'f',
    'male': 'm', 'man': 'm'
})

df.loc[df['hospital'] == 'prenatal', 'gender'] = \
    df.loc[df['hospital'] == 'prenatal', 'gender'].fillna('f')

columns_to_fill = [
    'bmi', 'diagnosis', 'blood_test', 'ecg',
    'ultrasound', 'mri', 'xray', 'children', 'months'
]
df[columns_to_fill] = df[columns_to_fill].fillna(0)

# -------------------
# Question 1: Age histogram
# -------------------
age_bins = [0, 15, 35, 55, 70, 80]
age_labels = ['0-15', '15-35', '35-55', '55-70', '70-80']

df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels)

age_counts = df['age_group'].value_counts()
most_common_age_group = age_counts.idxmax()

df['age'].plot(kind='hist', bins=age_bins)
plt.title('Age Distribution')
plt.xlabel('Age')
plt.ylabel('Number of Patients')
plt.show()

# -------------------
# Question 2: Diagnosis pie chart
# -------------------
diagnosis_counts = df['diagnosis'].value_counts()
most_common_diagnosis = diagnosis_counts.idxmax()

diagnosis_counts.plot(kind='pie', autopct='%1.1f%%')
plt.title('Diagnosis Distribution')
plt.ylabel('')
plt.show()

# -------------------
# Question 3: Violin plot (height by hospital)
# -------------------
sns.violinplot(data=df, x='hospital', y='height')
plt.title('Height Distribution by Hospital')
plt.show()

# -------------------
# Output answers
# -------------------
print(f"The answer to the 1st question: {most_common_age_group}")
print(f"The answer to the 2nd question: {most_common_diagnosis}")
print(
    "The answer to the 3rd question: "
    "The gap and two peaks appear because different hospitals treat different types of patients. "
    "The prenatal hospital includes children and newborns, while general and sports hospitals "
    "mostly treat adults. This creates two height clusters (small and tall values)."
)


