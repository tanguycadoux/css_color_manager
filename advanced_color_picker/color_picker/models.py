from django.db import models

import colorsys
import colour


def lin_to_srgb(c):
    if c <= 0.0031308:
        return 12.92 * c
    else:
        return 1.055 * (c ** (1/2.4)) - 0.055


class Color(models.Model):
    MODE_CHOICES = [
        ("rgb", "RGB"),
        ("hsl", "HSL"),
        ("oklch", "OKLCH"),
    ]

    name = models.CharField(max_length=100, blank=True)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, null=True, blank=True)
    values = models.JSONField(null=True, blank=True)


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
                l = self.values["l"]
                c = self.values["c"]
                h = self.values["h"]
                return f"oklch({l} {c} {h})"
            
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

                # --- oklch → oklab
                oklab = colour.convert([L, C, H], 'OKLCH', 'OKLAB')

                # --- oklab → linear srgb
                rgb_linear = colour.convert(oklab, 'OKLAB', 'RGB',
                                            target_colourspace=colour.RGB_COLOURSPACES['sRGB'])

                # --- clamp
                r, g, b = [min(max(lin_to_srgb(c), 0.0), 1.0) for c in rgb_linear]

                # --- rgb linear → HSL
                h, l, s = colorsys.rgb_to_hls(r, g, b)
                return (h * 360, s, l)
