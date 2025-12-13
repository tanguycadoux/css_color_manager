from django.db import models

import colorsys
import colour


def lin_to_srgb(c):
    if c <= 0.0031308:
        return 12.92 * c
    else:
        return 1.055 * (c ** (1/2.4)) - 0.055
    
def srgb_to_linear(c):
    if c <= 0.04045:
        return c / 12.92
    else:
        return ((c + 0.055) / 1.055) ** 2.4

def rgb_to_oklch(r, g, b):
    rgb = [r/255, g/255, b/255]

    # 1. sRGB → lin-sRGB
    lin_rgb = [srgb_to_linear(c) for c in rgb]

    # 2. lin-sRGB → OKLab
    oklab = colour.convert(
        lin_rgb,
        'RGB', 'OKLAB',
        source_colourspace=colour.RGB_COLOURSPACES['sRGB'],
        target_colourspace=colour.RGB_COLOURSPACES['sRGB']
    )

    # 3. OKLab → OKLCH
    oklch = colour.convert(oklab, 'OKLAB', 'OKLCH')
    L, C, H = oklch
    return (L, C, H*360)

def oklch_to_rgb(l, c, h):
    # --- oklch → oklab
    oklab = colour.convert([l, c, h/360], 'OKLCH', 'OKLAB')

    # --- oklab → linear srgb
    rgb_linear = colour.convert(oklab, 'OKLAB', 'RGB',
                                target_colourspace=colour.RGB_COLOURSPACES['sRGB'])

    # --- clamp
    r, g, b = [min(max(lin_to_srgb(c), 0.0), 1.0) for c in rgb_linear]

    return (r*255, g*255, b*255)


class ColorFamily(models.Model):
    name = models.CharField(max_length=50, blank=True)


    def __str__(self):
        return self.name
    
    def to_css_parameters(self):
        parameters = ""
        for color in self.colors.all():
            parameters += f"{color.name}: {color.to_css()};\n"
        print(parameters)
        return parameters


class Color(models.Model):
    MODE_CHOICES = [
        ("rgb", "RGB"),
        ("hsl", "HSL"),
        ("oklch", "OKLCH"),
    ]

    name = models.CharField(max_length=100, blank=True)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, null=True, blank=True)
    family = models.ForeignKey(ColorFamily, on_delete=models.CASCADE, related_name="colors", null=True, blank=True)
    values = models.JSONField(null=True, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name} ({self.mode})"


    def to_css(self):
        match self.mode:
            case "rgb":
                r = self.values["r"]
                g = self.values["g"]
                b = self.values["b"]
                return f"rgb({r}, {g}, {b})"

            case "hsl":
                h = self.values["h"]
                s = self.values["s"] * 100
                l = self.values["l"] * 100
                return f"hsl({h}, {s}%, {l}%)"

            case "oklch":
                l = self.values["l"] * 100
                c = self.values["c"]
                h = self.values["h"]
                return f"oklch({l}% {c} {h})"
    
    def to_rgb(self):
        match self.mode:
            case "rgb":
                return (
                    self.values["r"],
                    self.values["g"],
                    self.values["b"],
                )
            
            case "hsl":
                h = self.values["h"]
                s = self.values["s"]
                l = self.values["l"]
                r, g, b = colorsys.hls_to_rgb(h/360, l, s)
                return (255*r, 255*g, 255*b)
            
            case "oklch":
                L = self.values["l"]
                C = self.values["c"]
                H = self.values["h"]
                return oklch_to_rgb(L, C, H)

    def to_hsl(self):
        match self.mode:
            case "rgb":
                r = self.values["r"] / 255
                g = self.values["g"] / 255
                b = self.values["b"] / 255
                h, l, s = colorsys.rgb_to_hls(r, g, b)
                return (h * 360, s, l)
            
            case "hsl":
                return (
                    self.values["h"],
                    self.values["s"],
                    self.values["l"],
                )
            
            case "oklch":
                L = self.values["l"]
                C = self.values["c"]
                H = self.values["h"]

                # # --- oklch → oklab
                # oklab = colour.convert([L, C, H], 'OKLCH', 'OKLAB')

                # # --- oklab → linear srgb
                # rgb_linear = colour.convert(oklab, 'OKLAB', 'RGB',
                #                             target_colourspace=colour.RGB_COLOURSPACES['sRGB'])

                # # --- clamp
                # r, g, b = [min(max(lin_to_srgb(c), 0.0), 1.0) for c in rgb_linear]

                r, g, b = oklch_to_rgb(L, C, H)

                # --- rgb linear → HSL
                h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
                return (h * 360, s, l)

    def to_oklch(self):
        match self.mode:
            case "rgb":
                r = self.values["r"]
                g = self.values["g"]
                b = self.values["b"]
                return rgb_to_oklch(r, g, b)
            
            case "hsl":
                h = self.values["h"]
                s = self.values["s"]
                l = self.values["l"]
                r, g, b = colorsys.hls_to_rgb(h/360, l, s)
                return rgb_to_oklch(r*255, g*255, b*255)
            
            case "oklch":
                return (
                    self.values["l"],
                    self.values["c"],
                    self.values["h"],
                )
