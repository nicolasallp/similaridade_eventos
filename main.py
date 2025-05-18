import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
import subprocess, sys
from funcs import obter_similaridade, nltk_downloads
 
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                       'pandas', 'nltk', 'scikit-learn', 'customtkinter'])

nltk_downloads()

df = pd.read_csv("dataset/events.csv", sep=";")

class SimilaridadeEventosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Historical events")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.main_frame = ctk.CTkFrame(root, fg_color="#2b2b2b")
        self.main_frame.pack(fill="both", expand=True)
        
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Historical Events", 
            font=("Arial", 28, "bold")
        )
        self.title_label.pack(pady=(20, 20))
        
        # Frame input
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.pack(pady=(0, 20))
        
        # Aceitar apenas números ao pressionar uma tecla
        def on_key_press(event):
            if event.char.isdigit() or event.keysym in ('BackSpace', 'Delete', 'Left', 'Right'):
                return
            else:
                return "break"

        # Caixa input
        self.content_entry = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Enter a year (1-2024)",
            width=250,
            font=("Arial", 18)
        )
        self.content_entry.pack(side="left", expand=True, fill="y")
        self.content_entry.bind("<Key>", on_key_press)
        self.content_entry.bind("<Return>", lambda e: self.load_data(0))
        
        # Botão 'List events'
        self.generate_btn = ctk.CTkButton(
            self.input_frame, 
            text="List events", 
            font=("Arial", 18, "bold"),
            command=lambda: self.load_data(0),
            height=50
        )
        self.generate_btn.pack(side="left", expand=True, fill="y", padx=(5, 0))
        
        # Frame paginação
        self.pagination_frame = ctk.CTkFrame(self.main_frame, height=0)
        self.pagination_frame.pack(fill="x", padx=20, pady=(0, 10))

        # Frame eventos - lado esquerdo
        self.left_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.left_frame.pack(side="left", expand="True", fill="both")
        
        # Frame dos cards (eventos) - lado esquerdo
        self.cards_left_frame = ctk.CTkScrollableFrame(
            self.left_frame, 
            orientation="vertical",
            fg_color="#333333"
        )
        self.cards_left_frame.pack(fill="both", expand=True, padx=20)

        # Frame eventos - lado direito
        self.right_frame = ctk.CTkFrame(self.main_frame)
        self.right_frame.pack(side="right", expand="True", fill="both", pady=(0,0))

        # Frame dos cards (eventos) - lado direito
        self.cards_right_frame = ctk.CTkScrollableFrame(
          self.right_frame, 
          orientation="vertical",
          fg_color="#333333"
        )
        self.cards_right_frame.pack(fill="both", expand=True, padx=20)
    

    def load_data(self, page):
      # Remover todos os cards renderizados (caso houver)
      for card in self.cards_left_frame.winfo_children():
        card.destroy()

      # Remover todos os botões da paginação (caso houver)
      for p in self.pagination_frame.winfo_children():
        p.destroy()
      content = self.content_entry.get()
      
      if not content:
        messagebox.showwarning("Warning", "Please enter a valid year")
        return
      
      pages = self.pagination(content)
      self.list_events(content, pages[page])
        
    def pagination(self, year_input):
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        pages = []
        # Obtém todos os eventos do ano fornecido no parâmetro 'year_input'
        year_df = df[(df["Year"] == int(year_input))]
        for m in months:
            # Verifica se existe um evento no mês lido (m)
            if year_df["Date"].str.contains(m).any():
              # O mês é inserido na lista 'pages'
              pages.append(m)
              btn = ctk.CTkButton(
                  self.pagination_frame,
                  text=m,
                  width=50,
                  command=lambda page=len(pages)-1: self.load_data(page)
              )
              btn.pack(side="left", padx=2)
        # Retorna uma lista de todos os meses onde há eventos
        return pages

    def list_events(self, year_input, month):
        # Obtém todos os eventos do ano e mês fornecidos
        month_df = df[(df["Year"] == int(year_input)) & (df["Date"].str.contains(month))]
        # Ordena a data dos eventos
        month_df['date_num'] = month_df['Date'].str.extract(r'(\d+)').astype(int)
        month_df = month_df.sort_values('date_num').drop(columns='date_num')
        for _, row in month_df[["Year", "Date", "Event"]].iterrows():
          year =  row["Year"]
          date = row["Date"]
          event = row["Event"]

          card = ctk.CTkFrame(self.cards_left_frame, corner_radius=10)
          card.pack(fill="x", expand=True, pady=10, padx=5)

          def on_enter(e, card=card):
              card.configure(border_width=2, border_color="#1f6aa5", fg_color="#505050")

          def on_leave(e, card=card):
              card.configure(border_width=0, border_color="#000000", fg_color="#2b2b2b")
              
          def on_click(e, event=event):
            list_similarity_events(event)

          card.bind("<Enter>", on_enter)
          card.bind("<Leave>", on_leave)
          card.bind("<Button-1>", on_click)

          card_title = ctk.CTkLabel(
              card, 
              text=f"{year} ({date})",
              font=("Arial", 20, "bold"),
              anchor="w"
          )
          card_title.pack(fill="x", padx=10, pady=(10, 5))

          card_content = ctk.CTkLabel(
              card, 
              text=event.replace('\n', ''),
              font=("Arial", 16),
              anchor="w",
              justify='left',
              wraplength=700
          )
          card_content.pack(fill="x", padx=10, pady=(0, 10))

          # Efeito hover para todos os elementos filhos dos cards
          for widget in (card_title, card_content):
              widget.bind("<Enter>", lambda e, card=card: on_enter(e, card))
              widget.bind("<Leave>", lambda e, card=card: on_leave(e, card))
              widget.bind("<Button-1>", lambda e, event=event: on_click(e, event))

          def list_similarity_events(content):
            for c in self.cards_right_frame.winfo_children():
              c.destroy()

            similaridade = obter_similaridade(content, df, 15)
            
            for _, row in similaridade[["Year", "Date", "Event"]].iterrows():
              year =  row["Year"]
              date = row["Date"]
              event = row["Event"]

              card = ctk.CTkFrame(self.cards_right_frame,
                                  corner_radius=10,
                                  border_width=2,
                                  border_color="#1f6aa5",
                                  fg_color="#505050")
              card.pack(fill="x", pady=5, padx=5)

              card_title = ctk.CTkLabel(
                  card, 
                  text=f"{year} ({date})",
                  font=("Arial", 20, "bold"),
                  anchor="w"
              )
              card_title.pack(fill="x", padx=10, pady=(10, 5))
              
              card_content = ctk.CTkLabel(
                  card, 
                  text=event.replace('\n', ''),
                  font=("Arial", 16),
                  anchor="w",
                  justify='left',
                  wraplength=700
              )
              card_content.pack(fill="x", padx=10, pady=(0, 10))

if __name__ == "__main__":
    root = ctk.CTk()
    root.after(0, lambda:root.state('zoomed'))
    app = SimilaridadeEventosApp(root)
    root.mainloop()