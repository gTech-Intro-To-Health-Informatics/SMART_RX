import pandas as pd

class PatientData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self.load_csv()

    # Load CSV file into a DataFrame
    def load_csv(self):
        return pd.read_csv(self.file_path)
    
    # Save the DataFrame back to the CSV
    def save_csv(self):
        self.df.to_csv(self.file_path, index=False)

    # Function to retrieve column data by ID
    def get_column_data_by_id(self, column_name, id_value):
        try:
            # Filter the DataFrame by id and retrieve the specified column's value
            result = self.df.loc[self.df['id'] == id_value, column_name]
            if not result.empty:
                return result.iloc[0]  # Return the first matched result
            else:
                return f"No data found for ID {id_value} in column {column_name}."
        except KeyError:
            return f"Column '{column_name}' not found in the CSV file."

    # Methods to retrieve specific columns by ID
    def get_name(self, id_value):
        return self.get_column_data_by_id('name', id_value)

    def get_email(self, id_value):
        return self.get_column_data_by_id('email', id_value)

    def get_phone(self, id_value):
        return self.get_column_data_by_id('phone', id_value)

    def get_drugs(self, id_value):
        return self.get_column_data_by_id('drugs', id_value)

    def get_patient_history(self, id_value):
        return self.get_column_data_by_id('patient_history', id_value)

    def get_conversation_history(self, id_value):
        return self.get_column_data_by_id('conversation_history', id_value)
    
    def get_all_conversation_data(self):
        json_string = self.df.to_json(orient='records')
        return json_string

    # Methods to update specific columns by ID
    def set_name(self, id_value, new_value):
        self.update_column_by_id('name', id_value, new_value)

    def set_email(self, id_value, new_value):
        self.update_column_by_id('email', id_value, new_value)

    def set_phone(self, id_value, new_value):
        self.update_column_by_id('phone', id_value, new_value)

    def set_drugs(self, id_value, new_value):
        self.update_column_by_id('drugs', id_value, new_value)

    def set_patient_history(self, id_value, new_value):
        self.update_column_by_id('patient_history', id_value, new_value)

    def set_conversation_history(self, id_value, new_value):
        self.update_column_by_id('conversation_history', id_value, new_value)

    def set_new_patient_conversation(self,id,name,email,phone,drugs,patient_history,conversation_history):
        with open(self.file_path,'a') as doc:
            doc.write(f"\n{id},{name},{email},{phone},{drugs},{patient_history},{conversation_history}")

    # General method to update any column by ID
    def update_column_by_id(self, column_name, id_value, new_value):
        if column_name not in self.df.columns:
            return f"Column '{column_name}' not found in the CSV file."
        if id_value not in self.df['id'].values:
            return f"No data found for ID {id_value}."
        
        # Update the value
        self.df.loc[self.df['id'] == id_value, column_name] = new_value
        self.save_csv()  # Save changes back to the CSV
        return f"Updated {column_name} for ID {id_value} to '{new_value}'."

# # Usage example
# file_path = 'Tables/patient.csv'
# patient_data = PatientData(file_path)
# # Define ID and column to retrieve
# id_value = 1
# # Retrieve data for each column
# print(patient_data.get_name(id_value))
# print(patient_data.get_email(id_value))
# print(patient_data.get_phone(id_value))
# print(patient_data.get_drugs(id_value))
# print(patient_data.get_patient_history(id_value))
# print(patient_data.get_conversation_history(id_value))
