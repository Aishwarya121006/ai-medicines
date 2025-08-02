import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict
import warnings

warnings.filterwarnings('ignore')

class DrugIntakeTracker:
    def __init__(self):
        self.intake_records = []
        self.drug_database = {
            'Aspirin': {'type': 'Painkiller', 'max_daily_dose': 4000, 'unit': 'mg'},
            'Ibuprofen': {'type': 'Anti-inflammatory', 'max_daily_dose': 2400, 'unit': 'mg'},
            'Acetaminophen': {'type': 'Painkiller', 'max_daily_dose': 3000, 'unit': 'mg'},
            'Lisinopril': {'type': 'Blood Pressure', 'max_daily_dose': 40, 'unit': 'mg'},
            'Metformin': {'type': 'Diabetes', 'max_daily_dose': 2000, 'unit': 'mg'},
            'Atorvastatin': {'type': 'Cholesterol', 'max_daily_dose': 80, 'unit': 'mg'},
            'Omeprazole': {'type': 'Acid Reducer', 'max_daily_dose': 40, 'unit': 'mg'},
            'Vitamin D': {'type': 'Supplement', 'max_daily_dose': 4000, 'unit': 'IU'}
        }

    def add_intake_record(self, drug_name, dose, timestamp, patient_id="P001"):
        record = {
            'patient_id': patient_id,
            'drug_name': drug_name,
            'dose': dose,
            'timestamp': pd.to_datetime(timestamp),
            'drug_type': self.drug_database.get(drug_name, {}).get('type', 'Unknown'),
            'unit': self.drug_database.get(drug_name, {}).get('unit', 'mg')
        }
        self.intake_records.append(record)

    def generate_sample_data(self):
        print("Generating sample drug intake data...")
        patients = ['P001', 'P002', 'P003']
        drugs = list(self.drug_database.keys())
        base_date = datetime.now() - timedelta(days=30)

        for patient in patients:
            for day in range(30):
                current_date = base_date + timedelta(days=day)
                daily_drugs = np.random.choice(drugs, size=np.random.randint(2, 5), replace=False)

                for drug in daily_drugs:
                    doses_per_day = np.random.randint(1, 4)
                    max_dose = self.drug_database[drug]['max_daily_dose']

                    for _ in range(doses_per_day):
                        hour = np.random.randint(6, 22)
                        minute = np.random.randint(0, 60)
                        timestamp = current_date.replace(hour=hour, minute=minute)
                        dose = round(max_dose * np.random.uniform(0.1, 0.4), 1)
                        self.add_intake_record(drug, dose, timestamp, patient)

    def get_dataframe(self):
        return pd.DataFrame(self.intake_records)

    def analyze_daily_intake(self, patient_id=None):
        df = self.get_dataframe()
        if patient_id:
            df = df[df['patient_id'] == patient_id]
        df['date'] = df['timestamp'].dt.date

        daily_intake = df.groupby(['patient_id', 'drug_name', 'date'])['dose'].sum().reset_index()
        warnings_list = []

        for _, row in daily_intake.iterrows():
            max_dose = self.drug_database.get(row['drug_name'], {}).get('max_daily_dose', float('inf'))
            if row['dose'] > max_dose:
                warnings_list.append({
                    'patient': row['patient_id'],
                    'drug': row['drug_name'],
                    'date': row['date'],
                    'actual_dose': row['dose'],
                    'max_dose': max_dose
                })

        return daily_intake, warnings_list

    def plot_drug_usage_over_time(self):
        df = self.get_dataframe()
        df['date'] = df['timestamp'].dt.date
        daily_by_type = df.groupby(['date', 'drug_type'])['dose'].sum().reset_index()

        plt.figure(figsize=(14, 10))

        # Plot 1
        plt.subplot(2, 2, 1)
        pivot_data = daily_by_type.pivot(index='date', columns='drug_type', values='dose').fillna(0)
        for col in pivot_data.columns:
            plt.plot(pivot_data.index, pivot_data[col], marker='o', label=col)
        plt.title('Daily Drug Intake by Type')
        plt.xlabel('Date')
        plt.ylabel('Total Dose')
        plt.xticks(rotation=45)
        plt.legend()

        # Plot 2
        plt.subplot(2, 2, 2)
        freq = df['drug_name'].value_counts().head(6)
        sns.barplot(x=freq.index, y=freq.values)
        plt.title('Most Frequently Used Drugs')
        plt.xticks(rotation=45)

        # Plot 3
        plt.subplot(2, 2, 3)
        totals = df.groupby('patient_id')['dose'].sum()
        plt.pie(totals.values, labels=totals.index, autopct='%1.1f%%')
        plt.title('Total Drug Intake by Patient')

        # Plot 4
        plt.subplot(2, 2, 4)
        df['hour'] = df['timestamp'].dt.hour
        hourly = df['hour'].value_counts().sort_index()
        sns.barplot(x=hourly.index, y=hourly.values)
        plt.title('Drug Intake Pattern by Hour')
        plt.xlabel('Hour')
        plt.ylabel('Intake Count')

        plt.tight_layout()
        plt.show()

    def generate_patient_report(self, patient_id):
        df = self.get_dataframe()
        patient_data = df[df['patient_id'] == patient_id]

        if patient_data.empty:
            print(f"No data found for patient {patient_id}")
            return

        print(f"\n=== PATIENT REPORT: {patient_id} ===")
        print(f"Report Period: {patient_data['timestamp'].min().date()} to {patient_data['timestamp'].max().date()}")
        print(f"Total Drug Intakes: {len(patient_data)}")

        print("\n--- DRUG SUMMARY ---")
        drug_summary = patient_data.groupby('drug_name').agg({
            'dose': ['count', 'sum', 'mean'],
            'drug_type': 'first'
        }).round(2)
        drug_summary.columns = ['Frequency', 'Total_Dose', 'Avg_Dose', 'Type']
        print(drug_summary.to_string())

        daily_intake, warnings = self.analyze_daily_intake(patient_id)

        if warnings:
            print("\n--- OVERDOSE WARNINGS ---")
            for w in warnings:
                print(f"⚠️  {w['date']}: {w['drug']} - {w['actual_dose']} > {w['max_dose']}")
        else:
            print("\n✅ No overdose warnings found")

        print("\n--- DRUG INTERACTION CHECK ---")
        drugs = set(patient_data['drug_name'])
        if 'Aspirin' in drugs and 'Ibuprofen' in drugs:
            print("⚠️  Aspirin + Ibuprofen: Increased bleeding risk")
        if 'Acetaminophen' in drugs and len(drugs) > 3:
            print("ℹ️  Multiple drugs with Acetaminophen: Monitor liver function")

        return drug_summary


def main():
    print("🏥 DRUG INTAKE TRACKING SYSTEM")
    tracker = DrugIntakeTracker()
    tracker.generate_sample_data()
    df = tracker.get_dataframe()

    print(f"\n📊 SYSTEM OVERVIEW")
    print(f"Total Records: {len(df)}")
    print(f"Unique Patients: {df['patient_id'].nunique()}")
    print(f"Unique Drugs: {df['drug_name'].nunique()}")
    print(f"Date Range: {df['timestamp'].min().date()} to {df['timestamp'].max().date()}")

    print(f"\n💊 DRUG DATABASE")
    for drug, info in tracker.drug_database.items():
        print(f"  {drug}: {info['type']} (Max: {info['max_daily_dose']} {info['unit']}/day)")

    print(f"\n📋 RECENT INTAKE RECORDS")
    print(df.sort_values('timestamp', ascending=False).head(10)[['patient_id', 'drug_name', 'dose', 'unit', 'timestamp']].to_string(index=False))

    print(f"\n📈 DAILY INTAKE ANALYSIS")
    daily_intake, warnings = tracker.analyze_daily_intake()
    print(daily_intake.nlargest(5, 'dose').to_string(index=False))

    if warnings:
        print(f"\n⚠️  OVERDOSE WARNINGS:")
        for w in warnings[:5]:
            print(f"  {w['patient']} - {w['drug']} on {w['date']}: {w['actual_dose']} > {w['max_dose']}")
    else:
        print("✅ No overdose warnings detected")

    for patient in df['patient_id'].unique()[:2]:
        tracker.generate_patient_report(patient)

    print(f"\n🔍 DRUG TYPE ANALYSIS")
    type_summary = df.groupby('drug_type').agg({
        'dose': ['count', 'sum'],
        'patient_id': pd.Series.nunique
    }).round(2)
    type_summary.columns = ['Total_Intakes', 'Total_Dose', 'Unique_Patients']
    print(type_summary.to_string())

    print(f"\n📊 Generating visualizations...")
    tracker.plot_drug_usage_over_time()

    print(f"\n✅ Analysis complete!")

if __name__ == "__main__":
    main()
