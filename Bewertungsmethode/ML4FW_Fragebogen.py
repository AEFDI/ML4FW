
import os
import customtkinter as ctk
from ml4fw_fragebogen import ML4FWQuestionnaireApp

if __name__ == "__main__":
    main_dir = os.path.dirname(os.path.abspath(__file__))
    if main_dir.endswith("_internal"):
        main_dir = os.path.dirname(main_dir)
    root = ctk.CTk()
    app = ML4FWQuestionnaireApp(master=root, main_dir=main_dir)
    root.mainloop()
