from photo_restoration import PhotoRestoration
import os
from pathlib import Path

def enhance_photo(input_path, output_path=None, preset="standard"):
    """
    Хуучин зургийг сайжруулах жишээ функц
    
    Parameters:
    -----------
    input_path : str
        Оролтын зургийн зам
    output_path : str, optional
        Гаралтын зургийн зам
    preset : str, default="standard"
        Сайжруулах горим ("standard", "dramatic", "subtle", "bw_restore")
    """
    # PhotoRestoration классыг үүсгэх
    restorer = PhotoRestoration()
    
    # Зургийг ачаалах
    restorer.load_image(input_path)
    
    # Сайжруулах горимыг сонгох
    if preset == "dramatic":
        # Драматик горим - илүү тод, илүү ханасан өнгөтэй
        restorer.restore_image(
            noise_strength=10,       # Дунд зэргийн шуугиан арилгах
            contrast_clip=3.0,       # Өндөр контраст
            sharpen_amount=1.0,      # Хүчтэй тодруулах
            saturation=1.5,          # Өндөр ханалт
            brightness=15            # Илүү гэрэлтэй
        )
    elif preset == "subtle":
        # Нарийн горим - бага зэргийн сайжруулалт
        restorer.restore_image(
            noise_strength=8,        # Бага зэргийн шуугиан арилгах
            contrast_clip=1.5,       # Бага зэргийн контраст
            sharpen_amount=0.3,      # Бага зэргийн тодруулах
            saturation=1.1,          # Бага зэргийн ханалт
            brightness=5             # Бага зэргийн гэрэлтүүлэг
        )
    elif preset == "bw_restore":
        # Хар цагаан зургийг сэргээх горим
        restorer.restore_image(
            noise_strength=12,       # Дунд зэргийн шуугиан арилгах
            contrast_clip=2.8,       # Өндөр контраст
            sharpen_amount=0.8,      # Хүчтэй тодруулах
            saturation=0.0,          # Өнгөгүй (хар цагаан)
            brightness=10            # Дунд зэргийн гэрэлтүүлэг
        )
    else:  # "standard" болон бусад
        # Стандарт горим - тэнцвэртэй сайжруулалт
        restorer.restore_image(
            noise_strength=12,       # Дунд зэргийн шуугиан арилгах
            contrast_clip=2.2,       # Дунд зэргийн контраст
            sharpen_amount=0.6,      # Дунд зэргийн тодруулах
            saturation=1.25,         # Дунд зэргийн ханалт
            brightness=8             # Дунд зэргийн гэрэлтүүлэг
        )
    
    # Үр дүнг харуулах
    restorer.show_result()
    
    # Хэрэв гаралтын зам өгөгдсөн бол хадгалах
    if output_path:
        restorer.save_result(output_path)
        print(f"Сайжруулсан зураг хадгалагдлаа: {output_path}")

if __name__ == "__main__":
    # Зургийн хавтас болон гаралтын хавтасыг тодорхойлох
    current_dir = Path(__file__).parent
    images_dir = current_dir / "images"
    output_dir = current_dir / "output"
    
    # Гаралтын хавтас байхгүй бол үүсгэх
    output_dir.mkdir(exist_ok=True)
    
    # images хавтас дотор байгаа зургуудыг жагсаах
    image_files = list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.jpeg")) + list(images_dir.glob("*.png"))
    
    if not image_files:
        print("Анхааруулга: 'images' хавтас дотор зураг олдсонгүй!")
        print(f"Зураг файлуудаа '{images_dir}' хавтас руу хуулна уу.")
        print("Дэмжигдэх форматууд: .jpg, .jpeg, .png")
    else:
        # Олдсон зургуудыг харуулах
        print(f"{len(image_files)} зураг олдлоо:")
        for i, img_path in enumerate(image_files):
            print(f"{i+1}. {img_path.name}")
        
        # Хэрэглэгчээс зураг сонгохыг хүсэх
        try:
            if len(image_files) == 1:
                selected_index = 0
            else:
                selected_index = int(input("\nСайжруулах зургийн дугаарыг оруулна уу (жишээ: 1): ")) - 1
            
            if 0 <= selected_index < len(image_files):
                input_image = str(image_files[selected_index])
                file_name = image_files[selected_index].stem
                
                # Сайжруулах горимыг сонгох
                print("\nСайжруулах горимыг сонгоно уу:")
                print("1. Стандарт - тэнцвэртэй сайжруулалт")
                print("2. Драматик - илүү тод, илүү ханасан өнгөтэй")
                print("3. Нарийн - бага зэргийн сайжруулалт")
                print("4. Хар цагаан сэргээлт - хар цагаан зургийг сайжруулах")
                
                preset_choice = input("\nГоримын дугаарыг оруулна уу (1-4): ")
                preset_map = {
                    "1": "standard",
                    "2": "dramatic",
                    "3": "subtle",
                    "4": "bw_restore"
                }
                preset = preset_map.get(preset_choice, "standard")
                
                output_image = str(output_dir / f"{file_name}_{preset}_restored{image_files[selected_index].suffix}")
                
                print(f"\nСонгосон зураг: {image_files[selected_index].name}")
                print(f"Сонгосон горим: {preset}")
                print(f"Сайжруулсан зураг хадгалагдах зам: {output_image}")
                
                # Зургийг сайжруулах
                enhance_photo(input_image, output_image, preset)
            else:
                print("Буруу дугаар! Дахин оролдоно уу.")
        except ValueError:
            print("Буруу оролт! Тоо оруулна уу.")
        except Exception as e:
            print(f"Алдаа гарлаа: {e}")
            print("\nЗөвлөмж:")
            print("1. Зураг файлуудаа 'images' хавтас руу хуулна уу")
            print("2. Дэмжигдэх форматууд: .jpg, .jpeg, .png")
            print("3. Эсвэл photo_restoration.py файлыг шууд ажиллуулж болно:")
            print("   python photo_restoration.py --input \"images/your_photo.jpg\" --output \"output/restored_photo.jpg\"") 