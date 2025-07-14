
import customtkinter as ctk
from ml4fw_fragebogen import ML4FWQuestionnaireApp

if __name__ == "__main__":
    root = ctk.CTk()
    app = ML4FWQuestionnaireApp(master=root)
    root.mainloop()
