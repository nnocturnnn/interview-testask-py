import whisper

model = whisper.load_model("base")  # TODO maybe move to main???


async def transcribe_audio() -> str:
    # audio = whisper.load_audio("audio.mp3")
    # audio = whisper.pad_or_trim(audio)
    # mel = whisper.log_mel_spectrogram(audio).to(model.device)
    # _, probs = model.detect_language(mel)
    # print(f"Detected language: {max(probs, key=probs.get)}")
    # options = whisper.DecodingOptions()
    # result = whisper.decode(model, mel, options)
    result = model.transcribe("audio.mp3")
    return result["text"]
