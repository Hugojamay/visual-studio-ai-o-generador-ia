import urllib.parse
from typing import Optional

class ArtDirectorEngine:
    def optimize(self, user_instruction: str, category: str, aspect_ratio: str, realism_level: int, image_url: Optional[str] = None):
        dimensions = {
            "1:1": (512, 512),
            "16:9": (768, 432),
            "9:16": (432, 768)
        }
        width, height = dimensions.get(aspect_ratio, (512, 512))

        # Prompt optimizado enfocado en producto comercial
        positive_prompt = (
            f"Commercial product photography, ({user_instruction}:1.3), "
            "elegant composition, studio lighting, hyper-realistic, 8k resolution, "
            "sharp focus, professional advertising aesthetics, macro details."
        )

        negative_prompt = (
            "deformed, blurry, bad anatomy, low quality, noise, artifacts, "
            "watermark, human face, portrait, person, extra limbs, ugly."
        )

        encoded_prompt = urllib.parse.quote(positive_prompt)
        
        # Si el usuario envió una imagen de referencia, la añadimos al motor de Pollinations
        if image_url:
            generated_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true&image={urllib.parse.quote(image_url)}"
        else:
            generated_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true&seed=42"

        return {
            "positive_prompt": positive_prompt,
            "negative_prompt": negative_prompt,
            "camera_spec": "90mm Macro f/2.8",
            "lighting_spec": "Studio Softbox & Accent Lighting",
            "width": width,
            "height": height,
            "image_url": generated_url
        }