import numpy as np
import cv2
import matplotlib.pyplot as plt
from pathlib import Path

class PhotoRestoration:
    """
    Хуучин зургийн чанарыг сайжруулах класс
    """
    def __init__(self):
        """
        Зураг сайжруулах классын эхлүүлэгч
        """
        self.original_image = None
        self.enhanced_image = None
        
    def load_image(self, image_path):
        """
        Зургийг файлаас ачаалах
        
        Parameters:
        -----------
        image_path : str
            Зургийн файлын зам
        
        Returns:
        --------
        self : object
            Классын объект
        """
        # Зургийг ачаалах
        self.original_image = cv2.imread(image_path)
        
        # OpenCV BGR-ээс RGB руу хөрвүүлэх
        if self.original_image is not None:
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            self.enhanced_image = self.original_image.copy()
            return self
        else:
            raise ValueError(f"Зураг ачаалахад алдаа гарлаа: {image_path}")
    
    def remove_noise(self, strength=10):
        """
        Зургаас шуугианыг арилгах
        
        Parameters:
        -----------
        strength : int, default=10
            Шуугиан арилгах хүч
        
        Returns:
        --------
        self : object
            Классын объект
        """
        # Bilateral filter ашиглан шуугиан арилгах
        self.enhanced_image = cv2.bilateralFilter(
            self.enhanced_image, 
            d=strength,  # Шүүлтүүрийн диаметр
            sigmaColor=75,  # Өнгөний сигма
            sigmaSpace=75  # Орон зайн сигма
        )
        return self
    
    def enhance_contrast(self, clip_limit=2.0, tile_grid_size=(8, 8)):
        """
        Зургийн контрастыг сайжруулах
        
        Parameters:
        -----------
        clip_limit : float, default=2.0
            Гистограмм тэгшитгэлийн хязгаарлалт
        tile_grid_size : tuple, default=(8, 8)
            Гистограмм тэгшитгэлийн блокийн хэмжээ
        
        Returns:
        --------
        self : object
            Классын объект
        """
        # Зургийг LAB өнгөний орон зай руу хөрвүүлэх
        lab = cv2.cvtColor(self.enhanced_image, cv2.COLOR_RGB2LAB)
        
        # L суваг дээр CLAHE (Contrast Limited Adaptive Histogram Equalization) хэрэглэх
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        lab[:,:,0] = clahe.apply(lab[:,:,0])
        
        # Буцаан RGB руу хөрвүүлэх
        self.enhanced_image = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        return self
    
    def sharpen(self, amount=1.0):
        """
        Зургийн ирмэгүүдийг тодруулах
        
        Parameters:
        -----------
        amount : float, default=1.0
            Тодруулах хэмжээ
        
        Returns:
        --------
        self : object
            Классын объект
        """
        # Unsharp mask ашиглан тодруулах
        gaussian = cv2.GaussianBlur(self.enhanced_image, (0, 0), 3.0)
        self.enhanced_image = cv2.addWeighted(
            self.enhanced_image, 1.0 + amount, 
            gaussian, -amount, 
            0
        )
        return self
    
    def adjust_colors(self, saturation_factor=1.3, brightness=5):
        """
        Зургийн өнгийг тохируулах
        
        Parameters:
        -----------
        saturation_factor : float, default=1.3
            Өнгөний ханалтын коэффициент
        brightness : int, default=5
            Гэрэлтүүлгийн өөрчлөлт
        
        Returns:
        --------
        self : object
            Классын объект
        """
        # HSV өнгөний орон зай руу хөрвүүлэх
        hsv = cv2.cvtColor(self.enhanced_image, cv2.COLOR_RGB2HSV).astype(np.float32)
        
        # Ханалтыг өөрчлөх
        hsv[:,:,1] = hsv[:,:,1] * saturation_factor
        hsv[:,:,1] = np.clip(hsv[:,:,1], 0, 255)
        
        # Гэрэлтүүлгийг өөрчлөх
        hsv[:,:,2] = hsv[:,:,2] + brightness
        hsv[:,:,2] = np.clip(hsv[:,:,2], 0, 255)
        
        # Буцаан RGB руу хөрвүүлэх
        self.enhanced_image = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
        return self
    
    def restore_image(self, noise_strength=10, contrast_clip=2.0, 
                     sharpen_amount=0.5, saturation=1.2, brightness=5):
        """
        Зургийг бүрэн сайжруулах
        
        Parameters:
        -----------
        noise_strength : int, default=10
            Шуугиан арилгах хүч
        contrast_clip : float, default=2.0
            Контраст сайжруулах хязгаарлалт
        sharpen_amount : float, default=0.5
            Тодруулах хэмжээ
        saturation : float, default=1.2
            Өнгөний ханалтын коэффициент
        brightness : int, default=5
            Гэрэлтүүлгийн өөрчлөлт
        
        Returns:
        --------
        self : object
            Классын объект
        """
        return (self
                .remove_noise(noise_strength)
                .enhance_contrast(contrast_clip)
                .sharpen(sharpen_amount)
                .adjust_colors(saturation, brightness))
    
    def save_result(self, output_path):
        """
        Сайжруулсан зургийг хадгалах
        
        Parameters:
        -----------
        output_path : str
            Гаралтын файлын зам
        """
        # Гаралтын замыг үүсгэх
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # RGB-ээс BGR руу хөрвүүлэх (OpenCV формат)
        output_image = cv2.cvtColor(self.enhanced_image, cv2.COLOR_RGB2BGR)
        
        # Зургийг хадгалах
        cv2.imwrite(str(output_path), output_image)
        print(f"Сайжруулсан зураг хадгалагдлаа: {output_path}")
    
    def show_result(self):
        """
        Эх болон сайжруулсан зургийг харьцуулан харуулах
        """
        if self.original_image is None or self.enhanced_image is None:
            print("Зураг ачаалагдаагүй эсвэл сайжруулагдаагүй байна.")
            return
        
        # Зургуудыг харьцуулан харуулах
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        plt.title('Эх зураг')
        plt.imshow(self.original_image)
        plt.axis('off')
        
        plt.subplot(1, 2, 2)
        plt.title('Сайжруулсан зураг')
        plt.imshow(self.enhanced_image)
        plt.axis('off')
        
        plt.tight_layout()
        plt.show()


# Жишээ ашиглалт
if __name__ == "__main__":
    import argparse
    
    # Аргументуудыг тодорхойлох
    parser = argparse.ArgumentParser(description='Хуучин зургийн чанарыг сайжруулах')
    parser.add_argument('--input', type=str, required=True, help='Оролтын зургийн зам')
    parser.add_argument('--output', type=str, help='Гаралтын зургийн зам')
    parser.add_argument('--noise', type=int, default=10, help='Шуугиан арилгах хүч')
    parser.add_argument('--contrast', type=float, default=2.0, help='Контраст сайжруулах хязгаарлалт')
    parser.add_argument('--sharpen', type=float, default=0.5, help='Тодруулах хэмжээ')
    parser.add_argument('--saturation', type=float, default=1.2, help='Өнгөний ханалтын коэффициент')
    parser.add_argument('--brightness', type=int, default=5, help='Гэрэлтүүлгийн өөрчлөлт')
    
    args = parser.parse_args()
    
    # Зургийг сайжруулах
    restorer = PhotoRestoration()
    
    try:
        restorer.load_image(args.input)
        restorer.restore_image(
            noise_strength=args.noise,
            contrast_clip=args.contrast,
            sharpen_amount=args.sharpen,
            saturation=args.saturation,
            brightness=args.brightness
        )
        
        # Үр дүнг харуулах
        restorer.show_result()
        
        # Хэрэв гаралтын зам өгөгдсөн бол хадгалах
        if args.output:
            restorer.save_result(args.output)
            
    except Exception as e:
        print(f"Алдаа гарлаа: {e}") 