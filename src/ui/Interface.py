import pathlib
import tkinter
from PIL import Image, ImageTk
import film
import json_store
from review import Review
from user import User
import customtkinter as customtk
import encrypt
from film import Film
import tkinter as tk

img_path = pathlib.Path().resolve().parent / "images/"
review_path = pathlib.Path().resolve().parent / "storage/items.json"

class Interface(customtk.CTk):
    WIDTH = 1024
    HEIGHT = 768

	def __init__(self):
		# Generate initial hooks, generate entry login form
        super().__init__()
        self._initial_hooks()
        self._create_entrform()

    def on_closing(self, event=0):
		# Cleanup
        self.curr_user = None
        self.destroy()

    def prompt_new_review(self, title):
		# Go to newitem activity
        self._create_new_item_Activity(title)

    def entry_event(self):
        """
		Login entry logic
        Here can happen 3 things:
            - New user -> Generate new user and continue as normal
            - Old user good passwd -> We got an old user correct info and continue as normal
            - Old user bad info -> We got bad info, we need to notify it and wait again for an entry_event.
        :return: None
        """
		#TODO: This logic should not be handled by an interface method!!! Maybe refactor into user?
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
            print("Bienvenido, nuevo usuario!")
            # It stores the new user data in the json
            User.store_user(in_usr, hash_passw, in_passwd)
            # Then updates the data variable
            data_user = User.user_exists(in_usr)
        # If the user exists, checks if the password is correct
        else:
            if (data_user["password"] == hash_passw):
                print("Sesión iniciada")
            else:
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
		"""
			helper function to create a new item
		"""
        title = self.newitem_title_label.text
        score = self.newitem_score_var.get()
        new_review = Review(self.curr_user)
        new_review.store_review(title, review, str(score))
        self.goback(self.newitem_frame)

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
        # self.mainmenu_centralframe.rowconfigure(0, weight=0)
        # self.mainmenu_centralframe.rowconfigure(1, weight=0)
        # self.mainmenu_centralframe.rowconfigure(2, weight=0)
        # self.mainmenu_centralframe.columnconfigure(0, weight=0)
        # self.mainmenu_centralframe.columnconfigure(1, weight=0)
        # self.mainmenu_centralframe.columnconfigure(2, weight=0)
		# generate img
        self.default_img = self.load_image("avatar.jpg", 80, 100)
        canvas = tk.Canvas(self.mainmenu_centralframe, bg="black", width=700, height=self.HEIGHT-30, highlightthickness=0)
        scrolly = tk.Scrollbar(self.mainmenu_centralframe, orient='vertical', command=canvas.yview)
        # dynamically generate a film button for each film stored
        all_films = Film.get_all_films()
        film_buttons = []
		film_frames = []
		column_flag = 0
		row_start = 10
        # generate film buttons
		for film in all_films:
            # first check signature
            signature = encrypt.text_to_bytes(film["signature"])
            creador = User.user_exists(film["creador"])
            check = encrypt.verify_signature(
                signature=signature,
                message=encrypt.text_to_bytes(
                    str(Film(film["title"], film["creador"]).film_item)
                ),
                public_key=encrypt.deserialize_public_key(creador["ku"])
            )
            if not check:
                # Check for signature faild -> Malicious database. Inside check raises error
                pass
			film_frames.append(
				customtk.CTkFrame(
            		master=canvas,
            		width=340,
            		corner_radius=5
            	)
			)
            film_buttons.append(
                customtk.CTkButton(
					# master is last appended frame
					master=film_frames[-1],
                    image=self.default_img,
                    text=film["title"],
                    height=152,
					width=300,
                    compound="right", command=lambda: self.prompt_new_review(film["title"])
				)
            )
			film_buttons[-1].grid(column=0, row=0, sticky="news", padx=20, pady=20)

			canvas.create_window(10 + column_flag * 320 , row_start + 10, anchor='nwse', window=film_frames[-1],
                                 height=180, width=340)
			row_start += 152
			column_flag = 0 if column_flag else 1
        canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scrolly.set)
        canvas.pack(fill='both', expand=True, side='left')
        scrolly.pack(fill='y', side='right')
		"""
        film_gird_x = 0
        film_gird_y = 0
        for btn_elem in film_buttons:
            # Appendearlos conforme existen
            btn_elem.grid(row=film_gird_y, column=film_gird_x, columnspan=1, padx=5, pady=(20, 10), sticky="news")
            film_gird_y += 1
            if film_gird_y == 3:
                film_gird_y = 0
                film_gird_x += 1
				"""
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
                                                      command=self.go_to_ask_password)
        self.mainmenu_button_crfilm.grid(row=1, column=0, columnspan=1, padx=10, pady=10, sticky="news")

    def go_to_see_reviews(self):
        store = json_store.JsonStore(review_path)
        if(store.find_item_usr(self.curr_user.username)==None):
            print("No hay reviews")
            return
        self.mainmenu_frame.destroy()
        self._create_viewrev_Activity()

    def _create_viewrev_Activity(self):
		"""
		Interface to see the reviews that the user had generated
		"""
        self.viewrev_main = customtk.CTkFrame(master=self, width=Interface.WIDTH)
        self.viewrev_main.grid(row=0, column=0, columnspan=1, sticky="news")
        self.viewrev_frame = customtk.CTkFrame(master=self.viewrev_main, width=Interface.WIDTH)
        self.viewrev_frame.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="news")
		# back button
        self.viewrev_backbutton = customtk.CTkButton(master=self.viewrev_main,
                                                     text="Ir atrás",
                                                     command=lambda : self.goback(self.viewrev_main)
                                                     )
        self.viewrev_backbutton.grid(row=0, column=1, columnspan=1, padx=10, pady=10, sticky="e")
		# we need to have an infinite scroll for each review generated so we need a canvas
        canvas = tk.Canvas(self.viewrev_frame, bg="black", width=self.WIDTH - 200, height=self.HEIGHT-30, highlightthickness=0)
        scrolly = tk.Scrollbar(self.viewrev_frame, orient='vertical', command=canvas.yview)
        reviews = Review(self.curr_user)
        user_reviews = reviews.find_user_reviews(self.curr_user.username)
		# Dinamically store the review label and frames used to display them
        viewrev_revframes = []
        viewrev_labels = []
        # display elements in the canvas
        for i, item in enumerate(user_reviews):
			# Remember that reviews are encoded in order to sanitize 'em for JSON
			item = Review.decode_review(item)
			# We left this print to see in terminal what is happening in the background
            print(f"I: {i}, Item: {item} ")
			# Append the frame
            viewrev_revframes.append(customtk.CTkFrame(
                master=canvas,
                width=Interface.WIDTH,
                corner_radius=5
            ))
			# Append the title
            viewrev_labels.append([])
            viewrev_labels[i].append(
                customtk.CTkLabel(
                    master=viewrev_revframes[i],
                    text=item["title"],
                    text_font=("Roboto Medium", -20),
                    corner_radius=6,
                    justify=tkinter.LEFT
                )
            )
			# Append the review
            viewrev_labels[i].append(
                customtk.CTkLabel(
                    master=viewrev_revframes[i],
                    text=item["text"],
                    text_font=("Roboto Medium", -14),
                    corner_radius=6,
                    justify=tkinter.LEFT,
                    wraplength=800
                )
            )
			# Append the score
            viewrev_labels[i].append(
                customtk.CTkLabel(
                    master=viewrev_revframes[i],
                    text=f"Rating: {item['rating']}",
                    text_font=("Roboto Medium", -14),
                    corner_radius=6,
                    justify=tkinter.LEFT
                )
            )
			# Set them on display their frame
            viewrev_labels[i][0].grid(column=0, row=0, sticky="news", padx=20, pady=20)
            viewrev_labels[i][1].grid(column=0, row=1, sticky="news", padx=20, pady=20)
            viewrev_labels[i][2].grid(column=0, row=2, sticky="news", padx=20, pady=20)
			# Set the frame on the canvas
            canvas.create_window(100, i * 350, anchor='nw', window=viewrev_revframes[i],
                                 height=300, width=self.WIDTH - 180)
            viewrev_labels.append([])
		# When canvas is filled, we can display it.
        canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scrolly.set)
        canvas.pack(fill='both', expand=True, side='left')
        scrolly.pack(fill='y', side='right')


    def _create_crfilm_Activity(self, passwd: str):
		"""
		Interface to generate a new film
		"""
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
                                                        command=lambda: self.critem_generate(passwd))
        self.critem_sumbit_button.grid(row=0, column=0, pady=40, padx=180, sticky="nwe")
        self.critem_back_button = customtk.CTkButton(master=self.critem_submitframe,
                                                      text="Atras",
                                                      command=lambda: self.goback(self.crfilm_frame))
        self.critem_back_button.grid(row=0, column=1, pady=40, padx=180, sticky="nwe")


    def critem_generate(self, passwd):
        """
        Generates a new film with the title inputed from the user.
        :return: Returns on failure
        """
        title = self.critem_review.textbox.get("1.0", tkinter.END)
        print(f"Creando nueva pelicula {title}")
        if title == "\n" or not title:
            print("No se puede generar una pelicula con titulo vacío")
            return
        new_film = Film(title, self.curr_user.username)
        new_film.sign_film(self.curr_user.get_private_key(passwd))
        new_film.store_film()
        self.goback(self.crfilm_frame)

    def go_to_ask_password(self):
        self.mainmenu_frame.destroy()
        self._ask_password_Activity()

    def _ask_password_Activity(self):
        self.passw_frame = customtk.CTkFrame(master=self, width=Interface.WIDTH)
        self.passw_frame.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="news")
        self.passw_frame.rowconfigure(0, weight=0)
        self.passw_frame.rowconfigure(1, weight=0)
        self.passw_frame.rowconfigure(2, weight=0)
        self.passw_label_review = customtk.CTkLabel(master=self.passw_frame,
                                                      text="Escribe tu contraseña: ",
                                                      text_font=("Roboto Medium", -16),
                                                      padx=15, pady=15)
        self.passw_label_review.grid(column=0, row=0, sticky="nw", padx=20, pady=20)
        self.passw_get = customtk.CTkEntry(master=self.passw_frame,
                                                    width=6,
                                                    text_font=("Roboto Medium", -16),
                                                    placeholder_text="Contraseña",
                                                    show="*"
                                                    )
        self.passw_get.grid(column=0, row=1, sticky="news", padx=20, pady=5)
        self.passw_submitframe = customtk.CTkFrame(master=self.passw_frame)
        self.passw_submitframe.grid(column=0, row=2, sticky="nwes", padx=10, pady=20)
        self.passw_submitframe.columnconfigure(0, weight=0)
        self.passw_submitframe.columnconfigure(1, weight=0)
        self.passw_sumbit_button = customtk.CTkButton(master=self.passw_submitframe,
                                                        text="Enviar",
                                                        command=self.check_and_get_passw)
        self.passw_sumbit_button.grid(row=0, column=0, pady=40, padx=180, sticky="nwe")
        self.passw_back_button = customtk.CTkButton(master=self.passw_submitframe,
                                                      text="Atras",
                                                      command=lambda: self.goback(self.passw_frame))
        self.passw_back_button.grid(row=0, column=1, pady=40, padx=180, sticky="nwe")

    def check_and_get_passw(self):
        passw = self.passw_get.get()
        hash_passw = encrypt.password_hash(passw)
        user_item= User.user_exists(self.curr_user.username)
        if user_item==None:
            print("Error al encontrar el usuario actual!")
            return
        elif user_item["password"]!=hash_passw:
            print("Contraseña incorrecta!")
            return
        self.passw_frame.destroy()
        self._create_crfilm_Activity(passw)

    def goback(self, frame):
        frame.destroy()
        self._create_mainmenu_Activity()
