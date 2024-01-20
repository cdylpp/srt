from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QMessageBox, QLineEdit, QComboBox, QDialog

class HomeScreen(QMainWindow):
    def __init__(self, user_type, full_name, db_manager):
        super().__init__()

        self.db_manager = db_manager

        self.setWindowTitle(f'{user_type} Dashboard - {full_name}')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.resize(800, 900) #width, height
        layout = QVBoxLayout(central_widget)

        welcome_label = QLabel(f'Welcome, {full_name}!')
        layout.addWidget(welcome_label)

        self.stacked_widget = QStackedWidget() #stacked widget to hold different views
        layout.addWidget(self.stacked_widget)

        #views for different users
        self.create_admin_view()
        self.create_teacher_view()
        self.create_student_view()

        #view based on user type
        if user_type == 'Admin':
            self.stacked_widget.setCurrentIndex(0)  #admin view
        elif user_type == 'Teacher':
            self.stacked_widget.setCurrentIndex(1)
        elif user_type in ['Student', 'Parent']:
            self.stacked_widget.setCurrentIndex(2)

        logout_button = QPushButton('Logout')
        layout.addWidget(logout_button)
        logout_button.clicked.connect(self.logout)

    def create_admin_view(self):
        admin_view = QWidget()
        admin_layout = QVBoxLayout(admin_view)

        admin_layout.addWidget(QPushButton('Profile', clicked=lambda: self.handle_admin_option('Profile')))
        admin_layout.addWidget(QPushButton('Student', clicked=lambda: self.handle_admin_option('Student')))
        admin_layout.addWidget(QPushButton('Teacher', clicked=lambda: self.handle_admin_option('Teacher')))
        admin_layout.addWidget(QPushButton('Admin Options', clicked=lambda: self.handle_admin_option('Admin Options')))

        self.stacked_widget.addWidget(admin_view)

    def handle_admin_option(self, option):
        if option == 'Profile':
            self.show_admin_profile()

        elif option == 'Student':
            self.show_student_options()

        elif option == 'Teacher':

            pass

        elif option == 'Admin Options':

            pass

    def show_admin_profile(self):
        admin_profile_widget = AdminProfileWidget()
        admin_profile_widget.exec()

    def show_student_options(self):
        student_options_widget = StudentOptionsWidget()
        student_options_widget.exec()


    def create_teacher_view(self):
        teacher_view = QWidget()
        teacher_layout = QVBoxLayout(teacher_view)

        student_label = QLabel('Student')
        teacher_layout.addWidget(student_label)

        student_options = ['Add New Student', 'View Students', 'Edit Current Student', 'Disenroll Student']
        for option in student_options:
            teacher_layout.addWidget(QPushButton(option, clicked=lambda ch, option=option: self.handle_teacher_option(option)))

        teacher_options = ['Grades', 'Coursework', 'Progress', 'Standardized Test Scores', 'Participation']
        for option in teacher_options:
            teacher_layout.addWidget(QPushButton(option, clicked=lambda ch, option=option: self.handle_teacher_option(option)))

        teacher_layout.addWidget(QPushButton('Attendance', clicked=lambda: self.handle_attendance_option()))

        self.stacked_widget.addWidget(teacher_view)

    def create_student_view(self):
        student_view = QWidget()
        student_layout = QVBoxLayout(student_view)

        student_options = ['Profile', 'Academics']
        for option in student_options:
            student_layout.addWidget(QPushButton(option, clicked=lambda ch, option=option: self.handle_student_option(option)))

        self.stacked_widget.addWidget(student_view)

    def logout(self):
        self.close()  #Close main window, return to login screen

    def handle_teacher_option(self, option):
        if option == 'Grades':

            pass
        elif option == 'Coursework':

            pass
        elif option == 'Progress':

            pass
        elif option == 'Standardized Test Scores':

            pass
        elif option == 'Attendance':

            pass
        elif option == 'Participation':

            pass
        else:

            pass

    def handle_attendance_option(self):
        attendance_window = AttendanceWindow(self.db_manager)
        attendance_window.exec()

    def handle_student_option(self, option):
        if option == 'Profile':
            QMessageBox.information(self, 'Profile', 'View and Edit Your Profile')

        elif option == 'Academics':
            QMessageBox.information(self, 'Academics', 'View Your Grades, Coursework, Progress, and Standardized Test Scores')

        elif option == 'Attendance':
            QMessageBox.information(self, 'Attendance', 'View Your Attendance Record')

        elif option == 'Participation':
            QMessageBox.information(self, 'Participation', 'View Your Participation Record')

class AdminProfileWidget(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Admin Profile')

        layout = QVBoxLayout()

        layout.addWidget(QLabel('First Name:'))
        self.first_name_input = QLineEdit()
        layout.addWidget(self.first_name_input)

        layout.addWidget(QLabel('Last Name:'))
        self.last_name_input = QLineEdit()
        layout.addWidget(self.last_name_input)

        layout.addWidget(QLabel('Preferred Contact Method:'))
        self.last_name_input = QLineEdit()
        layout.addWidget(self.last_name_input)


        submit_button = QPushButton('Save Changes', clicked=self.save_admin_profile)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def save_admin_profile(self):

        pass


class StudentOptionsWidget(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Student Options')

        layout = QVBoxLayout()

        student_options = ['Enroll New Student', 'View Student', 'Disenroll Student']
        for option in student_options:
            layout.addWidget(QPushButton(option, clicked=lambda ch, option=option: self.handle_student_option(option)))

        self.setLayout(layout)

    def handle_student_option(self, option):
        if option == 'Enroll New Student':
            enroll_student_widget = EnrollStudentWidget()
            enroll_student_widget.exec()

        elif option == 'View Student':

            pass

        elif option == 'Disenroll Student':

            pass


class EnrollStudentWidget(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Enroll New Student')

        layout = QVBoxLayout()

        layout.addWidget(QLabel('First Name:'))
        self.first_name_input = QLineEdit()
        layout.addWidget(self.first_name_input)

        layout.addWidget(QLabel('Last Name:'))
        self.last_name_input = QLineEdit()
        layout.addWidget(self.last_name_input)

        layout.addWidget(QLabel('DOB (M-D-YYYY)'))
        self.dob = QLineEdit()
        layout.addWidget(self.dob)

        layout.addWidget(QLabel('Email:'))
        self.email = QLineEdit()
        layout.addWidget(self.email)

        layout.addWidget(QLabel('Grade:'))
        self.grade_combo = QComboBox()
        self.grade_combo.addItems(
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 'Post Secondary', '1st Year Freshman',
             '2nd Year Sophomore', '3rd Year Junior', '4th Year Senior'])
        layout.addWidget(self.grade_combo)

        layout.addWidget(QLabel('Plan on Attending College:'))
        self.college_plan_combo = QComboBox()
        self.college_plan_combo.addItems(['Yes', 'No'])
        layout.addWidget(self.college_plan_combo)

        submit_button = QPushButton('Enroll Student', clicked=self.enroll_student)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def enroll_student(self):

        pass


class AttendanceWindow(QDialog):
    def __init__(self, db_manager):
        super().__init__()

        self.db_manager = db_manager
        self.setWindowTitle('Attendance')


        layout = QVBoxLayout()

        layout.addWidget(QLabel('Student ID:'))
        self.student_id_input = QLineEdit()
        layout.addWidget(self.student_id_input)

        layout.addWidget(QLabel('Date:'))
        self.date_input = QLineEdit()
        layout.addWidget(self.date_input)

        layout.addWidget(QLabel('Status:'))
        self.status_input = QLineEdit()
        layout.addWidget(self.status_input)

        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.submit_attendance)
        layout.addWidget(submit_button)

        cancel_button = QPushButton('Cancel', clicked=self.close)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def submit_attendance(self):

        student_id = self.student_id_input.text()
        date = self.date_input.text()
        status = self.status_input.text()

        if not student_id or not date or not status:
            QMessageBox.warning(self, "Warning", "All fields are required.")
            return

        try:
            cursor = self.db_manager.db_connection.cursor()

            query = "INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)"
            cursor.execute(query, (student_id, date, status))
            self.db_manager.db_connection.commit()

            QMessageBox.information(self, "Success", "Attendance recorded successfully.")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {e}")

        finally:
            if cursor:
                cursor.close()


