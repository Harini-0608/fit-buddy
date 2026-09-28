from functools import lru_cache

from .config import GEMINI_API_KEY, DEMO_MODE


@lru_cache(maxsize=1)
def get_client():

    if not GEMINI_API_KEY:
        return None

    from google import genai

    return genai.Client(api_key=GEMINI_API_KEY)


def generate_text(prompt: str, model: str) -> str:

    # Demo mode: don't contact Gemini
    if DEMO_MODE:
        if "7-day workout plan" in prompt:
            return """
Day 1 – Full Body Strength
Focus: Full body
Warm-up: 5–10 minutes of light walking and mobility.
Main workout:
- Squats – 3 × 12
- Wall push-ups – 3 × 10
- Glute bridges – 3 × 12
- Standing lunges – 2 × 10 each leg
Rest: 45–60 seconds between sets.
Cooldown: 5–10 minutes of stretching.

Day 2 – Cardio
Focus: Cardiovascular fitness
Warm-up: 5 minutes easy walking.
Main workout:
- Brisk walking – 20 minutes
- Marching in place – 3 × 2 minutes
- Step-ups – 3 × 10
Rest: Take short breaks whenever needed.
Cooldown: 5–10 minutes easy walking and stretching.

Day 3 – Upper Body
Focus: Upper-body strength
Warm-up: Arm circles and shoulder mobility for 5–10 minutes.
Main workout:
- Wall push-ups – 3 × 12
- Shoulder taps – 3 × 10
- Light resistance rows – 3 × 12
Rest: 45–60 seconds between sets.
Cooldown: Gentle shoulder and arm stretches.

Day 4 – Recovery
Focus: Active recovery
Warm-up: 5 minutes easy walking.
Main workout:
- Easy walking – 15–20 minutes
- Gentle full-body mobility
Rest: Keep the intensity comfortable.
Cooldown: Slow breathing and gentle stretching.

Day 5 – Lower Body
Focus: Legs and glutes
Warm-up: 5–10 minutes of walking and leg mobility.
Main workout:
- Squats – 3 × 12
- Glute bridges – 3 × 15
- Reverse lunges – 2 × 10 each leg
- Calf raises – 3 × 15
Rest: 45–60 seconds between sets.
Cooldown: Lower-body stretching.

Day 6 – Full Body Circuit
Focus: Full-body fitness
Warm-up: 5–10 minutes.
Main workout:
- Squats – 3 × 12
- Wall push-ups – 3 × 10
- Glute bridges – 3 × 12
- Marching – 3 × 2 minutes
Rest: 60 seconds between rounds.
Cooldown: 5–10 minutes of stretching.

Day 7 – Rest & Recovery
Focus: Recovery
Warm-up: Optional gentle walking.
Main workout:
- Easy walking or light stretching for 15–20 minutes.
Rest: Prioritize hydration and adequate sleep.
Cooldown: Gentle stretching and relaxed breathing.

Always exercise within your comfortable ability. If an exercise is unsuitable because of an injury or medical condition, seek professional advice before doing it.
""".strip()

        return """
FitBuddy Demo Mode:
Stay hydrated, eat balanced meals with vegetables, fruits,
whole grains and adequate protein, and prioritize sufficient sleep
to support workout recovery.
""".strip()

    # Real Gemini mode
    client = get_client()

    if client is None:
        raise RuntimeError(
            "Gemini API key is not configured. Add GEMINI_API_KEY to your .env file."
        )

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    text = getattr(response, "text", None)

    if not text:
        raise RuntimeError("Gemini returned an empty response.")

    return text.strip()