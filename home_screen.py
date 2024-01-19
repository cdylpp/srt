from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QMessageBox

class HomeScreen(QMainWindow):
    def __init__(self, user_type, full_name):
        super().__init__()

        self.setWindowTitle(f'{user_type} Dashboard - {full_name}')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.resize(800, 900) #width, height
        layout = QVBoxLayout(central_widget)

        welcome_label = QLabel(f'Welcome, {full_name}!')
        layout.addWidget(welcome_label)

        # Create a stacked widget to hold different views
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Create views for different options
        self.create_admin_view()
        self.create_teacher_view()
        self.create_student_view()

        # Set default view based on user type
        if user_type == 'Admin':
            self.stacked_widget.setCurrentIndex(0)  # Show admin view
        elif user_type == 'Teacher':
            self.stacked_widget.setCurrentIndex(1)  # Show teacher view
        elif user_type in ['Student', 'Parent']:
            self.stacked_widget.setCurrentIndex(2)  # Show student view

        logout_button = QPushButton('Logout')
        layout.addWidget(logout_button)
        logout_button.clicked.connect(self.logout)

    def create_admin_view(self):
        admin_view = QWidget()
        admin_layout = QVBoxLayout(admin_view)

        student_label = QLabel('Student')
        admin_layout.addWidget(student_label)

        student_options = ['Add New User', 'View Users', 'Edit Current User', 'Disenroll User']
        for option in student_options:
            admin_layout.addWidget(QPushButton(option))

        teachers_label = QLabel('Teachers:')
        admin_layout.addWidget(teachers_label)

        teachers_options = ['Add New Teacher', 'View Teachers', 'Edit Current Teacher', 'Disenroll Teacher']
        for option in teachers_options:
            admin_layout.addWidget(QPushButton(option))

        admin_layout.addWidget(QPushButton('Admin Options'))

        self.stacked_widget.addWidget(admin_view)

    def create_teacher_view(self):
        teacher_view = QWidget()
        teacher_layout = QVBoxLayout(teacher_view)

        student_label = QLabel('Student')
        teacher_layout.addWidget(student_label)

        student_options = ['Add New Student', 'View Students', 'Edit Current Student', 'Disenroll Student']
        for option in student_options:
            teacher_layout.addWidget(QPushButton(option, clicked=lambda ch, option=option: self.handle_teacher_option(option)))

        # Additional Teacher Options (Grades, Coursework, Progress, Standardized Test Scores, Attendance, Participation)
        teacher_options = ['Grades', 'Coursework', 'Progress', 'Standardized Test Scores', 'Attendance', 'Participation']
        for option in teacher_options:
            teacher_layout.addWidget(QPushButton(option, clicked=lambda ch, option=option: self.handle_teacher_option(option)))

        self.stacked_widget.addWidget(teacher_view)

    def create_student_view(self):
        student_view = QWidget()
        student_layout = QVBoxLayout(student_view)

        # Student Options (Profile, Academics)
        student_options = ['Profile', 'Academics']
        for option in student_options:
            student_layout.addWidget(QPushButton(option, clicked=lambda ch, option=option: self.handle_student_option(option)))

        self.stacked_widget.addWidget(student_view)

    def logout(self):
        self.close()  # Close the main window to return to the login screen

    def handle_teacher_option(self, option):
        if option == 'Grades':
            # Implement the functionality for 'Grades' here
            pass
        elif option == 'Coursework':
            # Implement the functionality for 'Coursework' here
            pass
        elif option == 'Progress':
            # Implement the functionality for 'Progress' here
            pass
        elif option == 'Standardized Test Scores':
            # Implement the functionality for 'Standardized Test Scores' here
            pass
        elif option == 'Attendance':
            # Implement the functionality for 'Attendance' here
            pass
        elif option == 'Participation':
            # Implement the functionality for 'Participation' here
            pass
        else:
            # Handle other teacher options
            pass

    def handle_student_option(self, option):
        if option == 'Profile':
            QMessageBox.information(self, 'Profile', 'View and Edit Your Profile')

        elif option == 'Academics':
            QMessageBox.information(self, 'Academics', 'View Your Grades, Coursework, Progress, and Standardized Test Scores')

        elif option == 'Attendance':
            QMessageBox.information(self, 'Attendance', 'View Your Attendance Record')

        elif option == 'Participation':
            QMessageBox.information(self, 'Participation', 'View Your Participation Record')