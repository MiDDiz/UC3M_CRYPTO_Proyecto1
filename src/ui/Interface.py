import tkinter
from user import User
import customtkinter as customtk


class Interface(customtk.CTk):
    WIDTH = 1024
    HEIGHT = 768

    def on_closing(self, event=0):
        self.destroy()

    def entry_event(self):
        # TODO: Eliminar prints
        """
        Here can happen 3 things:
            - New user -> Generate new user and continue as normal
            - Old user good passwd -> We got an old user correct info and continue as normal
            - Old user bad info -> We got bad info, we need to notify it and wait again for an entry_event.
        :return: None
        """
        in_usr = self.login_user_entry.get()
        in_passwd = self.login_passwd_entry.get()
        # print("Button pressed! Getting values: " + in_usr + " + " + in_passwd)
        if not User.password_parser(in_passwd):
            #    print("Bad passwd!")
            self._show_password_error_msg()
            self.login_passwd_entry.bind("<Button-1>", self._hide_password_error_msg)
            return
        # TODO: Checkear contra usuarios actuales
        self.login_frame.destroy()
        self._create_new_item_Activity()

    def newitem_generate(self):
        title = self.newitem_title_label.text
        review = self.newitem_review.textbox.get("1.0", tkinter.END)
        score = self.newitem_score_var.get()
        print(f"Title: {title}, review: {review} Score: {score}")

    def newitem_goback(self):
        print("Atras")

    def __init__(self):
        super().__init__()

        self._initial_hooks()
        self._create_entrform()

    def _initial_hooks(self):
        self.title("Netlix's Library")
        self.geometry(f"{Interface.WIDTH}x{Interface.HEIGHT}")
        self.protocol("WN_DELETE_WINDOW", self.on_closing)
        self.resizable(False, False)
        customtk.set_appearance_mode("Dark")

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

    def _show_password_error_msg(self):
        self.login_bad_passwd_label = customtk.CTkLabel(master=self.login_info,
                                                        text="|La contraseña no es correcta!",
                                                        text_font=("Roboto Medium", -16),
                                                        text_color="red",
                                                        corner_radius=6,
                                                        justify=tkinter.LEFT)
        self.login_bad_passwd_label.grid(column=1, row=5, sticky="nwe", padx=15, pady=5)
        self.login_passwd_explanation = customtk.CTkLabel(master=self.login_info,
                                                          text="Debe tener menos de 8 carácteres, "
                                                               "debe contener una mayuscula, una minuscula, un digito y un "
                                                               "carácter especial soportado.\nLos carácteres soportados son: !@#$&*. Así mismo ,no puedes tener una contraseña muy común!",
                                                          text_font=("Roboto Medium", -10),
                                                          text_color="#%02x%02x%02x" % (255, 153, 153),
                                                          corner_radius=6,
                                                          justify=tkinter.LEFT)
        self.login_passwd_explanation.grid(column=1, row=6, sticky="nwe", padx=15, pady=5)

    # Para eliminar los labels que notifican
    def _hide_password_error_msg(self, arg):
        try:
            if (self.login_passwd_explanation):
                self.login_passwd_explanation.destroy()
        except AttributeError:
            pass
        try:
            if (self.login_bad_passwd_label):
                self.login_bad_passwd_label.destroy()
        except AttributeError:
            pass

    def _create_new_item_Activity(self):
        """
        Esta es la funcion principal de create new Item
        :return:
        """
        # main frame
        self.newitem_frame = customtk.CTkFrame(master=self, width=Interface.WIDTH)
        self.newitem_frame.columnconfigure(0, weight=0)
        self.newitem_frame.columnconfigure(1, weight=1)
        self.newitem_frame.columnconfigure(2, weight=0)
        self.newitem_frame.grid(row=0, column=0, sticky="news", padx=20, pady=20)
        # title frame
        self.newitem_toptitle_frame = customtk.CTkFrame(master=self.newitem_frame,
                                                        corner_radius=6,
                                                        width=800)
        self.newitem_top_label = customtk.CTkLabel(master=self.newitem_toptitle_frame,
                                                   text="Creando una nueva reseña de: ",
                                                   text_font=("Roboto Medium", -16),
                                                   justify=tkinter.LEFT)
        self.newitem_top_label.grid(column=1, row=0, sticky="nwe", padx=15, pady=15)
        self.newitem_title_label = customtk.CTkLabel(master=self.newitem_toptitle_frame,
                                                     text="TOP GUN",  # TODO: sacar el titulo del activity.
                                                     text_font=("Roboto Medium", -20),
                                                     justify=tkinter.LEFT)
        self.newitem_top_label.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)
        self.newitem_title_label.grid(column=0, row=1, sticky="nwe", padx=15, pady=15)
        self.newitem_toptitle_frame.grid(column=0, columnspan=3, row=0, sticky="nwe", padx=60, pady=15)
        # end title frame
        self.newitem_label_review = customtk.CTkLabel(master=self.newitem_frame,
                                                      text="Escribe tu reseña: ",
                                                      text_font=("Roboto Medium", -16),
                                                      padx=15, pady=15)
        self.newitem_label_review.grid(column=0, row=1, columnspan=3, sticky="nw", padx=20, pady=20)
        self.newitem_review = customtk.CTkTextbox(master=self.newitem_frame,
                                                  padx=15,
                                                  pady=15,
                                                  text_font=("Roboto Medium", -16),
                                                  )
        self.newitem_review.grid(column=0, row=2, columnspan=3, sticky="news", padx=20, pady=5)
        self.newitem_label_score = customtk.CTkLabel(master=self.newitem_frame,
                                                     text="Anota tu puntuación: ",
                                                     text_font=("Roboto Medium", -16),
                                                     padx=15, pady=15)
        self.newitem_label_score.grid(column=0, row=3, columnspan=3, sticky="nw", padx=20, pady=10)

        self.newitem_score_var = tkinter.IntVar(value=0)
        self.newitem_score_frame = customtk.CTkFrame(master=self.newitem_frame,
                                                     corner_radius=6,
                                                     width=800)
        self.newitem_score_frame.grid(column=0, row=4, columnspan=3, sticky="nwe", padx=20, pady=10)
        self.newitem_score_1 = customtk.CTkRadioButton(master=self.newitem_score_frame,
                                                       variable=self.newitem_score_var,
                                                       value=1,
                                                       text="⭐")
        self.newitem_score_frame.columnconfigure(0, weight=1)
        self.newitem_score_frame.columnconfigure(6, weight=1)
        self.newitem_score_1.grid(row=0, column=1, pady=10, padx=10, sticky="nwe")

        self.newitem_score_2 = customtk.CTkRadioButton(master=self.newitem_score_frame,
                                                       variable=self.newitem_score_var,
                                                       value=2,
                                                       text="⭐⭐")
        self.newitem_score_2.grid(row=0, column=2, pady=10, padx=10, sticky="nwe")

        self.newitem_score_3 = customtk.CTkRadioButton(master=self.newitem_score_frame,
                                                       variable=self.newitem_score_var,
                                                       value=3,
                                                       text="⭐⭐⭐")
        self.newitem_score_3.grid(row=0, column=3, pady=10, padx=10, sticky="nwe")

        self.newitem_score_4 = customtk.CTkRadioButton(master=self.newitem_score_frame,
                                                       variable=self.newitem_score_var,
                                                       value=4,
                                                       text="⭐⭐⭐⭐")
        self.newitem_score_4.grid(row=0, column=4, pady=10, padx=10, sticky="nwe")

        self.newitem_score_5 = customtk.CTkRadioButton(master=self.newitem_score_frame,
                                                       variable=self.newitem_score_var,
                                                       value=5,
                                                       text="⭐⭐⭐⭐⭐")
        self.newitem_score_5.grid(row=0, column=5, pady=10, padx=10, sticky="nwe")

        self.newitem_sumbit_button = customtk.CTkButton(master=self.newitem_frame,
                                                        text="Enviar",
                                                        command=self.newitem_generate)
        self.newitem_sumbit_button.grid(row=5, column=0, pady=40, padx=180, sticky="nwe")
        self.newitem_back_button = customtk.CTkButton(master=self.newitem_frame,
                                                      text="Atras",
                                                      command=self.newitem_goback)
        self.newitem_back_button.grid(row=5, column=2, pady=40, padx=180, sticky="nwe")
