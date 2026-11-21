import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import win32com.client

output_dir = r"e:\work station\gta 6\anthropology_presentation"
gemini_img = os.path.join(output_dir, "assets", "human_diversity_gemini.jpg")

# =========================================================================
# 1. CINEMATIC FULL-SCREEN KEYNOTE (APPLE / TED TALK LIVE STAGE FORMAT)
# =========================================================================
prs_cinematic = pptx.Presentation()
prs_cinematic.slide_width = Inches(13.333)
prs_cinematic.slide_height = Inches(7.5)
slide1 = prs_cinematic.slides.add_slide(prs_cinematic.slide_layouts[6])

# Full-bleed 16:9 Masterpiece photograph
pic1 = slide1.shapes.add_picture(gemini_img, 0, 0, Inches(13.333), Inches(7.5))

# Sophisticated dark lower-third / left backdrop for text readability
# Left-side gradient bar shape (deep dark vignette)
panel = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(5.8), Inches(7.5))
panel.fill.solid()
panel.fill.fore_color.rgb = RGBColor(10, 15, 26) # Rich Obsidian Blue
panel.line.fill.background()

# Minimalist Top Category Badge
badge = slide1.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(4.5), Inches(0.4))
tf_b = badge.text_frame
tf_b.word_wrap = True
pb = tf_b.paragraphs[0]
pb.text = "ANTHROPOLOGY KEYNOTE  •  TOPIC 01"
pb.font.name = "Segoe UI"
pb.font.size = Pt(11)
pb.font.bold = True
pb.font.color.rgb = RGBColor(56, 189, 248) # Cyan

# Giant Bold Headline
title_box = slide1.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(4.8), Inches(2.2))
tf_t = title_box.text_frame
tf_t.word_wrap = True
pt1 = tf_t.paragraphs[0]
pt1.text = "Human\nDiversity"
pt1.font.name = "Segoe UI"
pt1.font.size = Pt(44)
pt1.font.bold = True
pt1.font.color.rgb = RGBColor(255, 255, 255)

pt2 = tf_t.add_paragraph()
pt2.text = "One species. Infinite ways of being human."
pt2.font.name = "Segoe UI"
pt2.font.size = Pt(14)
pt2.font.color.rgb = RGBColor(148, 163, 184)
pt2.space_before = Pt(6)

# Stage Talking Anchors (3 Clear Points for the Speaker)
points = [
    ("BIOLOGICAL UNITY", "All 8 billion humans share 99.9% identical DNA."),
    ("PHYSICAL PLASTICITY", "Bodies adapt to extreme Andes altitudes, desert heat, and Arctic cold."),
    ("CULTURAL INVENTIVENESS", "Culture is the learned toolkit that lets us thrive where biology alone cannot.")
]

y = Inches(3.8)
for title, desc in points:
    tb = slide1.shapes.add_textbox(Inches(0.8), y, Inches(4.8), Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "•  " + title
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(11.5)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(226, 232, 240)
    
    p2 = tf.add_paragraph()
    p2.text = "   " + desc
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = RGBColor(148, 163, 184)
    p2.space_before = Pt(2)
    y += Inches(0.95)

# Golden Audience Takeaway at Bottom
cue = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.5), Inches(4.6), Inches(0.5))
cue.fill.solid()
cue.fill.fore_color.rgb = RGBColor(20, 27, 45)
cue.line.color.rgb = RGBColor(51, 65, 85)
cue.line.width = Pt(1)
tf_c = cue.text_frame
tf_c.word_wrap = True
pc = tf_c.paragraphs[0]
pc.text = 'Core Insight: "Culture is invisible until compared to another."'
pc.font.name = "Segoe UI"
pc.font.size = Pt(10)
pc.font.italic = True
pc.font.color.rgb = RGBColor(241, 245, 249)
pc.alignment = PP_ALIGN.CENTER

# Speaker Notes in PPTX
notes1 = slide1.notes_slide.notes_text_frame
notes1.text = """[STAGE SPEAKING SCRIPT - TOPIC 01: HUMAN DIVERSITY]
মঞ্চে দাঁড়িয়ে লাখো মানুষের সামনে যেভাবে কথা বলবে:

(স্ক্রিনের দিকে হাত ইশারা করে শান্ত অথচ দৃঢ় আত্মবিশ্বাসের সাথে শুরু করো):
'ভদ্রমহিলা ও মহোদয়গণ,
পেছনের স্ক্রিনের ছবিটির দিকে একবার তাকান। এরা সবাই মানুষ। বিভিন্ন মহাদেশ, বিভিন্ন বর্ণ, বিভিন্ন ঐতিহ্য—অথচ সবার চোখের ভাষা ও মানবিক মর্যাদা এক।

নৃবিজ্ঞানী কনরাড কটকের গবেষণার সবচেয়ে বড় শিক্ষা হলো:
'আমরা যদি শুধু নিজেদের সমাজকে দেখি, তবে আমরা কোনোদিন মানবজাতিকে চিনতে পারব না।'

আজকের পৃথিবীর দিকে তাকালে আপনারা দুটি যুগান্তকারী সত্য দেখতে পাবেন:
১. আমাদের বায়োলজিক্যাল ঐক্য: জেনেটিক্স প্রমাণ করেছে সারা পৃথিবীর সব মানুষ ৯৯.৯% হুবহু এক। অথচ আন্দিজের ১৬,০০০ ফুট বরফে যেমন মানুষ কাজ করে, সাহারার ৫০ ডিগ্রি গরমেও মানুষ বেঁচে থাকে।
২. আমাদের কালচারাল উদ্ভাবন: বাঘ বা সিংহ শুধু দাঁত আর নখ দিয়ে বাঁচে। কিন্তু মানুষ আগুন আবিষ্কার করেছে, পোশাক বানিয়েছে, সমাজ আর ভাষা তৈরি করেছে। যেখানে শরীর একা হার মানে, সেখানে মানুষের সংস্কৃতি তাকে জিতিয়ে দেয়।

মনে রাখবেন: আমরা জীববিজ্ঞানের দিক থেকে এক পরিবারের রক্ত, কিন্তু সংস্কৃতির দিক থেকে এক অসীম সম্ভাবনার মহাবিশ্ব!'"""

pptx_cinematic = os.path.join(output_dir, "Slide_01_Masterpiece_Cinematic.pptx")
prs_cinematic.save(pptx_cinematic)
print("Cinematic PPTX saved successfully:", pptx_cinematic)


# =========================================================================
# 2. EDITORIAL GALLERY FORMAT (SWISS MAGAZINE / NATIONAL GEOGRAPHIC)
# =========================================================================
prs_editorial = pptx.Presentation()
prs_editorial.slide_width = Inches(13.333)
prs_editorial.slide_height = Inches(7.5)
slide2 = prs_editorial.slides.add_slide(prs_editorial.slide_layouts[6])

# Pure White Gallery Background
bg2 = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
bg2.fill.solid()
bg2.fill.fore_color.rgb = RGBColor(255, 255, 255)
bg2.line.fill.background()

# Hero Framed Image on the Left
pic2 = slide2.shapes.add_picture(gemini_img, Inches(0.8), Inches(0.8), Inches(6.8), Inches(5.9))

# Right Editorial Column
rx = Inches(7.9)
rw = Inches(4.7)

# Category
cat = slide2.shapes.add_textbox(rx, Inches(0.8), rw, Inches(0.4))
tf_cat = cat.text_frame
p_c = tf_cat.paragraphs[0]
p_c.text = "ANTHROPOLOGY MASTERCLASS  /  01"
p_c.font.name = "Segoe UI"
p_c.font.size = Pt(11)
p_c.font.bold = True
p_c.font.color.rgb = RGBColor(2, 132, 199)

# Title
t2 = slide2.shapes.add_textbox(rx, Inches(1.2), rw, Inches(1.6))
tf_t2 = t2.text_frame
tf_t2.word_wrap = True
pt2_1 = tf_t2.paragraphs[0]
pt2_1.text = "Human Diversity"
pt2_1.font.name = "Segoe UI"
pt2_1.font.size = Pt(38)
pt2_1.font.bold = True
pt2_1.font.color.rgb = RGBColor(15, 23, 42)

pt2_2 = tf_t2.add_paragraph()
pt2_2.text = "The exploration of human adaptability, biology, and culture across space and time."
pt2_2.font.name = "Segoe UI"
pt2_2.font.size = Pt(13)
pt2_2.font.color.rgb = RGBColor(100, 116, 139)
pt2_2.space_before = Pt(4)

# Line
div = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, rx, Inches(2.95), rw, Pt(1))
div.fill.solid()
div.fill.fore_color.rgb = RGBColor(226, 232, 240)
div.line.fill.background()

# Key Insights
insights = [
    ("Cross-Cultural Lens", "One culture cannot explain humanity. Culture is invisible until compared with another."),
    ("Biological Plasticity", "The human body physically adapts to altitude, temperature, and disease across generations."),
    ("The Cultural Toolkit", "Traditions, languages, and learned customs allow humans to solve survival in infinite ways.")
]

iy = Inches(3.2)
for heading, body in insights:
    ibox = slide2.shapes.add_textbox(rx, iy, rw, Inches(0.95))
    itf = ibox.text_frame
    itf.word_wrap = True
    ip1 = itf.paragraphs[0]
    ip1.text = heading
    ip1.font.name = "Segoe UI"
    ip1.font.size = Pt(12)
    ip1.font.bold = True
    ip1.font.color.rgb = RGBColor(15, 23, 42)
    
    ip2 = itf.add_paragraph()
    ip2.text = body
    ip2.font.name = "Segoe UI"
    ip2.font.size = Pt(10.5)
    ip2.font.color.rgb = RGBColor(71, 85, 105)
    ip2.space_before = Pt(2)
    iy += Inches(0.95)

# Bottom Takeaway Box
bb = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, Inches(6.25), rw, Inches(0.55))
bb.fill.solid()
bb.fill.fore_color.rgb = RGBColor(241, 245, 249)
bb.line.fill.background()
tf_bb = bb.text_frame
tf_bb.word_wrap = True
pbb = tf_bb.paragraphs[0]
pbb.text = "Keynote Takeaway: Biologically unified. Culturally limitless."
pbb.font.name = "Segoe UI"
pbb.font.size = Pt(10.5)
pbb.font.bold = True
pbb.font.color.rgb = RGBColor(15, 23, 42)
pbb.alignment = PP_ALIGN.CENTER

notes2 = slide2.notes_slide.notes_text_frame
notes2.text = notes1.text

pptx_editorial = os.path.join(output_dir, "Slide_01_Masterpiece_Editorial.pptx")
prs_editorial.save(pptx_editorial)
print("Editorial PPTX saved successfully:", pptx_editorial)

# =========================================================================
# 3. EXPORT TO HIGH-RES PDF & PNG
# =========================================================================
ppt_app = win32com.client.Dispatch("PowerPoint.Application")

# Export Cinematic
p_cin = ppt_app.Presentations.Open(os.path.abspath(pptx_cinematic), WithWindow=False)
pdf_cin = os.path.join(output_dir, "Slide_01_Masterpiece_Cinematic.pdf")
png_cin = os.path.join(output_dir, "Slide_01_Masterpiece_Cinematic.png")
p_cin.SaveAs(os.path.abspath(pdf_cin), 32)
p_cin.Slides(1).Export(os.path.abspath(png_cin), "PNG", 1920, 1080)
p_cin.Close()

# Export Editorial
p_ed = ppt_app.Presentations.Open(os.path.abspath(pptx_editorial), WithWindow=False)
pdf_ed = os.path.join(output_dir, "Slide_01_Masterpiece_Editorial.pdf")
png_ed = os.path.join(output_dir, "Slide_01_Masterpiece_Editorial.png")
p_ed.SaveAs(os.path.abspath(pdf_ed), 32)
p_ed.Slides(1).Export(os.path.abspath(png_ed), "PNG", 1920, 1080)
p_ed.Close()

ppt_app.Quit()
print("All exports to PPTX, PDF, and 1080p PNG completed successfully!")
