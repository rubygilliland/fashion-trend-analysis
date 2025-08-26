import tkinter as tk
from tkinter import messagebox, ttk
from scraper import run_scraper_for_season  
from analyze import analyze_single_season, compare_seasons
from plot import plot_single_season, plot_compared_seasons
import threading, requests, matplotlib
from io import BytesIO
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image
matplotlib.use("TkAgg")


# creates and displays main frame that holds all pages
class FashionTrendAnalyzer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Fashion Trend Analyzer")

        # pink background color
        self.configure(bg="#EECACA")  

        # creates large rigid frame size
        self.geometry("1000x1000")   
        self.resizable(False, False) 

        # container to hold all pages
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # allows for positioning of widgets on grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # standardizes setup for page classes
        for F in (StartPage, AnalyzeOneSeasonPage, CompareTwoSeasonsPage, LoadingPage, ResultsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # initializes display of frames
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

# Page 1 - title and navigation buttons
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#EECACA")

        title = tk.Label(self, text="FASHION TREND ANALYZER", font=("Arial", 24, "bold"), bg="#EECACA")
        title.pack(pady=(220, 10))

        subtitle = tk.Label(self, text="using VOGUE runway data", font=("Times", 12, "bold", "italic"), bg="#EECACA")
        subtitle.pack(pady=(0,10))

        # upon action displays AnalyzeOneSeasonPage
        analyze_btn = tk.Button(self, text="analyze a show", font=("Times", 12), width=25,
                                command=lambda: controller.show_frame(AnalyzeOneSeasonPage))
        analyze_btn.pack(pady=20)

        # upon action displays CompareTwoSeasonsPage
        compare_btn = tk.Button(self, text="compare two shows", font=("Times", 12), width=25,
                                command=lambda: controller.show_frame(CompareTwoSeasonsPage))
        compare_btn.pack(pady=10)


# Page 2 - Runs analysis and plots data for a single runway season
class AnalyzeOneSeasonPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#EECACA")

        label = tk.Label(self, text="ENTER VOGUE RUNWAY SEASON TO ANALYZE", 
                         font=("Arial", 18, "bold"), bg="#EECACA")
        label.pack(pady=(220, 20))

        # entry text box for user to type existing Vogue runway season name into
        self.entry = tk.Entry(self, font=("Times", 12, "italic"), width=30)
        self.entry.pack(pady=10)

        # upon action calls run_analysis function
        analyze_btn = tk.Button(self, text="Analyze", font=("Times", 12), width=20, 
                                command=lambda: self.run_analysis(controller))
        analyze_btn.pack(pady=10)

        # upon action displays start page
        back_btn = tk.Button(self, text="Back", font=("Times", 12), command=lambda: controller.show_frame(StartPage))
        back_btn.pack(pady=10)

    # formats user-input and begins threading
    def run_analysis(self, controller):

        # formats user input for web search usability (to be used in scraper)
        show_name = self.entry.get().strip().lower().replace(" ", "-")

        # gives warning message if no input is provided
        if not show_name:
            messagebox.showwarning("Missing Input", "Please enter a season.")
            return

        # displays loading page
        controller.show_frame(LoadingPage)

        # begins threading so data can be analyzed in backend while loading bar progesses on UI
        thread = threading.Thread(target=self.run_pipeline, args=(show_name, controller), daemon=True)
        thread.start()

    # runs necessary functions for gathering desired data
    def run_pipeline(self, season, controller):
        try:

            # loading page process begins
            loading_page = controller.frames[LoadingPage]
            controller.after(0, loading_page.label.config, {"text": "Gathering data . . ."})

            # allows scraping data to be displayed on loading page
            def progress_callback(current, total, show_name, cover_url):
                controller.after(0, loading_page.update_status, current, total, show_name, cover_url)

            # runs scraper to gather a csv file path for parsing
            csv_path = run_scraper_for_season(season, progress_callback=progress_callback)

            # changes loading page title
            controller.after(0, loading_page.label.config, {"text": "Analyzing data . . ."})
            results = analyze_single_season(csv_path)  

            # when data is loaded result page is displayed
            results_page = controller.frames[ResultsPage]
            controller.after(0, results_page.display_results, results, season, False)
            controller.after(0, controller.show_frame, ResultsPage)

        # error message displays if error occurs in scraping proccess
        except Exception as e:
            controller.after(0, messagebox.showerror, "Error", str(e))

# Page 3 - runs analysis and plots data for a comparison of two seasons
class CompareTwoSeasonsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#EECACA")

        label = tk.Label(self, text="ENTER VOGUE RUNWAY SHOWS TO COMPARE", 
                         font=("Arial", 18, "bold"), bg="#EECACA")
        label.pack(pady=(220, 20))

        # entry text box for user to type existing Vogue runway season name into
        self.entry1 = tk.Entry(self, font=("Times", 12, "italic"), width=30)
        self.entry1.pack(pady=5)

        # entry text box for user to type a different existing Vogue runway season name into
        self.entry2 = tk.Entry(self, font=("Times", 12, "italic"), width=30)
        self.entry2.pack(pady=5)

        # upon action calls run_analysis function
        analyze_btn = tk.Button(self, text="Analyze", font=("Times", 12), width=20, 
                                command=lambda:self.run_analysis(controller))
        analyze_btn.pack(pady=10)

        # upon action displays start page
        back_btn = tk.Button(self, text="Back", font=("Times", 12), command=lambda: controller.show_frame(StartPage))
        back_btn.pack(pady=10)

    def run_analysis(self, controller):

        # formats user input for web search usability (to be used in scraper)
        season_1 = self.entry1.get().strip().lower().replace(" ", "-")
        season_2 = self.entry2.get().strip().lower().replace(" ", "-")

        # gives warning message if no input is provided
        if not season_1 or not season_2:
            messagebox.showwarning("Missing Input", "Please enter a season.")
            return

        # displays loading page
        controller.show_frame(LoadingPage)

        # begins threading so data can be analyzed in backend while loading bar progesses on UI
        thread = threading.Thread(target=self.run_pipeline, args=(season_1, season_2, controller), daemon=True)
        thread.start()

    def run_pipeline(self, season_1, season_2, controller):
        try:

            # loading page process begins
            loading_page = controller.frames[LoadingPage]
            controller.after(0, loading_page.label.config, {"text": "Gathering season one data . . ."})

            # allows scraping data to be displayed on loading page
            def progress_callback(current, total, show_name, cover_url):
                controller.after(0, loading_page.update_status, current, total, show_name, cover_url)

            # runs scraper to gather a csv file path for parsing
            csv_path_1 = run_scraper_for_season(season_1, progress_callback=progress_callback)

            # loading page displays that season two data scraping has begun
            controller.after(0, loading_page.label.config, {"text": "Gathering season two data . . ."})

            # runs scraper to gather a csv file path for parsing
            csv_path_2 = run_scraper_for_season(season_2, progress_callback=progress_callback)

            # changes text displayed on loading page
            controller.after(0, loading_page.label.config, {"text": "Analyzing data . . ."})
            results = compare_seasons(csv_path_1, csv_path_2)  

            # when data is loaded result page is displayed
            results_page = controller.frames[ResultsPage]
            controller.after(0, results_page.display_results, results[0], season_1, True, results[1], season_2)
            controller.after(0, controller.show_frame, ResultsPage)

        # error message displays if error occurs in scraping proccess
        except Exception as e:
            controller.after(0, messagebox.showerror, "Error", str(e))

# Page 4 - Results Page that displays final matplotlib plots of data
class ResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F5E9E9")

        # title of page
        self.label = tk.Label(self, text="Analysis Results", font=("Arial", 18, "bold"), bg = "#F5E9E9")
        self.label.pack(pady=5)

        # adds frame to place matplotlib plot onto
        self.plot_frame = tk.Frame(self, bg="#F5E9E9")
        self.plot_frame.pack(expand=True, fill = tk.BOTH)

        # upon interaction displays start page
        back_btn = tk.Button(self, text="Back to Start", command=lambda: controller.show_frame(StartPage))
        back_btn.pack(pady=20)

    def display_results(self, results_1, season_1, compare, results_2= '', season_2 = ''):

        # removes any existing plots from frame
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        # if season comparison was made display comparison graphs
        if compare:
            fig = plot_compared_seasons(results_1, season_1, results_2, season_2)

        # if single season was analyzed display single season graphs
        else:
            fig = plot_single_season(results_1, season_1)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Temp Page
class LoadingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E8C5C5")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg="#E8C5C5")
        content.pack(expand=True)

        # initialize loading page label
        self.label = tk.Label(content, text="",
                              font=("Arial", 18, "bold"), bg="#E8C5C5")
        self.label.pack(pady=(2, 5))
        
        # initialize subtitle
        self.sublabel = tk.Label(content, text="", font=("Times", 12, "italic"), bg="#E8C5C5")
        self.sublabel.pack(pady=5)

        # set loading bar color to pink
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('pink.Horizontal.TProgressbar', background="#E8C5C5")

        # create progressive loading bar
        self.progress = ttk.Progressbar(content, orient="horizontal",
                        length=300, style = 'pink.Horizontal.TProgressbar', mode="determinate")
        self.progress.pack(pady=5)

        self.image_label = tk.Label(content, bg="#E8C5C5")
        self.image_label.pack(pady=5)
        self._current_img = None
    
    # update loading bar and sublabel dynamically
    def update_status(self, current, total, show_name, cover_url=None):
        self.sublabel.config(text=f"Loading Show {current}/{total}: {show_name}")
        self.progress["value"] = (current / total) * 100

        if cover_url:
                try:
                    response = requests.get(cover_url, timeout=5)
                    response.raise_for_status()
                    print(f"Fetching cover for {show_name}: {cover_url}, status={response.status_code}")
                    pil_img = Image.open(BytesIO(response.content))
                    pil_img = pil_img.resize((167, 251))  
                    self._current_img = ImageTk.PhotoImage(pil_img)
                    self.image_label.config(image=self._current_img)
                    self.update_idletasks()  # force refresh

                except Exception as e:
                    print(f"Could not load cover image for {show_name}: {e}")
                    self.image_label.config(image="")  # fallback: clear image


if __name__ == "__main__":
    app = FashionTrendAnalyzer()
    app.mainloop()

