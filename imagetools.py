import os
import random
from PIL import Image, ImageSequence, ImageEnhance, ImageDraw, ImageFont, ImageDraw
from itertools import product


class ImageText(object):
    def __init__(self, filename_or_size_or_Image, mode='RGBA', background=(0, 0, 0, 0),
                 encoding='utf8'):
        if isinstance(filename_or_size_or_Image, str):
            self.filename = filename_or_size_or_Image
            self.image = Image.open(self.filename)
            self.size = self.image.size
        elif isinstance(filename_or_size_or_Image, (list, tuple)):
            self.size = filename_or_size_or_Image
            self.image = Image.new(mode, self.size, color=background)
            self.filename = None
        elif isinstance(filename_or_size_or_Image, PIL.Image.Image):
            self.image = filename_or_size_or_Image
            self.size = self.image.size
            self.filename = None
        self.draw = ImageDraw.Draw(self.image)
        self.encoding = encoding

    def save(self, filename=None):
        self.image.save(filename or self.filename)
    
    def show(self):
        self.image.show()

    def get_font_size(self, text, font, max_width=None, max_height=None):
        if max_width is None and max_height is None:
            raise ValueError('You need to pass max_width or max_height')
        font_size = 1
        text_size = self.get_text_size(font, font_size, text)
        if (max_width is not None and text_size[0] > max_width) or \
           (max_height is not None and text_size[1] > max_height):
            raise ValueError("Text can't be filled in only (%dpx, %dpx)" % \
                    text_size)
        while True:
            if (max_width is not None and text_size[0] >= max_width) or \
               (max_height is not None and text_size[1] >= max_height):
                return font_size - 1
            font_size += 1
            text_size = self.get_text_size(font, font_size, text)

    def write_text(self, xy, text, font_filename, font_size=11,
                   color=(0, 0, 0), max_width=None, max_height=None):
        x, y = xy
        if font_size == 'fill' and \
           (max_width is not None or max_height is not None):
            font_size = self.get_font_size(text, font_filename, max_width,
                                           max_height)
        text_size = self.get_text_size(font_filename, font_size, text)
        font = ImageFont.truetype(font_filename, font_size)
        if x == 'center':
            x = (self.size[0] - text_size[0]) / 2
        if y == 'center':
            y = (self.size[1] - text_size[1]) / 2
        self.draw.text((x, y), text, font=font, fill=color)
        return text_size

    def get_text_size(self, font_filename, font_size, text):
        font = ImageFont.truetype(font_filename, font_size)
        return font.getsize(text)

    def write_text_box(self, xy, text, box_width, font_filename,
                       font_size=11, color=(0, 0, 0), place='left',
                       justify_last_line=False, position='top',
                       line_spacing=1.0):
        x, y = xy
        lines = []
        line = []
        words = text.split()
        for word in words:
            new_line = ' '.join(line + [word])
            size = self.get_text_size(font_filename, font_size, new_line)
            text_height = size[1] * line_spacing
            last_line_bleed = text_height - size[1]
            if size[0] <= box_width:
                line.append(word)
            else:
                lines.append(line)
                line = [word]
        if line:
            lines.append(line)
        lines = [' '.join(line) for line in lines if line]
        
        if position == 'middle':
            height = (self.size[1] - len(lines)*text_height + last_line_bleed)/2
            height -= text_height # the loop below will fix this height
        elif position == 'bottom':
            height = self.size[1] - len(lines)*text_height + last_line_bleed
            height -= text_height  # the loop below will fix this height
        else:
            height = y
            
        for index, line in enumerate(lines):
            height += text_height
            if place == 'left':
                self.write_text((x, height), line, font_filename, font_size,
                                color)
            elif place == 'right':
                total_size = self.get_text_size(font_filename, font_size, line)
                x_left = x + box_width - total_size[0]
                self.write_text((x_left, height), line, font_filename,
                                font_size, color)
            elif place == 'center':
                total_size = self.get_text_size(font_filename, font_size, line)
                x_left = int(x + ((box_width - total_size[0]) / 2))
                self.write_text((x_left, height), line, font_filename,
                                font_size, color)
            elif place == 'justify':
                words = line.split()
                if (index == len(lines) - 1 and not justify_last_line) or \
                   len(words) == 1:
                    self.write_text((x, height), line, font_filename, font_size,
                                    color)
                    continue
                line_without_spaces = ''.join(words)
                total_size = self.get_text_size(font_filename, font_size,
                                                line_without_spaces)
                space_width = (box_width - total_size[0]) / (len(words) - 1.0)
                start_x = x
                for word in words[:-1]:
                    self.write_text((start_x, height), word, font_filename,
                                    font_size, color)
                    word_size = self.get_text_size(font_filename, font_size,
                                                    word)
                    start_x += word_size[0] + space_width
                last_word_size = self.get_text_size(font_filename, font_size,
                                                    words[-1])
                last_word_x = x + box_width - last_word_size[0]
                self.write_text((last_word_x, height), words[-1], font_filename,
                                font_size, color)
        return (box_width, height - y)


def tile(img, x, y):
    w, h = img.size
    dx = int(w / x)
    dy = int(h / y)
    grid = product(range(0, h-h%dy, dy), range(0, w-w%dx, dx))
    tiles = []
    for i, j in grid:
        box = (j, i, j+dx, i+dy)
        tiles.append(img.crop(box))
    return tiles

def desaturate(img):
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.46)
    return img

def gif(frames, target, background=None, overlay=None, dim=(100, 100), transparent=False, duration=600):
    images = []
    icc = None
    for image in frames:
        image = image.convert('RGBA', dither=None)
        if background is not None:
            bg = Image.open(background).convert('RGBA', dither=None)
            bg.paste(image, (-4, 3), image)
        else:
            bg = image
        if overlay is not None:
            fg = Image.open(overlay).convert('RGBA', dither=None)
            bg.paste(fg, (0, 0), fg)
        final_image = bg if not None else image
        final_image = final_image.resize(dim) #, Image.NEAREST)
        images.append(final_image)
    if transparent:
        images[0].save(target, save_all=True, append_images=images[1:], optimize=False, quality=100, duration=duration, loop=0, transparency=255, disposal=2)
    else:
        images[0].save(target, save_all=True, append_images=images[1:], optimize=False, quality=100, duration=duration, loop=0)

def overlay(images, scale=1):
    bg = None
    for img, offset in images:
        if bg is not None:
            bg.paste(img, offset, img)
        else:
            size = (img.size[0]*scale, img.size[1]*scale)
            bg = img
    bg.resize(size) #, Image.NEAREST)
    return bg

def all_png(path):
    return [f for f in sorted(os.listdir(path)) if f.endswith('.png')]


###########################################################################################

def bg_wide(semi):
    bg_trait = semi.meta_trait("background")
    if "Skulls" in bg_trait or "Burst" in bg_trait:
        resource_name = "resources/assets/bg_{}.png".format(bg_trait.replace(" Background", "").replace(" ", "_").lower())
        return Image.open(resource_name).convert("RGBA")
    else:
        return Image.open(semi.traits[-1]).resize((2400, 1080)).convert("RGBA")

def pfp(semi, background=True):
    root = Image.open(semi.traits[-1]) if background else Image.new("RGBA", (1080, 1080), (255,255,255,0))
    for layer in reversed(semi.traits[:-1]):
        if os.path.isfile(layer):
            img = Image.open(layer).convert("RGBA")
            if root is None:
                root = img
            else:
                root.paste(img, (0,0), img)
    return root

def head(semi, background=True):
    root = Image.open(semi.traits[-1]) if background else Image.new("RGBA", (1080, 1080), (255,255,255,0))
    for layer in reversed([s for i,s in enumerate(semi.traits) if i != 1][:-4]):
        if os.path.isfile(layer):
            img = Image.open(layer).convert("RGBA")
            if root is None:
                root = img
            else:
                root.paste(img, (0,50), img)
    return root

def gm(semi, gn=False):
    background = bg_wide(semi)
    semi_pfp = pfp(semi, background=False)
    gm = Image.open("resources/assets/{}!_{}.png".format("GN" if gn else "GM", "villain" if semi.is_villain else "hero"))
    pfp_coords = (1320,0) if semi.is_villain else (0,0)
    background.paste(semi_pfp, pfp_coords, semi_pfp)
    background.paste(gm, (0,0), gm)
    return background

def catchphrase(semi, phrase):
    background = bg_wide(semi)
    semi_pfp = pfp(semi, background=False)
    ss_logo = Image.open("resources/assets/semisupers_burst_{}.png".format("villain" if semi.is_villain else "hero"))
    speech_bubble = Image.open("resources/assets/speech_bubble_{}.png".format("villain" if semi.is_villain else "hero"))
    pfp_coords = (1320,0) if semi.is_villain else (0,0)
    background.paste(semi_pfp, pfp_coords, semi_pfp)
    background.paste(speech_bubble, (0,0), speech_bubble)
    background.paste(ss_logo, (0,0), ss_logo)
    # Add the text, for now truncated to 100 chars to avoid overflow - TODO: fill vertically to fix, adjusting font size
    font = 'resources/fonts/LitterboxICG.ttf'
    truncated_phrase = phrase[:100]
    img_text = ImageText((850, 380), background=(255, 255, 255, 0))
    img_text.write_text_box((0, 0), truncated_phrase, box_width=850, font_filename=font, font_size=82, color=(0,0,0), place='center', position='middle')
    background.paste(img_text.image, (390, 140) if semi.is_villain else (1160, 140), img_text.image)
    return background

def vs(semi1, semi2, fight_round=None):
    root = Image.new("RGBA", (2400, 1080), (255,255,255,0))
    # Starburst in the middle, allow for specifying "fight", semi" or final", otherwise go with "fight"
    starburst_file = "resources/assets/fn_fight_starburst.png"
    if isinstance(fight_round, str):
        if fight_round == "fight":
            starburst_file = "resources/assets/fn_fight_starburst.png"
        elif fight_round == "semi":
            starburst_file = "resources/assets/fn_semifinal_starburst.png"
        elif fight_round == "final":
            starburst_file = "resources/assets/fn_final_starburst.png"
    starburst = Image.open(starburst_file)
    # Mask for overlaying backgrounds, randomize the angle of the cut with a coin toss
    bg_mask = Image.open("resources/assets/bg_mask.png")
    if random.randint(0, 1) == 0:
        bg_mask = bg_mask.transpose(Image.FLIP_TOP_BOTTOM)
    # Backgrounds and PFPs
    background1 = bg_wide(semi1)
    background2 = bg_wide(semi2)
    pfp1 = pfp(semi1, background=False)
    pfp2 = pfp(semi2, background=False)
    # Make sure to flip semis depending on orientation (hero/villain)
    # and what side they end up on (left/right)
    if semi1.is_villain:
        pfp1 = pfp1.transpose(Image.FLIP_LEFT_RIGHT)
        background1 = background1.transpose(Image.FLIP_LEFT_RIGHT)
    if not semi2.is_villain:
        pfp2 = pfp2.transpose(Image.FLIP_LEFT_RIGHT)
        background2 = background2.transpose(Image.FLIP_LEFT_RIGHT)
    # Put it all together
    pfp1_coords = (0,0)
    pfp2_coords = (1320,0)
    root.paste(background2, (0,0), background2)
    root.paste(background1, (0,0), bg_mask) # Remember to mask 
    root.paste(starburst, (0,0), starburst)
    root.paste(pfp1, pfp1_coords, pfp1)
    root.paste(pfp2, pfp2_coords, pfp2)
    return root

