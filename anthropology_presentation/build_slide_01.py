import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import win32com.client

output_dir = r"e:\work station\gta 6\anthropology_presentation"
os.makedirs(output_dir, exist_ok=True)
pptx_path = os.path.join(output_dir, "Slide_01_Human_Diversity_V3.pptx")
pdf_path = os.path.join(output_dir, "Slide_01_Human_Diversity_V3.pdf")
png_path = os.path.join(output_dir, "Slide_01_Human_Diversity_V3.png")

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

blank_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_layout)

# Crisp, Pure Clean White Editorial Theme
bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
bg.fill.solid()
bg.fill.fore_color.rgb = RGBColor(255, 255, 255)
bg.line.fill.background()

# Subtle top grid line
top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.5), Inches(11.733), Pt(1.5))
top_line.fill.solid()
top_line.fill.fore_color.rgb = RGBColor(226, 232, 240)
top_line.line.fill.background()

# Top Header / Meta Tag
top_tag = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(6.0), Inches(0.4))
tf_tag = top_tag.text_frame
tf_tag.word_wrap = True
p_tag = tf_tag.paragraphs[0]
p_tag.text = "TOPIC 01  •  HUMAN DIVERSITY"
p_tag.font.name = "Segoe UI"
p_tag.font.size = Pt(11)
p_tag.font.bold = True
p_tag.font.color.rgb = RGBColor(37, 99, 235) # Royal Blue Accent

# Top Sub-tag right aligned
top_tag_r = slide.shapes.add_textbox(Inches(7.5), Inches(0.6), Inches(5.0), Inches(0.4))
tf_tag_r = top_tag_r.text_frame
tf_tag_r.word_wrap = True
p_tag_r = tf_tag_r.paragraphs[0]
p_tag_r.alignment = PP_ALIGN.RIGHT
p_tag_r.text = "EXPLORING BIOLOGY & CULTURE ACROSS TIME"
p_tag_r.font.name = "Segoe UI"
p_tag_r.font.size = Pt(10)
p_tag_r.font.color.rgb = RGBColor(148, 163, 184)

# LEFT COLUMN: Dual High-Impact Documentary Imagery
assets_dir = os.path.join(output_dir, "assets")
img1_path = os.path.join(assets_dir, "cultural_diversity_portrait.jpg")
img2_path = os.path.join(assets_dir, "mountain_high_altitude.jpg")

# Photo 1: Cultural Portrait (Top Left)
pic1 = slide.shapes.add_picture(img1_path, Inches(0.8), Inches(1.15), Inches(5.4), Inches(3.2))

# Photo 2: Extreme Adaptation / Nature (Bottom Left)
pic2 = slide.shapes.add_picture(img2_path, Inches(0.8), Inches(4.5), Inches(5.4), Inches(2.2))

# Caption overlay badge on bottom image
cap_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.3), Inches(5.4), Inches(0.4))
cap_box.fill.solid()
cap_box.fill.fore_color.rgb = RGBColor(15, 23, 42)
cap_box.line.fill.background()
tf_cap = cap_box.text_frame
p_cap = tf_cap.paragraphs[0]
p_cap.text = "From extreme climates to vibrant societies — humans adapt everywhere."
p_cap.font.name = "Segoe UI"
p_cap.font.size = Pt(9.5)
p_cap.font.color.rgb = RGBColor(241, 245, 249)
p_cap.alignment = PP_ALIGN.CENTER

# RIGHT COLUMN: Content & Stage Speaking Anchors
rc_left = Inches(6.6)
rc_width = Inches(5.9)

# Main Headline
head_box = slide.shapes.add_textbox(rc_left, Inches(1.05), rc_width, Inches(1.1))
tf_head = head_box.text_frame
tf_head.word_wrap = True
p_h1 = tf_head.paragraphs[0]
p_h1.text = "Why We Are Never Identical"
p_h1.font.name = "Segoe UI"
p_h1.font.size = Pt(30)
p_h1.font.bold = True
p_h1.font.color.rgb = RGBColor(15, 23, 42)

p_h2 = tf_head.add_paragraph()
p_h2.text = "Human diversity is the joint story of our bodies and our inventions."
p_h2.font.name = "Segoe UI"
p_h2.font.size = Pt(13.5)
p_h2.font.color.rgb = RGBColor(100, 116, 139)
p_h2.space_before = Pt(3)

# Core Formula Banner
formula_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rc_left, Inches(2.25), rc_width, Inches(0.65))
formula_box.fill.solid()
formula_box.fill.fore_color.rgb = RGBColor(241, 245, 249)
formula_box.line.color.rgb = RGBColor(203, 213, 225)
formula_box.line.width = Pt(1)
tf_f = formula_box.text_frame
tf_f.word_wrap = True
p_f = tf_f.paragraphs[0]
p_f.text = "THE FORMULA:   Human Diversity = Biology × Culture"
p_f.font.name = "Segoe UI"
p_f.font.size = Pt(12)
p_f.font.bold = True
p_f.font.color.rgb = RGBColor(30, 41, 59)
p_f.alignment = PP_ALIGN.CENTER

# Two Visual Cards (Stage Anchors)
# Card 1: Biological Plasticity
card1 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rc_left, Inches(3.05), rc_width, Inches(1.55))
card1.fill.solid()
card1.fill.fore_color.rgb = RGBColor(255, 255, 255)
card1.line.color.rgb = RGBColor(226, 232, 240)
card1.line.width = Pt(1.2)

tf_c1 = card1.text_frame
tf_c1.word_wrap = True
pc1_tag = tf_c1.paragraphs[0]
pc1_tag.text = "1. BIOLOGICAL PLASTICITY (Our Bodies Adapt)"
pc1_tag.font.name = "Segoe UI"
pc1_tag.font.size = Pt(11)
pc1_tag.font.bold = True
pc1_tag.font.color.rgb = RGBColor(37, 99, 235)

pc1_b1 = tf_c1.add_paragraph()
pc1_b1.text = "• Physical Plasticity: Skin pigmentation shifts for UV protection; lungs and blood adapt to high altitudes (Andes & Himalayas)."
pc1_b1.font.name = "Segoe UI"
pc1_b1.font.size = Pt(11)
pc1_b1.font.color.rgb = RGBColor(51, 65, 85)
pc1_b1.space_before = Pt(4)

pc1_b2 = tf_c1.add_paragraph()
pc1_b2.text = "• Genetic Unity: Despite physical differences, all humans share 99.9% identical DNA."
pc1_b2.font.name = "Segoe UI"
pc1_b2.font.size = Pt(11)
pc1_b2.font.color.rgb = RGBColor(100, 116, 139)
pc1_b2.space_before = Pt(2)

# Card 2: Cultural Ingenuity
card2 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rc_left, Inches(4.75), rc_width, Inches(1.55))
card2.fill.solid()
card2.fill.fore_color.rgb = RGBColor(255, 255, 255)
card2.line.color.rgb = RGBColor(226, 232, 240)
card2.line.width = Pt(1.2)

tf_c2 = card2.text_frame
tf_c2.word_wrap = True
pc2_tag = tf_c2.paragraphs[0]
pc2_tag.text = "2. CULTURAL INGENUITY (Our Minds Create)"
pc2_tag.font.name = "Segoe UI"
pc2_tag.font.size = Pt(11)
pc2_tag.font.bold = True
pc2_tag.font.color.rgb = RGBColor(217, 119, 6) # Amber/Gold

pc2_b1 = tf_c2.add_paragraph()
pc2_b1.text = "• Learned Survival: Clothing, fire, housing, and social rules let us survive where biology alone would fail."
pc2_b1.font.name = "Segoe UI"
pc2_b1.font.size = Pt(11)
pc2_b1.font.color.rgb = RGBColor(51, 65, 85)
pc2_b1.space_before = Pt(4)

pc2_b2 = tf_c2.add_paragraph()
pc2_b2.text = "• Endless Solutions: Different groups invent completely different traditions to solve the exact same life challenges."
pc2_b2.font.name = "Segoe UI"
pc2_b2.font.size = Pt(11)
pc2_b2.font.color.rgb = RGBColor(100, 116, 139)
pc2_b2.space_before = Pt(2)

# Presenter Stage Anchor Bar (Golden Takeaway)
takeaway = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rc_left, Inches(6.45), rc_width, Inches(0.48))
takeaway.fill.solid()
takeaway.fill.fore_color.rgb = RGBColor(238, 242, 255) # Light indigo
takeaway.line.color.rgb = RGBColor(199, 210, 254)
tf_t = takeaway.text_frame
tf_t.word_wrap = True
pt = tf_t.paragraphs[0]
pt.text = 'STAGE CUE: "Biologically, we are one family; Culturally, we are a universe of ideas."'
pt.font.name = "Segoe UI"
pt.font.size = Pt(10.5)
pt.font.bold = True
pt.font.color.rgb = RGBColor(67, 56, 202)

# Speaker Notes
notes_slide = slide.notes_slide
tf_notes = notes_slide.notes_text_frame
tf_notes.text = """[STAGE SPEAKING SCRIPT - TOPIC 1: HUMAN DIVERSITY]
মঞ্চে সহজ বাংলায় উপস্থাপনা:
'শ্রদ্ধেয় অডিয়েন্স, আমাদের আলোচনার প্রথম বিষয়—'Human Diversity' বা মানব বৈচিত্র্য।
স্লাইডের বাম পাশের ছবিগুলোর দিকে তাকালে আপনারা দুটো বাস্তব সত্য দেখতে পাবেন: একদিকে বিভিন্ন সংস্কৃতি ও ঐতিহ্যের মানুষ, অন্যদিকে পাহাড়ে ও চরম বৈরী আবহাওয়ায় মানুষের লড়াই। নৃবিজ্ঞানের দৃষ্টিতে মানুষের এই বিশাল বৈচিত্র্য মূলত দুটি স্তম্ভের গুণফল:
১. বায়োলজিক্যাল অভিযোজন (Biological Plasticity): মানুষ যেখানে যায়, তার শরীর সেই পরিবেশের সাথে খাপ খায়। আন্দিজ ও হিমালয়ের পর্বতের উচ্চতায় পাতলা বাতাসেও রক্তে অক্সিজেন ধারণের বিশেষ শারীরবৃত্তীয় ক্ষমতা তৈরি হয়েছে। অথচ সবচেয়ে মজার বিষয় হলো—শারীরিক পার্থক্যের পরও পৃথিবীর সব মানুষ জিনগতভাবে ৯৯.৯% হুবহু এক!
২. কালচারাল উদ্ভাবন (Cultural Ingenuity): অন্য সব প্রাণী শুধু শারীরিক শক্তির ওপর নির্ভর করে। কিন্তু মানুষ আগুন আবিষ্কার করেছে, পোশাক বানিয়েছে, সমাজ ও হাতিয়ার গড়ে তুলেছে। তাই মানুষ বরফে যেমন বাঁচে, তীব্র গরমেও তেমনি সভ্যতা গড়ে তোলে।
মঞ্চের সমাপ্তি ডায়ালগ: 'জীববিজ্ঞানের দিক থেকে আমরা সবাই এক পরিবারের সন্তান, কিন্তু সংস্কৃতির দিক থেকে আমরা সীমাহীন বৈচিত্র্যের এক মহাবিশ্ব।'"""

prs.save(pptx_path)
print("PPTX saved successfully at:", pptx_path)

# Export to PDF and PNG via PowerPoint COM
ppt_app = win32com.client.Dispatch("PowerPoint.Application")
ppt_pres = ppt_app.Presentations.Open(os.path.abspath(pptx_path), WithWindow=False)
ppt_pres.SaveAs(os.path.abspath(pdf_path), 32)
slide_obj = ppt_pres.Slides(1)
slide_obj.Export(os.path.abspath(png_path), "PNG", 1920, 1080)
ppt_pres.Close()
ppt_app.Quit()

print("PDF and PNG exported successfully!")
