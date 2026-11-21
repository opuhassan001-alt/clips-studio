import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import win32com.client

output_dir = r"e:\work station\gta 6\anthropology_presentation"
gemini_img = os.path.join(output_dir, "assets", "human_diversity_gemini.jpg")

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
slide = prs.slides.add_slide(prs.slide_layouts[6])

# 1. Full-bleed background cinematic image
pic = slide.shapes.add_picture(gemini_img, 0, 0, Inches(13.333), Inches(7.5))

# 2. Rich Left Panel (Dark Slate Backdrop: 6.3 inches wide, letting 7.03 inches of the image shine on the right)
panel = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(6.3), Inches(7.5))
panel.fill.solid()
panel.fill.fore_color.rgb = RGBColor(10, 15, 28) # #0A0F1C
panel.line.fill.background()

# Subtle accent border between panel and image
border = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.28), 0, Pt(1.5), Inches(7.5))
border.fill.solid()
border.fill.fore_color.rgb = RGBColor(30, 41, 59)
border.line.fill.background()

# Top Category Tag
tag_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.4), Inches(5.2), Inches(0.35))
tf_tag = tag_box.text_frame
tf_tag.word_wrap = True
ptg = tf_tag.paragraphs[0]
ptg.text = "ANTHROPOLOGY MASTERCLASS  •  TOPIC 01 / 10"
ptg.font.name = "Segoe UI"
ptg.font.size = Pt(10.5)
ptg.font.bold = True
ptg.font.color.rgb = RGBColor(56, 189, 248) # Cyan Accent

# Title & Subtitle
title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.75), Inches(5.3), Inches(1.15))
tf_title = title_box.text_frame
tf_title.word_wrap = True
p_t1 = tf_title.paragraphs[0]
p_t1.text = "Human Diversity"
p_t1.font.name = "Segoe UI"
p_t1.font.size = Pt(32)
p_t1.font.bold = True
p_t1.font.color.rgb = RGBColor(255, 255, 255)

p_t2 = tf_title.add_paragraph()
p_t2.text = "Exploring human adaptability, biology, and culture across space and time."
p_t2.font.name = "Segoe UI"
p_t2.font.size = Pt(12)
p_t2.font.color.rgb = RGBColor(148, 163, 184)
p_t2.space_before = Pt(3)

# 4 Rich Explanatory Pillars (Built for the Speaker to Explain In-Depth)
pillars = [
    {
        "num": "01",
        "title": "Holistic Exploration (In Time & Space)",
        "color": RGBColor(56, 189, 248),
        "points": [
            "Studies the whole human condition: past, present, and future; biology, society, language, and culture.",
            "Anthropologists study humans everywhere: from Amazon forests to urban shopping malls."
        ]
    },
    {
        "num": "02",
        "title": "Biological Plasticity (Physical Adaptation)",
        "color": RGBColor(52, 211, 153), # Emerald Green
        "points": [
            "Extreme Resilience: Andes & Himalayan populations adapt larger lungs and efficient hemoglobin to thrive at 16,000+ ft.",
            "Genetic Unity: Despite visible physical differences, all 8 billion humans share 99.9% identical DNA."
        ]
    },
    {
        "num": "03",
        "title": "Cultural Ingenuity (Non-Biological Survival)",
        "color": RGBColor(251, 191, 36), # Warm Amber
        "points": [
            "Our primary survival toolkit: Language, tools, clothing, fire, and social customs allow humans to master every ecosystem.",
            "Where biological evolution takes millennia, cultural adaptation solves problems in generations."
        ]
    },
    {
        "num": "04",
        "title": "The Cross-Cultural Test (The Invisible Culture)",
        "color": RGBColor(244, 114, 182), # Rose/Pink
        "points": [
            "Culture is 'invisible' to us—we assume our own habits are 'natural' until compared to another culture.",
            "Studying only our own society blinds us to the full spectrum of human potential."
        ]
    }
]

start_y = Inches(1.95)
gap_y = Inches(1.18)

for idx, p in enumerate(pillars):
    cur_y = start_y + idx * gap_y
    
    # Pillar Container
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.7), cur_y, Inches(5.3), Inches(1.12))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(17, 24, 39) # #111827
    box.line.color.rgb = RGBColor(31, 41, 55)
    box.line.width = Pt(1)
    
    tf = box.text_frame
    tf.word_wrap = True
    
    # Heading line with number badge
    p_head = tf.paragraphs[0]
    p_head.text = f"{p['num']}.  {p['title']}"
    p_head.font.name = "Segoe UI"
    p_head.font.size = Pt(11)
    p_head.font.bold = True
    p_head.font.color.rgb = p["color"]
    
    # Bullet 1
    pb1 = tf.add_paragraph()
    pb1.text = "• " + p["points"][0]
    pb1.font.name = "Segoe UI"
    pb1.font.size = Pt(9.5)
    pb1.font.color.rgb = RGBColor(226, 232, 240)
    pb1.space_before = Pt(3)
    
    # Bullet 2
    pb2 = tf.add_paragraph()
    pb2.text = "• " + p["points"][1]
    pb2.font.name = "Segoe UI"
    pb2.font.size = Pt(9.5)
    pb2.font.color.rgb = RGBColor(156, 163, 175)
    pb2.space_before = Pt(1.5)

# Bottom Takeaway Callout (The Presenter's Climax)
callout = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.7), Inches(6.75), Inches(5.3), Inches(0.48))
callout.fill.solid()
callout.fill.fore_color.rgb = RGBColor(30, 27, 75) # Deep Indigo
callout.line.color.rgb = RGBColor(79, 70, 229)
callout.line.width = Pt(1)
tf_cl = callout.text_frame
tf_cl.word_wrap = True
pcl = tf_cl.paragraphs[0]
pcl.text = 'STAGE SUMMARY: "Biologically one species. Culturally infinite."'
pcl.font.name = "Segoe UI"
pcl.font.size = Pt(10.5)
pcl.font.bold = True
pcl.font.color.rgb = RGBColor(199, 210, 254)
pcl.alignment = PP_ALIGN.CENTER

# Detailed Speaking Notes embedded in PPTX
notes = slide.notes_slide.notes_text_frame
notes.text = """[STAGE PRESENTATION SCRIPT - TOPIC 01: HUMAN DIVERSITY]
মঞ্চে লাখো মানুষের সামনে বিস্তারিত ব্যাখ্যা করার পূর্ণাঙ্গ স্ক্রিপ্ট:

(১. শুরুর হুক ও ছবির সাথে পরিচয়):
'ভদ্রমহিলা ও মহোদয়গণ,
পেছনের স্ক্রিনের অসাধারণ ছবিটির দিকে তাকান। বিভিন্ন মহাদেশ, বিভিন্ন বর্ণ, বিভিন্ন পোশাক—অথচ সবার চোখের মানবিক ভাষা এক। নৃবিজ্ঞানের প্রথম ও প্রধান ভিত্তি হলো এই 'Human Diversity' বা মানব বৈচিত্র্য।

বাম পাশের ৪টি মূল পয়েন্ট ধরে আমি আপনাদের কাছে এই বৈচিত্র্যের গভীর সত্যটি তুলে ধরছি:

(পয়েন্ট ১: সার্বিক অন্বেষণ - Holistic Exploration):
নৃবিজ্ঞান মানুষকে কোনো একটি সময় বা স্থানে বন্দি করে দেখে না। নৃবিজ্ঞান মানুষকে দেখে অতীত, বর্তমান এবং ভবিষ্যতের সার্বিক আলোতে। অ্যামাজনের গহীন জঙ্গল থেকে শুরু করে আধুনিক নিউইয়র্কের শপিং মল—সব জায়গার মানুষই এই গবেষণার অংশ।

(পয়েন্ট ২: শারীরিক অভিযোজন - Biological Plasticity):
মানুষের শরীর কতটা পরিবর্তনশীল? আন্দিজ ও হিমালয়ের পর্বতের ১৬,০০০ ফুট উচ্চতায় যেখানে সাধারণ মানুষ বাতাসের অভাবে অজ্ঞান হয়ে যায়, সেখানে মানুষ বংশপরম্পরায় খনিতে কাজ করে টিকে আছে। তাদের ফুসফুস ও রক্ত বাতাস থেকে অক্সিজেন ধারণের বিশেষ ক্ষমতা অর্জন করেছে। অথচ বিজ্ঞানের সবচেয়ে বড় বিস্ময় হলো—শারীরিক এত বৈচিত্র্যের পরও পৃথিবীর ৮০০ কোটি মানুষের রক্ত ও ডিএনএ ৯৯.৯% হুবহু এক!

(পয়েন্ট ৩: সাংস্কৃতিক উদ্ভাবন - Cultural Ingenuity):
বাঘ বা সিংহ শুধু শারীরিক শক্তির ওপর নির্ভর করে। কিন্তু মানুষ আগুন আবিষ্কার করেছে, বরফে চামড়ার পোশাক বানিয়েছে, মরুভূমিতে পানির কৌশল শিখেছে। জীববিজ্ঞানের বিবর্তনে লাখ লাখ বছর লাগে, কিন্তু মানুষ সংস্কৃতি দিয়ে মাত্র কয়েক প্রজন্মে যেকোনো প্রতিকূল প্রকৃতিকে জয় করতে পারে।

(পয়েন্ট ৪: ক্রস-কালচারাল পরীক্ষা - The Cross-Cultural Test):
নৃবিজ্ঞানী কনরাড কটকের সবচেয়ে মূল্যবান বার্তা: মাছ সারা জীবন পানির ভেতর সাঁতার কাটলেও বুঝতে পারে না পানি কী—যতক্ষণ না তাকে বাতাস দেখানো হয়। আমাদের সংস্কৃতিও আমাদের কাছে অদৃশ্য। আমরা মনে করি আমাদের রীতিনীতিই পুরো পৃথিবীর 'স্বাভাবিক নিয়ম'। কিন্তু যখনই আমরা অন্য সংস্কৃতিকে দেখি, তখনই মানুষের আসল সম্ভাবনা আমাদের চোখে ধরা পড়ে।

(মঞ্চের সমাপ্তি পাঞ্চলাইন):
'মনে রাখবেন—জীববিজ্ঞানের দিক থেকে আমরা সবাই এক রক্তের পরিবার, কিন্তু সংস্কৃতির দিক থেকে মানুষ এক অসীম সম্ভাবনার মহাবিশ্ব!'"""

pptx_path = os.path.join(output_dir, "Slide_01_Cinematic_Enriched.pptx")
prs.save(pptx_path)
print("Enriched PPTX saved successfully:", pptx_path)

# Export to PDF and PNG via PowerPoint COM
ppt_app = win32com.client.Dispatch("PowerPoint.Application")
pdf_path = os.path.join(output_dir, "Slide_01_Cinematic_Enriched.pdf")
png_path = os.path.join(output_dir, "Slide_01_Cinematic_Enriched.png")

pres = ppt_app.Presentations.Open(os.path.abspath(pptx_path), WithWindow=False)
pres.SaveAs(os.path.abspath(pdf_path), 32)
pres.Slides(1).Export(os.path.abspath(png_path), "PNG", 1920, 1080)
pres.Close()
ppt_app.Quit()

print("Enriched PDF and 1080p PNG exported successfully!")
