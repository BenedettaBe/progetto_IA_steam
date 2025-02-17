import tkinter as tk
from PIL import Image, ImageDraw
import cv2
from skimage.metrics import structural_similarity as ssim

class Quaderno:
    def __init__(self, root):
        self.root = root
        self.root.title("Draw & Compare")

        # Impostazioni della finestra di disegno
        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack()

        # Variabili per tracciare il disegno
        self.drawing = False
        self.last_x, self.last_y = None, None

        # Crea un oggetto Image per salvare il disegno
        self.image = Image.new("RGB", (600, 400), color="white")
        self.draw = ImageDraw.Draw(self.image)

        # Aggiungi eventi per il disegno a mano libera
        self.canvas.bind("<Button-1>", self.start_drawing)  # Inizia il disegno al click
        self.canvas.bind("<B1-Motion>", self.draw_on_canvas)  # Disegna durante il movimento del mouse
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)  # Ferma il disegno al rilascio del click

        # Aggiungi l'evento per premere ESC per salvare
        self.root.bind("<Escape>", self.salva_immagine)

    def start_drawing(self, event):
        self.drawing = True
        self.last_x, self.last_y = event.x, event.y

    def draw_on_canvas(self, event):
        if self.drawing:
            # Disegna sulla tela
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=2, fill="black", capstyle=tk.ROUND, smooth=True)

            # Disegna anche sull'immagine in memoria
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill="black", width=2)

            self.last_x, self.last_y = event.x, event.y

    def stop_drawing(self, event):
        self.drawing = False
        self.last_x, self.last_y = None, None

    def salva_immagine(self, event):
        # Salva l'immagine come PNG
        file_path = "immagine_disegnata.png"
        self.image.save(file_path)
        print(f"Immagine salvata come '{file_path}'.")

        # Chiamare la funzione per confrontare le immagini
        img2_path = "/Users/viola/Desktop/steam/codice/immagine5.jpg"  # Il percorso della tua foto
        self.compara_immagini(file_path, img2_path)

    def compara_immagini(self, img1_path, img2_path):
        # Funzione per calcolare la similarità tra le due immagini usando SSIM
        try:
            # Carica le immagini in scala di grigi
            img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
            img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

            if img1 is None:
                raise ValueError(f"Immagine non trovata o il file è corrotto: {img1_path}")
            if img2 is None:
                raise ValueError(f"Immagine non trovata o il file è corrotto: {img2_path}")

            # Ridimensiona le immagini per confrontarle (28x28)
            img1 = cv2.resize(img1, (28, 28))
            img2 = cv2.resize(img2, (28, 28))

            # Calcola la similarità SSIM
            score, _ = ssim(img1, img2, full=True)

            perc_sim = score * 100
            print(f"🔍 Similarità tra le immagini: {score:.4f}")

            if score == 1:
                print(f"Le immagini sono identiche ({int(perc_sim)}%)")
            elif score > 0.8:
                print(f"Le immagini sono molto simili ({int(perc_sim)}%)")
            elif score > 0.5:
                print(f"Le immagini sono abbastanza simili ({int(perc_sim)}%)")
            else:
                print(f"Le immagini sono diverse ({int(perc_sim)}%)")

        except Exception as e:
            print(f"Errore nel confronto delle immagini: {e}")

# Crea la finestra principale
root = tk.Tk()
quaderno = Quaderno(root)

# Avvia l'interfaccia grafica
root.mainloop()