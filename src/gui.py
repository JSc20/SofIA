from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog, QListWidget
import sys, requests

API_URL = "http://TU_SERVIDOR:5000"

class ProfesorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.token = None
        self.setWindowTitle("ChatBot y Archivos")
        self.setGeometry(100, 100, 500, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Login
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Correo")
        self.layout.addWidget(self.email_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Contraseña")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.pass_input)

        self.login_button = QPushButton("Iniciar sesión")
        self.layout.addWidget(self.login_button)
        self.login_button.clicked.connect(self.login)

        # Archivos
        self.subir_button = QPushButton("Subir archivo")
        self.layout.addWidget(self.subir_button)
        self.subir_button.clicked.connect(self.subir_archivo)
        self.subir_button.setEnabled(False)

        self.lista_archivos = QListWidget()
        self.layout.addWidget(self.lista_archivos)

        self.refrescar_button = QPushButton("Refrescar lista")
        self.layout.addWidget(self.refrescar_button)
        self.refrescar_button.clicked.connect(self.listar_archivos)
        self.refrescar_button.setEnabled(False)

    def login(self):
        r = requests.post(f"{API_URL}/login", json={
            "correo": self.email_input.text(),
            "contraseña": self.pass_input.text()
        })
        if r.status_code == 200:
            self.token = r.json()["token"]
            self.subir_button.setEnabled(True)
            self.refrescar_button.setEnabled(True)
        else:
            print("Login fallido")

    def subir_archivo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecciona un archivo")
        if file_path:
            with open(file_path, "rb") as f:
                headers = {"Authorization": self.token}
                r = requests.post(f"{API_URL}/subir_archivo", files={"archivo": f}, headers=headers)
            self.listar_archivos()

    def listar_archivos(self):
        self.lista_archivos.clear()
        headers = {"Authorization": self.token}
        r = requests.get(f"{API_URL}/listar_archivos", headers=headers)
        if r.status_code == 200:
            for a in r.json():
                self.lista_archivos.addItem(f"{a['nombre_archivo']} - {a['fecha_subida']}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfesorWindow()
    window.show()
    sys.exit(app.exec())