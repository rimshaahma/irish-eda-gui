# Class for Irish dataset preprocessing and EDA with GUI
import tkinter as tk  # This imports the tkinter module and gives it the alias 'tk'

class IrishEDAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Irish Dataset EDA Tool")
        self.data = None

        # Upload Button
        upload_btn = tk.Button(root, text="Upload CSV", command=self.upload_csv, width=20, bg="blue", fg="white")
        upload_btn.pack(pady=20)

        # Show Data Button
        show_data_btn = tk.Button(root, text="Show Data", command=self.show_data, width=20, bg="green", fg="white")
        show_data_btn.pack(pady=10)

        # EDA Button
        eda_btn = tk.Button(root, text="Perform EDA", command=self.perform_eda, width=20, bg="purple", fg="white")
        eda_btn.pack(pady=10)

    def upload_csv(self):
        # Open file dialog to upload CSV file
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)
            messagebox.showinfo("Success", "CSV loaded successfully!")
        else:
            messagebox.showwarning("Error", "No file selected!")

    def show_data(self):
        # Display the first 5 rows of the dataset
        if self.data is not None:
            print(self.data.head())
            messagebox.showinfo("Data Head", "First 5 rows printed in console.")
        else:
            messagebox.showerror("Error", "No data loaded!")

    def perform_eda(self):
        if self.data is not None:
            # Show Missing Values
            print("\nMissing Values:")
            print(self.data.isnull().sum())

            # Fill missing numerical values with median
            numerical_columns = self.data.select_dtypes(include=['float64', 'int64']).columns
            for col in numerical_columns:
                if self.data[col].isnull().sum() > 0:
                    self.data[col].fillna(self.data[col].median(), inplace=True)
            print("\nFilled missing numerical data")

            # Fill missing categorical values with mode
            categorical_columns = self.data.select_dtypes(include=['object']).columns
            for col in categorical_columns:
                if self.data[col].isnull().sum() > 0:
                    self.data[col].fillna(self.data[col].mode()[0], inplace=True)
            print("\nFilled missing categorical data")

            # Encoding categorical variables using One-Hot Encoding
            self.data = pd.get_dummies(self.data, drop_first=True)
            print("\nApplied One-Hot Encoding to categorical variables")

            # Encoding categorical variables using Label Encoding
            label_encoder = LabelEncoder()
            for col in categorical_columns:
                if self.data[col].dtype == 'object':
                    self.data[col] = label_encoder.fit_transform(self.data[col])
            print("\nApplied Label Encoding to categorical variables")

            # Feature Normalization using Min-Max Scaler
            scaler = MinMaxScaler()
            self.data[numerical_columns] = scaler.fit_transform(self.data[numerical_columns])
            print("\nNormalized numerical features using Min-Max Scaling")

            # Create a new feature 'Title' extracted from a column (assuming 'Name' exists)
            if 'Name' in self.data.columns:
                self.data['Title'] = self.data['Name'].apply(lambda x: x.split(',')[1].split('.')[0].strip())
                print("\nExtracted 'Title' feature from 'Name' column")

            # Create 'FamilySize' feature by combining 'SibSp' and 'Parch'
            if 'SibSp' in self.data.columns and 'Parch' in self.data.columns:
                self.data['FamilySize'] = self.data['SibSp'] + self.data['Parch']
                print("\nCreated 'FamilySize' feature")

            # Correlation Heatmap for numerical features
            correlation_matrix = self.data.corr(numeric_only=True)
            plt.figure(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
            plt.title("Correlation Heatmap")
            plt.show()

        else:
            messagebox.showerror("Error", "No data loaded!")
# Run the GUI
root = tk.Tk()
app = IrishEDAApp(root)
root.mainloop()
