import tkinter

import customtkinter as customtk


class Interface(customtk.CTk):
    WIDTH = 1024
    HEIGHT = 768

    def on_closing(self, event=0):
        self.destroy()

    def entry_event(self):
        """
        Here can happen 3 things:
            - New user -> Generate new user and continue as normal
            - Old user good passwd -> We got an old user correct info and continue as normal
            - Old user bad info -> We got bad info, we need to notify it and wait again for an entry_event.
        :return: None
        """
        print("Button pressed! Getting values: " + self.login_user_entry.get() + " + " + self.login_passwd_entry.get())

    def change_appearance_mode(self, new_appearance_mode):
        customtk.set_appearance_mode(new_appearance_mode)

    def __init__(self):
        super().__init__()

        self._initial_hooks()
        self._create_entrform()

    def _initial_hooks(self):
        self.title("Netlix's Library")
        self.geometry(f"{Interface.WIDTH}x{Interface.HEIGHT}")
        self.protocol("WN_DELETE_WINDOW", self.on_closing)
        self.resizable(False, False)

    def _create_entrform(self):
        """
        Entry form generation method.
        :return:
        """
        # Create setup
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # Create setup loginframe
        self.login_frame = customtk.CTkFrame(master=self,
                                             width=Interface.WIDTH)
        # Create place loginframe
        self.login_frame.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)
        # Add loginframe padding
        self.login_frame.rowconfigure((0, 1), weight=0)
        self.login_frame.rowconfigure(5, weight=1)
        self.login_frame.columnconfigure(1, weight=1)
        # Generate login widget and set
        self.login_info = customtk.CTkFrame(master=self.login_frame)
        self.login_info.grid(row=2, column=1, rowspan=4, pady=20, padx=200, sticky="nsew")

        # login widget padding
        self.login_info.columnconfigure((0, 3), weight=10)
        # generate and place top label
        self.login_top_label = customtk.CTkLabel(master=self.login_info,
                                                 text="Por favor, introduce tus datos de entrada",
                                                 text_font=("Roboto Medium", -16),
                                                 corner_radius=6,
                                                 justify=tkinter.LEFT)
        self.login_top_label.grid(column=1, row=0, sticky="nwe", padx=15, pady=60)
        # generate and place user label and entry
        self.login_user_label = customtk.CTkLabel(master=self.login_info,
                                                  text="Usuario",
                                                  text_font=("Roboto Medium", -16),
                                                  corner_radius=6,
                                                  justify=tkinter.LEFT)
        self.login_user_label.grid(column=1, row=1, sticky="nwe", padx=15, pady=5)

        self.login_user_entry = customtk.CTkEntry(master=self.login_info,
                                                  width=6,
                                                  text_font=("Roboto Medium", -16),
                                                  placeholder_text="Nombre de usuario")
        self.login_user_entry.grid(row=2, column=1, columnspan=2, pady=5, padx=20, sticky="nswe")
        # generate and place password label and entry
        self.login_passwd_label = customtk.CTkLabel(master=self.login_info,
                                                    text="Contraseña",
                                                    text_font=("Roboto Medium", -16),
                                                    corner_radius=6,
                                                    justify=tkinter.LEFT)
        self.login_passwd_label.grid(column=1, row=3, sticky="nwe", padx=15, pady=5)

        self.login_passwd_entry = customtk.CTkEntry(master=self.login_info,
                                                    width=6,
                                                    text_font=("Roboto Medium", -16),
                                                    placeholder_text="Contraseña",
                                                    show="*"
                                                    )
        self.login_passwd_entry.grid(row=4, column=1, columnspan=2, pady=5, padx=20, sticky="nswe")
        # generate and place entry button and padding
        self.button_login = customtk.CTkButton(master=self.login_info,
                                               text="Entrar",
                                               command=self.entry_event)
        self.login_info.rowconfigure((5, 6), weight=2)
        self.button_login.grid(row=7, column=1, pady=10, padx=20)
        self.login_info.rowconfigure((8, 9), weight=2)
