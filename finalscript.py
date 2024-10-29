from PyQt5.QtWidgets import QApplication, QWidget,QMessageBox, QFileDialog, QPushButton, QGridLayout, QTextEdit, QLabel
from PyQt5.QtGui import QPixmap,QImage
from PIL import Image
from PyQt5.QtCore import Qt


class SteganographyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(400,200,450,350)
        self.border_style = "border: 1.5px solid grey; border-radius: 5px;"
        self.setStyleSheet('''
                            QWidget{
                                background-image: url("/Users/gurpartapsingh/asdf/bgphphoto.png");  # Properly escaped quote
                                background-repeat: no-repeat;
                            }
                        ''')
        
        self.show()
        self.msg_length = ""
        self.image_path = None
        self.output_path = None
        self.en_message = ""
        self.de_message = ""
        #label - input image
        self.image_title = QLabel("Stegano Image")
        self.in_image_preview = QLabel()
        self.in_image_preview.setFixedHeight(300)
        self.in_image_preview.setFixedWidth(250)
        self.placeholder_image = QImage("/Users/gurpartapsingh/asdf/py project/pholder.png")
        self.placeholder_image_pixmap = QPixmap.fromImage(self.placeholder_image)
        self.placeholder_image_pixmap = self.placeholder_image_pixmap.scaled(
            self.in_image_preview.width(), self.in_image_preview.height(),Qt.KeepAspectRatio)
       
        self.in_image_preview.setPixmap(self.placeholder_image_pixmap)
        self.in_image_preview.setStyleSheet(self.border_style)

        #label - text box for hiding data
        self.input_label = QLabel("Type Message")
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Enter message to hide...")
        self.message_input.setStyleSheet(self.border_style)

        #label - text box for showing hiddin data
        self.input_label1 = QLabel("Extracted Message")
        self.message_output = QTextEdit()
        self.message_output.setPlaceholderText("Hidden message will be shown here...")
        self.message_output.setStyleSheet(self.border_style)

        #label - button for selecting image
        self.select_image_button = QPushButton("Select Image")
        self.select_image_button.clicked.connect(self.select_image)

        #label - button for saving image
        self.save_image_button = QPushButton("Save Image")
        self.save_image_button.clicked.connect(self.save_image)

        #label - button for hiding message
        self.hide_data_button = QPushButton("Hide Data")
        self.hide_data_button.clicked.connect(self.hide_data)

        #label - button for showing message
        self.show_data_button = QPushButton("Show Data")
        self.show_data_button.clicked.connect(self.show_data)

        #Grid Layout
        layout = QGridLayout()
        layout.addWidget(self.image_title,0,0,1,2)
        layout.addWidget(self.in_image_preview,1,0,3,2)
        layout.addWidget(self.input_label,0,2,1,2)
        layout.addWidget(self.message_input,1,2,1,4)
        layout.addWidget(self.hide_data_button,1,6,1,2)
        layout.addWidget(self.input_label1,2,2,1,2)
        layout.addWidget(self.message_output,3,2,1,4)
        layout.addWidget(self.show_data_button,3,6,1,2)
        layout.addWidget(self.select_image_button,4,0,1,2)
        layout.addWidget(self.save_image_button,5,0,1,2)
        self.setLayout(layout)

        self.setWindowTitle("Invisible Scripts")
        self.show()

    def select_image(self):
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if self.image_path:
            self.display_preview()

    def save_image(self, image):
        try:
            self.output_path, _ = QFileDialog.getSaveFileName(
                self, "Save Stego Image", "", "Image Files (*.png *.jpg *.jpeg)"
            )
            if self.output_path:
                image.save(self.output_path)
                message = QMessageBox()
                message.setText("Image saved successfully!")
                message.exec_()  # Ensure message box is displayed
        except (FileNotFoundError, IOError) as e:
            message = QMessageBox()
            message.setText(f"Error saving image: {e}")
            message.exec_()

    def display_preview(self):
        pixmap = QPixmap(self.image_path)
        # Resize the image to fit the label (optional)
        pixmap = pixmap.scaled(self.in_image_preview.width(), self.in_image_preview.height(), Qt.KeepAspectRatio)
        self.in_image_preview.setPixmap(pixmap)

    def hide_data(self):
        self.en_message = self.message_input.toPlainText()
        self.message_input.setText("")
        self.msg_length = len(self.en_message)
        if (not self.image_path or not self.en_message):
            message = QMessageBox()
            message.setText("Please select an image and enter a message.")
            message.exec_()
            return

        
        image = Image.open(self.image_path).convert("RGB")

        
        message_bits = "".join(format(ord(char), '08b') for char in self.en_message)

       
        width, height = image.size
        i = 0
        for y in range(height):
            for x in range(width):
                if i < len(message_bits):
                    
                    r, g, b = image.getpixel((x, y))
                    new_r = r & ~1 | int(message_bits[i])
                    image.putpixel((x, y), (new_r, g, b))
                    i += 1

        
        self.output_path,_ = QFileDialog.getSaveFileName(self, "Save Stego Image", "", "Image Files (*.png *.jpg *.jpeg)")
        image.save(self.output_path)

    def show_data(self):
            if not self.image_path:
                message = QMessageBox()
                message.setText("Please select an image first.")
                message.exec_()
                return

            
            image = Image.open(self.image_path).convert("RGB")

        
            extracted_bits = ""
            width, height = image.size
            for y in range(height):
                for x in range(width):
                    r, g, b = image.getpixel((x, y))
                    extracted_bits += str(r & 1)

            # Convert binary to characters
            extracted_message = "".join(chr(int(extracted_bits[i:i+8], 2)) for i in range(0, len(extracted_bits), 8))
            # Display extracted message
            self.message_output.setText(extracted_message)
            print(f"Extracted message: {extracted_message}")

if __name__ == "__main__":
    app = QApplication([])
    window = SteganographyApp()
    app.exec_()
