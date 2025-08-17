import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
                             QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox,
                             QDialog, QHBoxLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Import from database and blockchain (assuming you have these modules)
from database import get_candidates, add_candidate, delete_candidate, get_voting_results, add_voter, vote_for_candidate
from blockchain import add_vote_to_blockchain
from face_recognition_module import face_authenticate

# SQL password (for demo, you can validate from a secure source)
SQL_ADMIN_PASSWORD = "Sabrin@cse"

# ------------ Admin Login Dialog ------------------ #
class AdminLoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Admin Login")
        self.setFixedSize(300, 150)
        self.setStyleSheet("background-color: #2E4053; color: white;")

        layout = QVBoxLayout()

        label = QLabel("Enter Admin SQL Password")
        label.setFont(QFont('Arial', 12))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setStyleSheet("padding: 8px;")
        layout.addWidget(self.password_input)

        btn_layout = QHBoxLayout()
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.check_password)
        login_btn.setStyleSheet("background-color: #1ABC9C; color: white; padding: 5px; font-weight: bold;")
        btn_layout.addWidget(login_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("background-color: #E74C3C; color: white; padding: 5px; font-weight: bold;")
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def check_password(self):
        entered_password = self.password_input.text()
        if entered_password == SQL_ADMIN_PASSWORD:
            QMessageBox.information(self, "Access Granted", "Welcome, Admin!")
            self.accept()
        else:
            QMessageBox.critical(self, "Access Denied", "Incorrect Password!")

# ------------ Admin Page Class ------------------ #
class AdminPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Panel")
        self.setGeometry(300, 300, 650, 600)
        self.setStyleSheet("background-color: #34495E; color: white;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        label = QLabel("Admin Panel - Manage Candidates & View Results")
        label.setFont(QFont('Arial', 16))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Candidates Table
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: black;
                alternate-background-color: #f2f2f2;
            }
        """)
        self.table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: white;
                color: black;
                font-weight: bold;
                padding: 5px;
            }
        """)
        layout.addWidget(QLabel("Candidates List:"))
        self.load_candidates()
        layout.addWidget(self.table)

        # Voting Results Table
        self.results_table = QTableWidget()
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: black;
                alternate-background-color: #f2f2f2;
            }
        """)
        self.results_table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: white;
                color: black;
                font-weight: bold;
                padding: 5px;
            }
        """)
        layout.addWidget(QLabel("Voting Results:"))
        self.load_results()
        layout.addWidget(self.results_table)

        # Input Fields
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Candidate Name")
        layout.addWidget(self.name_input)

        self.party_input = QLineEdit()
        self.party_input.setPlaceholderText("Party Name")
        layout.addWidget(self.party_input)

        # Buttons
        add_btn = QPushButton("Add Candidate")
        add_btn.clicked.connect(self.add_candidate_action)
        add_btn.setStyleSheet("background-color: #1ABC9C; padding: 8px;")
        layout.addWidget(add_btn)

        del_btn = QPushButton("Delete Candidate")
        del_btn.clicked.connect(self.delete_candidate_action)
        del_btn.setStyleSheet("background-color: #E74C3C; padding: 8px;")
        layout.addWidget(del_btn)

        refresh_btn = QPushButton("Refresh Results")
        refresh_btn.clicked.connect(self.load_results)
        refresh_btn.setStyleSheet("background-color: #2980B9; padding: 8px;")
        layout.addWidget(refresh_btn)

        back_btn = QPushButton("Back to Home")
        back_btn.clicked.connect(self.close)
        back_btn.setStyleSheet("background-color: #F39C12; padding: 8px;")
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def load_candidates(self):
        candidates = get_candidates()
        self.table.setRowCount(len(candidates))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Name", "Party"])
        for i, (name, party) in enumerate(candidates):
            self.table.setItem(i, 0, QTableWidgetItem(name))
            self.table.setItem(i, 1, QTableWidgetItem(party))

    def load_results(self):
        results = get_voting_results()
        self.results_table.setRowCount(len(results))
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Name", "Party", "Total Votes"])
        for i, (name, party, votes) in enumerate(results):
            self.results_table.setItem(i, 0, QTableWidgetItem(name))
            self.results_table.setItem(i, 1, QTableWidgetItem(party))
            self.results_table.setItem(i, 2, QTableWidgetItem(str(votes)))

    def add_candidate_action(self):
        name = self.name_input.text()
        party = self.party_input.text()
        if name and party:
            add_candidate(name, party)
            QMessageBox.information(self, "Success", "Candidate added successfully!")
            self.load_candidates()
        else:
            QMessageBox.warning(self, "Input Error", "Please fill both fields.")

    def delete_candidate_action(self):
        name = self.name_input.text()
        if name:
            delete_candidate(name)
            QMessageBox.information(self, "Success", "Candidate deleted successfully!")
            self.load_candidates()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter candidate name to delete.")

# ------------ Main Window ------------------ #
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blockchain Voting System")
        self.setGeometry(300, 300, 500, 400)
        self.setStyleSheet("background-color: #2C3E50; color: White;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        welcome = QLabel("Welcome to Blockchain Voting System")
        welcome.setFont(QFont('Arial', 16))
        welcome.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome)

        admin_btn = QPushButton("Admin Login")
        admin_btn.clicked.connect(self.open_admin)
        admin_btn.setStyleSheet("background-color: #8E44AD; color: white; padding: 10px; font-size: 14px;")
        layout.addWidget(admin_btn)

        voter_btn = QPushButton("Voter Login")
        voter_btn.clicked.connect(self.open_voter)
        voter_btn.setStyleSheet("background-color: #3498DB; color: white; padding: 10px; font-size: 14px;")
        layout.addWidget(voter_btn)

        self.setLayout(layout)

    def open_admin(self):
        dialog = AdminLoginDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.admin = AdminPage()
            self.admin.show()

    def open_voter(self):
        self.voter = VoterPage()
        self.voter.show()

# ------------ Voter Page Class ------------ #
class VoterPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voter Page")
        self.setGeometry(300, 300, 500, 600)
        self.setStyleSheet("background-color: #283747; color: white;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("Voter Registration and Voting")
        title.setFont(QFont('Arial', 14))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Full Name")
        layout.addWidget(self.name_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter Phone Number")
        layout.addWidget(self.phone_input)

        self.gender_input = QComboBox()
        self.gender_input.addItems(["Select Gender", "Male", "Female", "Other"])
        layout.addWidget(self.gender_input)

        self.dob_input = QLineEdit()
        self.dob_input.setPlaceholderText("Enter Date of Birth (YYYY-MM-DD)")
        layout.addWidget(self.dob_input)

        self.face_authenticated = False

        self.face_btn = QPushButton("Face Authenticate")
        self.face_btn.clicked.connect(self.face_authenticate_user)
        self.face_btn.setStyleSheet("background-color: #16A085; padding: 8px;")
        layout.addWidget(self.face_btn)

        self.candidate_combo = QComboBox()
        self.load_candidates()
        layout.addWidget(self.candidate_combo)

        vote_btn = QPushButton("Vote")
        vote_btn.clicked.connect(self.cast_vote)
        vote_btn.setStyleSheet("background-color: #2980B9; padding: 8px;")
        layout.addWidget(vote_btn)

        back_btn = QPushButton("Back to Home")
        back_btn.clicked.connect(self.close)
        back_btn.setStyleSheet("background-color: #F39C12; padding: 8px;")
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def load_candidates(self):
        candidates = get_candidates()
        self.candidate_combo.clear()
        self.candidate_combo.addItem("Select Candidate")
        for name, _ in candidates:
            self.candidate_combo.addItem(name)

    def face_authenticate_user(self):
        name = self.name_input.text()
        if name:
            if face_authenticate(name):
                self.face_authenticated = True
                QMessageBox.information(self, "Success", "Face recognized successfully!")
            else:
                self.face_authenticated = False
                QMessageBox.critical(self, "Failed", "Face recognition failed!")
        else:
            QMessageBox.warning(self, "Input Error", "Please enter your name for face recognition.")

    def cast_vote(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        gender = self.gender_input.currentText()
        dob = self.dob_input.text()
        candidate = self.candidate_combo.currentText()

        if candidate == "Select Candidate" or not name or not phone or gender == "Select Gender" or not dob:
            QMessageBox.warning(self, "Input Error", "Fill in all details and select candidate.")
            return

        if not self.face_authenticated:
            QMessageBox.warning(self, "Authentication Error", "Please complete face authentication before voting.")
            return

        voter_id, message = add_voter(name, phone, gender, dob)
        if message == "Already voted":
            QMessageBox.critical(self, "Error", "You have already voted!")
            return

        vote_for_candidate(voter_id, candidate)

        candidates = dict(get_candidates())  # Convert to dict: {name: party}
        party = candidates.get(candidate, "Unknown")

        add_vote_to_blockchain(name, candidate, party)

        QMessageBox.information(self, "Vote Cast", f"Vote casted for {candidate} successfully!")
        self.close()

# ------------ Run App ------------------ #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
