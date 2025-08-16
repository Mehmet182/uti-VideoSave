import time


class FPSCounter:
    def __init__(self, update_interval=1.0):
        self.update_interval = update_interval
        self.frame_count = 0
        self.total_frames = 0  # Toplam frame sayısı
        self.start_time = time.time()
        self.fps = 0.0

    def update(self):
        self.frame_count += 1
        self.total_frames += 1  # Toplam frame sayısını artır
        current_time = time.time()
        elapsed = current_time - self.start_time

        if elapsed >= self.update_interval:
            self.fps = self.frame_count / elapsed
            self.frame_count = 0  # Sadece FPS hesabı için sayacı sıfırla
            self.start_time = current_time
            print(f"FPS güncellendi: {self.fps:.2f}")
            print(f"Toplam işlenen frame: {self.total_frames}")
        else:
            print(f"Anlık frame sayısı: {self.frame_count}")
            print(f"Toplam frame sayısı: {self.total_frames}")

    def get_fps(self):
        return self.fps