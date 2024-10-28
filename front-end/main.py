import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class CalendarApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the layout
        self.layout = QVBoxLayout()

        # Create UI elements
        self.label = QLabel("Enter Company House No:")
        self.company_number_input = QLineEdit(self)
        self.submit_button = QPushButton("Create Calendar Events", self)

        # Add elements to layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.company_number_input)
        self.layout.addWidget(self.submit_button)

        # Set the layout
        self.setLayout(self.layout)

        # Connect button to function
        self.submit_button.clicked.connect(self.create_events)

    def create_events(self):
        company_number = self.company_number_input.text()
        response = requests.get('http://localhost:5001/getToken', json={"company_number": company_number})

        if response.status_code == 200:
            QMessageBox.information(self, "Success", "Events created successfully!")
        else:
            QMessageBox.warning(self, "Error", f"Failed to create events: {response.text}")  # Show detailed error

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calendar_app = CalendarApp()
    calendar_app.setWindowTitle("Company Calendar App")
    calendar_app.show()
    sys.exit(app.exec_())