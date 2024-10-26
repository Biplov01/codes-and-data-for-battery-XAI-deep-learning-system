import tkinter as tk
from tkinter import messagebox
import joblib  # Ensure to have joblib installed
import numpy as np
from PIL import Image, ImageTk

# Load the trained model
model_path = r"D:\battery management\trained_xgb_model.pkl"
model = joblib.load(model_path)

def predict_rul(cycle_index, discharge_time, decrement, max_voltage, min_voltage, time_4_15v, time_constant_current, charging_time):
    """Predicts the RUL using the provided model."""
    input_features = np.array([[cycle_index, discharge_time, decrement, max_voltage,
                                min_voltage, time_4_15v, time_constant_current, charging_time]])
    prediction = model.predict(input_features)
    return prediction[0]

class BatteryRULPredictor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Battery RUL Predictor")
        self.geometry("400x600")  # Set the window size

        # Load and display the main image
        try:
            self.img = Image.open(r"D:\battery management\batt.png")  # Use full path to image
            self.img = self.img.resize((200, 100), Image.LANCZOS)  # Resize the image
            self.img_tk = ImageTk.PhotoImage(self.img)  # Convert image to PhotoImage
            self.image_label = tk.Label(self, image=self.img_tk)
            self.image_label.pack(pady=10)  # Add padding for aesthetics
        except Exception as e:
            print(f"Error loading main image: {e}")  # Print error if image loading fails

        # Input fields for the model
        self.create_input_fields()

        # Predict button
        self.predict_button = tk.Button(self, text="Predict", command=self.make_prediction)
        self.predict_button.pack(pady=20)

        # Add "Created by:" label
        self.created_by_label = tk.Label(self, text="Created by:", font=("Arial", 10))
        self.created_by_label.pack(anchor='e', padx=10, pady=(0, 5))  # Align to the right

        # Load and display additional images with names
        self.load_additional_images()

    def create_input_fields(self):
        """Creates input fields for the model."""
        self.input_labels = [
            "Cycle Index:",
            "Discharge Time (s):",
            "Decrement 3.6-3.4V (s):",
            "Max. Voltage Discharge (V):",
            "Min. Voltage Charge (V):",
            "Time at 4.15V (s):",
            "Time Constant Current (s):",
            "Charging Time (s):"
        ]
        
        self.input_entries = []
        for label in self.input_labels:
            lbl = tk.Label(self, text=label)
            lbl.pack()
            entry = tk.Entry(self)
            entry.pack()
            self.input_entries.append(entry)

    def load_additional_images(self):
        """Loads and displays additional images with labels."""
        # List of images and their corresponding names
        images_info = [
            (r"D:\battery management\1.jpg", "Biplov Paneru"),
            (r"D:\battery management\2.jpg", "Bishwash Paneru"),
            (r"D:\battery management\3.jpeg", "DP Sharma Mainali")
        ]

        # Create a frame to hold the images and names
        frame = tk.Frame(self)
        frame.pack(side='bottom', anchor='e', padx=10, pady=10)  # Align to bottom right

        for image_path, name in images_info:
            try:
                img = Image.open(image_path)  # Open the image
                img = img.resize((50, 50), Image.LANCZOS)  # Resize the image to be smaller
                img_tk = ImageTk.PhotoImage(img)  # Convert image to PhotoImage
                
                # Create a frame for each image and its name
                img_frame = tk.Frame(frame)
                img_frame.pack(side='left', padx=5)  # Pack images side by side

                image_label = tk.Label(img_frame, image=img_tk)
                image_label.image = img_tk  # Keep a reference to avoid garbage collection
                image_label.pack(side='top')  # Add the image label

                name_label = tk.Label(img_frame, text=name.lower(), font=("Arial", 8))  # Label in lowercase
                name_label.pack(side='top')  # Add the name label
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")

    def make_prediction(self):
        """Makes a prediction and displays the result."""
        try:
            inputs = [float(entry.get()) for entry in self.input_entries]
            prediction = predict_rul(*inputs)
            messagebox.showinfo("Prediction Result", f"The predicted RUL is: {prediction:.2f}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")

if __name__ == "__main__":
    app = BatteryRULPredictor()
    app.mainloop()
