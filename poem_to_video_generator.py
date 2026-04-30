# ===================================================================
# 🦅 Bashar's Epic: "The Free Bird" - فيديو عمودي 1080x1920
# ===================================================================
# تحويل الملحمة الشعرية إلى فيديو احترافي
# الدقة: 1080x1920 (9:16 عمودي)
# معدل الإطارات: 60 FPS
# الصيغة: MP4
# ===================================================================

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips
import time

# ===================================================================
# 🎨 1. إعدادات الفيديو
# ===================================================================

VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 60
OUTPUT_FORMAT = "mp4"

# الألوان والأنماط
COLORS = {
    "background": (15, 20, 30),      # أسود عميق
    "primary": (255, 215, 0),        # ذهبي (نجمة)
    "accent": (220, 20, 60),         # قرمزي (عاطفة)
    "text_white": (255, 255, 255),
    "text_secondary": (200, 200, 200),
    "highlight": (0, 255, 150),      # أخضر نيون
    "glow": (135, 206, 250),         # أزرق سماوي
}

# ===================================================================
# 🔤 2. نصوص القصيدة
# ===================================================================

POEM_LAYERS = {
    "layer_1": {
        "title": "الطبقة الأولى - الهمس الداخلي 🕯️",
        "lines": [
            "سَأَعْطِيكَ الكَلِمَاتِ لِلرَّبْطِ أُنْثَى",
            "وَلَكِنْ يَا سَيِّدَ الغَدْرِ",
            "ضَاعَ بِكَ العُمُرُ",
            "أَنَسِيتَ قِصَّتَنَا",
            "أَمْ زَاغَ بِكَ البَصَرُ؟"
        ],
        "color": COLORS["text_secondary"],
        "duration_per_line": 3,
        "animation": "fade_in_slow"
    },
    "layer_2": {
        "title": "الطبقة الثانية - النداء القوي 💪",
        "lines": [
            "عَنِ النَّاسِ سِرِّي",
            "فِي القَلْبِ مُسْتَتِرُ",
            "أَمِينُ قَلْبِي",
            "لَا يُفْشَى لَهُ سِرُّ",
            "يَا خَائِنَ الكَلِمَاتِ"
        ],
        "color": COLORS["primary"],
        "duration_per_line": 2.5,
        "animation": "slide_up"
    },
    "layer_3": {
        "title": "الطبقة الثالثة - الصرخة المدوية ⚡",
        "lines": [
            "يَا نَاكِرَ الحُبِّ",
            "إِنَّ الحُبَّ مَدْرَسَتِي",
            "عَلَى يَدَيْكَ",
            "رَاحَ الحُبُّ يَحْتَضِرُ",
            "آنَ الرَّحِيلُ",
            "لِلْعُصْفُورِ مِنْ قَفَصٍ"
        ],
        "color": COLORS["accent"],
        "duration_per_line": 2,
        "animation": "pulse"
    },
    "layer_4": {
        "title": "الطبقة الرابعة - الخاتمة 🕊️",
        "lines": [
            "آنَ الفِرَاقُ",
            "فَلَا وِصَالَ يَهُمُّنِي",
            "كَأَنْغَامٍ",
            "قَدْ شَدَا بِهَا الوَتَرُ",
            "🦅 العصفور حرٌّ أخيراً 💔"
        ],
        "color": COLORS["glow"],
        "duration_per_line": 3,
        "animation": "fade_out_slow"
    }
}

# ===================================================================
# 🎨 3. وظائف إنشاء الصور والرسومات
# ===================================================================

def create_background_gradient(width, height, color1, color2):
    """إنشاء خلفية متدرجة"""
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        
        for x in range(width):
            pixels[x, y] = (r, g, b)
    
    return img

def add_stars_background(img, star_count=150):
    """إضافة نجوم للخلفية"""
    pixels = img.load()
    np.random.seed(42)  # للحصول على نفس النتيجة دائماً
    
    for _ in range(star_count):
        x = np.random.randint(0, img.width)
        y = np.random.randint(0, img.height)
        brightness = np.random.randint(150, 255)
        pixels[x, y] = (brightness, brightness, brightness)
    
    return img

def create_frame_with_text(width, height, text, layer_name, frame_number=0, total_frames=60):
    """إنشاء إطار مع نص مع تأثيرات"""
    # الخلفية المتدرجة
    img = create_background_gradient(
        width, height,
        COLORS["background"],
        (30, 40, 60)
    )
    
    # إضافة النجوم
    img = add_stars_background(img, star_count=150)
    
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # تحميل الخط
    try:
        font_size = 80
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", 80)
        except:
            font = ImageFont.load_default()
    
    layer_info = POEM_LAYERS.get(layer_name, {})
    text_color = layer_info.get("color", COLORS["text_white"])
    animation_type = layer_info.get("animation", "fade_in_slow")
    
    # حساب الشفافية
    if animation_type == "fade_in_slow":
        alpha = int(255 * min(1.0, frame_number / max(1, total_frames)))
    elif animation_type == "fade_out_slow":
        alpha = int(255 * max(0.0, 1 - frame_number / max(1, total_frames)))
    elif animation_type == "pulse":
        import math
        alpha = int(255 * (0.6 + 0.4 * math.sin(max(0, frame_number) / max(1, total_frames) * 3.14159)))
    else:
        alpha = 255
    
    alpha = max(0, min(255, alpha))
    text_color_with_alpha = text_color + (alpha,)
    
    # حساب موضع النص
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # رسم ظل
    shadow_offset = 3
    draw.text((x + shadow_offset, y + shadow_offset), text, 
              font=font, fill=(0, 0, 0, min(255, alpha // 2)))
    
    # رسم النص الرئيسي
    draw.text((x, y), text, font=font, fill=text_color_with_alpha)
    
    return img

def create_title_frame(width, height):
    """إنشاء إطار العنوان"""
    img = create_background_gradient(
        width, height,
        COLORS["background"],
        (0, 0, 0)
    )
    
    img = add_stars_background(img, star_count=200)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    try:
        title_font = ImageFont.truetype("arial.ttf", 100)
        subtitle_font = ImageFont.truetype("arial.ttf", 50)
    except:
        try:
            title_font = ImageFont.truetype("DejaVuSans.ttf", 100)
            subtitle_font = ImageFont.truetype("DejaVuSans.ttf", 50)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
    
    # رسم العنوان الرئيسي
    title = "🦅 The Free Bird"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = bbox[2] - bbox[0]
    x = (width - title_width) // 2
    y = height // 3
    
    draw.text((x, y), title, font=title_font, fill=COLORS["primary"] + (255,))
    
    # رسم العنوان الفرعي
    subtitle = "ملحمة باشر الشعرية"
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = bbox[2] - bbox[0]
    x = (width - subtitle_width) // 2
    y = height // 2 + 100
    
    draw.text((x, y), subtitle, font=subtitle_font, fill=COLORS["accent"] + (255,))
    
    return img

def create_credits_frame(width, height):
    """إنشاء إطار الشكر والنهاية"""
    img = create_background_gradient(
        width, height,
        (0, 0, 0),
        COLORS["background"]
    )
    
    img = add_stars_background(img, star_count=200)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    try:
        credits_font = ImageFont.truetype("arial.ttf", 60)
        subtitle_font = ImageFont.truetype("arial.ttf", 40)
    except:
        try:
            credits_font = ImageFont.truetype("DejaVuSans.ttf", 60)
            subtitle_font = ImageFont.truetype("DejaVuSans.ttf", 40)
        except:
            credits_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
    
    # النص الرئيسي
    main_text = "شكراً لك 🙏"
    bbox = draw.textbbox((0, 0), main_text, font=credits_font)
    main_width = bbox[2] - bbox[0]
    x = (width - main_width) // 2
    y = height // 3
    
    draw.text((x, y), main_text, font=credits_font, fill=COLORS["glow"] + (255,))
    
    # النص الثانوي
    sub_text = "استمتع بملحمة 'العصفور الحر' 💔"
    bbox = draw.textbbox((0, 0), sub_text, font=subtitle_font)
    sub_width = bbox[2] - bbox[0]
    x = (width - sub_width) // 2
    y = height // 2 + 150
    
    draw.text((x, y), sub_text, font=subtitle_font, fill=COLORS["text_secondary"] + (255,))
    
    return img

# ===================================================================
# 🎬 4. إنشاء الفيديو
# ===================================================================

def generate_poem_video(output_path="poem_video.mp4", simple_mode=True):
    """إنشاء الفيديو الكامل"""
    
    print("="*70)
    print("🎬 بدء إنشاء الفيديو...")
    print("="*70)
    print(f"📺 الدقة: {VIDEO_WIDTH}x{VIDEO_HEIGHT}")
    print(f"⚡ معدل الإطارات: {FPS} FPS")
    print(f"📁 مسار الحفظ: {output_path}")
    print("="*70 + "\n")
    
    temp_dir = "temp_frames"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    frame_paths = []
    frame_durations = []
    
    # ===== 1. إطار العنوان =====
    print("📌 إنشاء إطار العنوان...")
    title_frame = create_title_frame(VIDEO_WIDTH, VIDEO_HEIGHT)
    title_path = os.path.join(temp_dir, "00_title.png")
    title_frame.save(title_path)
    
    for _ in range(int(3 * FPS)):  # 3 ثوان
        frame_paths.append(title_path)
        frame_durations.append(1/FPS)
    
    # ===== 2. إطارات الطبقات الأربع =====
    layer_order = ["layer_1", "layer_2", "layer_3", "layer_4"]
    frame_counter = 0
    
    for layer_idx, layer_name in enumerate(layer_order):
        print(f"\n📝 معالجة {POEM_LAYERS[layer_name]['title']}...")
        
        layer_info = POEM_LAYERS[layer_name]
        lines = layer_info['lines']
        duration_per_line = layer_info['duration_per_line']
        total_frames = int(duration_per_line * FPS)
        
        for line_idx, line in enumerate(lines):
            print(f"   ✏️  السطر {line_idx + 1}/{len(lines)}: {line[:30]}...")
            frame_counter += 1
            
            if simple_mode:
                # في الوضع البسيط، نستخدم إطار واحد لكل سطر
                frame = create_frame_with_text(
                    VIDEO_WIDTH, VIDEO_HEIGHT,
                    line,
                    layer_name,
                    frame_number=total_frames // 2,
                    total_frames=total_frames
                )
                frame_path = os.path.join(temp_dir, f"{frame_counter:04d}_line.png")
                frame.save(frame_path)
                
                for _ in range(total_frames):
                    frame_paths.append(frame_path)
                    frame_durations.append(1/FPS)
            else:
                # في الوضع المتقدم، نإنشاء إطارات متحركة
                for frame_num in range(total_frames):
                    frame = create_frame_with_text(
                        VIDEO_WIDTH, VIDEO_HEIGHT,
                        line,
                        layer_name,
                        frame_number=frame_num,
                        total_frames=total_frames
                    )
                    frame_path = os.path.join(temp_dir, f"{frame_counter:04d}_{frame_num:03d}.png")
                    frame.save(frame_path)
                    frame_paths.append(frame_path)
                    frame_durations.append(1/FPS)
    
    # ===== 3. إطار النهاية =====
    print("\n📌 إنشاء إطار النهاية...")
    credits_frame = create_credits_frame(VIDEO_WIDTH, VIDEO_HEIGHT)
    credits_path = os.path.join(temp_dir, "99_credits.png")
    credits_frame.save(credits_path)
    
    for _ in range(int(4 * FPS)):  # 4 ثوان
        frame_paths.append(credits_path)
        frame_durations.append(1/FPS)
    
    # ===== 4. دمج جميع الإطارات =====
    print("\n🔗 دمج جميع الإطارات...")
    clips = []
    for frame_path in frame_paths:
        clip = ImageClip(frame_path).set_duration(1/FPS)
        clips.append(clip)
    
    final_video = concatenate_videoclips(clips, method="compose")
    
    # ===== 5. تصدير الفيديو =====
    print(f"\n💾 تصدير الفيديو...")
    try:
        final_video.write_videofile(
            output_path,
            fps=FPS,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
    except Exception as e:
        print(f"خطأ في التصدير: {e}")
        print("سيتم محاولة استخدام إعدادات بديلة...")
        final_video.write_videofile(
            output_path,
            fps=FPS,
            verbose=False,
            logger=None
        )
    
    # ===== 6. تنظيف الملفات المؤقتة =====
    print("\n🧹 تنظيف الملفات المؤقتة...")
    import shutil
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    print("\n" + "="*70)
    print("✅ تم إنشاء الفيديو بنجاح!")
    print(f"📺 المسار: {os.path.abspath(output_path)}")
    print("="*70)

# ===================================================================
# 🚀 5. البرنامج الرئيسي
# ===================================================================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║  🦅 Bashar's Epic: "The Free Bird" - Video Generator   ║
    ║                                                          ║
    ║         تحويل الملحمة الشعرية إلى فيديو احترافي         ║
    ║                                                          ║
    ║    الدقة: 1080x1920 | المعدل: 60 FPS | الصيغة: MP4     ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # فحص المكتبات
    print("\n📚 فحص المكتبات المطلوبة...")
    try:
        from PIL import Image
        print("   ✅ Pillow (PIL)")
    except ImportError:
        print("   ❌ Pillow - جاري التثبيت...")
        os.system("pip install pillow")
    
    try:
        import numpy
        print("   ✅ NumPy")
    except ImportError:
        print("   ❌ NumPy - جاري التثبيت...")
        os.system("pip install numpy")
    
    try:
        from moviepy.editor import ImageClip, concatenate_videoclips
        print("   ✅ MoviePy")
    except ImportError:
        print("   ❌ MoviePy - جاري التثبيت...")
        os.system("pip install moviepy")
    
    print("\n" + "="*70)
    print("🎬 اختر وضع الإنشاء:")
    print("   1. وضع بسيط (أسرع - مناسب للاختبار)")
    print("   2. وضع متقدم (أفضل جودة - تأثيرات سلسة)")
    print("="*70)
    
    choice = input("\n👉 اختيارك (1 أو 2): ").strip()
    
    output_file = "poem_video.mp4"
    simple_mode = choice != "2"
    
    try:
        print("\n🎬 بدء الإنشاء...")
        generate_poem_video(output_file, simple_mode=simple_mode)
        
        print("\n🎉 تم بنجاح!")
        print(f"📺 الفيديو متاح هنا: {os.path.abspath(output_file)}")
        
    except Exception as e:
        print(f"\n❌ حدث خطأ: {e}")
        print("\n💡 تلميح: تأكد من تثبيت ffmpeg على نظامك")
        print("   Windows: choco install ffmpeg")
        print("   Mac: brew install ffmpeg")
        print("   Linux: sudo apt-get install ffmpeg")
