import unittest
import pandas as pd
from data_layer import PatientData

# Custom PatientData class for testing with in-memory data
class TestPatientData(unittest.TestCase):
    def setUp(self):
        # Load mock CSV data into a DataFrame for testing
        self.patient_data = PatientData('Tables/test_patient.csv')

    def test_get_name(self):
        # Test retrieval of 'name' by ID
        self.assertEqual(self.patient_data.get_name(1), "John Doe")
        self.assertEqual(self.patient_data.get_name(2), "Jane Smith")
        self.assertEqual(self.patient_data.get_name(3), "No data found for ID 3 in column name.")

    def test_get_email(self):
        # Test retrieval of 'email' by ID
        self.assertEqual(self.patient_data.get_email(1), "johndoe@example.com")
        self.assertEqual(self.patient_data.get_email(2), "janesmith@example.com")
        self.assertEqual(self.patient_data.get_email(3), "No data found for ID 3 in column email.")

    def test_get_phone(self):
        # Test retrieval of 'phone' by ID
        self.assertEqual(self.patient_data.get_phone(1), "123-456-7890")
        self.assertEqual(self.patient_data.get_phone(2), "987-654-3210")
        self.assertEqual(self.patient_data.get_phone(3), "No data found for ID 3 in column phone.")

    def test_get_drugs(self):
        # Test retrieval of 'drugs' by ID
        self.assertEqual(self.patient_data.get_drugs(1), "DrugA")
        self.assertEqual(self.patient_data.get_drugs(2), "DrugB")
        self.assertEqual(self.patient_data.get_drugs(3), "No data found for ID 3 in column drugs.")

    def test_get_patient_history(self):
        # Test retrieval of 'patient_history' by ID
        self.assertEqual(self.patient_data.get_patient_history(1), "HistoryA")
        self.assertEqual(self.patient_data.get_patient_history(2), "HistoryB")
        self.assertEqual(self.patient_data.get_patient_history(3), "No data found for ID 3 in column patient_history.")

    def test_get_conversation_history(self):
        # Test retrieval of 'conversation_history' by ID
        self.assertEqual(self.patient_data.get_conversation_history(1), "ConversationA")
        self.assertEqual(self.patient_data.get_conversation_history(2), "ConversationB")
        self.assertEqual(self.patient_data.get_conversation_history(3), "No data found for ID 3 in column conversation_history.")

    def test_get_column_data_by_id_nonexistent_column(self):
        # Test retrieval of a non-existent column
        self.assertEqual(self.patient_data.get_column_data_by_id("nonexistent_column", 1), "Column 'nonexistent_column' not found in the CSV file.")

    def test_get_all_conversation_data(self):
        print(self.patient_data.get_all_conversation_data())
        return True
    
    def test_set_new_patient_conversation(self):
        self.patient_data.set_new_patient_conversation(3,'Juan Smith','juansmith@example.com','987-743-3210','DrugC','HistoryC','ConversationC')
        return True

# Run the tests
if __name__ == '__main__':
    unittest.main()
