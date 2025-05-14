import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
from funcs import obter_similaridade

df = pd.read_csv("dataset/events.csv", sep=";")

class SimilaridadeEventosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Eventos históricos")

        # Set appearance
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(root, fg_color="#2b2b2b")
        self.main_frame.pack(fill="both", expand=True)
        
        # Title label
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Historical Events", 
            font=("Arial", 28, "bold")
        )
        self.title_label.pack(pady=(20, 20))
        
        # Input frame
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.pack(pady=(0, 20))
        
        def on_key_press(event):
            # Allow control keys (backspace, delete, etc.)
            if event.char.isdigit() or event.keysym in ('BackSpace', 'Delete', 'Left', 'Right'):
                return
            else:
                return "break"

        # Content input
        self.content_entry = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Enter a year (1-2024)",
            width=250,
            font=("Arial", 18)
        )
        self.content_entry.pack(side="left", expand=True, fill="y")
        self.content_entry.bind("<Key>", on_key_press)
        self.content_entry.bind("<Return>", lambda e: self.list_events())
        
        # Generate button
        self.generate_btn = ctk.CTkButton(
            self.input_frame, 
            text="Search", 
            font=("Arial", 18, "bold"),
            command=self.list_events,
            height=50
        )
        self.generate_btn.pack(side="left", expand=True, fill="y", padx=(5, 0))
        
        # Cards frame (scrollable)
        self.left_frame = ctk.CTkFrame(self.main_frame)
        self.left_frame.pack(side="left", expand="True", fill="both")

        self.right_frame = ctk.CTkFrame(self.main_frame)
        self.right_frame.pack(side="right", expand="True", fill="both")

        self.cards_left_frame = ctk.CTkScrollableFrame(
            self.left_frame, 
            orientation="vertical",
            fg_color="#333333"
        )
        self.cards_left_frame.pack(fill="both", expand=True, padx=20)

        self.cards_right_frame = ctk.CTkScrollableFrame(
          self.right_frame, 
          orientation="vertical",
          fg_color="#333333"
        )
        self.cards_right_frame.pack(fill="both", expand=True, padx=20)
    
    def list_events(self):
        for card in self.cards_left_frame.winfo_children():
          card.destroy()
        content = self.content_entry.get()
        
        if not content:
          messagebox.showwarning("Warning", "Please enter a valid year")
          return
        
        #similaridade = obter_similaridade(content, df, 30)
        
        for _, row in df[df["Year"] == int(content)][["Year", "Date", "Event"]].iterrows():
          year =  row["Year"]
          date = row["Date"]
          event = row["Event"]

          # Create card frame
          card = ctk.CTkFrame(self.cards_left_frame, corner_radius=10)
          card.pack(fill="x", expand=True, pady=10, padx=5)

          # Store original border settings
          card.original_border_width = 0
          card.original_border_color = "#000000"

          # Hover functions (defined inside the loop)
          def on_enter(e, card=card):  # Pass card as default argument
              card.configure(border_width=2, border_color="#1f6aa5", fg_color="#505050")

          def on_leave(e, card=card):  # Pass card as default argument
              card.configure(border_width=card.original_border_width, 
                          border_color=card.original_border_color,
                          fg_color="#2b2b2b")

          # Bind events to this card
          card.bind("<Enter>", on_enter)
          card.bind("<Leave>", on_leave)

          # Card title
          card_title = ctk.CTkLabel(
              card, 
              text=f"{year} ({date})",
              font=("Arial", 20, "bold"),
              anchor="w"
          )
          card_title.pack(fill="x", padx=10, pady=(10, 5))

          # Card content
          card_content = ctk.CTkLabel(
              card, 
              text=event.replace('\n', ''),
              font=("Arial", 16),
              anchor="w",
              justify='left',
              wraplength=700
          )
          card_content.pack(fill="x", padx=10, pady=(0, 10))

          # Make child widgets propagate hover events
          for widget in (card_title, card_content):
              widget.bind("<Enter>", lambda e, card=card: on_enter(e, card))
              widget.bind("<Leave>", lambda e, card=card: on_leave(e, card))

          def on_click(e,event=event):
            list_sim_events(event)

          card.bind("<Button-1>", on_click)
          for widget in (card_title, card_content):
              widget.bind("<Button-1>", lambda e, event=event: on_click(e, event))

          def list_sim_events(content):
            for c in self.cards_right_frame.winfo_children():
              c.destroy()

            recomendacao = obter_similaridade(content, df, 30)
            
            for _, row in recomendacao[["Year", "Date", "Event"]].iterrows():
              year =  row["Year"]
              date = row["Date"]
              event = row["Event"]

                            # Create card frame
              card2 = ctk.CTkFrame(self.cards_right_frame,
                                  corner_radius=10,
                                  border_width=2,
                                  border_color="#1f6aa5",
                                  fg_color="#505050")
              card2.pack(fill="x", pady=5, padx=5)

              card_title = ctk.CTkLabel(
                  card2, 
                  text=f"{year} ({date})",  # Auto-generated title
                  font=("Arial", 20, "bold"),
                  anchor="w"
              )
              card_title.pack(fill="x", padx=10, pady=(10, 5))
              
              # Card content
              card_content = ctk.CTkLabel(
                  card2, 
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