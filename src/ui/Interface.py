import pathlib
import tkinter
from PIL import Image, ImageTk
from review import Review
from user import User
import customtkinter as customtk
import encrypt

img_path = pathlib.Path().resolve().parent / "images/"

from tkinter import ttk

import tkinter as tk

class ScrollbarFrame(tk.Frame):
    """
    Extends class tk.Frame to support a scrollable Frame
    This class is independent from the widgets to be scrolled and
    can be used to replace a standard tk.Frame
    """
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        # The Scrollbar, layout to the right
        vsb = tk.Scrollbar(self, orient="vertical")
        vsb.pack(side="right", fill="y")

        # The Canvas which supports the Scrollbar Interface, layout to the left
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Bind the Scrollbar to the self.canvas Scrollbar Interface
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.configure(command=self.canvas.yview)

        # The Frame to be scrolled, layout into the canvas
        # All widgets to be scrolled have to use this Frame as parent
        self.scrolled_frame = tk.Frame(self.canvas, background=self.canvas.cget('bg'))
        self.canvas.create_window((4, 4), window=self.scrolled_frame, anchor="nw")

        # Configures the scrollregion of the Canvas dynamically
        self.scrolled_frame.bind("<Configure>", self.on_configure)

    def on_configure(self, event):
        """Set the scroll region to encompass the scrolled frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

class Interface(customtk.CTk):
    WIDTH = 1024
    HEIGHT = 768

    def on_closing(self, event=0):
        self.curr_user = None
        self.destroy()

    def prompt_new_review(self, title):

        self._create_new_item_Activity(title)

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

        # generates the hash of the pasword
        hash_passw = encrypt.password_hash(in_passwd)
        # Checks if the user exist
        data_user = User.user_exists(in_usr)
        # If the user does not exist, it tries to create one
        if (data_user == None):
            # If the password is not valid, then the user is not created
            if not User.password_parser(in_passwd):
                self._show_password_error_msg()
                self.login_passwd_entry.bind("<Button-1>", self._hide_password_error_msg)
                return
            print("Bienbenido, nuevo usuario!")
            # It stores the new user data in the json
            User.store_user(in_usr, hash_passw)
            # Then updates the data variable
            data_user = User.user_exists(in_usr)
        # If the user exists, checks if the password is correct
        else:
            if (data_user["password"] == hash_passw):
                print("Sesión iniciada")
            else:
                # TODO: Mensaje de usuario existe pero contraseña incorrecta
                print("Contraseña incorrecta")
                return
        # Now, generate the datakey for the user
        newkey = encrypt.generate_secret_datakey(in_passwd, data_user["salt"])
        self.curr_user = User()
        self.curr_user.username = in_usr
        self.curr_user.data_key = newkey
        self.login_frame.destroy()
        self._create_mainmenu_Activity()

    def load_image(self, path, image_size_x, image_size_y):
        """ load rectangular image with path relative to PATH """
        return ImageTk.PhotoImage(Image.open(img_path / path).resize((image_size_x, image_size_y)))

    def newitem_generate(self):
        title = self.newitem_title_label.text
        # Low cost sanitizer
        review = self.newitem_review.textbox.get("1.0", tkinter.END).\
            replace("\"", "").replace("'", "").replace(":", "")\
            .replace("{", "").replace("}", "").replace("[", "").replace("]", "")
        score = self.newitem_score_var.get()
        new_review = Review(self.curr_user)
        new_review.store_review(title, review, str(score))

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

    def _create_new_item_Activity(self, title):
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
                                                     text=title,
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
                                                      command=lambda:self.goback(self.newitem_frame))
        self.newitem_back_button.grid(row=5, column=2, pady=40, padx=180, sticky="nwe")

    def _create_mainmenu_Activity(self):
        self.mainmenu_frame = customtk.CTkFrame(master=self, width=Interface.WIDTH)
        # 3 columns the middle one more important
        self.mainmenu_frame.columnconfigure(0, weight=0)
        self.mainmenu_frame.columnconfigure(1, weight=1)
        self.mainmenu_frame.columnconfigure(2, weight=0)
        # set master
        self.mainmenu_frame.grid(row=0, column=0, sticky="news", padx=20, pady=20)
        # generate subframes
        self.mainmenu_leftframe = customtk.CTkFrame(master=self.mainmenu_frame)
        self.mainmenu_centralframe = customtk.CTkFrame(master=self.mainmenu_frame)
        self.mainmenu_rightframe = customtk.CTkFrame(master=self.mainmenu_frame)
        # set subframes
        self.mainmenu_leftframe.grid(column=0, row=0, sticky="nwes", padx=10, pady=20)
        self.mainmenu_centralframe.grid(column=1, row=0, sticky="nwes", padx=10, pady=20)
        self.mainmenu_rightframe.grid(column=2, row=0, sticky="nwes", padx=10, pady=20)

        self.mainmenu_centralframe.rowconfigure(0, weight=0)
        self.mainmenu_centralframe.rowconfigure(1, weight=0)
        self.mainmenu_centralframe.rowconfigure(2, weight=0)
        self.mainmenu_centralframe.columnconfigure(0, weight=0)
        self.mainmenu_centralframe.rowconfigure(1, weight=0)
        self.mainmenu_centralframe.rowconfigure(2, weight=0)

        # generate img
        self.img_avatar = self.load_image("avatar.jpg", 80, 100)
        self.img_cars = self.load_image("Cars.jpg", 80, 100)
        self.img_harrypotter = self.load_image("harrypotter.jpg", 80, 100)
        self.img_hunger = self.load_image("hunger.jpg", 80, 100)
        self.img_intocable = self.load_image("Intocable.jpg", 80, 100)
        self.img_midsomar = self.load_image("Midsommar.jpg", 80, 100)
        self.img_startwars = self.load_image("starwars.jpg", 80, 100)
        self.img_ironman = self.load_image("ironman.jpg", 80, 100)
        self.img_pacific = self.load_image("Pacificrim.jpg", 80, 100)

        # Avatar
        self.mainmenu_button_1 = customtk.CTkButton(master=self.mainmenu_centralframe,
                                                    image=self.img_avatar,
                                                    text="Avatar",
                                                    height=152,
                                                    compound="right", command=lambda: self.prompt_new_review("Avatar"))
        self.mainmenu_button_1.grid(row=0, column=0, columnspan=1, padx=5, pady=(20, 10), sticky="news")
        # Cars
        self.mainmenu_button_2 = customtk.CTkButton(master=self.mainmenu_centralframe,
                                                    image=self.img_cars,
                                                    text="Cars",
                                                    height=152,
                                                    compound="right", command=lambda: self.prompt_new_review("Cars"))
        self.mainmenu_button_2.grid(row=0, column=1, columnspan=1, padx=5, pady=(20, 10), sticky="news")
        # Hp
        self.mainmenu_button_3 = customtk.CTkButton(master=self.mainmenu_centralframe,
                                                    image=self.img_harrypotter,
                                                    text="Harry\nPotter",
                                                    height=152,
                                                    compound="right",
                                                    command=lambda: self.prompt_new_review("Harry Potter"))
        self.mainmenu_button_3.grid(row=0, column=2, columnspan=1, padx=5, pady=(20, 10), sticky="news")
        # Hunger
        self.mainmenu_button_4 = customtk.CTkButton(master=self.mainmenu_centralframe,
                                                    image=self.img_hunger,
                                                    text="Hunger\nGames",
                                                    height=152,
                                                    compound="right",
                                                    command=lambda: self.prompt_new_review("Hunger Games"))
        self.mainmenu_button_4.grid(row=1, column=0, columnspan=1, padx=5, pady=(20, 10), sticky="news")
        # Intocable
        self.mainmenu_button_5 = customtk.CTkButton(master=self.mainmenu_centralframe,
                                                    image=self.img_intocable,
                                                    text="avatar",
                                                    height=152,
                                                    compound="right",
                                                    command=lambda: self.prompt_new_review("Intocable"))
        self.mainmenu_button_5.grid(row=1, column=1, columnspan=1, padx=5, pady=(20, 10), sticky="news")
        # midsomar
        self.mainmenu_button_6 = customtk.CTkButton(master=self.mainmenu_centralframe,
                                                    image=self.img_midsomar,
                                                    text="Midsommar",
                                                    height=152,
                                                    compound="right",
                                                    command=lambda: self.prompt_new_review("Midsommar"))
        self.mainmenu_button_6.grid(row=1, column=2, columnspan=1, padx=5, pady=(20, 10), sticky="news")
        # img_startwars
        self.mainmenu_button_7 = customtk.CTkButton(master=self.mainmenu_centralframe,
                                                    image=self.img_startwars,
                                                    text="Star Wars",
                                                    height=152,
                                                    compound="right",
                                                    command=lambda: self.prompt_new_review("Star Wars"))
        self.mainmenu_button_7.grid(row=2, column=0, columnspan=1, padx=5, pady=(20, 10), sticky="news")
        # ironman
        self.mainmenu_button_8 = customtk.CTkButton(master=self.mainmenu_centralframe,
                                                    image=self.img_ironman,
                                                    text="Iron\nMan",
                                                    height=152,
                                                    compound="right",
                                                    command=lambda: self.prompt_new_review("Iron Man"))
        self.mainmenu_button_8.grid(row=2, column=1, columnspan=1, padx=5, pady=(20, 10), sticky="news")
        # img_pacific
        self.mainmenu_button_9 = customtk.CTkButton(master=self.mainmenu_centralframe,
                                                    image=self.img_pacific,
                                                    text="Pacific\nRim",
                                                    height=152,
                                                    compound="right",
                                                    command=lambda: self.prompt_new_review("Pacific Rim"))
        self.mainmenu_button_9.grid(row=2, column=2, columnspan=1, padx=5, pady=(20, 10), sticky="news")
        # end btn imgs
        # button to see reviews
        self.mainmenu_button_rev = customtk.CTkButton(master=self.mainmenu_rightframe,
                                                      text="Ver reviews",
                                                      height=30,
                                                      command=self.go_to_see_reviews)
        self.mainmenu_button_rev.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="news")


        self.mainmenu_button_crfilm = customtk.CTkButton(master=self.mainmenu_rightframe,
                                                      text="Crear película",
                                                      height=30,
                                                      command=self.go_to_create_film)

        self.mainmenu_button_crfilm.grid(row=1, column=0, columnspan=1, padx=10, pady=10, sticky="news")

    def go_to_see_reviews(self):
        self.mainmenu_frame.destroy()
        self._create_viewrev_Activity()

    def _create_viewrev_Activity(self):

        self.viewrev_frame = customtk.CTkFrame(master=self, width=Interface.WIDTH)
        self.viewrev_frame.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="news")

        self.canvas = tkinter.Canvas(self.viewrev_frame)
        self.canvas.grid(row=0, column=0, sticky="news")

        v = tkinter.Scrollbar(master=self.viewrev_frame, orient="vertical", command=self.canvas.yview)
        v.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=v.set)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        # obtenemos todas las reviews
        self.viewrev_revframes = []
        self.viewrev_labels = []
        review = Review(self.curr_user)
        user_reviews = review.find_user_reviews(self.curr_user.username)
        sbf = ScrollbarFrame(self.viewrev_frame)
        self.viewrev_frame.grid_rowconfigure(0, weight=1)
        self.viewrev_frame.grid_columnconfigure(0, weight=1)
        sbf.grid(row=0, column=0, sticky='nsew')
        frame = sbf.scrolled_frame
        for i, item in enumerate(user_reviews):
            print(f"I: {i}, Item: {item} ")
            self.viewrev_revframes.append(customtk.CTkFrame(
                master=frame,
                width=Interface.WIDTH,
                corner_radius=5
            ))
            # Add review frame
            self.viewrev_revframes[i].grid(column=0, row=i, sticky="news", padx=20, pady=20)
            # Add title label
            self.viewrev_labels.append([])
            self.viewrev_labels[i].append(
                customtk.CTkLabel(
                    master=self.viewrev_revframes[i],
                    text=item["title"],
                    text_font=("Roboto Medium", -20),
                    corner_radius=6,
                    justify=tkinter.LEFT
                )
            )
            self.viewrev_labels[i].append(
                customtk.CTkLabel(
                    master=self.viewrev_revframes[i],
                    text=item["text"],
                    text_font=("Roboto Medium", -14),
                    corner_radius=6,
                    justify=tkinter.LEFT
                )
            )
            self.viewrev_labels[i].append(
                customtk.CTkLabel(
                    master=self.viewrev_revframes[i],
                    text=f"Rating: {item['rating']}",
                    text_font=("Roboto Medium", -14),
                    corner_radius=6,
                    justify=tkinter.LEFT
                )
            )
            self.viewrev_labels[i][0].grid(column=0, row=0, sticky="news", padx=20, pady=20)
            self.viewrev_labels[i][1].grid(column=0, row=1, sticky="news", padx=20, pady=20)
            self.viewrev_labels[i][2].grid(column=0, row=2, sticky="news", padx=20, pady=20)
            # Add text


    def go_to_create_film(self):
        self.mainmenu_frame.destroy()
        self._create_crfilm_Activity()


    def _create_crfilm_Activity(self):

        self.crfilm_frame = customtk.CTkFrame(master=self, width=Interface.WIDTH)
        self.crfilm_frame.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="news")

        self.crfilm_frame.rowconfigure(0, weight=0)
        self.crfilm_frame.rowconfigure(1, weight=1)
        self.crfilm_frame.rowconfigure(2, weight=0)

        self.critem_label_review = customtk.CTkLabel(master=self.crfilm_frame,
                                                      text="Escribe el título de la nueva película: ",
                                                      text_font=("Roboto Medium", -16),
                                                      padx=15, pady=15)
        self.critem_label_review.grid(column=0, row=0, sticky="nw", padx=20, pady=20)
        self.critem_review = customtk.CTkTextbox(master=self.crfilm_frame,
                                                  padx=15,
                                                  pady=15,
                                                  text_font=("Roboto Medium", -16),
                                                  )
        self.critem_review.grid(column=0, row=1, sticky="news", padx=20, pady=5)

        self.critem_submitframe = customtk.CTkFrame(master=self.crfilm_frame)
        self.critem_submitframe.grid(column=0, row=2, sticky="nwes", padx=10, pady=20)
        self.critem_submitframe.columnconfigure(0, weight=0)
        self.critem_submitframe.columnconfigure(1, weight=0)


        self.critem_sumbit_button = customtk.CTkButton(master=self.critem_submitframe,
                                                        text="Enviar",
                                                        command=self.critem_generate)
        self.critem_sumbit_button.grid(row=0, column=0, pady=40, padx=180, sticky="nwe")
        self.critem_back_button = customtk.CTkButton(master=self.critem_submitframe,
                                                      text="Atras",
                                                      command=lambda: self.goback(self.crfilm_frame))
        self.critem_back_button.grid(row=0, column=1, pady=40, padx=180, sticky="nwe")

    def goback(self,frame):
        frame.destroy()
        self._create_mainmenu_Activity()

    def critem_generate(self):
        title = self.critem_review.textbox.get("1.0", tkinter.END)
