import time

class FPSCounter:
    def __init__(self, update_interval=4.0):
        """
        update_interval: FPS'nin kaç saniyede bir hesaplanacağını belirler.
        """
        self.update_interval = update_interval
        self.frame_count = 0
        self.start_time = time.time()
        self.fps = 0.0

    def update(self):
        # Frame geldiğinde bunu gör
        print("Frame geldi:", time.time())

        self.frame_count += 1
        current_time = time.time()
        elapsed = current_time - self.start_time

        if elapsed >= 1.0:
            self.fps = self.frame_count / elapsed
            self.frame_count = 0
            self.start_time = current_time
            print(f"FPS güncellendi: {self.fps:.2f}")
        else:
            # FPS henüz güncellenmediğinde de sayacı görelim
            print(f"FPS Counter frame count: {self.frame_count}")

    def get_fps(self):
        """
        Son hesaplanan FPS değerini döndürür.
        """
        return self.fps
