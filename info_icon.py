from typing import Tuple
import customtkinter as ctk


class InfoIcon:
    """ Creates a CTk canvas that contains an info icon.

    Args:
        master (ctk.CTkFrame): The master frame for the info icon.
        icon_size (int): The size of the icon in pixels.
        window_geometry (str): The geometry of the info window (e.g., "300x200+100+100").
        text_font (Tuple[str, int, str]): The font settings for the info text, defined as a tuple
            (e.g. ("arial", 18, "bold")).
        wrap_length (int): Wrap length for info text given in number of charakters.

    Attributes:
        canvas (ctk.CTkCanvas): The canvas containing the info icon.
        info_text (str): Information that is displayed, when the info icon is clicked.
        info_window_open (bool): Indicates whether the info window is currently open.

    Methods:
        set_info_text(info_text: str):
            Sets the info text to be displayed in the info window.

        place(x_pos: int, y_pos: int):
            Places the info icon at the specified coordinates.

        create_info_icon() -> ctk.CTkCanvas:
            Creates the info icon canvas with a circular shape and "i" text.

        open_info_window(event, info_text):
            Opens a new window displaying the info text when the icon is clicked.

        close_info_window(info_window: ctk.CTkToplevel):
            Closes the info window.
    """

    def __init__(self, master: ctk.CTkFrame, icon_size: int, window_geometry: str, text_font: Tuple[str, int, str],
                 wrap_length: int):
        self.master: ctk.CTkFrame = master
        self.icon_size: int = icon_size
        self.window_geometry: str = window_geometry
        self.text_font: Tuple[str, int, str] = text_font
        self.info_text: str = ""
        self.info_window_open: bool = False
        self.canvas: ctk.CTkCanvas = self.create_info_icon()
        self.wrap_length: int = wrap_length

    def set_info_text(self, info_text: str):
        """ Sets the info text to be displayed in the info window.

        Args:
            info_text (str): The text to display when the info icon is clicked.
        """
        self.info_text = info_text

    def place(self, x_pos: int, y_pos: int):
        """ Places the info icon at the specified coordinates.

        Args:
            x_pos (int): The x-coordinate for placement.
            y_pos (int): The y-coordinate for placement.
        """
        self.canvas.place(x=x_pos, y=y_pos)

    def create_info_icon(self) -> ctk.CTkCanvas:
        """ Creates the info icon canvas with a circular shape and "i" text.

        Returns:
            ctk.CTkCanvas: The canvas containing the info icon.
        """
        self.canvas = ctk.CTkCanvas(self.master, width=self.icon_size, height=self.icon_size,
                                    highlightthickness=0, bg="#2E2E2E")

        # Define colors
        border_color = "#6495ED"
        text_color = border_color

        # Draw the circle
        self.canvas.create_oval(int(self.icon_size * 1 / 10), int(self.icon_size * 1 / 10),
                                int(self.icon_size * 9 / 10), int(self.icon_size * 9 / 10),
                                fill="white", outline=border_color, width=2)

        # Draw the "i"
        self.canvas.create_text(int(self.icon_size) / 2, int(self.icon_size) / 2, text="i",
                                font=("Arial", int(self.icon_size / 2.2), "bold"),
                                fill=text_color)
        self.canvas.bind("<Button-1>", lambda event: self.open_info_window(event, info_text=self.info_text))
        return self.canvas

    def open_info_window(self, event, info_text: str):
        """ Opens a new window displaying the info text when the icon is clicked.

        Args:
            event: The event that triggered this method.
            info_text (str): The text to display in the info window.
        """
        if not self.info_window_open:
            info_window = ctk.CTkToplevel(self.master)
            info_window.title("Information")
            info_window.geometry(self.window_geometry)
            info_label = ctk.CTkLabel(info_window, text=info_text, font=self.text_font, wraplength=self.wrap_length,
                                      justify="left")
            info_label.pack(pady=20)
            close_button = ctk.CTkButton(info_window, text="Schließen",
                                         command=lambda: self.close_info_window(info_window=info_window))
            close_button.pack(pady=10)
            info_window.attributes("-topmost", True)
            self.info_window_open = True

    def close_info_window(self, info_window: ctk.CTkToplevel):
        """ Closes the info window.

        Args:
            info_window (ctk.CTkToplevel): The window to be closed.
        """
        info_window.destroy()
        self.info_window_open = False
