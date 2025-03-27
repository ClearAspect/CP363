import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox


class MovieMusicStoreGUI:
    """Main GUI class for the Movie Music Store application"""

    def __init__(self):
        """Initialize the main application window and setup UI components"""
        self.root = tk.Tk()
        self.root.title("Movie Music Store Management System")
        self.root.geometry("800x600")

        # Setup database connection
        self.db = self.connect_db()

        # Initialize search variables
        self.movie_search_var = tk.StringVar()
        self.music_search_var = tk.StringVar()

        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)

        # Setup tabs
        self.setup_movie_tab()
        self.setup_music_tab()

    def connect_db(
        self, use_database: bool = True
    ) -> mysql.connector.connection.MySQLConnection:
        """
        Establish database connection with error handling

        Args:
            use_database: Whether to connect to specific database or just server

        Returns:
            MySQL connection object
        """
        try:
            if use_database:
                return mysql.connector.connect(
                    host="localhost",
                    user="root",  # Replace with your username
                    password="",  # Replace with your password
                    database="MovieMusicStore",
                )
            else:
                return mysql.connector.connect(
                    host="localhost",
                    user="root",  # Replace with your username
                    password="",  # Replace with your password
                )
        except mysql.connector.Error as err:
            messagebox.showerror(
                "Database Error", f"Failed to connect to database: {err}"
            )
            return None

    def setup_movie_tab(self):
        """Setup the Movies tab with all CRUD operations"""
        movie_tab = ttk.Frame(self.notebook)
        self.notebook.add(movie_tab, text="Movies")

        # Movie Search Frame
        search_frame = ttk.LabelFrame(movie_tab, text="Search Movies", padding=10)
        search_frame.pack(fill="x", padx=5, pady=5)

        ttk.Entry(search_frame, textvariable=self.movie_search_var).pack(
            side="left", padx=5
        )
        ttk.Button(search_frame, text="Search", command=self.search_movies).pack(
            side="left"
        )

        # Movie List
        list_frame = ttk.LabelFrame(movie_tab, text="Movie List", padding=10)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        columns = (
            "ID",
            "Title",
            "Genre",
            "Release Date",
            "Rating",
            "Runtime (min)",
            "Stock",
        )
        self.movie_tree = ttk.Treeview(list_frame, columns=columns, show="headings")

        for col in columns:
            self.movie_tree.heading(col, text=col)
            self.movie_tree.column(col, width=100)

        self.movie_tree.pack(fill="both", expand=True)

        # Movie CRUD Frame
        crud_frame = ttk.Frame(movie_tab)
        crud_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            crud_frame, text="Add Movie", command=self.show_add_movie_dialog
        ).pack(side="left", padx=5)
        ttk.Button(
            crud_frame, text="Edit Movie", command=self.show_edit_movie_dialog
        ).pack(side="left", padx=5)
        ttk.Button(crud_frame, text="Delete Movie", command=self.delete_movie).pack(
            side="left", padx=5
        )

        # Load initial data
        self.refresh_movie_list()

    def setup_music_tab(self):
        """Setup the Music tab with all CRUD operations"""
        music_tab = ttk.Frame(self.notebook)
        self.notebook.add(music_tab, text="Music")

        # Music Search Frame
        search_frame = ttk.LabelFrame(music_tab, text="Search Music", padding=10)
        search_frame.pack(fill="x", padx=5, pady=5)

        ttk.Entry(search_frame, textvariable=self.music_search_var).pack(
            side="left", padx=5
        )
        ttk.Button(search_frame, text="Search", command=self.search_music).pack(
            side="left"
        )

        # Music List
        list_frame = ttk.LabelFrame(music_tab, text="Music List", padding=10)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        columns = ("ID", "Title", "Artist", "Genre", "Release Date", "Stock")
        self.music_tree = ttk.Treeview(list_frame, columns=columns, show="headings")

        for col in columns:
            self.music_tree.heading(col, text=col)
            self.music_tree.column(col, width=100)

        self.music_tree.pack(fill="both", expand=True)

        # Music CRUD Frame
        crud_frame = ttk.Frame(music_tab)
        crud_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            crud_frame, text="Add Music", command=self.show_add_music_dialog
        ).pack(side="left", padx=5)
        ttk.Button(
            crud_frame, text="Edit Music", command=self.show_edit_music_dialog
        ).pack(side="left", padx=5)
        ttk.Button(crud_frame, text="Delete Music", command=self.delete_music).pack(
            side="left", padx=5
        )

        # Load initial data
        self.refresh_music_list()

    def refresh_movie_list(self):
        """Refresh the movie list from database"""
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT movie_id, title, genre, release_date, rating, runtime_minutes, stock_count 
                FROM Movie
            """)

            # Clear existing items
            for item in self.movie_tree.get_children():
                self.movie_tree.delete(item)

            # Insert new data
            for row in cursor.fetchall():
                self.movie_tree.insert("", "end", values=row)

            cursor.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch movies: {err}")

    def refresh_music_list(self):
        """Refresh the music list from database"""
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT ma.album_id, ma.title, a.artist_name, ma.genre, ma.release_date, ma.stock_count 
                FROM MusicAlbum ma 
                LEFT JOIN Album_Artist aa ON ma.album_id = aa.album_id
                LEFT JOIN Artist a ON aa.artist_id = a.artist_id
            """)

            # Clear existing items
            for item in self.music_tree.get_children():
                self.music_tree.delete(item)

            # Insert new data
            for row in cursor.fetchall():
                self.music_tree.insert("", "end", values=row)

            cursor.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch music: {err}")

    def show_add_movie_dialog(self):
        """Show dialog for adding a new movie"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Movie")
        dialog.geometry("300x200")

        # Create input fields
        ttk.Label(dialog, text="Title:").pack()
        title_entry = ttk.Entry(dialog)
        title_entry.pack()

        ttk.Label(dialog, text="Genre:").pack()
        genre_entry = ttk.Entry(dialog)
        genre_entry.pack()

        ttk.Label(dialog, text="Release Date (YYYY-MM-DD):").pack()
        year_entry = ttk.Entry(dialog)
        year_entry.pack()

        ttk.Label(dialog, text="Rating:").pack()
        rating_entry = ttk.Entry(dialog)
        rating_entry.pack()

        ttk.Label(dialog, text="Runtime (minutes):").pack()
        runtime_entry = ttk.Entry(dialog)
        runtime_entry.pack()

        ttk.Label(dialog, text="Stock Count:").pack()
        stock_entry = ttk.Entry(dialog)
        stock_entry.pack()

        def save():
            try:
                cursor = self.db.cursor()
                cursor.execute(
                    """INSERT INTO Movie 
                       (title, genre, release_date, rating, runtime_minutes, stock_count) 
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (
                        title_entry.get(),
                        genre_entry.get(),
                        year_entry.get(),
                        rating_entry.get(),
                        runtime_entry.get(),
                        stock_entry.get(),
                    ),
                )
                self.db.commit()
                cursor.close()
                self.refresh_movie_list()
                dialog.destroy()
                messagebox.showinfo("Success", "Movie added successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to add movie: {err}")

        ttk.Button(dialog, text="Save", command=save).pack(pady=10)

    def show_add_music_dialog(self):
        """Show dialog for adding new music"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Music")
        dialog.geometry("300x250")

        # Create input fields
        ttk.Label(dialog, text="Title:").pack()
        title_entry = ttk.Entry(dialog)
        title_entry.pack()

        ttk.Label(dialog, text="Artist:").pack()
        artist_entry = ttk.Entry(dialog)
        artist_entry.pack()

        ttk.Label(dialog, text="Genre:").pack()
        genre_entry = ttk.Entry(dialog)
        genre_entry.pack()

        ttk.Label(dialog, text="Release Date (YYYY-MM-DD):").pack()
        release_date_entry = ttk.Entry(dialog)
        release_date_entry.pack()

        ttk.Label(dialog, text="Stock Count:").pack()
        stock_entry = ttk.Entry(dialog)
        stock_entry.pack()

        def save():
            try:
                cursor = self.db.cursor()
                cursor.execute(
                    """INSERT INTO MusicAlbum (title, genre, release_date, stock_count) 
                       VALUES (%s, %s, %s, %s)""",
                    (
                        title_entry.get(),
                        genre_entry.get(),
                        release_date_entry.get(),
                        stock_entry.get(),
                    ),
                )
                # Get the last inserted album_id
                album_id = cursor.lastrowid

                # Insert the artist
                cursor.execute(
                    """INSERT INTO Artist (artist_name, active_status) 
                       VALUES (%s, 'ACTIVE')
                       ON DUPLICATE KEY UPDATE artist_id=LAST_INSERT_ID(artist_id)""",
                    (artist_entry.get(),),
                )
                artist_id = cursor.lastrowid

                # Create the album-artist relationship
                cursor.execute(
                    """INSERT INTO Album_Artist (album_id, artist_id) 
                       VALUES (%s, %s)""",
                    (album_id, artist_id),
                )
                self.db.commit()
                cursor.close()
                self.refresh_music_list()
                dialog.destroy()
                messagebox.showinfo("Success", "Music added successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to add music: {err}")

        ttk.Button(dialog, text="Save", command=save).pack(pady=10)

    def show_edit_movie_dialog(self):
        """Show dialog for editing selected movie"""
        selected = self.movie_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a movie to edit")
            return

        # Get selected movie data
        movie_id = self.movie_tree.item(selected[0])["values"][0]

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Movie")
        dialog.geometry("300x200")

        # Get current values
        current_values = self.movie_tree.item(selected[0])["values"]

        # Create input fields with current values
        ttk.Label(dialog, text="Title:").pack()
        title_entry = ttk.Entry(dialog)
        title_entry.insert(0, current_values[1])
        title_entry.pack()

        ttk.Label(dialog, text="Genre:").pack()
        genre_entry = ttk.Entry(dialog)
        genre_entry.insert(0, current_values[2])
        genre_entry.pack()

        ttk.Label(dialog, text="Release Year:").pack()
        year_entry = ttk.Entry(dialog)
        year_entry.insert(0, current_values[3])
        year_entry.pack()

        ttk.Label(dialog, text="Price:").pack()
        price_entry = ttk.Entry(dialog)
        price_entry.insert(0, current_values[4])
        price_entry.pack()

        def save():
            try:
                cursor = self.db.cursor()
                cursor.execute(
                    """UPDATE Movies 
                       SET title=%s, genre=%s, release_year=%s, price=%s 
                       WHERE movie_id=%s""",
                    (
                        title_entry.get(),
                        genre_entry.get(),
                        year_entry.get(),
                        price_entry.get(),
                        movie_id,
                    ),
                )
                self.db.commit()
                cursor.close()
                self.refresh_movie_list()
                dialog.destroy()
                messagebox.showinfo("Success", "Movie updated successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to update movie: {err}")

        ttk.Button(dialog, text="Save", command=save).pack(pady=10)

    def show_edit_music_dialog(self):
        """Show dialog for editing selected music"""
        selected = self.music_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a music item to edit")
            return

        # Get selected music data
        music_id = self.music_tree.item(selected[0])["values"][0]

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Music")
        dialog.geometry("300x250")

        # Get current values
        current_values = self.music_tree.item(selected[0])["values"]

        # Create input fields with current values
        ttk.Label(dialog, text="Title:").pack()
        title_entry = ttk.Entry(dialog)
        title_entry.insert(0, current_values[1])
        title_entry.pack()

        ttk.Label(dialog, text="Artist:").pack()
        artist_entry = ttk.Entry(dialog)
        artist_entry.insert(0, current_values[2])
        artist_entry.pack()

        ttk.Label(dialog, text="Genre:").pack()
        genre_entry = ttk.Entry(dialog)
        genre_entry.insert(0, current_values[3])
        genre_entry.pack()

        ttk.Label(dialog, text="Release Year:").pack()
        year_entry = ttk.Entry(dialog)
        year_entry.insert(0, current_values[4])
        year_entry.pack()

        ttk.Label(dialog, text="Price:").pack()
        price_entry = ttk.Entry(dialog)
        price_entry.insert(0, current_values[5])
        price_entry.pack()

        def save():
            try:
                cursor = self.db.cursor()
                cursor.execute(
                    """UPDATE Music 
                       SET title=%s, artist=%s, genre=%s, release_year=%s, price=%s 
                       WHERE music_id=%s""",
                    (
                        title_entry.get(),
                        artist_entry.get(),
                        genre_entry.get(),
                        year_entry.get(),
                        price_entry.get(),
                        music_id,
                    ),
                )
                self.db.commit()
                cursor.close()
                self.refresh_music_list()
                dialog.destroy()
                messagebox.showinfo("Success", "Music updated successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to update music: {err}")

        ttk.Button(dialog, text="Save", command=save).pack(pady=10)

    def delete_movie(self):
        """Delete selected movie"""
        selected = self.movie_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a movie to delete")
            return

        if messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this movie?"
        ):
            try:
                movie_id = self.movie_tree.item(selected[0])["values"][0]
                cursor = self.db.cursor()
                cursor.execute("DELETE FROM Movie WHERE movie_id = %s", (movie_id,))
                self.db.commit()
                cursor.close()
                self.refresh_movie_list()
                messagebox.showinfo("Success", "Movie deleted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to delete movie: {err}")

    def delete_music(self):
        """Delete selected music"""
        selected = self.music_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a music item to delete")
            return

        if messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this music?"
        ):
            try:
                music_id = self.music_tree.item(selected[0])["values"][0]
                cursor = self.db.cursor()
                # Delete from Album_Artist first (cascade will handle the rest)
                cursor.execute(
                    "DELETE FROM MusicAlbum WHERE album_id = %s", (music_id,)
                )
                self.db.commit()
                cursor.close()
                self.refresh_music_list()
                messagebox.showinfo("Success", "Music deleted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to delete music: {err}")

    def search_movies(self):
        """Search movies based on title"""
        search_term = self.movie_search_var.get()
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "SELECT * FROM Movies WHERE title LIKE %s", (f"%{search_term}%",)
            )

            # Clear existing items
            for item in self.movie_tree.get_children():
                self.movie_tree.delete(item)

            # Insert matching data
            for row in cursor.fetchall():
                self.movie_tree.insert("", "end", values=row)

            cursor.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to search movies: {err}")

    def search_music(self):
        """Search music based on title or artist"""
        search_term = self.music_search_var.get()
        try:
            cursor = self.db.cursor()
            cursor.execute(
                """
                SELECT ma.album_id, ma.title, a.artist_name, ma.genre, ma.release_date, ma.stock_count 
                FROM MusicAlbum ma 
                LEFT JOIN Album_Artist aa ON ma.album_id = aa.album_id
                LEFT JOIN Artist a ON aa.artist_id = a.artist_id
                WHERE ma.title LIKE %s OR a.artist_name LIKE %s
            """,
                (f"%{search_term}%", f"%{search_term}%"),
            )

            # Clear existing items
            for item in self.music_tree.get_children():
                self.music_tree.delete(item)

            # Insert matching data
            for row in cursor.fetchall():
                self.music_tree.insert("", "end", values=row)

            cursor.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to search music: {err}")

    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    app = MovieMusicStoreGUI()
    app.run()


if __name__ == "__main__":
    main()
